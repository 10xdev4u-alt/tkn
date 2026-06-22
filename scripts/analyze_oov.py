# Find OOV tokens (words in the corpus not in the vocab) and report stats.
# ponytail: this is what tells you whether to grow the corpus or the vocab.
import sys, re
from collections import Counter
sys.path.insert(0, ".")
from tkn import TamilTokenizer

CORPUS = "data/tamil_clean.txt"
N = 5000
TA = re.compile(r"[\u0b80-\u0bff]+")

def main():
    t = TamilTokenizer(vocab=32000)
    vocab_set = set(t.vocab().keys())
    word_count = 0
    oov_count = 0
    oov_examples = Counter()
    with open(CORPUS, encoding="utf-8") as f:
        for i, line in enumerate(f):
            if i >= N: break
            for w in TA.findall(line):
                word_count += 1
                if w not in vocab_set:
                    oov_count += 1
                    oov_examples[w] += 1
    rate = 100 * oov_count / max(word_count, 1)
    print(f"corpus words: {word_count}")
    print(f"oov words:    {oov_count} ({rate:.2f}%)")
    print(f"\ntop 20 OOV words:")
    for w, c in oov_examples.most_common(20):
        print(f"  {c:>5}  {w!r}")

if __name__ == "__main__":
    main()
