# Quick smoke test.
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tkn import TamilTokenizer

t = TamilTokenizer()  # 32k
s = "வணக்கம்! இது Tkn tokenizer. தமிழ் உரையை மிகச் சிறிய token எண்ணிக்கையில் குறியாக்குகிறது."
ids = t.encode(s)
print(f"text   : {s}")
print(f"tokens : {t.tokenize(s)}")
print(f"count  : {len(ids)} (GPT-4 produces ~7x more on the same text)")
