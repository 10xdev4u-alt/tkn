# ponytail: catch a 2x slowdown in encoding. CI-friendly threshold.
import sys, os, time
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tkn import TamilTokenizer

# 5KB of Tamil text
CORPUS_TEXT = "வணக்கம் உலகம், இது Tkn tokenizer. " * 200

def test_encode_speed():
    t = TamilTokenizer()
    t0 = time.perf_counter()
    for _ in range(100):
        t.encode(CORPUS_TEXT)
    elapsed = time.perf_counter() - t0
    per_call_ms = elapsed / 100 * 1000
    # Should be well under 50ms per call on any modern CPU
    assert per_call_ms < 50, f"too slow: {per_call_ms:.2f}ms/call"
    print(f"  encode: {per_call_ms:.3f}ms/call ({len(CORPUS_TEXT)} chars)")

def test_batch_speed():
    t = TamilTokenizer()
    texts = ["வணக்கம் உலகம்"] * 1000
    t0 = time.perf_counter()
    out = t.encode_batch(texts)
    elapsed = time.perf_counter() - t0
    per_call_us = elapsed / 1000 * 1_000_000
    assert per_call_us < 5000, f"batch too slow: {per_call_us:.2f}us/text"
    assert len(out) == 1000
    print(f"  batch encode: {per_call_us:.1f}us/text")

if __name__ == "__main__":
    test_encode_speed(); test_batch_speed()
    print("ok")
