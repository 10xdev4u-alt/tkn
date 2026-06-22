# ponytail: Tamil Wikipedia fetcher.
# Workaround for a pyarrow/datasets GIL-release crash on streaming cleanup:
# use os._exit(0) to skip Python's interpreter finalization entirely.
import os
os.makedirs("data", exist_ok=True)
from datasets import load_dataset
ds = load_dataset("wikimedia/wikipedia", "20231101.ta", split="train", streaming=True)
texts = []
for ex in ds:
    t = ex.get("text", "")
    if t and any('\u0b80' <= c <= '\u0bff' for c in t):
        texts.append(t.strip())
        if len(texts) >= 30000:
            break
with open("data/tamil_raw.txt", "w", encoding="utf-8") as f:
    for t in texts:
        f.write(t + "\n")
print(f"rows {len(texts)}")
# Hard exit — pyarrow's streaming iterator crashes in __del__ during shutdown.
os._exit(0)
