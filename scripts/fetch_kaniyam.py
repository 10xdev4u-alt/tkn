# ponytail: Kaniyam Foundation's Tamil ebook collection.
# Uses urllib.parse.quote to handle Tamil chars in URLs.
import os, sys, urllib.request, urllib.parse
DEST = "data/kaniyam_raw.txt"

BASE = "https://raw.githubusercontent.com/KaniyamFoundation/datasets/master/tamil/"
FILES = ["தமிழ்_மொழி_இலக்கணம்.txt", "கல்வி.txt", "வரலாறு.txt"]

def main():
    n = 0
    with open(DEST, "w", encoding="utf-8") as fo:
        for name in FILES:
            url = BASE + urllib.parse.quote(name)
            try:
                with urllib.request.urlopen(url, timeout=15) as r:
                    data = r.read().decode("utf-8", errors="replace")
                    for line in data.splitlines():
                        line = line.strip()
                        if line:
                            fo.write(line + "\n")
                            n += 1
            except Exception as e:
                print(f"  skip {name}: {e}", file=sys.stderr)
    print(f"kaniyam rows: {n} → {DEST}")

if __name__ == "__main__":
    main()
