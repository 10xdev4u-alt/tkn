import sys, os, random, string
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tkn import TamilTokenizer

TA = list("அஆஇஈஉஊஎஏஐஒஓஔகஙசஞடணதநபமயரலவழளறன")
ASCII = list(string.ascii_letters + string.punctuation + " ")
random.seed(42)

def test_random_short():
    t = TamilTokenizer()
    for _ in range(200):
        n_chars = random.randint(1, 50)
        s = "".join(random.choice(TA + ASCII) for _ in range(n_chars))
        ids = t.encode(s)
        assert isinstance(ids, list)
        if ids:
            back = t.decode(ids)
            ta_chars = [c for c in s if 'அ' <= c <= 'ள']
            if ta_chars:
                ta_back = [c for c in back if 'அ' <= c <= 'ள']
                assert len(ta_back) >= len(ta_chars) - 1, f"lost Tamil chars: {s!r} -> {back!r}"

def test_punctuation_only():
    t = TamilTokenizer()
    for s in ["!@#$%", "...", "   ", "\n\n", "—" * 10]:
        ids = t.encode(s)
        assert isinstance(ids, list)

def test_extreme_lengths():
    t = TamilTokenizer()
    # 1000x "வணக்கம் " (with space) — should produce roughly 1000-2000 tokens
    s = "வணக்கம் " * 1000
    ids = t.encode(s)
    assert len(ids) > 500
    # 10000 x's — ASCII compresses well but should still produce many tokens
    s = "x" * 10000
    ids = t.encode(s)
    assert len(ids) > 10  # at least 10 tokens for 10k chars

if __name__ == "__main__":
    test_random_short(); test_punctuation_only(); test_extreme_lengths()
    print("ok")
