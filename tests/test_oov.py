# OOV words still tokenize (just into multiple subwords). The lib should not crash.
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tkn import TamilTokenizer

def test_oov_tokenizes():
    t = TamilTokenizer()
    # long compound word unlikely to be in 32k vocab as a single token
    s = "கண்டுபிடிக்கப்பட்டுள்ளன"
    ids = t.encode(s)
    assert isinstance(ids, list) and len(ids) >= 1
    assert all(isinstance(i, int) for i in ids)

def test_unicode_garbage_doesnt_crash():
    t = TamilTokenizer()
    for s in ["", " ", "!", "வணக்கம்", "வணக்கம்!", "🎉", "\n", "a" * 1000]:
        ids = t.encode(s)
        assert isinstance(ids, list)

if __name__ == "__main__":
    test_oov_tokenizes(); test_unicode_garbage_doesnt_crash()
    print("ok")
