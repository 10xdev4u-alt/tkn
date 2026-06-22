# Algorithm: Why BPE with Whitespace pre-tokenization?

Tamil is an abugida script with ~247 letters and rich agglutination (suffixes stack on a root).
A standard BPE trainer (HuggingFace `tokenizers`) handles it well if you:

1. **Use `Whitespace` pre-tokenization** — splits on spaces, so each Tamil "word"
   (which may be a long compound) becomes one pre-token. Without this, byte-level
   BPE treats Tamil as raw UTF-8 bytes and produces 1-2 char pieces.

2. **Train on Tamil-dominant text** — the corpus filter (`scripts/filter_corpus.py`)
   drops lines that are <50% Tamil to keep the merges Tamil-meaningful.

3. **Skip normalization during training** — we let the BPE merges learn from the
   natural surface form. The optional `normalize` flag in `TamilTokenizer` applies
   NFC + ZWJ strip at *inference* time only.

4. **Choose vocab by use case:**
   - 16k: small model, mobile, still 6.5x compression
   - 32k: default, 7.2x, balances size and accuracy
   - 64k: 7.9x, better OOV for rare forms
   - 128k: 8.4x, diminishing returns past here

## What we did NOT do
- **Byte-level BPE** — first attempt, 0.5x compression (worse than gpt-4). Tamil
  characters get split into individual bytes; the BPE merges can't recover whole
  graphemes.
- **Unigram** — would be a strict regression for pure Tamil. BPE wins.
- **SentencePiece** — same algorithm, different Rust binding. No win.

## See also
- `benchmarks/results/REPORT.md` — empirical compression numbers
- `scripts/analyze_oov.py` — OOV rate by vocab size
