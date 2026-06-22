# Lazy Tamil BPE tokenizer.
#   t = TamilTokenizer()                      # 32k (default)
#   t = TamilTokenizer(vocab=16000)           # 16k (mobile)
#   t = TamilTokenizer(vocab=64000)           # 64k (better OOV)
#   t = TamilTokenizer(vocab=128000)          # 128k (max compression)
from pathlib import Path
from tokenizers import Tokenizer
from .normalize import normalize as _normalize

_HERE = Path(__file__).parent

# ponytail: any vocab works — file naming is the only contract.
def _model_path(vocab: int) -> Path:
    if vocab == 32000:
        p = _HERE / "tokenizer.json"
    else:
        p = _HERE / f"tokenizer_{vocab//1000}k.json"
    if not p.exists():
        raise FileNotFoundError(f"tokenizer model not found: {p}. Run train_bpe.py --vocab {vocab}.")
    return p

class TamilTokenizer:
    def __init__(self, vocab: int = 32000, path: str | None = None, normalize: bool = True):
        p = Path(path) if path else _model_path(vocab)
        self._tok = Tokenizer.from_file(str(p))
        self.vocab_size = vocab
        self.normalize = normalize
        self._token_to_id = self._tok.get_vocab()
        self._id_to_token = {v: k for k, v in self._token_to_id.items()}

    def encode(self, text: str) -> list[int]:
        if not isinstance(text, str):
            raise TypeError(f"encode() expects str, got {type(text).__name__}. Use encode_batch([...])")
        if self.normalize:
            text = _normalize(text)
        return self._tok.encode(text).ids

    def encode_batch(self, texts: list[str]) -> list[list[int]]:
        return [self.encode(t) for t in texts]

    def decode(self, ids) -> str:
        if not ids:
            return ""
        if isinstance(ids[0], list):
            return [self._tok.decode(i) for i in ids]
        return self._tok.decode(ids)

    def tokenize(self, text: str) -> list[str]:
        if not isinstance(text, str):
            raise TypeError(f"tokenize() expects str, got {type(text).__name__}")
        if self.normalize:
            text = _normalize(text)
        return self._tok.encode(text).tokens

    def vocab(self) -> dict[str, int]:
        return dict(self._token_to_id)

    def id_to_token(self, idx: int) -> str | None:
        return self._id_to_token.get(idx)

    def token_to_id(self, token: str) -> int | None:
        return self._token_to_id.get(token)

    def __len__(self) -> int:
        return self.vocab_size

    def __contains__(self, token: str) -> bool:
        return token in self._token_to_id

    def __repr__(self) -> str:
        return f"TamilTokenizer(vocab={self.vocab_size})"
