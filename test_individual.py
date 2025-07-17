import chromo_map as cm
import pytest
from chromo_map import Gradient

def test_gradient_03():
    # Use matplotlib viridis which should be available
    grad1 = cm.cmaps.matplotlib.miscellaneous.viridis
    grad2 = Gradient('viridis', "viridis") 
    assert grad1 == grad2
    print("✓ test_gradient_03 passed")

if __name__ == "__main__":
    test_gradient_03()
