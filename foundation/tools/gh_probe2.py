# -*- coding: utf-8 -*-
"""gh_probe2.py - GitHub API probe with mirror fallback and retries."""
import json
import time

import requests

UA = {"User-Agent": "hana-probe", "Accept": "application/vnd.github+json"}

MIRRORS = [
    "{u}",
    "https://ghfast.top/{u}",
    "https://gh-proxy.com/{u}",
    "https://ghproxy.net/{u}",
]


def fetch(path, as_json=True, tries=2):
    for tpl in MIRRORS:
        url = tpl.format(u=path)
        host = tpl.split("/")[2] if "//" in tpl else "direct"
        for attempt in range(tries):
            try:
                r = requests.get(url, headers=UA, timeout=30)
                if r.status_code == 200:
                    print(f"  OK [{host}] {path} ({len(r.content)}B)")
                    return r.json() if as_json else r.text
                print(f"  [{host}] HTTP {r.status_code} attempt{attempt}")
            except Exception as exc:  # noqa: BLE001
                print(f"  [{host}] {type(exc).__name__} attempt{attempt}")
            time.sleep(1.5)
    return None


def main():
    repo = "WUBING2023/PaperSpine"
    api = f"https://api.github.com/repos/{repo}"
    meta = fetch(api)
    if meta:
        lic = (meta.get("license") or {}).get("spdx_id")
        print("  name    :", meta.get("full_name"))
        print("  desc    :", meta.get("description"))
        print("  stars   :", meta.get("stargazers_count"), "forks:", meta.get("forks_count"))
        print("  license :", lic, "|", (meta.get("license") or {}).get("name"))
        print("  branch  :", meta.get("default_branch"))
        print("  pushed  :", meta.get("pushed_at"))
        print("  topics  :", meta.get("topics"))
    else:
        print("  META FAILED")

    tree = fetch(f"{api}/git/trees/HEAD?recursive=1")
    if tree:
        blobs = [t for t in tree.get("tree", []) if t.get("type") == "blob"]
        print(f"  blobs: {len(blobs)}")
        for t in blobs[:200]:
            print("    ", t.get("path"), t.get("size"))
    else:
        print("  TREE FAILED")


if __name__ == "__main__":
    main()
