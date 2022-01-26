"""tests for load_frill_module"""

from msvc.src.features.load_frill_module import load_frill_module


class TestLoadFrillModule(object):
    def test_type(self) -> None:
        """checks type of loaded module"""
        class_str = (
            "<class 'tensorflow.python.saved_model.load.Loader."
            + "_recreate_base_user_object.<locals>._UserObject'>"
        )
        assert str(type(load_frill_module())) == class_str
