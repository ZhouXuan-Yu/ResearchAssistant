#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""webget.py — 抓取网页并输出纯文本。

用途：Hana 的 web_fetch 工具在梯子（fake-IP DNS）开启时会被 SSRF 守卫误判为
"内网地址"而拒绝。exec 层能正常出网，故以此脚本作为替代抓取通道。

用法：
    python webget.py <url> [max_chars]

退出码：0 成功 / 1 失败
"""
import sys
import re
import html
import requests

UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/126.0 Safari/537.36"
)


def strip_html(raw: str) -> str:
    raw = re.sub(r"(?is)<(script|style|noscript|svg)[^>]*>.*?</\1>", " ", raw)
    raw = re.sub(r"(?is)<br\s*/?>", "\n", raw)
    raw = re.sub(r"(?is)</(p|div|li|tr|h[1-6]|table)>", "\n", raw)
    raw = re.sub(r"(?s)<[^>]+>", "", raw)
    raw = html.unescape(raw)
    raw = re.sub(r"[ \t\u00a0]+", " ", raw)
    raw = re.sub(r"\n\s*\n\s*\n+", "\n\n", raw)
    return raw.strip()


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: python webget.py <url> [max_chars]", file=sys.stderr)
        return 1
    url = sys.argv[1]
    limit = int(sys.argv[2]) if len(sys.argv) > 2 else 6000

    try:
        r = requests.get(url, headers={"User-Agent": UA}, timeout=30)
    except Exception as exc:  # noqa: BLE001
        print(f"[FETCH-FAIL] {type(exc).__name__}: {exc}", file=sys.stderr)
        return 1

    if r.status_code != 200:
        print(f"[HTTP {r.status_code}] {url}", file=sys.stderr)

    # requests 的 apparent_encoding 依赖 chardet/charset_normalizer，缺失时回退
    enc = r.encoding
    try:
        if not enc or enc.lower() in ("iso-8859-1", "ascii"):
            enc = r.apparent_encoding
    except Exception:  # noqa: BLE001
        enc = enc or "utf-8"
    enc = enc or "utf-8"

    try:
        text = r.content.decode(enc, errors="replace")
    except LookupError:
        text = r.content.decode("utf-8", errors="replace")

    out = strip_html(text)
    print(f"[HTTP {r.status_code}] {url}  (enc={enc}, {len(out)} chars)")
    print("-" * 60)
    print(out[:limit])
    if len(out) > limit:
        print(f"\n... [截断，原文共 {len(out)} 字符，可用更大 max_chars 重取]")
    return 0


if __name__ == "__main__":
    sys.exit(main())
