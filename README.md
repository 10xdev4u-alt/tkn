# Tkn — Tamil BPE Tokenizer for LLM Cost Reduction

A specialized BPE tokenizer trained on Tamil text. Holds its own — and then some — against GPT-4 and Llama-3.

## Headline

On a held-out slice of clean Tamil Wikipedia (200 lines, 76,498 UTF-8 bytes):

| tokenizer      | tokens | bytes/token | vs gpt-4 | vs llama-3 |
|----------------|-------:|------------:|---------:|-----------:|
| **tkn-bpe-16k**  |  5,808 |       13.17 |   **6.50x** |   **6.50x** |
| **tkn-bpe-32k**  |  5,229 |       14.63 |   **7.22x** |   **7.22x** |
| **tkn-bpe-64k**  |  4,786 |       15.98 |   **7.89x** |   **7.89x** |
| **tkn-bpe-128k** |  4,482 |       17.07 |   **8.43x** |   **8.43x** |
| gpt-4 (cl100k)   | 37,767 |        2.03 |       1.0x |       1.0x |
| llama-3-8b       | 37,754 |        2.03 |       1.0x |       1.0x |

GPT-4 and Llama-3 produce near-identical token counts on Tamil because they both fall back to byte-level encoding for non-Latin scripts.

On **mixed Tamil/English** (code-mixed chat): **1.5x to 2.3x** more efficient depending on vocab size.

→ Full report: [`benchmarks/results/REPORT.md`](benchmarks/results/REPORT.md)

## Use

```python
from tkn import TamilTokenizer
t = TamilTokenizer()                    # 32k (default)
ids = t.encode("வணக்கம் உலகம்")           # → [17701, 5310]
```

Or via HuggingFace (no custom code):

```python
from transformers import AutoTokenizer
t = AutoTokenizer.from_pretrained("10xdev4u-alt/tkn")
```

CLI:

```bash
python cli.py "வணக்கம் உலகம்" --vocab 64000
python compare.py "தமிழ் மொழி உலகின் மிகப் பழமையான மொழிகளில் ஒன்றாகும்"
python token_count.py path/to/file.txt     # cost estimate
python batch_tokenize.py in.jsonl out.jsonl  # JSONL → id stream
```

## Which vocab to pick

- **16k** — mobile/edge, smallest model, 6.5x compression.
- **32k** — default. 7.2x compression, balanced size and accuracy.
- **64k** — better OOV for rare-script words. 7.9x.
- **128k** — max compression, 8.4x. Worth it only if you have RAM to spare.

OOV rate (Tamil words that aren't a single vocab entry) at 5,000 sample lines:

| vocab | OOV rate |
|------:|---------:|
|  16k  |   41.8%  |
|  32k  |   30.8%  |
|  64k  |   22.1%  |
| 128k  |   15.4%  |

(OOV still tokenizes into subwords; this is a structural proxy, not a failure.)

## Train your own

```bash
make data           # ~30k lines of Tamil Wikipedia → data/tamil_raw.txt
make clean          # Tamil-dominance filter → data/tamil_clean.txt (656k lines)
make train          # → tkn/tokenizer.json (32k)
make train-all      # → 16k, 32k, 64k, 128k
make oov            # OOV rate by vocab size
make vocab-stats    # Tamil/ASCII split, longest tokens
make bench          # full benchmark vs gpt-4 + llama-3
make test           # all tests
```

## Known limitations

- **Mixed-script chat** is only ~2x more efficient than gpt-4 because English falls back to byte splitting. Add a normalizer pass + include English/Indic code-mixed corpora if you need this.
- **Decode drops whitespace** (BPE Whitespace pretokenizer). For reconstruction, use offset mapping from `tokenizers` directly.
- **Vocab is Tamil-only.** A combined Tamil + English + Indic model is the next big project; this one wins the pure-Tamil head-to-head and we want to keep that property clear.

## Skipped, add when

- **Rust inference crate** — `tokenizers` is already Rust under the hood.
- **Go client** — no Go binding; would be a small new dep.
- **Unigram / SentencePiece** — switch only if BPE plateaus.
- **Larger corpus (1GB+ Kaniyam)** — current 656k-line clean corpus is enough to prove the ratio; bigger corpus helps tail frequency.
- **Mixed-script normalizer** — pre-pass for code-mixed chat; needed if you target conversational data.

## Files

```
tkn/                       library
  tokenizer.json           32k BPE model (default)
  tokenizer_16k.json       16k BPE model (mobile)
  tokenizer_64k.json       64k BPE model
  tokenizer_128k.json       128k BPE model
  tokenizer_config.json    HF-compatible config (32k)
  special_tokens_map.json  HF special tokens
  normalize.py             NFC + ZWJ strip + ws collapse
tok_train/                 BPE training
  train_bpe.py             single-model trainer
  train_all.py             train all 4 vocabs
benchmarks/                vs gpt-4 / llama-3
  bench.py                 full + quick mode
  samples/                 curated Tamil test sentences
scripts/                   fetch_corpus, filter_corpus, analyze_oov, inspect_vocab, make_report
tests/                     roundtrip, batch, normalize, hf_compat
cli.py                     one-shot tokenization
compare.py                 side-by-side vs gpt-4
token_count.py             file-level cost estimation
batch_tokenize.py          JSONL processing
examples/demo.py           smoke test
.github/workflows/ci.yml   CI: train + test + bench across 4 vocabs
```

## License

Apache 2.0.
