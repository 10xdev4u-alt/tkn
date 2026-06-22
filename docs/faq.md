# FAQ

**Q: Why not use a pre-trained Indic tokenizer?**
A: There aren't great public ones. ai4bharat's models cover Hindi/Bengali well
but Tamil vocab is sparse. Tkn fills that gap with a Tamil-only 8x-compression
model.

**Q: Why not WordPiece (BERT-style)?**
A: BPE and WordPiece are nearly identical for Tamil. BPE is simpler to implement
and trains faster; no measurable difference in compression for our corpus.

**Q: Can I train on a different corpus?**
A: Yes. `python tok_train/train_bpe.py --corpus path/to/your.txt --vocab 32000`.
Wikipedia Tamil is just the default; Kaniyam ebooks or news work too.

**Q: How do I integrate with LangChain / LlamaIndex?**
A: Use `AutoTokenizer.from_pretrained("10xdev4u-alt/tkn")` and pass to your
framework's tokenizer hook.

**Q: License for the model weights?**
A: Apache 2.0. Trained on Wikipedia (CC-BY-SA) which is compatible.

**Q: Can I use this commercially?**
A: Yes. Apache 2.0 allows commercial use. Attribution appreciated.
