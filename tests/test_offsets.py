import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tkn import TamilTokenizer

def test_offsets_basic():
    t = TamilTokenizer()
    s = "வணக்கம் உலகம்"
    ids, spans = t.encode_with_offsets(s)
    assert len(ids) == len(spans)
    # Reconstruct the text from spans
    for i, (start, end) in zip(ids, spans):
        assert s[start:end].strip() == t.id_to_token(i).replace(" ", "")

def test_offsets_empty():
    t = TamilTokenizer()
    ids, spans = t.encode_with_offsets("")
    assert ids == [] and spans == []

if __name__ == "__main__":
    test_offsets_basic(); test_offsets_empty(); print("ok")
