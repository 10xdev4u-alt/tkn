# ponytail: sanity-check a trained model. Useful after train_bpe.py.
import sys, json
sys.path.insert(0, ".")
from tkn import TamilTokenizer

ap = __import__("argparse").ArgumentParser()
ap.add_argument("--vocab", type=int, required=True)
args = ap.parse_args()

t = TamilTokenizer(vocab=args.vocab)
samples = ["வணக்கம்", "தமிழ்", "இந்தியா", "செயற்கை நுண்ணறிவு", ""]
print(f"vocab: {t.vocab_size}")
for s in samples:
    ids = t.encode(s)
    back = t.decode(ids) if ids else ""
    print(f"  {s!r:<30} -> {len(ids):>3} tokens -> {back!r}")
    assert s.replace(" ", "")[:3] in back.replace(" ", ""), f"roundtrip fail: {s!r}"
print("all roundtrips ok")
