#!/usr/bin/env python3
# ponytail: one-liner CLI. `python tokenize.py "வணக்கம் உலகம்" [--vocab 64000]`
import argparse, sys
sys.path.insert(0, ".")
from tkn import TamilTokenizer

ap = argparse.ArgumentParser(description="Tamil BPE tokenizer CLI")
ap.add_argument("text", help="Tamil text to tokenize")
ap.add_argument("--vocab", type=int, default=32000, choices=[32000, 64000])
ap.add_argument("--no-decode", action="store_true")
args = ap.parse_args()
t = TamilTokenizer(vocab=args.vocab)
ids = t.encode(args.text)
print(f"text   : {args.text!r}")
print(f"tokens : {t.tokenize(args.text)}")
print(f"ids    : {ids}")
print(f"count  : {len(ids)}")
if not args.no_decode:
    print(f"decode : {t.decode(ids)!r}")
