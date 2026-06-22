# Changelog

## 0.1.0 — 2026-06-22

### Added
- 4 vocab sizes: 16k, 32k, 64k, 128k (BPE, Whitespace pre-tokenizer)
- 8.43x more text per token than gpt-4 / llama-3 on pure Tamil (128k)
- 2.27x more text per token than gpt-4 / llama-3 on mixed-script chat (128k)
- HuggingFace-compatible `tokenizer_config.json` for all vocabs
- Tamil normalizer (NFC, ZWJ strip, whitespace collapse)
- `TamilTokenizer` Python class with encode/decode/encode_batch/tokenize/vocab helpers
- `__len__`, `__contains__`, `__repr__` dunder methods
- Full type hints + `py.typed` marker
- CLI tools: `cli.py`, `compare.py`, `token_count.py`, `batch_tokenize.py`
- Scripts: `analyze_oov.py`, `inspect_vocab.py`, `validate_model.py`, `merge_corpora.py`, `make_report.py`, `export_hf.py`
- Benchmark: `benchmarks/bench.py` (full + quick + JSON modes)
- Tests: roundtrip, batch, normalize, idempotent, OOV, special tokens, HF compat, API
- CI: train + test + bench across 4 vocab sizes; quickstart workflow
- GitHub: issue templates, PR template, Dependabot
- Docs: `docs/algorithm.md`, `docs/limitations.md`, `docs/benchmarks.md`, `docs/faq.md`
- Docker support, `MANIFEST.in`, `setup.cfg`

### Limitations
- Decode drops whitespace (BPE Whitespace pretokenizer)
- Mixed-script compression is ~2x (English falls back to byte splitting)
- Tamil-only vocab (no Sanskrit/Grantha/Hindi coverage)
