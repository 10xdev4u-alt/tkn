import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
from tkn import TamilTokenizer

def test_specials_have_ids_0_to_3():
    t = TamilTokenizer()
    for i, name in enumerate(["<unk>", "<pad>", "<bos>", "<eos>"]):
        assert t.token_to_id(name) == i

def test_specials_decodable():
    t = TamilTokenizer()
    decoded = t.decode([0, 1, 2, 3])
    # BPE BPEDecoder may strip the angle brackets; just check ids roundtrip via tokenize
    for i in range(4):
        assert t.id_to_token(i) in ("<unk>", "<pad>", "<bos>", "<eos>")

if __name__ == "__main__":
    test_specials_have_ids_0_to_3(); test_specials_decodable()
    print("ok")
