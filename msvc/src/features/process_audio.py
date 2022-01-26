"""preprocess audio for featurization"""

# typing
from pydub import AudioSegment
from streamlit.state.session_state import LazySessionState
from typing import Callable

# core
import numpy as np
import pandas as pd
import streamlit as st

# audio processing
# from os import remove
from pydub import effects
from pydub.silence import detect_leading_silence
from torchaudio import load as torchaudio_load

trim_leading_silence: Callable[[AudioSegment], AudioSegment] = lambda x: x[
    detect_leading_silence(x, silence_threshold=-30.0) :
]


# TODO: separation of concerns / single reponsibility principle
# put the steps in their own methods for better unit testing
def process_audio(session: LazySessionState, frill_module) -> pd.DataFrame:
    """standardizes audio and extracts FRILL embeddings"""
    # set sample_width 16 bits and normalize
    spinner = st.spinner
    with spinner("normalizaing audio and setting sample width..."):
        audio = effects.normalize(session.audio_buffer.set_sample_width(2))

    # trim leading and trailing silence
    with spinner("trimming leading and trailing silence..."):
        try:
            audio = trim_leading_silence(
                trim_leading_silence(audio).reverse()
            ).reverse()
        except IndexError:
            st.exception(IndexError("Audio was too quiet to discern!"))
        if (duration := len(audio)) < 200:
            st.exception(ValueError("Audio contains less than 200 ms of non-silence."))
        elif duration > 60000:
            st.exception(ValueError("Audio exceeds 1 minute in duration."))

    # set mono 16 kHz
    with spinner("setting to mono 16 kHz frame rate..."):
        audio = audio.set_channels(1).set_frame_rate(16000)

    # update session variable
    session.audio_buffer = audio

    # set wav format
    with spinner("exporting PCM S16 LE .wav at 128 kbps..."):
        audio = audio.export(
            # won't play with st.audio if .export called before updating session_state
            format="wav",
            codec="pcm_s16le",
            bitrate="128k",
        )

    with spinner("formatting audio array..."):
        # trim leading zeros
        audio = np.trim_zeros(torchaudio_load(audio)[0][0].numpy())
        if len(audio) < 150:
            st.exception(ValueError("Audio sample is too short."))

    with spinner("extracting FRILL embeddings..."):
        # extract FRILL embeddings
        audio: pd.DataFrame = pd.DataFrame(
            [frill_module(np.expand_dims(audio, axis=0))["embedding"][0]]
        ).astype(
            np.float32
        )  # audio is now a float32 DataFrame of 2,048 FRILL features
        # all cols should be str since the classifier was trained with .feather
        audio.columns = audio.columns.astype(str)

    return audio
