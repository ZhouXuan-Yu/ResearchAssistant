# -*- coding: utf-8 -*-
"""gh_probe.py - read GitHub repo metadata / tree / file via API (requests)."""
import sys

import requests

UA = {
    "User-Agent": "hana-probe",
    "Accept": "application/vnd.github+json",
}


def get(url, as_json=True):
    try:
        r = requests.get(url, headers=UA, timeout=45)
    except Exception as exc:  # noqa: BLE001
        print(f"  NETFAIL {url} :: {type(exc).__name__}: {str(exc)[:90]}")
        return None
    print(f"  HTTP {r.status_code}  {url}  ({len(r.content)} bytes)")
    if r.status_code != 200:
        print("  BODY:", r.text[:300])
        return None
    return r.json() if as_json else r.text


def main():
    repos = ["WUBING2023/PaperSpine", "PKUMichael/PaperSpine"]
    for repo in repos:
        print("=" * 60)
        print("REPO", repo)
        meta = get(f"https://api.github.com/repos/{repo}")
        if meta:
            lic = (meta.get("license") or {}).get("spdx_id")
            print("  desc    :", meta.get("description"))
            print("  stars   :", meta.get("stargazers_count"), "forks:", meta.get("forks_count"))
            print("  license :", lic, "|", (meta.get("license") or {}).get("name"))
            print("  branch  :", meta.get("default_branch"))
            print("  pushed  :", meta.get("pushed_at"))
            print("  size_kb :", meta.get("size"))
        tree = get(f"https://api.github.com/repos/{repo}/git/trees/HEAD?recursive=1")
        if tree:
            blobs = [t for t in tree.get("tree", []) if t.get("type") == "blob"]
            print("  blobs:", len(blobs))
            for t in blobs[:120]:
                print("    ", t.get("path"), t.get("size"))


if __name__ == "__main__":
    sys.exit(main())
