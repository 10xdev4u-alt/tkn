# Benchmark Tamil BPE vs gpt-4 (cl100k) and llama-3 on pure + mixed Tamil.
# Supports all 4 vocab sizes; use BENCH_QUICK=1 for a 50-line smoke test.
import os, json, time
from tokenizers import Tokenizer

CORPUS = "data/tamil_clean.txt"
QUICK = os.environ.get("BENCH_QUICK") == "1"
N = 50 if QUICK else 200

# Find all model files
import glob
MODELS = {}
for p in sorted(glob.glob("tkn/tokenizer*.json")):
    if "_meta" in p or "tokenizer_config" in p: continue
    name = os.path.basename(p).replace(".json", "")
    if "_meta" in name: continue
    label = name.replace("tokenizer", "tkn-bpe").replace("_", "-")
    if label == "tkn-bpe": label = "tkn-bpe-32k"  # default
    MODELS[label] = p

def load_lines(n):
    out = []; stride = 50 if QUICK else 200
    with open(CORPUS, encoding="utf-8") as f:
        for i, line in enumerate(f):
            line = line.strip()
            if not line: continue
            if i % stride == 0:
                out.append(line)
                if len(out) >= n: break
    return out

MIXED = [
    "நான் இன்று office-ல் meeting-க்கு போகிறேன்",
    "AI-ல் Tamil model train பண்ணணும்",
    "இந்த PDF-ஐ download பண்ணி read பண்ணுங்க",
    "WhatsApp-ல் Tamil typing செய்ய type பண்ணலாம்",
    "Python-ல் tokenizer library use பண்ணுறேன்",
    "mobile phone-ல் app install பண்ணுங்க",
    "என் friend-க்கு birthday wish சொல்லு",
    "online-ல் Tamil course படிங்க",
    "Google-ல் Tamil content search பண்ணலாம்",
    "இந்த video-வை YouTube-ல் share பண்ணு",
] * (5 if QUICK else 20)

def measure(name, encode_fn, lines):
    toks = bytes_ = 0; secs = 0.0
    for s in lines:
        b = s.encode("utf-8"); bytes_ += len(b)
        t0 = time.perf_counter(); ids = encode_fn(s); secs += time.perf_counter() - t0
        toks += len(ids)
    return {"name": name, "tokens": toks, "utf8_bytes": bytes_,
            "bytes_per_token": bytes_/toks, "ms_per_line": 1000*secs/len(lines)}

def main():
    if not MODELS:
        print("no model files found in tkn/. Run `make train` first.")
        return
    results = {}
    for label, samples in [("pure-tamil", load_lines(N)), ("mixed-script", MIXED)]:
        rows = []
        for name, path in MODELS.items():
            tok = Tokenizer.from_file(path)
            rows.append(measure(name, lambda s: tok.encode(s).ids, samples))
        try:
            import tiktoken
            enc = tiktoken.get_encoding("cl100k_base")
            rows.append(measure("gpt-4 (cl100k_base)",
                                lambda s: enc.encode(s, disallowed_special=()), samples))
        except Exception as e:
            print("gpt-4 skipped:", e)
        try:
            from huggingface_hub import snapshot_download
            from transformers import AutoTokenizer
            path = snapshot_download("NousResearch/Meta-Llama-3-8B-Instruct",
                                     allow_patterns=["tokenizer.json","tokenizer_config.json","special_tokens_map.json"])
            lt = AutoTokenizer.from_pretrained(path)
            rows.append(measure("llama-3-8b",
                                lambda s: lt.encode(s, add_special_tokens=False), samples))
        except Exception as e:
            print("llama-3 skipped:", e)
        results[label] = rows

    os.makedirs("benchmarks/results", exist_ok=True)
    import os as _os
    if _os.environ.get("BENCH_JSON"): print(json.dumps(results, indent=2))
    with open("benchmarks/results/bench.json", "w") as f:
        json.dump(results, f, indent=2)

    for label, rows in results.items():
        print(f"\n=== {label} (N={len(samples)}) ===")
        print(f"{'tokenizer':<22} {'tokens':>8} {'bytes':>8} {'b/tok':>7} {'ms/line':>8}")
        for r in rows:
            print(f"{r['name']:<22} {r['tokens']:>8} {r['utf8_bytes']:>8} "
                  f"{r['bytes_per_token']:>7.2f} {r['ms_per_line']:>8.2f}")
        base = next((r for r in rows if r["name"].startswith("gpt-4")), rows[-1])
        for r in rows:
            if r["name"].startswith("tkn"):
                ratio = r["bytes_per_token"] / base["bytes_per_token"]
                print(f"  → {r['name']} packs {ratio:.2f}x more text per token than {base['name']}")

if __name__ == "__main__":
    main()
