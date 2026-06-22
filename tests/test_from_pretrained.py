import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tkn import TamilTokenizer, from_pretrained

def test_local_load_via_path():
    # Direct file-path load (no network) — same code path as from_pretrained
    t = TamilTokenizer(path="tkn/tokenizer.json")
    assert t.vocab_size == 32000
    ids = t.encode("வணக்கம்")
    assert len(ids) == 1
    assert ids[0] == t.token_to_id("வணக்கம்")

def test_from_pretrained_signature():
    import inspect
    sig = inspect.signature(from_pretrained)
    assert "repo_id" in sig.parameters
    assert "vocab" in sig.parameters
    assert sig.parameters["vocab"].default == 32000

if __name__ == "__main__":
    test_local_load_via_path(); test_from_pretrained_signature()
    print("ok")
