"""test visualization"""
from msvc.src.visualization.visualize import visualize
import numpy as np
import pytest


@pytest.mark.mpl_image_compare(tolerance=8.95)
class TestVisualize(object):
    def test_visualization(self) -> None:
        """compare output visualization with expected"""
        return visualize(np.array([[0.423, 0.166, 0.411]]))
