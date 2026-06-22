# Tkn — Tamil BPE Tokenizer for LLM Cost Reduction

A specialized BPE tokenizer trained on Tamil text. On a held-out slice of clean Tamil Wikipedia:

| tokenizer        | tokens | utf-8 bytes | bytes/token | vs gpt-4 |
|------------------|-------:|------------:|------------:|---------:|
| **tkn-bpe-32k**  |  5,229 |      76,498 |    **14.63** | **7.22x** |
| **tkn-bpe-64k**  |  4,786 |      76,498 |    **15.98** | **7.89x** |
| gpt-4 (cl100k)   | 37,767 |      76,498 |        2.03 |     1.0x |
| llama-3-8b       | 37,754 |      76,498 |        2.03 |     1.0x |

GPT-4 and Llama-3 produce nearly identical token counts on Tamil because they both fall back to byte-level encoding for non-Latin scripts. **A Tamil-tuned tokenizer wins by 7-8x on pure Tamil text** and **~2x on mixed Tamil/English chat**.

→ Full report: [`benchmarks/results/REPORT.md`](benchmarks/results/REPORT.md)

## Use

```python
from tkn import TamilTokenizer
t = TamilTokenizer()                    # 32k model (default)
ids = t.encode("வணக்கம் உலகம்")           # → [17701, 5310]
print(t.decode(ids))                    # 'வணக்கம்உலகம்'
```

Or via HuggingFace (no custom code required):

```python
from transformers import AutoTokenizer
t = AutoTokenizer.from_pretrained("10xdev4u-alt/tkn")
t.encode("வணக்கம் உலகம்")
```

CLI:

```bash
$ python cli.py "வணக்கம் உலகம்"
text   : 'வணக்கம் உலகம்'
tokens : ['வணக்கம்', 'உலகம்']
ids    : [17701, 5310]
count  : 2

$ python compare.py "தமிழ் மொழி உலகின் மிகப் பழமையான மொழிகளில் ஒன்றாகும்"
input: 'தமிழ் மொழி உலகின் மிகப் பழமையான மொழிகளில் ஒன்றாகும்'
  tkn-bpe-32k  :   7 tokens
  gpt-4 (cl100k) :  71 tokens
  ratio          : 10.14x
```

## Train your own

```bash
make data     # ~30k lines of Tamil Wikipedia → data/tamil_raw.txt
make clean    # filter to Tamil-dominant lines → data/tamil_clean.txt
make train    # → tkn/tokenizer.json (32k vocab)
make train-64k  # → tkn/tokenizer_64k.json (64k vocab)
make bench    # compares to gpt-4 + llama-3
make test     # roundtrip + ≥3x compression assertion
```

## Vocab size

| vocab | bytes/tok | vs gpt-4 | notes                                    |
|-------|-----------|----------|------------------------------------------|
|  32k  |   14.63   |  7.22x   | default, ships in repo                   |
|  64k  |   15.98   |  7.89x   | better for rare-script OOV, slightly bigger |

Past 64k, diminishing returns for pure Tamil — 128k only helps if you're mixing in English/Sanskrit/code.

## Known limitations

- **Mixed-script / code-mixed text** is only ~2x more efficient than gpt-4 because English falls back to byte splitting. Add a normalizer pass + include English/Indic code-mixed corpora if you need this.
- **Decode drops whitespace** (BPE Whitespace pretokenizer). For reconstruction, use offset mapping from `tokenizers` directly, or pre-segment your input.
- **Vocab is Tamil-only.** A combined Tamil + English + Indic model would be the next big project; this one wins the pure-Tamil head-to-head and we want to keep that property clear.

## Skipped, add when

- **Rust inference crate** — `tokenizers` is already Rust under the hood. Wrap a `pyo3` binding when you ship an HTTP service.
- **Go client** — no Go binding for `tokenizers`; would be a small new dep.
- **Unigram / SentencePiece** — switch only if BPE plateaus (it hasn't on pure Tamil).
- **Larger corpus (1GB+ Kaniyam)** — current 656k-line clean corpus is enough to prove the ratio; bigger corpus helps tail frequency, not the headline.
- **Mixed-script normalizer** — pre-pass for `வணக்கம்!` style chat; needed if you target conversational data.

## Files

```
tkn/                       library (load + encode/decode)
  tokenizer.json           32k BPE model
  tokenizer_64k.json       64k BPE model
  tokenizer_config.json    HF-compatible config
  special_tokens_map.json  HF special tokens
tok_train/train_bpe.py     BPE trainer (HF tokenizers)
benchmarks/bench.py        vs gpt-4 / llama-3, pure + mixed
scripts/fetch_corpus.py    Wikipedia Tamil fetcher
scripts/filter_corpus.py   Tamil-dominance filter
scripts/export_hf.py       HF tokenizer_config exporter
scripts/make_report.py     bench.json → REPORT.md
tests/test_roundtrip.py    roundtrip + compression assertion
cli.py                     one-liner CLI
compare.py                 side-by-side comparison
examples/demo.py           notebook-friendly smoke test
.github/workflows/ci.yml   CI: train + test + bench
```

## License

Apache 2.0.
