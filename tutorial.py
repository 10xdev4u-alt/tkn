# ponytail: 5-minute tutorial. Read top-to-bottom.
# Each step prints what it does.
from tkn import TamilTokenizer

print("=" * 50)
print("Tkn tutorial — 5 minutes")
print("=" * 50)

# Step 1: load
print("\n[1] Load the 32k tokenizer")
t = TamilTokenizer()
print(f"    {t!r}, vocab size = {len(t)}")

# Step 2: encode
print("\n[2] Encode a Tamil sentence")
s = "வணக்கம் உலகம், இது Tkn tokenizer."
ids = t.encode(s)
print(f"    text:    {s!r}")
print(f"    ids:     {ids}")
print(f"    tokens:  {t.tokenize(s)}")

# Step 3: decode
print("\n[3] Decode back to text")
back = t.decode(ids)
print(f"    decoded: {back!r}")

# Step 4: stats
print("\n[4] Get compression stats")
stats = t.stats(s)
print(f"    {stats}")

# Step 5: batch encode
print("\n[5] Batch encode multiple sentences")
batch = t.encode_batch(["வணக்கம்", "உலகம்", "தமிழ்"])
print(f"    {batch}")

# Step 6: vocab lookup
print("\n[6] Look up a specific token")
print(f"    'வணக்கம்' id: {t.token_to_id('வணக்கம்')}")
print(f"    id 17701 token: {t.id_to_token(17701)!r}")

# Step 7: offsets
print("\n[7] Encode with char offsets (whitespace-preserving)")
ids, spans = t.encode_with_offsets(s)
for i, (start, end) in zip(ids, spans):
    print(f"    {i:>6}  [{start}:{end}]  {s[start:end]!r}")

# Step 8: switch vocab
print("\n[8] Switch to 16k (mobile) and 128k (max compression)")
for v in [16000, 64000, 128000]:
    tt = TamilTokenizer(vocab=v)
    print(f"    vocab={v:>6}:  {len(tt.encode(s)):>3} tokens for {len(s)} chars")

print("\nDone.")
