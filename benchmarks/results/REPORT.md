# Tkn benchmark report

_Generated: 2026-06-22_

## pure-tamil

| tokenizer | tokens | utf-8 bytes | bytes/token | ms/line |
|---|---:|---:|---:|---:|
| `tkn-bpe-16k` | 1126 | 15602 | 13.86 | 0.09 |
| `tkn-bpe-32k` | 992 | 15602 | 15.73 | 0.14 |
| `tkn-bpe-64k` | 916 | 15602 | 17.03 | 0.10 |
| `tkn-bpe-128k` | 877 | 15602 | 17.79 | 0.09 |
| `gpt-4 (cl100k_base)` | 7741 | 15602 | 2.02 | 0.06 |
| `llama-3-8b` | 7741 | 15602 | 2.02 | 0.33 |

**tkn-bpe-16k** packs **6.87x** more text per token than `gpt-4 (cl100k_base)`.

**tkn-bpe-32k** packs **7.80x** more text per token than `gpt-4 (cl100k_base)`.

**tkn-bpe-64k** packs **8.45x** more text per token than `gpt-4 (cl100k_base)`.

**tkn-bpe-128k** packs **8.83x** more text per token than `gpt-4 (cl100k_base)`.

## mixed-script

| tokenizer | tokens | utf-8 bytes | bytes/token | ms/line |
|---|---:|---:|---:|---:|
| `tkn-bpe-16k` | 815 | 3180 | 3.90 | 0.04 |
| `tkn-bpe-32k` | 690 | 3180 | 4.61 | 0.03 |
| `tkn-bpe-64k` | 585 | 3180 | 5.44 | 0.03 |
| `tkn-bpe-128k` | 535 | 3180 | 5.94 | 0.04 |
| `gpt-4 (cl100k_base)` | 1215 | 3180 | 2.62 | 0.02 |
| `llama-3-8b` | 1215 | 3180 | 2.62 | 0.11 |

**tkn-bpe-16k** packs **1.49x** more text per token than `gpt-4 (cl100k_base)`.

**tkn-bpe-32k** packs **1.76x** more text per token than `gpt-4 (cl100k_base)`.

**tkn-bpe-64k** packs **2.08x** more text per token than `gpt-4 (cl100k_base)`.

**tkn-bpe-128k** packs **2.27x** more text per token than `gpt-4 (cl100k_base)`.

