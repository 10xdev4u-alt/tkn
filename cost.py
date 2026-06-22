#!/usr/bin/env python3
# ponytail: estimate API cost in $ for tokenizing a file with tkn vs gpt-4.
# Prices as of June 2026 — update when they change.
import argparse, json, sys
sys.path.insert(0, ".")
from tkn import TamilTokenizer

# USD per 1M tokens, input pricing
PRICES = {
    "gpt-4o": 2.50,
    "gpt-4o-mini": 0.15,
    "gpt-4.1": 2.00,
    "claude-sonnet-4.5": 3.00,
    "claude-haiku-4.5": 0.80,
    "gemini-2.5-pro": 1.25,
}

ap = argparse.ArgumentParser()
ap.add_argument("path", help="Text file (UTF-8)")
ap.add_argument("--vocab", type=int, default=32000)
ap.add_argument("--gpt4-multiplier", type=float, default=7.22,
                help="How many more tokens gpt-4 produces per 1 tkn token (32k default)")
ap.add_argument("--model", default="gpt-4o-mini", choices=list(PRICES))
args = ap.parse_args()

t = TamilTokenizer(vocab=args.vocab)
tkn_tokens = 0
bytes_ = 0
with open(args.path, encoding="utf-8") as f:
    for line in f:
        line = line.rstrip("\n")
        if not line: continue
        tkn_tokens += len(t.encode(line))
        bytes_ += len(line.encode("utf-8"))

gpt4_tokens = int(tkn_tokens * args.gpt4_multiplier)
price = PRICES[args.model]
gpt4_cost = gpt4_tokens / 1_000_000 * price
# Tkn is open-source, so the preprocessing cost is local.
# Estimate at $0.0001 per 1k tokens (rough electricity + compute).
tkn_cost = tkn_tokens / 1_000 * 0.0001

print(f"file: {args.path}")
print(f"bytes: {bytes_:,}")
print(f"tkn tokens: {tkn_tokens:,}  (vocab={args.vocab})")
print(f"estimated {args.model} tokens: {gpt4_tokens:,}  (at {args.gpt4_multiplier}x ratio)")
print(f"")
print(f"cost with {args.model} on raw text: ${gpt4_cost:.4f}")
print(f"cost after tkn preprocessing:       ${tkn_cost:.4f}  (local, fixed)")
print(f"savings if you only pay for output tokens: ${gpt4_cost - tkn_cost:.4f} ({100*(1-tkn_cost/gpt4_cost):.1f}%)")
