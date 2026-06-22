# Lazy Tamil BPE tokenizer.
from pathlib import Path
from tokenizers import Tokenizer
from .normalize import normalize as _normalize

_HERE = Path(__file__).parent

SPECIALS = ("<unk>", "<pad>", "<bos>", "<eos>")

def _model_path(vocab: int) -> Path:
    p = _HERE / ("tokenizer_64k.json" if vocab >= 64000 else "tokenizer.json")
    if not p.exists():
        raise FileNotFoundError(f"tokenizer model not found: {p}. Run `make train`.")
    return p

class TamilTokenizer:
    def __init__(self, vocab: int = 32000, path: str | None = None, normalize: bool = True):
        p = Path(path) if path else _model_path(vocab)
        self._tok = Tokenizer.from_file(str(p))
        self.vocab_size = vocab
        self.normalize = normalize
        # Cache vocab lookup tables
        self._id_to_token = self._tok.get_vocab()  # actually token -> id; invert below
        self._token_to_id = {v: k for k, v in self._id_to_token.items()}

    def encode(self, text: str) -> list[int]:
        if self.normalize:
            text = _normalize(text)
        return self._tok.encode(text).ids

    def decode(self, ids) -> str:
        if not ids:
            return ""
        if isinstance(ids[0], list):
            return [self._tok.decode(i) for i in ids]
        return self._tok.decode(ids)

    def encode_batch(self, texts: list[str]) -> list[list[int]]:
        return [self.encode(t) for t in texts]

    def tokenize(self, text: str) -> list[str]:
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
