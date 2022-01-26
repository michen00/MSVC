"""tests for process_audio"""

from msvc.src.features.process_audio import process_audio


class TestProcessAudio(object):
    def test_dataframe(self):
        """checks the returned dataframe"""
        from pandas import DataFrame, read_feather
        from pydub import AudioSegment
        from tensorflow_hub import load
        import tensorflow.compat.v2 as tf

        tf.enable_v2_behavior()
        # AudioSegment.converter = "ffmpeg.exe"

        class mock_session:
            audio_buffer = AudioSegment.from_wav("msvc/tests/features/test.wav")


        test_audio = process_audio(
            mock_session,
            # load("https://tfhub.dev/google/nonsemantic-speech-benchmark/frill/1"),
            load("msvc/src/features/FRILL/"),
        )
        assert type(test_audio) == DataFrame
        assert len(test_audio.columns) == 2048
        assert not test_audio.isnull().values.any()
        assert all(test_audio == read_feather("msvc/tests/features/test_df.feather"))
