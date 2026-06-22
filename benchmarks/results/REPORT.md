# Tkn benchmark report

_Generated: 2026-06-22_

## pure-tamil

| tokenizer | tokens | utf-8 bytes | bytes/token | ms/line |
|---|---:|---:|---:|---:|
| `gpt-4 (cl100k_base)` | 37767 | 76498 | 2.03 | 0.07 |
| `llama-3-8b` | 37754 | 76498 | 2.03 | 0.49 |
| `tkn-bpe-16k` | 5808 | 76498 | 13.17 | 0.10 |
| `tkn-bpe-32k` | 5229 | 76498 | 14.63 | 0.11 |
| `tkn-bpe-64k` | 4786 | 76498 | 15.98 | 0.11 |
| `tkn-bpe-128k` | 4482 | 76498 | 17.07 | 0.11 |

**tkn-bpe-16k** packs **6.50x** more text per token than `gpt-4 (cl100k_base)`.

**tkn-bpe-32k** packs **7.22x** more text per token than `gpt-4 (cl100k_base)`.

**tkn-bpe-64k** packs **7.89x** more text per token than `gpt-4 (cl100k_base)`.

**tkn-bpe-128k** packs **8.43x** more text per token than `gpt-4 (cl100k_base)`.

## mixed-script

| tokenizer | tokens | utf-8 bytes | bytes/token | ms/line |
|---|---:|---:|---:|---:|
| `gpt-4 (cl100k_base)` | 4860 | 12720 | 2.62 | 0.04 |
| `llama-3-8b` | 4860 | 12720 | 2.62 | 0.15 |
| `tkn-bpe-16k` | 3260 | 12720 | 3.90 | 0.04 |
| `tkn-bpe-32k` | 2760 | 12720 | 4.61 | 0.04 |
| `tkn-bpe-64k` | 2460 | 12720 | 5.17 | 0.04 |
| `tkn-bpe-128k` | 2140 | 12720 | 5.94 | 0.02 |

**tkn-bpe-16k** packs **1.49x** more text per token than `gpt-4 (cl100k_base)`.

**tkn-bpe-32k** packs **1.76x** more text per token than `gpt-4 (cl100k_base)`.

**tkn-bpe-64k** packs **1.98x** more text per token than `gpt-4 (cl100k_base)`.

**tkn-bpe-128k** packs **2.27x** more text per token than `gpt-4 (cl100k_base)`.

