import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tkn import TamilTokenizer, from_pretrained

def test_local_load_via_path():
    # Direct file-path load (no network) — same code path as from_pretrained
    t = TamilTokenizer(path="tkn/tokenizer.json")
    assert t.vocab_size == 32000
    assert t.encode("வணக்கம்") == [17701]

def test_from_pretrained_signature():
    # Just check the function exists and accepts the expected args
    import inspect
    sig = inspect.signature(from_pretrained)
    assert "repo_id" in sig.parameters
    assert "vocab" in sig.parameters
    # default vocab is 32000
    assert sig.parameters["vocab"].default == 32000

if __name__ == "__main__":
    test_local_load_via_path(); test_from_pretrained_signature()
    print("ok")
