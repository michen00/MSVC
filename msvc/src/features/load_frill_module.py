"""load FRILL module"""

# core
import streamlit as st


@st.experimental_singleton
def load_frill_module():
    """returns the FRILL module as a tensorflow _UserObject"""
    with st.spinner("thank you for your patience..."):
        import tensorflow.compat.v2 as tf
        import tensorflow_hub as hub

        tf.enable_v2_behavior()
        frill_path = "msvc/src/features/FRILL"
        # frill_path = "https://tfhub.dev/google/nonsemantic-speech-benchmark/frill/1"
        return hub.load(frill_path)
