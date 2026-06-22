# Lazy Tamil BPE tokenizer.
#   t = TamilTokenizer()                      # 32k (default)
#   t = TamilTokenizer(vocab=16000)           # 16k (mobile)
#   t = TamilTokenizer(vocab=64000)           # 64k (better OOV)
#   t = TamilTokenizer(vocab=128000)          # 128k (max compression)
from __future__ import annotations
from pathlib import Path
from typing import Iterable
from tokenizers import Tokenizer
from .normalize import normalize as _normalize
from ._version import __version__

__all__ = ["TamilTokenizer", "from_pretrained", "__version__"]

_HERE = Path(__file__).parent

def _model_path(vocab: int) -> Path:
    """Return the on-disk path for a given vocab size."""
    if vocab == 32000:
        p = _HERE / "tokenizer.json"
    else:
        p = _HERE / f"tokenizer_{vocab // 1000}k.json"
    if not p.exists():
        raise FileNotFoundError(
            f"tokenizer model not found: {p}. "
            f"Run `make train-{vocab // 1000}k` (or train_bpe.py --vocab {vocab})."
        )
    return p

class TamilTokenizer:
    """A BPE tokenizer trained on Tamil text."""

    def __init__(
        self,
        vocab: int = 32000,
        path: str | None = None,
        normalize: bool = True,
    ) -> None:
        p = Path(path) if path else _model_path(vocab)
        self._tok: Tokenizer = Tokenizer.from_file(str(p))
        self.vocab_size: int = vocab
        self.normalize: bool = normalize
        self._token_to_id: dict[str, int] = self._tok.get_vocab()
        self._id_to_token: dict[int, str] = {v: k for k, v in self._token_to_id.items()}

    def encode(self, text: str) -> list[int]:
        if not isinstance(text, str):
            raise TypeError(
                f"encode() expects str, got {type(text).__name__}. "
                f"Use encode_batch([...]) for lists."
            )
        if self.normalize:
            text = _normalize(text)
        return self._tok.encode(text).ids

    def encode_batch(self, texts: Iterable[str]) -> list[list[int]]:
        return [self.encode(t) for t in texts]

    def encode_with_offsets(self, text: str) -> tuple[list[int], list[tuple[int, int]]]:
        """Encode text and return (ids, char_spans) for whitespace-preserving decode."""
        if not isinstance(text, str):
            raise TypeError(f"encode_with_offsets() expects str, got {type(text).__name__}")
        if self.normalize:
            text = _normalize(text)
        enc = self._tok.encode(text)
        return enc.ids, [(s, e) for s, e in enc.offsets]

    def decode(self, ids: list[int] | list[list[int]]) -> str | list[str]:
        if not ids:
            return "" if (isinstance(ids, list) and (not ids or isinstance(ids[0], int))) else []
        if isinstance(ids[0], list):
            return [self._tok.decode(i) for i in ids]
        return self._tok.decode(ids)

    def decode_with_offsets(self, ids: list[int]) -> list[tuple[str, int]]:
        """Decode each id to (token_string, id) pairs."""
        return [(self._id_to_token.get(i, ""), i) for i in ids]

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

    def stats(self, text: str) -> dict:
        """Return token count, char count, bytes, and bytes/token for a string."""
        ids = self.encode(text)
        return {
            "tokens": len(ids),
            "chars": len(text),
            "utf8_bytes": len(text.encode("utf-8")),
            "bytes_per_token": len(text.encode("utf-8")) / max(len(ids), 1),
        }

    def __len__(self) -> int:
        return self.vocab_size

    def __contains__(self, token: str) -> bool:
        return token in self._token_to_id

    def __repr__(self) -> str:
        return f"TamilTokenizer(vocab={self.vocab_size})"


def from_pretrained(repo_id: str = "10xdev4u-alt/tkn", vocab: int = 32000, **kwargs) -> TamilTokenizer:
    """Load a Tkn tokenizer from a HuggingFace Hub repo.

    Ponytail: thin wrapper around snapshot_download + TamilTokenizer.
    """
    from huggingface_hub import snapshot_download
    suffix = "" if vocab == 32000 else f"_{vocab // 1000}k"
    name = f"tokenizer{suffix}.json"
    cfg = "tokenizer_config.json" if vocab == 32000 else f"tokenizer_{vocab // 1000}k_config.json"
    path = snapshot_download(repo_id, allow_patterns=[name, cfg])
    return TamilTokenizer(path=f"{path}/{name}", **kwargs)
