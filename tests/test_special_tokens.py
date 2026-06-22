import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tkn import TamilTokenizer

def test_specials_have_ids_0_to_3():
    t = TamilTokenizer()
    for i, name in enumerate(["<unk>", "<pad>", "<bos>", "<eos>"]):
        assert t.token_to_id(name) == i, f"{name} should be id {i}, got {t.token_to_id(name)}"

def test_specials_decodable():
    t = TamilTokenizer()
    decoded = t.decode([0, 1, 2, 3])
    for s in ["<unk>", "<pad>", "<bos>", "<eos>"]:
        assert s in decoded

if __name__ == "__main__":
    test_specials_have_ids_0_to_3(); test_specials_decodable()
    print("ok")
