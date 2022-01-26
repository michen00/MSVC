"""tests for loading the classifier"""

from msvc.src.models.load_classifier import load_classifier


class TestLoadClassifier(object):
    def test_attributes(self) -> None:
        """check type and key attributes of classifier"""
        from sklearn.ensemble import StackingClassifier

        classifier = load_classifier()
        assert type(classifier) == StackingClassifier
        assert classifier.passthrough
        assert "predict_proba" in dir(classifier)
