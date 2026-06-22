# Find OOV words (corpus words that are NOT a single vocab entry) for all models.
# ponytail: this is the "do I need a bigger vocab or bigger corpus?" diagnostic.
# Note: BPE always tokenizes OOV into subwords. The compression ratio is the
# real metric; this is a structural proxy.
import sys, re
sys.path.insert(0, ".")
from tkn import TamilTokenizer

CORPUS = "data/tamil_clean.txt"
N = 5000
TA = re.compile(r"[\u0b80-\u0bff]+")

VOCABS = [16000, 32000, 64000, 128000]

def main():
    # First pass: count total words
    total = 0
    with open(CORPUS, encoding="utf-8") as f:
        for i, line in enumerate(f):
            if i >= N: break
            total += sum(1 for _ in TA.findall(line))
    # Second pass: OOV per vocab
    print(f"corpus words scanned: {total}")
    print(f"{'vocab':>8} | {'OOV words':>10} | {'OOV rate':>9}")
    print("-" * 36)
    for v in VOCABS:
        try:
            t = TamilTokenizer(vocab=v)
        except FileNotFoundError as e:
            print(f"{v:>8} | (not trained)"); continue
        vocab_set = set(t.vocab().keys())
        oov = 0
        with open(CORPUS, encoding="utf-8") as f:
            for i, line in enumerate(f):
                if i >= N: break
                for w in TA.findall(line):
                    if w not in vocab_set: oov += 1
        rate = 100 * oov / max(total, 1)
        print(f"{v:>8} | {oov:>10} | {rate:>8.2f}%")
    print("\nBigger vocab → fewer OOV words. But compression ratio (bench.py) is the truth.")

if __name__ == "__main__":
    main()
