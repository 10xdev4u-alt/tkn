import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import tkn
def test_version():
    assert tkn.__version__ == "0.1.0"
def test_all():
    assert "TamilTokenizer" in tkn.__all__
    assert "__version__" in tkn.__all__
if __name__ == "__main__":
    test_version(); test_all(); print("ok")
