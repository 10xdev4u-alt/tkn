# ponytail: small Tamil normalizer. NFC, strip ZWJ, collapse whitespace.
# Add more rules when a real failure case appears.
import re, unicodedata

_ZWJ_RE = re.compile(r"[\u200b-\u200d\u2060\ufeff]")  # ZWSP, ZWNJ, ZWJ, word joiner, BOM
_MULTI_WS_RE = re.compile(r"[ \t]+")

def normalize(text: str) -> str:
    """Apply Tamil-friendly normalizations. Idempotent."""
    text = unicodedata.normalize("NFC", text)
    text = _ZWJ_RE.sub("", text)
    text = _MULTI_WS_RE.sub(" ", text)
    return text.strip()

if __name__ == "__main__":
    s = "வணக்கம்\u200b  உலகம்"
    n = normalize(s)
    print(f"{s!r} -> {n!r}")
    assert normalize(n) == n, "normalize is not idempotent"
    print("ok")
