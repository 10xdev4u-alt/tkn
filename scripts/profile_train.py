# ponytail: profile a small BPE training run to find the bottleneck.
import cProfile, pstats, io
import sys
sys.path.insert(0, ".")

def tiny_train():
    from tokenizers import Tokenizer, models, trainers, pre_tokenizers
    def it():
        with open("data/tamil_clean.txt", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line: yield line
                if sum(1 for _ in range(1)) > 1000: break  # cap for profile
    tok = Tokenizer(models.BPE(unk_token="<unk>"))
    tok.pre_tokenizer = pre_tokenizers.Whitespace()
    trainer = trainers.BpeTrainer(vocab_size=8000, special_tokens=["<unk>"])
    tok.train_from_iterator(it(), trainer=trainer, length=2000)

p = cProfile.Profile()
p.enable()
tiny_train()
p.disable()
s = io.StringIO()
ps = pstats.Stats(p, stream=s).sort_stats("cumulative")
ps.print_stats(15)
print(s.getvalue())
