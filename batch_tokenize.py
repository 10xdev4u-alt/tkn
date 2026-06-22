#!/usr/bin/env python3
# ponytail: tokenize a JSONL file, write id-stream to a parallel file.
# Format: input {"text": "..."} per line → output [id, id, id] per line.
import argparse, json, sys
sys.path.insert(0, ".")
from tkn import TamilTokenizer

ap = argparse.ArgumentParser()
ap.add_argument("input", help="Input JSONL with 'text' field per line")
ap.add_argument("output", help="Output file: one int-list per line (JSON)")
ap.add_argument("--vocab", type=int, default=32000)
ap.add_argument("--limit", type=int, default=0, help="Max lines (0 = all)")
ap.add_argument("--text-key", default="text")
args = ap.parse_args()

t = TamilTokenizer(vocab=args.vocab)
n = 0; total_toks = 0
with open(args.input, encoding="utf-8") as fi, open(args.output, "w", encoding="utf-8") as fo:
    for line in fi:
        line = line.strip()
        if not line: continue
        rec = json.loads(line)
        text = rec[args.text_key]
        ids = t.encode(text)
        fo.write(json.dumps(ids, ensure_ascii=False) + "\n")
        total_toks += len(ids)
        n += 1
        if args.limit and n >= args.limit: break
print(f"wrote {n} lines, {total_toks} tokens to {args.output}")
