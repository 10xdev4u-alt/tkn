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
__all__ = ["TamilTokenizer", "__version__"]

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
        """Encode a single string into token ids."""
        if not isinstance(text, str):
            raise TypeError(
                f"encode() expects str, got {type(text).__name__}. "
                f"Use encode_batch([...]) for lists."
            )
        if self.normalize:
            text = _normalize(text)
        return self._tok.encode(text).ids

    def encode_batch(self, texts: Iterable[str]) -> list[list[int]]:
        """Encode multiple strings into a list of id-lists."""
        return [self.encode(t) for t in texts]

    def decode(self, ids: list[int] | list[list[int]]) -> str | list[str]:
        """Decode ids back to text. Handles batched input."""
        if not ids:
            return "" if isinstance(ids, list) and (not ids or isinstance(ids[0], int)) else []
        if isinstance(ids[0], list):
            return [self._tok.decode(i) for i in ids]
        return self._tok.decode(ids)

    def tokenize(self, text: str) -> list[str]:
        """Encode a string into human-readable tokens (strings)."""
        if not isinstance(text, str):
            raise TypeError(f"tokenize() expects str, got {type(text).__name__}")
        if self.normalize:
            text = _normalize(text)
        return self._tok.encode(text).tokens

    def vocab(self) -> dict[str, int]:
        """Return a copy of the vocab mapping (token -> id)."""
        return dict(self._token_to_id)

    def id_to_token(self, idx: int) -> str | None:
        """Look up a single token string by id."""
        return self._id_to_token.get(idx)

    def token_to_id(self, token: str) -> int | None:
        """Look up a single id by token string."""
        return self._token_to_id.get(token)

    def __len__(self) -> int:
        return self.vocab_size

    def __contains__(self, token: str) -> bool:
        return token in self._token_to_id

    def __repr__(self) -> str:
        return f"TamilTokenizer(vocab={self.vocab_size})"


# Ponytail: lazy import huggingface_hub so the base lib has zero extra deps.
def from_pretrained(repo_id: str = "10xdev4u-alt/tkn", vocab: int = 32000, **kwargs):
    """Load a Tkn tokenizer from a HuggingFace Hub repo.

    Ponytail: thin wrapper around snapshot_download + TamilTokenizer.
    """
    from huggingface_hub import snapshot_download
    path = snapshot_download(
        repo_id,
        allow_patterns=[
            f"tokenizer{'_' + str(vocab // 1000) + 'k' if vocab != 32000 else ''}.json",
            "tokenizer_config.json" if vocab == 32000 else f"tokenizer_{vocab//1000}k_config.json",
        ],
    )
    name = "tokenizer.json" if vocab == 32000 else f"tokenizer_{vocab//1000}k.json"
    return TamilTokenizer(path=f"{path}/{name}", **kwargs)


    def encode_with_offsets(self, text: str) -> tuple[list[int], list[tuple[int, int]]]:
        """Encode text and return (ids, char_spans) where each span is (start, end) in text.

        Ponytail: useful for roundtripping or rendering highlighted tokens.
        """
        if not isinstance(text, str):
            raise TypeError(f"encode_with_offsets() expects str, got {type(text).__name__}")
        if self.normalize:
            text = _normalize(text)
        enc = self._tok.encode(text)
        return enc.ids, [(s, e) for s, e in enc.offsets]

    def decode_with_offsets(self, ids: list[int]) -> list[tuple[str, tuple[int, int]]]:
        """Decode ids and return list of (token_string, (id, id)) pairs."""
        # Decode each id individually to get spans. Single-id decode returns the token.
        out = []
        for i in ids:
            tok = self._id_to_token.get(i, "")
            out.append((tok, (i, i)))
        return out
