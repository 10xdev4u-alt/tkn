# Tkn benchmark report

_Generated: 2026-06-22_

## pure-tamil

| tokenizer | tokens | utf-8 bytes | bytes/token | ms/line |
|---|---:|---:|---:|---:|
| `tkn-bpe-32k` | 5229 | 76498 | 14.63 | 0.11 |
| `tkn-bpe-64k` | 4786 | 76498 | 15.98 | 0.16 |
| `gpt-4 (cl100k_base)` | 37767 | 76498 | 2.03 | 0.06 |
| `llama-3-8b` | 37754 | 76498 | 2.03 | 0.49 |

**tkn-bpe-32k** packs **7.22x** more text per token than `gpt-4 (cl100k_base)`.

**tkn-bpe-64k** packs **7.89x** more text per token than `gpt-4 (cl100k_base)`.

## mixed-script

| tokenizer | tokens | utf-8 bytes | bytes/token | ms/line |
|---|---:|---:|---:|---:|
| `tkn-bpe-32k` | 2760 | 12720 | 4.61 | 0.03 |
| `tkn-bpe-64k` | 2460 | 12720 | 5.17 | 0.03 |
| `gpt-4 (cl100k_base)` | 4860 | 12720 | 2.62 | 0.02 |
| `llama-3-8b` | 4860 | 12720 | 2.62 | 0.09 |

**tkn-bpe-32k** packs **1.76x** more text per token than `gpt-4 (cl100k_base)`.

**tkn-bpe-64k** packs **1.98x** more text per token than `gpt-4 (cl100k_base)`.

