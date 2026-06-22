# Fetch additional Tamil text from public HF datasets.
# Kaniyam Foundation's original GitHub repo is gone; we use HF mirrors instead.
import os, sys
from datasets import load_dataset

DEST = "data/kaniyam_raw.txt"

# These are public mirrors of Tamil text corpora. Ponytail: pick what's available;
# a fetch failure on one shouldn't kill the whole script.
SOURCES = [
    ("Abirami/tamilwikipediadataset", None, "train", "text"),
    ("AnanthZeke/oscar_tamil_clean", None, "train", "text"),
]

def main():
    n = 0
    os.makedirs("data", exist_ok=True)
    with open(DEST, "w", encoding="utf-8") as fo:
        for name, cfg, split, key in SOURCES:
            try:
                if cfg:
                    ds = load_dataset(name, cfg, split=split, streaming=True)
                else:
                    ds = load_dataset(name, split=split, streaming=True)
                local_n = 0
                for ex in ds:
                    text = ex.get(key, "") if isinstance(ex, dict) else ""
                    if text and any('\u0b80' <= c <= '\u0bff' for c in text):
                        fo.write(text.strip() + "\n")
                        n += 1
                        local_n += 1
                        if local_n >= 5000:
                            break
                print(f"  ok {name}: {local_n} lines")
            except Exception as e:
                print(f"  skip {name}: {e}", file=sys.stderr)
    import os
    print(f"kaniyam rows: {n} → {DEST}")

if __name__ == "__main__":
    main()
    os._exit(0)
