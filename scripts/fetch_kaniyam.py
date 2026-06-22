# ponytail: Kaniyam Foundation's Tamil ebook collection.
# URL: https://github.com/KaniyamFoundation/datasets
import os, sys, urllib.request
DEST = "data/kaniyam_raw.txt"

URLS = [
    "https://raw.githubusercontent.com/KaniyamFoundation/datasets/master/tamil/தமிழ்_மொழி_இலக்கணம்.txt",
    "https://raw.githubusercontent.com/KaniyamFoundation/datasets/master/tamil/கல்வி.txt",
    "https://raw.githubusercontent.com/KaniyamFoundation/datasets/master/tamil/வரலாறு.txt",
]

def main():
    n = 0
    with open(DEST, "w", encoding="utf-8") as fo:
        for url in URLS:
            try:
                with urllib.request.urlopen(url, timeout=15) as r:
                    data = r.read().decode("utf-8", errors="replace")
                    for line in data.splitlines():
                        line = line.strip()
                        if line:
                            fo.write(line + "\n")
                            n += 1
            except Exception as e:
                print(f"  skip {url}: {e}", file=sys.stderr)
    print(f"kaniyam rows: {n} → {DEST}")

if __name__ == "__main__":
    main()
