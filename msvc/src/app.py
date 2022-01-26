<<<<<<< HEAD
"""streamlit app: multilingual speech valence classifier"""

# typing
from typing import Any, Dict
from streamlit.state.session_state import LazySessionState

# core
import pandas as pd
import streamlit as st
from streamlit_webrtc import webrtc_streamer, WebRtcMode

# utility
import queue

# audio preprocessing & featurization
from msvc.src.features.featurize import featurize
from msvc.src.features.load_frill_module import load_frill_module
from msvc.src.features.process_audio import process_audio
from pydub import AudioSegment

# inference and visualization
from msvc.src.models.load_classifier import load_classifier
from msvc.src.visualization.visualize import visualize

FIRST_LOAD: Dict[str, Any] = {
    "prediction": None,
    "audio_buffer": AudioSegment.empty(),
}

# provide ffmpeg.exe location
# AudioSegment.converter = "ffmpeg.exe"


def init_session(session_state: LazySessionState) -> None:
    """session_state initialization parameters"""
    for k, v in FIRST_LOAD.items():
        if k not in session_state:
            session_state[k] = v


def submit_button(session_state: LazySessionState, frill_module) -> None:
    """submits audio in buffer for inference"""
    with st.spinner("processing audio..."):
        audio: pd.DataFrame = featurize(process_audio(session_state, frill_module))
        # infer and update session
        session_state.prediction = load_classifier().predict_proba(audio)


def reset_session(session_state: LazySessionState) -> None:
    """reset session_state"""
    for k in FIRST_LOAD.keys():
        if k in session_state:
            del session_state[k]


def main() -> None:
    """main method"""
    session_state: LazySessionState = st.session_state
    init_session(session_state)
    # header
    with st.container():
        st.title("Multilingual speech valence classifier")
        st.markdown(
            "This app detects whether an utterance is colored with negative, "
            + "neutral, or positive emotional valence."
        )
        st.markdown(
            "Press the START button to record your voice. "
            + "If you are multilingual, try some languages!"
        )
        _ = (  # line length
            lambda _: "* Describe an event that gave rise to a "
            + f"{_} emotional experience."
        )
        with st.expander("Can't think of what to say?", expanded=False):
            st.markdown(
                "\n".join(
                    [
                        "* State the current time.",
                        "* Explain the process of sending an email.",
                        "* Recount an unpleasant dream.",
                        "* Describe the flavors of your least favorite food.",
                        "* Congratulate a good friend on a recent promotion at work.",
                        "* Describe the flavors of your favorite food.",
                    ]
                )
            )

    # display inference
    if session_state.prediction is not None:
        with st.container():
            st.pyplot(visualize(session_state.prediction))
            neg, neu, pos = session_state.prediction[0]
            st.caption(f"negative: {neg:.1%}; neutral: {neu:.1%}; positive: {pos:.1%}")

    # buttons
    with st.container():
        sample = session_state.audio_buffer
        audio_available = sample != AudioSegment.empty()
        if audio_available:
            st.audio(
                sample.export(format="wav", codec="pcm_s16le", bitrate="128k").read()
            )
            checkbox = st.checkbox(
                "I am ready to submit my voice for inference.", value=False
            )
            with st.spinner("loading audio processor..."):
                frill_module = load_frill_module()
            if checkbox:
                st.button(
                    label="submit",
                    on_click=submit_button,
                    args=[session_state, frill_module],
                )
        else:
            with (record_section := st.container()):
                webrtc_ctx = webrtc_streamer(
                    key="sendonly-audio",
                    mode=WebRtcMode.SENDONLY,
                    audio_receiver_size=1024,
                    rtc_configuration={
                        "iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]
                    },
                    media_stream_constraints={"audio": True, "video": False},
                )

                with st.spinner(text="recording..."):
                    while True:
                        if webrtc_ctx.audio_receiver:
                            try:
                                audio_frames = webrtc_ctx.audio_receiver.get_frames(
                                    timeout=3
                                )
                            except queue.Empty:
                                record_section.write("no audio received...")
                            sound_chunk = AudioSegment.empty()
                            try:
                                for audio_frame in audio_frames:
                                    sound = AudioSegment(
                                        data=audio_frame.to_ndarray().tobytes(),
                                        sample_width=audio_frame.format.bytes,
                                        frame_rate=audio_frame.sample_rate,
                                        channels=len(audio_frame.layout.channels),
                                    )
                                    sound_chunk += sound
                                if len(sound_chunk) > 0:
                                    session_state.audio_buffer += sound_chunk
                            except UnboundLocalError:
                                # UnboundLocalError when audio_frames is not set
                                record_section.write("no audio detected...")
                        else:
                            break

    # reset button
    if audio_available:
        with st.container():
            st.button(label="reset", on_click=reset_session, args=[session_state])


if __name__ == "__main__":
    main()
    with st.expander("disclaimer", expanded=False):
        st.write(
            """
THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS 'AS IS' AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT,
INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY
OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE
OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED
OF THE POSSIBILITY OF SUCH DAMAGE.
            """
        )
=======
"""streamlit app: multilingual speech valence classifier"""

# typing
from typing import Any, Dict
from streamlit.state.session_state import LazySessionState

# core
import pandas as pd
import streamlit as st
from streamlit_webrtc import webrtc_streamer, WebRtcMode

# utility
# from pydub.utils import which
import queue

# audio preprocessing & featurization
from msvc.src.features.featurize import featurize
from msvc.src.features.load_frill_module import load_frill_module
from msvc.src.features.process_audio import process_audio
from pydub import AudioSegment

# inference and visualization
from msvc.src.models.load_classifier import load_classifier
from msvc.src.visualization.visualize import visualize

FIRST_LOAD: Dict[str, Any] = {
    "prediction": None,
    "audio_buffer": AudioSegment.empty(),
}

def init_session(session_state: LazySessionState) -> None:
    """session_state initialization parameters"""
    for k, v in FIRST_LOAD.items():
        if k not in session_state:
            session_state[k] = v


def submit_button(session_state: LazySessionState, frill_module) -> None:
    """submits audio in buffer for inference"""
    with st.spinner("processing audio..."):
        audio: pd.DataFrame = featurize(process_audio(session_state, frill_module))
        # infer and update session
        session_state.prediction = load_classifier().predict_proba(audio)


def reset_session(session_state: LazySessionState) -> None:
    """reset session_state"""
    for k in FIRST_LOAD.keys():
        if k in session_state:
            del session_state[k]


def main() -> None:
    """main method"""
    session_state: LazySessionState = st.session_state
    init_session(session_state)
    # header
    with st.container():
        st.title("Multilingual speech valence classifier")
        st.markdown(
            "This app detects whether an utterance is colored with negative, "
            + "neutral, or positive emotional valence."
        )
        st.markdown(
            "Press the START button to record your voice. "
            + "If you are multilingual, try some languages!"
        )
        _ = (  # line length
            lambda _: "* Describe an event that gave rise to a "
            + f"{_} emotional experience."
        )
        with st.expander("Can't think of what to say?", expanded=False):
            st.markdown(
                "\n".join(
                    [
                        "* State the current time.",
                        "* Explain the process of sending an email.",
                        "* Recount an unpleasant dream.",
                        "* Describe the flavors of your least favorite food.",
                        "* Congratulate a good friend on a recent promotion at work.",
                        "* Describe the flavors of your favorite food.",
                    ]
                )
            )

    # display inference
    if session_state.prediction is not None:
        with st.container():
            st.pyplot(visualize(session_state.prediction))
            neg, neu, pos = session_state.prediction[0]
            st.caption(f"negative: {neg:.1%}; neutral: {neu:.1%}; positive: {pos:.1%}")

    # buttons
    with st.container():
        sample = session_state.audio_buffer
        audio_available = sample != AudioSegment.empty()
        if audio_available:
            # provide ffmpeg.exe location
            # AudioSegment.converter = which("/usr/bin/ffmpeg.exe")
            st.audio(
                sample.export(format="wav", codec="pcm_s16le", bitrate="128k").read()
            )
            checkbox = st.checkbox(
                "I am ready to submit my voice for inference.", value=False
            )
            with st.spinner("loading audio processor..."):
                frill_module = load_frill_module()
            if checkbox:
                st.button(
                    label="submit",
                    on_click=submit_button,
                    args=[session_state, frill_module],
                )
        else:
            with (record_section := st.container()):
                webrtc_ctx = webrtc_streamer(
                    key="sendonly-audio",
                    mode=WebRtcMode.SENDONLY,
                    audio_receiver_size=1024,
                    rtc_configuration={
                        "iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]
                    },
                    media_stream_constraints={"audio": True, "video": False},
                )

                with st.spinner(text="recording..."):
                    while True:
                        if webrtc_ctx.audio_receiver:
                            try:
                                audio_frames = webrtc_ctx.audio_receiver.get_frames(
                                    timeout=3
                                )
                            except queue.Empty:
                                record_section.write("no audio received...")
                            sound_chunk = AudioSegment.empty()
                            try:
                                for audio_frame in audio_frames:
                                    sound = AudioSegment(
                                        data=audio_frame.to_ndarray().tobytes(),
                                        sample_width=audio_frame.format.bytes,
                                        frame_rate=audio_frame.sample_rate,
                                        channels=len(audio_frame.layout.channels),
                                    )
                                    sound_chunk += sound
                                if len(sound_chunk) > 0:
                                    session_state.audio_buffer += sound_chunk
                            except UnboundLocalError:
                                # UnboundLocalError when audio_frames is not set
                                record_section.write("no audio detected...")
                        else:
                            break

    # reset button
    if audio_available:
        with st.container():
            st.button(label="reset", on_click=reset_session, args=[session_state])


if __name__ == "__main__":
    main()
    with st.expander("disclaimer", expanded=False):
        st.write(
            """
THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS 'AS IS' AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT,
INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY
OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE
OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED
OF THE POSSIBILITY OF SUCH DAMAGE.
            """
        )
>>>>>>> 7653142f3135c6475adc055d5424e8cba0e383ef
