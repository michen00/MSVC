"""tests for main.py"""
import pytest


from msvc.src.app import init_session, reset_session  # , submit_button


class TestInitSession(object):
    def test_no_argument(self) -> None:
        """tests with missing required argument"""
        with pytest.raises(TypeError):
            init_session()

    def test_session_keys(self) -> None:
        """use a dictionary to see if keys are set"""
        from pydub import AudioSegment

        init_session(session := {})  # easier to test with a Dict
        assert "prediction" in session
        assert "audio_buffer" in session
        assert session["prediction"] is None
        assert session["audio_buffer"] == AudioSegment.empty()


class TestResetSession(object):
    def test_session_keys(self) -> None:
        """checks if keys are deleted"""
        reset_session(session := {"prediction": None, "audio_buffer": None})
        # a dictionary is comparable to the session_state object
        assert "prediction" not in session.keys()
        assert "audio_buffer" not in session.keys()


# callback
# class TestSubmitButton(object):
