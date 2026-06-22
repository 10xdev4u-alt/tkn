PY := .venv/bin/python

.PHONY: data train bench test clean
data:
	$(PY) scripts/fetch_corpus.py
train:
	$(PY) tok_train/train_bpe.py
bench:
	$(PY) benchmarks/bench.py
test:
	$(PY) tests/test_roundtrip.py
clean:
	rm -rf tkn/tokenizer.json tkn/tokenizer_meta.json benchmarks/results/bench.json
