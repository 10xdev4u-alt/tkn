# ponytail: one-liner data fetch. Cached by HF after first run.
import os
from datasets import load_dataset
os.makedirs("data", exist_ok=True)
ds = load_dataset("wikimedia/wikipedia", "20231101.ta", split="train", streaming=True)
n = 0
with open("data/tamil_raw.txt", "w", encoding="utf-8") as f:
    for ex in ds:
        t = ex.get("text", "")
        if not any('\u0b80' <= c <= '\u0bff' for c in t):
            continue
        f.write(t.strip() + "\n")
        n += 1
        if n >= 30000:
            break
print("rows", n)
