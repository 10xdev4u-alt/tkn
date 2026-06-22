# Tkn — Tamil BPE Tokenizer for LLM Cost Reduction

[![CI](https://github.com/10xdev4u-alt/tkn/actions/workflows/ci.yml/badge.svg)](https://github.com/10xdev4u-alt/tkn/actions/workflows/ci.yml)
[![Quickstart](https://github.com/10xdev4u-alt/tkn/actions/workflows/quickstart.yml/badge.svg)](https://github.com/10xdev4u-alt/tkn/actions/workflows/quickstart.yml)
[![Release](https://img.shields.io/github/v/release/10xdev4u-alt/tkn)](https://github.com/10xdev4u-alt/tkn/releases)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue)](https://python.org)

A specialized BPE tokenizer trained on Tamil text. Holds its own — and then some — against GPT-4 and Llama-3.

## Headline

On a held-out slice of Tamil Wikipedia + Kaniyam (200 lines, 94KB UTF-8):

| tokenizer      | tokens | bytes/token | vs gpt-4 | vs llama-3 |
|----------------|-------:|------------:|---------:|-----------:|
| **tkn-bpe-16k**  |  5,810 |       16.20 |   **7.99x** |   **7.99x** |
| **tkn-bpe-32k**  |  5,148 |       18.28 |   **9.01x** |   **9.01x** |
| **tkn-bpe-64k**  |  5,830 |       16.14 |   **7.96x** |   **7.96x** |
| **tkn-bpe-128k** |  4,520 |       20.82 |  **10.27x** |  **10.27x** |
| gpt-4 (cl100k)   | 46,431 |        2.03 |       1.0x |       1.0x |
| llama-3-8b       | 46,425 |        2.03 |       1.0x |       1.0x |

→ Full report: [`benchmarks/results/REPORT.md`](benchmarks/results/REPORT.md)
→ Methodology: [`docs/benchmarks.md`](docs/benchmarks.md)

## Use

```python
from tkn import TamilTokenizer
t = TamilTokenizer()                    # 32k (default)
ids = t.encode("வணக்கம் உலகம்")           # → [17701, 5310]
```

Or via HuggingFace:

```python
from tkn import from_pretrained
t = from_pretrained("10xdev4u-alt/tkn", vocab=64000)
```

CLI:

```bash
python cli.py "வணக்கம் உலகம்" --vocab 64000
python compare.py "தமிழ் மொழி"
python token_count.py path/to/file.txt     # cost estimate
python cost.py path/to/file.txt            # USD estimate
python batch_tokenize.py in.jsonl out.jsonl  # JSONL → id stream
```

## Which vocab to pick

| vocab | bytes/token | vs gpt-4 | when to use |
|------:|------------:|---------:|-------------|
|  16k  |       16.20 |   7.99x  | mobile, edge, smallest model |
|  32k  |       18.28 |   9.01x  | default — best balance |
|  64k  |       16.14 |   7.96x  | better OOV for rare forms |
| 128k  |       20.82 |  10.27x  | max compression, server-side |

## API

```python
t = TamilTokenizer(vocab=64000)
t.encode("வணக்கம்")              # → [17701]
t.encode_batch(["அ", "ஆ"])        # → [[...], [...]]
t.decode([17701, 5310])          # → "வணக்கம்உலகம்"
t.encode_with_offsets("வணக்கம் உலகம்")  # → ([17701, 5310], [(0,7), (8,13)])
t.stats("வணக்கம்")               # → {tokens, chars, utf8_bytes, bytes_per_token}
"வணக்கம்" in t                  # → True
len(t)                          # → 32000
t.vocab()                       # → {"<unk>": 0, ..., "வணக்கம்": 17701, ...}
```

## Train your own

```bash
make data           # Tamil Wikipedia
make fetch-kaniyam  # optional: +Kaniyam ebooks
make train          # 32k BPE
make train-all      # all 4 sizes
make oov            # OOV rate by vocab
make bench          # full benchmark
make test           # all tests
```

## Known limitations

- **Decode drops whitespace** (BPE Whitespace pretokenizer). Use `encode_with_offsets()` for span-preserving decode.
- **Mixed-script chat** is only ~2x more efficient than gpt-4. Add English/Indic code-mixed corpus if you need this.
- **Tamil-only vocab.** A combined Tamil + English + Indic model is a separate project.

## Docs

- [`docs/algorithm.md`](docs/algorithm.md) — why BPE + Whitespace
- [`docs/limitations.md`](docs/limitations.md) — honest trade-offs
- [`docs/benchmarks.md`](docs/benchmarks.md) — methodology
- [`docs/faq.md`](docs/faq.md) — common questions

## Files

```
tkn/                       library + 4 BPE models
tok_train/                 BPE training
benchmarks/                vs gpt-4 / llama-3
scripts/                   fetch_corpus, filter_corpus, analyze_oov, inspect_vocab, make_report, export_hf, fetch_kaniyam, merge_corpora, validate_model
tests/                     roundtrip, batch, normalize, idempotent, oov, special, hf_compat, api, offsets, stats, from_pretrained, all_vocabs, fuzz, perf
cli.py / compare.py / token_count.py / cost.py / batch_tokenize.py
docs/                      algorithm, limitations, benchmarks, faq
.github/workflows/         CI: train + test + bench across 4 vocabs; quickstart
```

## License

Apache 2.0.
