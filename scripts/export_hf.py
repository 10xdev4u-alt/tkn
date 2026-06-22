# Export HF-compatible tokenizer_config.json + special_tokens_map.json
# for all model files in tkn/. Ponytail: don't write config by hand.
import json, glob, os
from tokenizers import Tokenizer

SPECIALS = ["<unk>", "<pad>", "<bos>", "<eos>"]

def export(model_path: str):
    name = os.path.basename(model_path)
    if "_meta" in name or "config" in name or "specials" in name: return
    tok = Tokenizer.from_file(model_path)
    inv = {v: k for k, v in tok.get_vocab().items()}
    for i, s in enumerate(SPECIALS):
        assert inv[i] == s, f"{model_path}: id {i} is {inv.get(i)}, expected {s}"
    base = name.replace(".json", "")
    cfg_path = f"tkn/{base}_config.json"
    spec_path = f"tkn/{base}_specials.json"
    cfg = {
        "tokenizer_class": "PreTrainedTokenizerFast",
        "model_max_length": 1_000_000,
        "padding_side": "right", "truncation_side": "right",
        "do_lower_case": False,
        "unk_token": "<unk>", "pad_token": "<pad>",
        "bos_token": "<bos>", "eos_token": "<eos>",
        "vocab_size": tok.get_vocab_size(),
        "clean_up_tokenization_spaces": False,
    }
    with open(cfg_path, "w") as f: json.dump(cfg, f, indent=2)
    with open(spec_path, "w") as f:
        json.dump({s.strip(""): s for s in SPECIALS}, f, indent=2)
    print(f"wrote {cfg_path} + {spec_path}")

def main():
    # Default 32k model: keep existing tokenizer_config.json + special_tokens_map.json
    # Other sizes: write tokenizer_{N}k_config.json + tokenizer_{N}k_specials.json
    for p in sorted(glob.glob("tkn/tokenizer*.json")):
        if "tokenizer_config" in p: continue
        export(p)

if __name__ == "__main__":
    main()
