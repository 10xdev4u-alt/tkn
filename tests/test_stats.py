import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tkn import TamilTokenizer

def test_stats_keys():
    t = TamilTokenizer()
    s = t.stats("வணக்கம்")
    assert set(s.keys()) == {"tokens", "chars", "utf8_bytes", "bytes_per_token"}
    assert s["tokens"] == 1
    assert s["chars"] == 7
    assert s["utf8_bytes"] > 0
    assert s["bytes_per_token"] > 0

def test_stats_empty():
    t = TamilTokenizer()
    s = t.stats("")
    assert s["tokens"] == 0
    assert s["chars"] == 0
    assert s["utf8_bytes"] == 0
    # bytes_per_token divides by max(len(ids), 1) → 0
    assert s["bytes_per_token"] == 0

if __name__ == "__main__":
    test_stats_keys(); test_stats_empty(); print("ok")
