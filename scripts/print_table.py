# ponytail: pretty-print the bench results as a markdown table.
import json
r = json.load(open("benchmarks/results/bench.json"))
for label, rows in r.items():
    print(f"\n## {label}\n")
    print("| tokenizer | tokens | bytes/token | vs gpt-4 |")
    print("|---|---:|---:|---:|")
    gpt = next((x for x in rows if x["name"].startswith("gpt-4")), rows[-1])
    for x in rows:
        ratio = x["bytes_per_token"] / gpt["bytes_per_token"]
        marker = "**" if x["name"].startswith("tkn") else ""
        print(f"| {marker}{x['name']}{marker} | {x['tokens']:,} | {x['bytes_per_token']:.2f} | {ratio:.2f}x |")
