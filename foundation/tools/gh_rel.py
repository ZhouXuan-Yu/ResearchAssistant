# -*- coding: utf-8 -*-
"""gh_rel.py - list releases and assets for a GitHub repo, with retries."""
import time

import requests

UA = {"User-Agent": "hana-audit", "Accept": "application/vnd.github+json"}
REPO = "WUBING2023/PaperSpine"


def get(url, tries=4):
    for i in range(tries):
        try:
            r = requests.get(url, headers=UA, timeout=30)
            if r.status_code == 200:
                return r.json()
            print(f"   HTTP {r.status_code} try{i}")
        except Exception as exc:  # noqa: BLE001
            print(f"   {type(exc).__name__} try{i}")
        time.sleep(1.5)
    return None


rels = get(f"https://api.github.com/repos/{REPO}/releases?per_page=10")
if not rels:
    print("RELEASES FAILED")
else:
    for rel in rels:
        print("=" * 60)
        print("tag      :", rel.get("tag_name"))
        print("name     :", rel.get("name"))
        print("prerelease:", rel.get("prerelease"), "draft:", rel.get("draft"))
        print("published:", rel.get("published_at"))
        assets = rel.get("assets") or []
        print("assets   :", len(assets))
        for a in assets:
            mb = round((a.get("size") or 0) / 1048576, 2)
            print(f"   - {a.get('name')}  {mb} MB  dl={a.get('download_count')}")
            print(f"     {a.get('browser_download_url')}")
