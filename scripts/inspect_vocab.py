# ponytail: peek at the vocab. Most common, longest, Tamil vs ASCII split.
import sys, re
sys.path.insert(0, ".")
from tkn import TamilTokenizer

ap = __import__("argparse").ArgumentParser()
ap.add_argument("--vocab", type=int, default=32000)
ap.add_argument("--top", type=int, default=20)
ap.add_argument("--longest", type=int, default=10)
args = ap.parse_args()

t = TamilTokenizer(vocab=args.vocab)
vocab = t.vocab()
TA = re.compile(r"[\u0b80-\u0bff]")
ASCII = re.compile(r"^[\x00-\x7f]+$")

# Skip special tokens for "top frequent"
SPECIALS = {"<unk>", "<pad>", "<bos>", "<eos>"}
by_id = sorted((kv for kv in vocab.items() if kv[0] not in SPECIALS), key=lambda kv: kv[1])

tamil_tokens = [t for t in vocab if TA.search(t) and t not in SPECIALS]
ascii_tokens = [t for t in vocab if ASCII.match(t) and t not in SPECIALS]
mixed = [t for t in vocab if t not in SPECIALS and t not in tamil_tokens and t not in ascii_tokens]

print(f"vocab size: {len(vocab)}")
print(f"  Tamil-containing: {len(tamil_tokens)} ({100*len(tamil_tokens)/len(vocab):.1f}%)")
print(f"  pure ASCII:       {len(ascii_tokens)} ({100*len(ascii_tokens)/len(vocab):.1f}%)")
print(f"  mixed/other:      {len(mixed)} ({100*len(mixed)/len(vocab):.1f}%)")
print(f"\nfirst {args.top} non-special tokens (lowest ids = most frequent):")
for tok, idx in by_id[:args.top]:
    flag = "TA" if TA.search(tok) else ("AS" if ASCII.match(tok) else "  ")
    print(f"  {idx:>6}  {flag}  {tok!r}")

longest = sorted(tamil_tokens, key=len, reverse=True)[:args.longest]
print(f"\nlongest {args.longest} Tamil tokens:")
for tok in longest:
    print(f"  {len(tok):>3} chars  {tok!r}")
