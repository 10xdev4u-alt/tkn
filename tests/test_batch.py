import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tkn import TamilTokenizer

def test_encode_batch():
    t = TamilTokenizer()
    out = t.encode_batch(["வணக்கம்", "உலகம்", "தமிழ்"])
    assert isinstance(out, list) and len(out) == 3
    assert all(isinstance(x, list) for x in out)
    assert all(isinstance(i, int) for x in out for i in x)

def test_encode_rejects_list():
    t = TamilTokenizer()
    try:
        t.encode(["a", "b"])
    except TypeError:
        return
    raise AssertionError("encode should reject list")

def test_dunder_methods():
    t = TamilTokenizer()
    assert len(t) == 32000
    assert "வணக்கம்" in t
    assert "" not in t

def test_id_token_roundtrip():
    t = TamilTokenizer()
    tok = "தமிழ்"
    assert t.id_to_token(t.token_to_id(tok)) == tok

if __name__ == "__main__":
    test_encode_batch(); test_encode_rejects_list(); test_dunder_methods(); test_id_token_roundtrip()
    print("ok")
