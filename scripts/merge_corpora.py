# ponytail: combine multiple Tamil text files, dedupe, output single file.
import sys, re
TA = re.compile(r"[\u0b80-\u0bff]")

def main():
    if len(sys.argv) < 3:
        print("usage: merge_corpora.py output.txt input1.txt [input2.txt ...]")
        sys.exit(1)
    out = sys.argv[1]
    seen = set()
    n_in = n_out = 0
    with open(out, "w", encoding="utf-8") as fo:
        for path in sys.argv[2:]:
            with open(path, encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    n_in += 1
                    if not line: continue
                    if not TA.search(line): continue
                    if line in seen: continue
                    seen.add(line)
                    fo.write(line + "\n")
                    n_out += 1
    print(f"in={n_in} out={n_out} unique={len(seen)} → {out}")

if __name__ == "__main__":
    main()
