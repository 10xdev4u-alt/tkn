# Train a BPE tokenizer on Tamil text using HuggingFace tokenizers.
# ponytail: Whitespace pre-tokenizer + BPE merges = whole Tamil words in 1 token.
# 32k is the sweet spot for pure Tamil; 64k only helps if corpus has rare-script OOV.
import os, json, argparse
from tokenizers import Tokenizer, models, trainers, pre_tokenizers, decoders

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--corpus", default="data/tamil_clean.txt")
    ap.add_argument("--out", default="tkn")
    ap.add_argument("--vocab", type=int, default=32000)
    ap.add_argument("--name", default="tokenizer.json")
    args = ap.parse_args()
    os.makedirs(args.out, exist_ok=True)
    n_lines = sum(1 for _ in open(args.corpus, encoding="utf-8"))
    def it():
        with open(args.corpus, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line: yield line
    tok = Tokenizer(models.BPE(unk_token="<unk>"))
    tok.pre_tokenizer = pre_tokenizers.Whitespace()
    tok.decoder = decoders.BPEDecoder()
    trainer = trainers.BpeTrainer(
        vocab_size=args.vocab,
        special_tokens=["<unk>", "<pad>", "<bos>", "<eos>"],
        show_progress=False,
    )
    tok.train_from_iterator(it(), trainer=trainer, length=n_lines)
    out_path = os.path.join(args.out, args.name)
    tok.save(out_path)
    meta = {"vocab_size": args.vocab, "algo": "BPE", "pre_tokenizer": "Whitespace",
            "corpus": args.corpus, "lines": n_lines, "file": args.name}
    meta_path = os.path.join(args.out, args.name.replace(".json", "_meta.json"))
    with open(meta_path, "w") as f:
        json.dump(meta, f, indent=2)
    print(f"saved {out_path} vocab={args.vocab} lines={n_lines}")

if __name__ == "__main__":
    main()
