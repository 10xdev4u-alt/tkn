# Encode twice should be idempotent (after normalize).
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tkn import TamilTokenizer

def test_idempotent_encode():
    t = TamilTokenizer()
    s = "  வணக்கம்\u200b  உலகம்  "
    once = t.encode(s)
    twice = t.encode(t.decode(once))
    assert once == twice, f"not idempotent: {once} vs {twice}"

def test_idempotent_normalize_then_encode():
    t = TamilTokenizer()
    a = t.encode("\u200bவணக்கம்")
    b = t.encode("வணக்கம்")
    assert a == b, f"ZWJ not stripped: {a} vs {b}"

if __name__ == "__main__":
    test_idempotent_encode(); test_idempotent_normalize_then_encode()
    print("ok")
