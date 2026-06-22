# Lazy Tamil BPE tokenizer.
#   from tkn import TamilTokenizer
#   t = TamilTokenizer()                  # 32k model
#   t = TamilTokenizer(vocab=64000)       # 64k model
from pathlib import Path
from tokenizers import Tokenizer

_HERE = Path(__file__).parent

def _model_path(vocab: int) -> Path:
    p = _HERE / ("tokenizer_64k.json" if vocab >= 64000 else "tokenizer.json")
    if not p.exists():
        raise FileNotFoundError(f"tokenizer model not found: {p}. Run `make train` (or train_bpe.py --vocab 64000).")
    return p

class TamilTokenizer:
    def __init__(self, vocab: int = 32000, path: str | None = None):
        p = Path(path) if path else _model_path(vocab)
        self._tok = Tokenizer.from_file(str(p))
        self.vocab_size = vocab
    def encode(self, text: str) -> list[int]:
        return self._tok.encode(text).ids
    def decode(self, ids) -> str:
        if not ids: return ""
        if isinstance(ids[0], list):
            return [self._tok.decode(i) for i in ids]
        return self._tok.decode(ids)
    def tokenize(self, text: str) -> list[str]:
        return self._tok.encode(text).tokens
    def __repr__(self) -> str:
        return f"TamilTokenizer(vocab={self.vocab_size})"
