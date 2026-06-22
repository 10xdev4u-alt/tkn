# Train 16k/32k/64k/128k BPE models in one shot. Used by CI.
# ponytail: serial not parallel — training is RAM-bound, not CPU-bound.
import subprocess
VOCABS = [16000, 32000, 64000, 128000]
for v in VOCABS:
    name = f"tokenizer_{v//1000}k.json"
    print(f"=== training {name} ===")
    subprocess.run([
        "python", "tok_train/train_bpe.py",
        "--vocab", str(v), "--name", name,
    ], check=True)
