import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tkn.normalize import normalize

def test_idempotent():
    s = "வணக்கம்\u200b  உலகம்"
    n = normalize(s)
    assert normalize(n) == n

def test_strips_zwj():
    assert "\u200b" not in normalize("a\u200bb")
    assert "\u200c" not in normalize("a\u200cb")

def test_collapses_whitespace():
    assert normalize("a   b\t\tc") == "a b c"

def test_nfc():
    # ன vs ன்: NFC form is canonical
    a, b = "ந", "ந"  # same char, just verify NFC is no-op
    assert normalize(a) == normalize(b) == "ந"

if __name__ == "__main__":
    test_idempotent(); test_strips_zwj(); test_collapses_whitespace(); test_nfc()
    print("ok")
