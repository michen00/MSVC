"""tests for featurization"""

from msvc.src.features.featurize import featurize, load_extractor


class TestLoadExtractor(object):
    def test_lda(self) -> None:
        """test load LinearDiscriminantAnalysis"""
        from sklearn.discriminant_analysis import LinearDiscriminantAnalysis

        for lda in [
            "ocSVM_sgdlinear_LDA1_-_ocSVM_sgdlinear_LDA2_backup",
            "spherical-ocLDA_neg",
            "spherical-LDA1_-_spherical-LDA2",
        ]:
            assert type(load_extractor(lda)) == LinearDiscriminantAnalysis

    def test_ocsvm(self) -> None:
        """test load OneClassSVM"""
        from sklearn.svm import OneClassSVM

        assert type(load_extractor("LDA-ocSVM_sigmoid_pos")) == OneClassSVM

    def test_ocsvm_sgdlinear(self) -> None:
        """test load SGDOneClassSVM"""
        from sklearn.linear_model import SGDOneClassSVM

        assert type(load_extractor("ocSVM_sgdlinear_neu")) == SGDOneClassSVM

    def test_lof(self) -> None:
        """test load LocalOutlierFactor"""
        from sklearn.neighbors import LocalOutlierFactor

        assert type(load_extractor("LDA-LOF_pos_20")) == LocalOutlierFactor

    def test_robust_scaler(self) -> None:
        """test load RobustScaler"""
        from sklearn.preprocessing import RobustScaler

        assert type(load_extractor("robust_scaler")) == RobustScaler


class TestFeaturize(object):
    def test_with_frill(self) -> None:
        """test featurization of FRILL embeddings"""
        import pandas as pd

        mock_frill_in: pd.DataFrame = pd.read_feather(
            "msvc/tests/features/test_df.feather"
        )
        mock_features_out: pd.DataFrame = pd.read_feather(
            "msvc/tests/features/test_features.feather"
        )
        test_output = featurize(mock_frill_in)
        assert all(test_output == mock_features_out)
        assert all(test_output.index == mock_features_out.index)
        assert all(test_output.columns == mock_features_out.columns)
