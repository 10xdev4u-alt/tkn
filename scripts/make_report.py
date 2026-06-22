# ponytail: turn benchmarks/results/bench.json into a markdown report.
# Tkn models first (sorted by vocab), then baselines.
import json, datetime, os

r = json.load(open("benchmarks/results/bench.json"))
out = ["# Tkn benchmark report", "", f"_Generated: {datetime.date.today()}_", ""]

def vocab_of(name):
    if not name.startswith("tkn"): return 999_999
    try:
        return int(name.split("-")[-1].rstrip("k")) * 1000
    except ValueError:
        return 0

for label, rows in r.items():
    rows_sorted = sorted(rows, key=lambda x: vocab_of(x["name"]))
    out += [f"## {label}", "",
            "| tokenizer | tokens | utf-8 bytes | bytes/token | ms/line |",
            "|---|---:|---:|---:|---:|"]
    for x in rows_sorted:
        out.append(f"| `{x['name']}` | {x['tokens']} | {x['utf8_bytes']} | {x['bytes_per_token']:.2f} | {x['ms_per_line']:.2f} |")
    base = next((x for x in rows_sorted if x["name"].startswith("gpt-4")), rows_sorted[-1])
    for x in rows_sorted:
        if x["name"].startswith("tkn"):
            ratio = x["bytes_per_token"] / base["bytes_per_token"]
            out += ["", f"**{x['name']}** packs **{ratio:.2f}x** more text per token than `{base['name']}`."]
    out.append("")
os.makedirs("benchmarks/results", exist_ok=True)
with open("benchmarks/results/REPORT.md", "w") as f:
    f.write("\n".join(out) + "\n")
print("wrote benchmarks/results/REPORT.md")
