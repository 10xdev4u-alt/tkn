# ponytail: one roundtrip + one compression test, no fixtures.
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from tkn import TamilTokenizer

def test_roundtrip():
    t = TamilTokenizer()
    s = "வணக்கம் உலகம்"
    ids = t.encode(s)
    assert ids and all(isinstance(i, int) for i in ids)
    back = t.decode(ids)
    assert "வணக்கம்" in back and "உலகம்" in back

def test_compression_beats_gpt4():
    # This is the project's core claim. If this fails, the whole library is a regression.
    import tiktoken
    t = TamilTokenizer()
    enc = tiktoken.get_encoding("cl100k_base")
    sample = "தமிழ் மொழி உலகின் மிகப் பழமையான மொழிகளில் ஒன்றாகும்"
    n_ours = len(t.encode(sample))
    n_gpt4 = len(enc.encode(sample, disallowed_special=()))
    assert n_ours <= n_gpt4 // 3, f"expected at least 3x compression, got ours={n_ours} gpt4={n_gpt4}"

if __name__ == "__main__":
    test_roundtrip(); test_compression_beats_gpt4(); print("tests ok")
