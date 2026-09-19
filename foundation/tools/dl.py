#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""dl.py — 多镜像下载器。

背景：本机代理会重置 GitHub 资产域（objects.githubusercontent.com / release-assets,
curl 报 Recv failure，Invoke-WebRequest 报"基础连接已经关闭"）。此脚本依次尝试直连与
若干公共镜像，取第一个成功者。

用法：
    python dl.py <url> <out_path> [min_bytes]
退出码：0 成功 / 1 全部失败
"""
import os
import sys

import requests

UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/126.0 Safari/537.36"
)

MIRRORS = [
    "{u}",                                   # 直连
    "https://ghfast.top/{u}",
    "https://ghproxy.net/{u}",
    "https://gh-proxy.com/{u}",
    "https://ghproxy.cc/{u}",
]


def try_download(url: str, out: str, min_bytes: int) -> bool:
    for tpl in MIRRORS:
        target = tpl.format(u=url)
        label = tpl.split("/")[2] if "//" in tpl else "direct"
        tmp = out + ".part"
        try:
            with requests.get(
                target, headers={"User-Agent": UA}, timeout=(20, 240), stream=True
            ) as r:
                if r.status_code != 200:
                    print(f"  [{label}] HTTP {r.status_code}")
                    continue
                size = 0
                with open(tmp, "wb") as fh:
                    for chunk in r.iter_content(65536):
                        if chunk:
                            fh.write(chunk)
                            size += len(chunk)
            if size < min_bytes:
                print(f"  [{label}] 太小 {size} < {min_bytes}")
                os.remove(tmp)
                continue
            os.replace(tmp, out)
            print(f"  [{label}] OK {size} bytes")
            return True
        except Exception as exc:  # noqa: BLE001
            print(f"  [{label}] {type(exc).__name__}: {str(exc)[:70]}")
            if os.path.exists(tmp):
                try:
                    os.remove(tmp)
                except OSError:
                    pass
    return False


def main() -> int:
    if len(sys.argv) < 3:
        print("usage: python dl.py <url> <out_path> [min_bytes]", file=sys.stderr)
        return 1
    url, out = sys.argv[1], sys.argv[2]
    min_bytes = int(sys.argv[3]) if len(sys.argv) > 3 else 10000
    print(f"下载 {url}\n目标 {out} (最小 {min_bytes} bytes)")
    return 0 if try_download(url, out, min_bytes) else 1


if __name__ == "__main__":
    sys.exit(main())
