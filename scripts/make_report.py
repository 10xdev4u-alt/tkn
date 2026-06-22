# ponytail: turn benchmarks/results/bench.json into a markdown report.
import json, datetime, os

r = json.load(open("benchmarks/results/bench.json"))
out = ["# Tkn benchmark report", "", f"_Generated: {datetime.date.today()}_", ""]
for label, rows in r.items():
    out += [f"## {label}", "",
            "| tokenizer | tokens | utf-8 bytes | bytes/token | ms/line |",
            "|---|---:|---:|---:|---:|"]
    for x in rows:
        out.append(f"| `{x['name']}` | {x['tokens']} | {x['utf8_bytes']} | {x['bytes_per_token']:.2f} | {x['ms_per_line']:.2f} |")
    base = next((x for x in rows if x["name"].startswith("gpt-4")), rows[-1])
    for x in rows:
        if x["name"].startswith("tkn"):
            ratio = x["bytes_per_token"] / base["bytes_per_token"]
            out += ["", f"**{x['name']}** packs **{ratio:.2f}x** more text per token than `{base['name']}`."]
    out.append("")
os.makedirs("benchmarks/results", exist_ok=True)
with open("benchmarks/results/REPORT.md", "w") as f:
    f.write("\n".join(out) + "\n")
print("wrote benchmarks/results/REPORT.md")
