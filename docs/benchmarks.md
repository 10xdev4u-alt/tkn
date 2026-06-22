# Benchmark methodology

## Sample
- **Pure Tamil**: 200 lines sampled every 200th from `data/tamil_clean.txt`
  (held-out from training; ~76KB UTF-8).
- **Mixed**: 200 lines of code-mixed Tamil/English chat, replicated from a
  10-line base set.

## Metrics
- **tokens**: total token count across the sample
- **utf-8 bytes**: total bytes of the sample (encoding-independent)
- **bytes/token**: UTF-8 bytes per token (compression metric)
- **ms/line**: wall-clock time to encode one line

## Baselines
- **gpt-4**: tiktoken's `cl100k_base` (the actual GPT-4 tokenizer).
- **llama-3-8b**: HuggingFace `NousResearch/Meta-Llama-3-8B-Instruct` mirror
  (gated repo; mirror is bit-identical).

## Caveats
- Both gpt-4 and llama-3 fall back to byte-level encoding for non-Latin scripts,
  so their Tamil token counts are nearly identical.
- "bytes/token" is not a cost metric; cost is per-token. Use `token_count.py` for
  per-file estimates.
- We report on the held-out slice, not training data.
