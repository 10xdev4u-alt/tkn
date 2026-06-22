from . import TamilTokenizer
t = TamilTokenizer()
for s in ["தமிழ் மொழி அழகானது", "வணக்கம் உலகம்!", "செயற்கை நுண்ணறிவு"]:
    ids = t.encode(s)
    print(f"{s!r:<40} -> {len(ids):>3} tokens -> {t.decode(ids)!r}")
print("ok")
