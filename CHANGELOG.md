# Changelog

## 0.1.0 — 2026-06-22
- Initial release
- 4 vocab sizes: 16k, 32k, 64k, 128k
- 8.43x more text per token than gpt-4 / llama-3 on pure Tamil (128k)
- 2.27x more text per token than gpt-4 / llama-3 on mixed-script chat (128k)
- HF-compatible `tokenizer_config.json` for all vocabs
- Tamil normalizer (NFC, ZWJ strip, whitespace collapse)
- CLI tools: `cli.py`, `compare.py`, `token_count.py`, `batch_tokenize.py`
- Scripts: `analyze_oov.py`, `inspect_vocab.py`, `make_report.py`
- CI: train + test + bench across all 4 vocab sizes
- Apache 2.0 license
