#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""fetch_file.py — 下载二进制文件到本地（带重定向与重试）。

用途：Windows 上 Invoke-WebRequest 与 curl.exe 在代理环境下对 GitHub 资源域
（objects.githubusercontent.com 等）常出现 "连接关闭 / Recv failure: Connection
was reset"。Python requests 走同一网络栈时更稳定，故作为下载通道。

用法：
    python fetch_file.py <url> <out_path> [min_bytes]

min_bytes：低于该字节数视为失败（默认 1024）。用于识别被截断的响应。
退出码：0 成功 / 1 失败
"""
import sys
import time
import requests

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"


def main() -> int:
    if len(sys.argv) < 3:
        print("usage: python fetch_file.py <url> <out_path> [min_bytes]", file=sys.stderr)
        return 1
    url, out = sys.argv[1], sys.argv[2]
    min_bytes = int(sys.argv[3]) if len(sys.argv) > 3 else 1024

    last_err = None
    for attempt in range(1, 4):
        try:
            with requests.get(
                url, headers={"User-Agent": UA}, timeout=300, stream=True, allow_redirects=True
            ) as r:
                r.raise_for_status()
                total = 0
                with open(out, "wb") as f:
                    for chunk in r.iter_content(65536):
                        if chunk:
                            f.write(chunk)
                            total += len(chunk)
            if total < min_bytes:
                last_err = f"too small: {total} bytes"
                print(f"[attempt {attempt}] {last_err}", file=sys.stderr)
                time.sleep(2)
                continue
            print(f"OK {out}  {total} bytes  (attempt {attempt})")
            return 0
        except Exception as exc:  # noqa: BLE001
            last_err = f"{type(exc).__name__}: {exc}"
            print(f"[attempt {attempt}] {last_err}", file=sys.stderr)
            time.sleep(3)

    print(f"FAILED after retries: {last_err}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
