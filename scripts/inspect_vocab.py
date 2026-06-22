# ponytail: peek at the vocab. Most common tokens, longest, shortest, sample OOV.
import sys, re
from collections import Counter
sys.path.insert(0, ".")
from tkn import TamilTokenizer

ap = __import__("argparse").ArgumentParser()
ap.add_argument("--vocab", type=int, default=32000)
ap.add_argument("--top", type=int, default=20)
ap.add_argument("--longest", type=int, default=10)
args = ap.parse_args()

t = TamilTokenizer(vocab=args.vocab)
vocab = t.vocab()
tokens = list(vocab.keys())

# Sort by id (training frequency) for "top"
by_id = sorted(vocab.items(), key=lambda kv: kv[1])
print(f"vocab size: {len(tokens)}")
print(f"\nfirst {args.top} tokens (lowest ids = most frequent in training):")
for tok, idx in by_id[:args.top]:
    print(f"  {idx:>6}  {tok!r}")

# Longest tokens
longest = sorted(tokens, key=len, reverse=True)[:args.longest]
print(f"\nlongest {args.longest} tokens:")
for tok in longest:
    print(f"  {len(tok):>3} chars  {tok!r}")

# Tamil vs non-Tamil
TA = re.compile(r"[\u0b80-\u0bff]")
ta = sum(1 for t in tokens if TA.search(t))
print(f"\nTamil-containing tokens: {ta}/{len(tokens)} ({100*ta/len(tokens):.1f}%)")
