# Contributing to Tkn

## Setup
```
python -m venv .venv
.venv/bin/pip install -r requirements-dev.txt
make data
```

## Run tests
```
make test-all      # all tests
make bench         # benchmark (needs internet for llama-3)
```

## Train a new model
```
make train-64k     # or any vocab size
```

## Adding a corpus source
Edit `scripts/fetch_corpus.py` and add a new HF dataset / URL.

## Pull request checklist
- [ ] Tests pass
- [ ] New corpus sources go through `scripts/filter_corpus.py`
- [ ] Bench numbers updated in `benchmarks/results/REPORT.md`
- [ ] Conventional commit messages
