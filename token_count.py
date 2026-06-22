#!/usr/bin/env python3
# ponytail: count tokens in a file. Useful for cost estimation.
import argparse, sys
sys.path.insert(0, ".")
from tkn import TamilTokenizer

ap = argparse.ArgumentParser()
ap.add_argument("path", help="Path to text file (UTF-8)")
ap.add_argument("--vocab", type=int, default=32000)
args = ap.parse_args()

t = TamilTokenizer(vocab=args.vocab)
total_tokens = 0
total_bytes = 0
total_lines = 0
with open(args.path, encoding="utf-8") as f:
    for line in f:
        line = line.rstrip("\n")
        if not line: continue
        ids = t.encode(line)
        total_tokens += len(ids)
        total_bytes += len(line.encode("utf-8"))
        total_lines += 1

print(f"file: {args.path}")
print(f"lines: {total_lines}")
print(f"utf-8 bytes: {total_bytes}")
print(f"tkn tokens: {total_tokens} (vocab={args.vocab})")
print(f"bytes/token: {total_bytes/total_tokens:.2f}")
# GPT-4 estimate: ~2 bytes/token for Tamil → ~7x more tokens
print(f"estimated gpt-4 tokens: ~{total_tokens*7:,} (at 7x ratio)")
