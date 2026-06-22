import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from transformers import AutoTokenizer

def test_autotokenizer_32k():
    t = AutoTokenizer.from_pretrained("tkn")
    assert t.vocab_size == 32000
    ids = t.encode("வணக்கம்")
    assert all(isinstance(i, int) for i in ids)

def test_specials():
    t = AutoTokenizer.from_pretrained("tkn")
    assert t.unk_token == "<unk>"
    assert t.pad_token == "<pad>"
    assert t.bos_token == "<bos>"
    assert t.eos_token == "<eos>"

def test_decode():
    t = AutoTokenizer.from_pretrained("tkn")
    ids = t.encode("வணக்கம் உலகம்")
    out = t.decode(ids)
    assert "வணக்கம்" in out and "உலகம்" in out

if __name__ == "__main__":
    test_autotokenizer_32k(); test_specials(); test_decode()
    print("ok")
