import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from transformers import AutoTokenizer

def test_autotokenizer_32k():
    t = AutoTokenizer.from_pretrained("tkn")
    assert t.vocab_size == 32000
    ids = t.encode("வணக்கம்")
    assert all(isinstance(i, int) for i in ids)

def test_autotokenizer_16k():
    t = AutoTokenizer.from_pretrained("tkn", vocab_size=16000)
    assert t.vocab_size == 16000

def test_specials():
    t = AutoTokenizer.from_pretrained("tkn")
    assert t.unk_token == "<unk>"
    assert t.pad_token == "<pad>"
    assert t.bos_token == "<bos>"
    assert t.eos_token == "<eos>"

if __name__ == "__main__":
    test_autotokenizer_32k(); test_autotokenizer_16k(); test_specials()
    print("ok")
