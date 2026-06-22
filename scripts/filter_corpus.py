# ponytail: drop lines that aren't Tamil-dominant. Default threshold 50%.
import sys, re
TA = re.compile(r"[\u0b80-\u0bff]")
THRESH = float(sys.argv[1]) if len(sys.argv) > 1 else 0.5
n_in = n_out = 0
with open("data/tamil_raw.txt", encoding="utf-8") as f, \
     open("data/tamil_clean.txt", "w", encoding="utf-8") as g:
    for line in f:
        n_in += 1
        line = line.rstrip("\n")
        if not line: continue
        c = len(line); t = sum(1 for ch in line if TA.match(ch))
        if t / max(c, 1) >= THRESH:
            g.write(line + "\n"); n_out += 1
print(f"in={n_in} kept={n_out} ({100*n_out/n_in:.1f}%) thresh={THRESH}")
