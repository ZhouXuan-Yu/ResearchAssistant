# -*- coding: utf-8 -*-
"""ps_fetch.py - download PaperSpine5 standalone skill + checksums + manifest, then verify."""
import hashlib
import os
import time

import requests

UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
TAG = "v0.4.0-alpha.1-dev"
BASE = f"https://github.com/WUBING2023/PaperSpine/releases/download/{TAG}/"
OUT = r"C:\Users\ZhouXuan\Desktop\OH-WorkSpace\foundation\downloads\paperspine"
FILES = ["checksums.sha256", "manifest.json", "paperspine5-skill-0.4.0-alpha.1-dev.zip"]
MIRRORS = ["{u}", "https://ghfast.top/{u}", "https://gh-proxy.com/{u}", "https://ghproxy.net/{u}"]


def dl(url, dst, min_bytes=1):
    for tpl in MIRRORS:
        target = tpl.format(u=url)
        host = tpl.split("/")[2] if "//" in tpl else "direct"
        tmp = dst + ".part"
        for attempt in range(2):
            try:
                with requests.get(target, headers=UA, timeout=(20, 300), stream=True) as r:
                    if r.status_code != 200:
                        print(f"   [{host}] HTTP {r.status_code}")
                        break
                    n = 0
                    with open(tmp, "wb") as fh:
                        for chunk in r.iter_content(65536):
                            if chunk:
                                fh.write(chunk)
                                n += len(chunk)
                if n >= min_bytes:
                    os.replace(tmp, dst)
                    print(f"   [{host}] OK {n} bytes")
                    return True
                print(f"   [{host}] too small {n}")
            except Exception as exc:  # noqa: BLE001
                print(f"   [{host}] {type(exc).__name__}: {str(exc)[:60]}")
            if os.path.exists(tmp):
                try:
                    os.remove(tmp)
                except OSError:
                    pass
            time.sleep(1.5)
    return False


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for blk in iter(lambda: fh.read(1 << 20), b""):
            h.update(blk)
    return h.hexdigest()


def main():
    os.makedirs(OUT, exist_ok=True)
    for name in FILES:
        print("download", name)
        dl(BASE + name, os.path.join(OUT, name), 10 if name.endswith((".sha256", ".json")) else 100000)

    print("\n--- sha256 verification ---")
    sums = {}
    cs = os.path.join(OUT, "checksums.sha256")
    if os.path.exists(cs):
        with open(cs, "r", encoding="utf-8") as fh:
            for line in fh:
                parts = line.split()
                if len(parts) >= 2:
                    sums[parts[-1].lstrip("*")] = parts[0]
    for name in FILES:
        p = os.path.join(OUT, name)
        if not os.path.exists(p):
            print(f"   {name}: MISSING")
            continue
        got = sha256(p)
        want = sums.get(name)
        if want is None:
            print(f"   {name}: no expected hash found (got {got[:16]}...)")
        else:
            print(f"   {name}: {'MATCH' if got.lower() == want.lower() else 'MISMATCH'}  {got[:16]}...")


if __name__ == "__main__":
    main()
