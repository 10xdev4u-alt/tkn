# Run a quick sanity check on every available vocab size.
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import glob
from tkn import TamilTokenizer

SAMPLE = "வணக்கம் உலகம், இது Tkn tokenizer. தமிழ் உரை சிறப்பாக கையாளப்படுகிறது."

def test_each_vocab_loads():
    paths = glob.glob("tkn/tokenizer*.json")
    for p in paths:
        if "_meta" in p or "tokenizer_config" in p: continue
        # vocab size from filename
        base = os.path.basename(p).replace(".json", "")
        if base == "tokenizer":
            v = 32000
        else:
            v = int(base.replace("tokenizer_", "").replace("k", "")) * 1000
        t = TamilTokenizer(vocab=v)
        assert t.vocab_size == v, f"{p}: expected {v}, got {t.vocab_size}"
        ids = t.encode(SAMPLE)
        assert len(ids) >= 1
        # larger vocab should produce <= tokens (monotonic compression)
        print(f"  vocab {v:>6}: {len(ids)} tokens")

def test_vocab_size_in_vocab():
    # each vocab should know its own size
    for v in [16000, 32000, 64000, 128000]:
        t = TamilTokenizer(vocab=v)
        assert len(t) == v

if __name__ == "__main__":
    test_each_vocab_loads()
    test_vocab_size_in_vocab()
    print("ok")
