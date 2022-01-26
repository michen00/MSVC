"""featurize incoming audio sample"""

# utility
from gc import collect as gc_collect

# core
import numpy as np
import pandas as pd
import streamlit as st

# trigonometry
from numpy import arctan2, sqrt

# typing
from typing import List, Union
from sklearn.base import BaseEstimator

# faster sklearn
from sklearnex import patch_sklearn

patch_sklearn()
del patch_sklearn


@st.experimental_singleton
def load_extractor(extractor: str) -> BaseEstimator:
    """loads a custom feature extractor"""
    from joblib import load as joblib_load

    return joblib_load(f"msvc/src/features/feature_extractors/{extractor}.joblib")


def featurize(frill_df: pd.DataFrame) -> pd.DataFrame:
    """featurize an incoming FRILL dataframe"""
    # setup
    VALENCE = {"neg": 0, "neu": 1, "pos": 2}
    OC_SVM = ("sgdlinear", "rbf", "sigmoid")

    def feature_trio(prefix: str = "", suffix: str = "") -> List[str]:
        """convenience function for making 'neg, neu, pos' feature names"""
        return [
            f"{f'{prefix}_' if prefix else ''}{valence}{f'_{suffix}' if suffix else ''}"
            for valence in VALENCE
        ]

    data_columns: List[
        Union[pd.DataFrame, pd.Series]
    ] = []  # to be concatenated column-wise
    features: List[List[str]] = []  # groups of column names
    spinner = st.spinner

    # select FRILL columns
    with open("msvc/src/features/FRILL/selected_frill_columns.txt", "r") as f:
        frill_df = frill_df.loc[:, [_.strip() for _ in f.readlines()]]

    # LDA components of FRILL embeddings
    with spinner("performing linear discriminant analysis..."):
        features.append(["LDA1", "LDA2"])
        components = load_extractor("LDA1_-_LDA2").transform(frill_df)
        data_columns.append(
            lda_df := pd.DataFrame(
                (
                    components
                    if len(components.shape) == 2
                    else load_extractor("LDA1_-_LDA2_backup").transform(frill_df)
                    # svd solver sometimes produces a degenerate component
                ),
                columns=features[-1],
            ).astype(np.float64)
        )

        # one-class LDA components of FRILL embeddings
        features.append(feature_trio("ocLDA", ""))
        data_columns.extend(
            [
                pd.Series(
                    np.squeeze(
                        load_extractor(feature := f"ocLDA_{valence}").transform(
                            frill_df
                        )
                    )
                )
                .astype(np.float64)
                .rename(feature)
                for valence in VALENCE
            ]
        )

    # local outlier factor of LDA components of FRILL embeddings
    with spinner("calculating local outlier factor..."):
        features.append(feature_trio("LDA-LOF", "20"))
        data_columns.extend(
            [
                pd.Series(
                    load_extractor(feature := f"LDA-LOF_{valence}_20").score_samples(
                        lda_df
                    )
                )
                .astype(np.float64)
                .rename(feature)
                for valence in VALENCE
            ]
        )

    # one-class SVM scores of LDA components of FRILL embeddings
    with spinner("scoring with one-class support-vector machines..."):
        for oc_svm in OC_SVM:
            features.append(feature_trio(f"LDA-ocSVM_{oc_svm}", ""))
            data_columns.extend(
                [
                    pd.Series(
                        load_extractor(
                            feature := f"LDA-ocSVM_{oc_svm}_{valence}"
                        ).score_samples(lda_df)
                    )
                    .astype(np.float64)
                    .rename(feature)
                    for valence in VALENCE
                ]
            )
        del lda_df
        gc_collect()

        # SGDOneClassSVM scores of FRILL embeddings
        features.append(feature_trio("ocSVM_sgdlinear", ""))
        data_columns.append(
            ocSVM_sgdlinear_df := pd.concat(
                [
                    pd.Series(
                        load_extractor(
                            feature := f"ocSVM_sgdlinear_{valence}"
                        ).score_samples(frill_df)
                    )
                    .astype(np.float64)
                    .rename(feature)
                    for valence in VALENCE
                ],
                axis="columns",
            )
        )
        del frill_df
        gc_collect()

    # LDA components of SGDOneClassSVM scores of FRILL embeddings
    with spinner("extracting secondary features..."):
        features.append(["ocSVM_sgdlinear_LDA1", "ocSVM_sgdlinear_LDA2"])
        components = load_extractor(feat := "_-_".join(features[-1])).transform(
            ocSVM_sgdlinear_df
        )
        data_columns.append(
            pd.DataFrame(
                (
                    components
                    if len(components.shape) == 2
                    else load_extractor(f"{feat}_backup").transform(ocSVM_sgdlinear_df)
                    # svd solver sometimes produces a degenerate component
                ),
                columns=features[-1],
            ).astype(np.float64)
        )
        del ocSVM_sgdlinear_df
        gc_collect()

        # intermediate aggregation
        data = pd.concat(data_columns, axis="columns")
        data.columns = data.columns.astype(str)
        assert not data.isnull().values.any()
        data_columns = [data]

    # spherical coordinates
    with spinner("converting to polar/spherical coordinates..."):
        sphericals = {}
        for feature_set in features:
            combo = "+".join(feature_set)
            df = data.loc[:, feature_set]
            x, y = df.loc[:, feature_set[0]], df.loc[:, feature_set[1]]
            theta, phi = f"theta_{combo}", f"phi_{combo}"
            # polar conversion
            sphericals[theta] = arctan2(y, x)
            if len(feature_set) == 3:
                # spherical conversion
                sphericals[phi] = arctan2(
                    sqrt(x ** 2 + y ** 2), df.loc[:, feature_set[2]]
                )
            del combo
            del df
            del phi
            del theta
            del x
            del y
            gc_collect()
        data_columns.append(sphericals := pd.DataFrame(sphericals).astype(np.float64))

        # LDA components of spherical coordinate features
        extractor = load_extractor(
            feat := "_-_".join(features := ["spherical-LDA1", "spherical-LDA2"])
        )
        # ensure intermediate column order
        assert len(extractor.feature_names_in_) == len(sphericals.columns)
        assert set(extractor.feature_names_in_) == set(sphericals.columns)
        sphericals = sphericals.loc[:, extractor.feature_names_in_]
        components = extractor.transform(sphericals)
        if len(components.shape) != 2:
            # svd solver sometimes produces a degenerate component
            extractor = load_extractor(f"{feat}_backup")
            assert len(extractor.feature_names_in_) == len(sphericals.columns)
            assert set(extractor.feature_names_in_) == set(sphericals.columns)
            sphericals = sphericals.loc[:, extractor.feature_names_in_]
            components = extractor.transform(sphericals)
        data_columns.append(
            pd.DataFrame(components, columns=features).astype(np.float64)
        )
        del components
        del feat
        gc_collect()

        # one-class LDA components of spherical coordinate features
        data_columns.append(
            pd.DataFrame(
                {
                    feature: [np.squeeze(load_extractor(feature).transform(sphericals))]
                    for feature in feature_trio("spherical-ocLDA", "")
                }
            ).astype(np.float64),
        )

    # aggregate and scale
    with spinner("scaling..."):
        scaler = load_extractor("robust_scaler")
        data = pd.concat(data_columns, axis="columns")
        assert len(scaler.feature_names_in_) == len(data.columns)
        assert set(scaler.feature_names_in_) == set(data.columns)
        data = pd.DataFrame(  # ensure intermediate column order
            scaler.transform(data.loc[:, scaler.feature_names_in_]),
            columns=scaler.feature_names_in_,
        ).astype(np.float64)
        del data_columns
        del scaler
        gc_collect()

    # verify columns and ensure column order
    with spinner("verifying column order..."):
        with open("msvc/src/features/column_order.txt", "r") as f:
            columns = [line.strip() for line in f.readlines()]
        assert set(data.columns) == set(columns)
        assert len(data.columns) == len(columns)
        data = data.loc[:, columns]  # ensure order
        data.columns = data.columns.astype(str)

    return data
