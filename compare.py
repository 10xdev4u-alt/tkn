#!/usr/bin/env python3
# ponytail: side-by-side token counts for one input. Useful for demos + docs.
import argparse, sys
sys.path.insert(0, ".")
from tkn import TamilTokenizer
import tiktoken

ap = argparse.ArgumentParser()
ap.add_argument("text", nargs="+", help="Text to compare")
ap.add_argument("--vocab", type=int, default=32000)
args = ap.parse_args()
text = " ".join(args.text)
t = TamilTokenizer(vocab=args.vocab)
gpt = tiktoken.get_encoding("cl100k_base").encode(text, disallowed_special=())
print(f"input: {text!r}")
print(f"  tkn-bpe-{args.vocab//1000}k  : {len(t.encode(text)):>3} tokens  ({t.tokenize(text)})")
print(f"  gpt-4 (cl100k) : {len(gpt):>3} tokens")
print(f"  ratio          : {len(gpt)/len(t.encode(text)):.2f}x")
