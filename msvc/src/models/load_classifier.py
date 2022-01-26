"""load the classifier"""

# core
from joblib import load
import streamlit as st

# typing
from sklearn.base import BaseEstimator


@st.experimental_singleton
def load_classifier() -> BaseEstimator:
    """returns the pipeline classifier"""

    return load("msvc/src/models/stacked_pass.joblib")
