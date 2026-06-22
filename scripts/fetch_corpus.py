# ponytail: Tamil Wikipedia fetcher.
# Collects into a list first to avoid a pyarrow GIL-release crash during streaming cleanup.
import os, sys
from datasets import load_dataset
os.makedirs("data", exist_ok=True)
ds = load_dataset("wikimedia/wikipedia", "20231101.ta", split="train", streaming=True)
texts = []
for ex in ds:
    t = ex.get("text", "")
    if t and any('\u0b80' <= c <= '\u0bff' for c in t):
        texts.append(t.strip())
        if len(texts) >= 30000:
            break
# Now write outside the streaming context
with open("data/tamil_raw.txt", "w", encoding="utf-8") as f:
    for t in texts:
        f.write(t + "\n")
print(f"rows {len(texts)}")
