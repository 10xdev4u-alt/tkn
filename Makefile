PY := .venv/bin/python

.PHONY: data filter train train-16k train-64k train-128k train-all bench bench-quick test test-all oov vocab-stats lint type clean help
help:
	@echo "data          fetch + filter Tamil Wikipedia"
	@echo "train         train 32k BPE (default)"
	@echo "train-16k     train 16k BPE (mobile)"
	@echo "train-64k     train 64k BPE"
	@echo "train-128k    train 128k BPE (max compression)"
	@echo "train-all     train all 4 sizes"
	@echo "bench         full benchmark vs gpt-4 + llama-3"
	@echo "bench-quick   50-line bench (for CI)"
	@echo "test          run all tests"
	@echo "oov           OOV rate by vocab"
	@echo "vocab-stats   peek at vocab composition"
	@echo "lint / type   ruff / mypy"
	@echo "clean         remove generated artifacts"

data:
	$(PY) scripts/fetch_corpus.py
	$(PY) scripts/filter_corpus.py 0.5
filter:
	$(PY) scripts/filter_corpus.py 0.5
train:
	$(PY) tok_train/train_bpe.py --vocab 32000 --name tokenizer.json
train-16k:
	$(PY) tok_train/train_bpe.py --vocab 16000 --name tokenizer_16k.json
train-64k:
	$(PY) tok_train/train_bpe.py --vocab 64000 --name tokenizer_64k.json
train-128k:
	$(PY) tok_train/train_bpe.py --vocab 128000 --name tokenizer_128k.json
train-all: train-16k train train-64k train-128k
bench:
	$(PY) benchmarks/bench.py
bench-quick:
	BENCH_QUICK=1 $(PY) benchmarks/bench.py
test:
	$(PY) tests/test_roundtrip.py
	$(PY) tests/test_normalize.py
	$(PY) tests/test_batch.py
	$(PY) tests/test_idempotent.py
	$(PY) tests/test_oov.py
	$(PY) tests/test_special_tokens.py
test-all: test
	$(PY) tests/test_hf_compat.py
oov:
	$(PY) scripts/analyze_oov.py
vocab-stats:
	$(PY) scripts/inspect_vocab.py
lint:
	$(PY) -m ruff check tkn/ tok_train/ scripts/ tests/ benchmarks/ cli.py compare.py token_count.py batch_tokenize.py 2>&1 || true
type:
	$(PY) -m mypy tkn/ 2>&1 || true
clean:
	rm -f tkn/tokenizer.json tkn/tokenizer_*k.json tkn/tokenizer_*k_meta.json tkn/tokenizer_meta.json tkn/tokenizer_*_config.json tkn/tokenizer_*_specials.json
	rm -f benchmarks/results/bench.json
