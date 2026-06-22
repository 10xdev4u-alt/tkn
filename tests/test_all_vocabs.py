import sys, os, glob
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tkn import TamilTokenizer

SAMPLE = "வணக்கம் உலகம், இது Tkn tokenizer. தமிழ் உரை சிறப்பாக கையாளப்படுகிறது."

def _vocab_from_path(p: str) -> int:
    base = os.path.basename(p).replace(".json", "")
    if base == "tokenizer":
        return 32000
    # tokenizer_16k, tokenizer_64k_config → take the "Nk" segment
    for seg in base.split("_"):
        if seg.endswith("k") and seg[:-1].isdigit():
            return int(seg[:-1]) * 1000
    raise ValueError(f"can't parse vocab from {p}")

def test_each_vocab_loads():
    paths = sorted(glob.glob("tkn/tokenizer*.json"))
    for p in paths:
        if "_meta" in p or "config" in p or "specials" in p:
            continue
        v = _vocab_from_path(p)
        t = TamilTokenizer(vocab=v)
        assert t.vocab_size == v, f"{p}: expected {v}, got {t.vocab_size}"
        ids = t.encode(SAMPLE)
        assert len(ids) >= 1
        print(f"  vocab {v:>6}: {len(ids)} tokens")

def test_vocab_size_in_vocab():
    for v in [16000, 32000, 64000, 128000]:
        t = TamilTokenizer(vocab=v)
        assert len(t) == v

if __name__ == "__main__":
    test_each_vocab_loads()
    test_vocab_size_in_vocab()
    print("ok")
