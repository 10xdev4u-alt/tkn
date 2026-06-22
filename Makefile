PY := .venv/bin/python

.PHONY: data clean train train-all train-16k train-64k train-128k bench bench-quick test oov vocab-stats help
help:
	@echo "make data           fetch + filter Tamil Wikipedia"
	@echo "make train          train 32k BPE"
	@echo "make train-16k      train 16k BPE (mobile)"
	@echo "make train-64k      train 64k BPE"
	@echo "make train-128k     train 128k BPE (max compression)"
	@echo "make train-all      train 16k+32k+64k+128k"
	@echo "make bench          benchmark vs gpt-4 + llama-3"
	@echo "make bench-quick    quick bench (50 lines, for CI)"
	@echo "make test           roundtrip + compression assertions"
	@echo "make oov            report OOV rate by vocab size"
	@echo "make vocab-stats    peek at vocab composition"
	@echo "make clean          remove generated artifacts"

data:
	$(PY) scripts/fetch_corpus.py
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
	$(PY) -c "import os, sys; sys.path.insert(0,'.'); os.environ['BENCH_QUICK']='1'; exec(open('benchmarks/bench.py').read())" 2>&1 | tail -20
test:
	$(PY) tests/test_roundtrip.py
	$(PY) tests/test_normalize.py
	$(PY) tests/test_batch.py
oov:
	$(PY) scripts/analyze_oov.py
vocab-stats:
	$(PY) scripts/inspect_vocab.py
clean:
	rm -rf tkn/tokenizer.json tkn/tokenizer_*k.json tkn/tokenizer_*k_meta.json tkn/tokenizer_meta.json benchmarks/results/bench.json

.PHONY: lint type test-all
lint:
	.venv/bin/python -m ruff check tkn/ tok_train/ scripts/ tests/ benchmarks/ cli.py compare.py token_count.py batch_tokenize.py 2>&1 || true
type:
	.venv/bin/python -m mypy tkn/ 2>&1 || true
test-all: test
	.venv/bin/python tests/test_hf_compat.py
