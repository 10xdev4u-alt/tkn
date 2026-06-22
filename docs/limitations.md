# Known limitations

1. **Decode drops whitespace** — BPE's `Whitespace` pre-tokenizer doesn't preserve
   space positions through `decode()`. For full reconstruction, use
   `tokenizer.encode(text).offsets` to get character spans.

2. **Mixed-script compression is ~2x** — when Tamil and English interleave (e.g.
   "office-ல் meeting"), English falls back to byte-level splits. Add a mixed
   corpus to retrain if you need >2x on chat data.

3. **Tamil-only vocab** — Sanskrit/Grantha/Hindi shared words may OOV. The 64k
   and 128k variants cover most cases, but a multilingual model is a separate
   project.

4. **No GPU/quantized inference** — this is a preprocessing tokenizer, not a
   model. The HF `tokenizers` library is already C++/Rust; a `pyo3` binding can
   shave 20-30% off latency if you need it.

5. **No incremental training** — the BPE trainer is one-shot. To grow the vocab,
   retrain from scratch with the new corpus (training is <1 minute on a laptop).

6. **No subword regularization** — BPE picks the deterministic split. If you
   need multiple splits for data augmentation, switch to Unigram.
