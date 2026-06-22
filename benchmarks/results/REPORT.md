# Tkn benchmark report

_Generated: 2026-06-22_

## pure-tamil

| tokenizer | tokens | utf-8 bytes | bytes/token | ms/line |
|---|---:|---:|---:|---:|
| `tkn-bpe-16k` | 7154 | 94122 | 13.16 | 0.11 |
| `tkn-bpe-32k` | 6397 | 94122 | 14.71 | 0.13 |
| `tkn-bpe-64k` | 5830 | 94122 | 16.14 | 0.11 |
| `tkn-bpe-128k` | 5481 | 94122 | 17.17 | 0.12 |
| `gpt-4 (cl100k_base)` | 46431 | 94122 | 2.03 | 0.08 |
| `llama-3-8b` | 46425 | 94122 | 2.03 | 0.47 |

**tkn-bpe-16k** packs **6.49x** more text per token than `gpt-4 (cl100k_base)`.

**tkn-bpe-32k** packs **7.26x** more text per token than `gpt-4 (cl100k_base)`.

**tkn-bpe-64k** packs **7.96x** more text per token than `gpt-4 (cl100k_base)`.

**tkn-bpe-128k** packs **8.47x** more text per token than `gpt-4 (cl100k_base)`.

## mixed-script

| tokenizer | tokens | utf-8 bytes | bytes/token | ms/line |
|---|---:|---:|---:|---:|
| `tkn-bpe-16k` | 3100 | 12720 | 4.10 | 0.03 |
| `tkn-bpe-32k` | 2660 | 12720 | 4.78 | 0.03 |
| `tkn-bpe-64k` | 2340 | 12720 | 5.44 | 0.02 |
| `tkn-bpe-128k` | 2140 | 12720 | 5.94 | 0.02 |
| `gpt-4 (cl100k_base)` | 4860 | 12720 | 2.62 | 0.01 |
| `llama-3-8b` | 4860 | 12720 | 2.62 | 0.09 |

**tkn-bpe-16k** packs **1.57x** more text per token than `gpt-4 (cl100k_base)`.

**tkn-bpe-32k** packs **1.83x** more text per token than `gpt-4 (cl100k_base)`.

**tkn-bpe-64k** packs **2.08x** more text per token than `gpt-4 (cl100k_base)`.

**tkn-bpe-128k** packs **2.27x** more text per token than `gpt-4 (cl100k_base)`.

