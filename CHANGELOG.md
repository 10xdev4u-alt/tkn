# Changelog

## 0.1.0 — 2026-06-22
- Initial release
- 32k and 64k Tamil BPE models
- 7.89x more text per token than gpt-4 / llama-3 on pure Tamil
- HF-compatible `tokenizer_config.json` for `AutoTokenizer.from_pretrained`
- CLI (`cli.py`) and side-by-side comparator (`compare.py`)
- CI: train + test + bench on push
