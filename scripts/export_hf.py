# Export HF-compatible tokenizer_config.json + special_tokens_map.json
# so this loads via AutoTokenizer.from_pretrained() with no custom code.
import json
from tokenizers import Tokenizer

META = json.load(open("tkn/tokenizer_meta.json"))
tok = Tokenizer.from_file("tkn/tokenizer.json")
inv = {v: k for k, v in tok.get_vocab().items()}

SPECIAL_TOKENS = ["<unk>", "<pad>", "<bos>", "<eos>"]
SPECIAL_IDS = {tok: inv[i] for i, tok in enumerate([]) }  # placeholder
ids = {inv[i]: i for i in range(len(SPECIAL_TOKENS))}
for t, i in ids.items():
    assert inv[i] == t, f"mismatch: id {i} is {inv.get(i)}, expected {t}"

cfg = {
    "tokenizer_class": "PreTrainedTokenizerFast",
    "model_max_length": 1_000_000,
    "padding_side": "right",
    "truncation_side": "right",
    "do_lower_case": False,
    "unk_token": "<unk>",
    "pad_token": "<pad>",
    "bos_token": "<bos>",
    "eos_token": "<eos>",
    "vocab_size": META["vocab_size"],
    "clean_up_tokenization_spaces": False,
}
with open("tkn/tokenizer_config.json", "w") as f:
    json.dump(cfg, f, indent=2)
# ponytail: special_tokens_map maps token-name -> the token string, not the id
special_map = {name.strip(""): name for name in SPECIAL_TOKENS}
with open("tkn/special_tokens_map.json", "w") as f:
    json.dump(special_map, f, indent=2)
print("wrote tokenizer_config.json + special_tokens_map.json")
print("special id mapping:", ids)
