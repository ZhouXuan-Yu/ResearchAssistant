# -*- coding: utf-8 -*-
"""gh_get.py - fetch selected files from a GitHub repo (API or raw, with mirror fallback)."""
import base64
import os
import time

import requests

UA = {"User-Agent": "hana-audit", "Accept": "application/vnd.github+json"}

REPO = "WUBING2023/PaperSpine"
OUT = r"C:\Users\ZhouXuan\Desktop\OH-WorkSpace\foundation\external\paper-spine"

FILES = [
    "README.md",
    "LICENSE",
    "INSTALL.md",
    "CLAUDE.md",
    "UPDATE.md",
    "ROLLBACK.md",
    "UNINSTALL.md",
    ".claude-plugin/plugin.json",
    "dist/claude/skills/paper-spine/SKILL.md",
    "dist/claude/skills/paper-spine/references/usage-telemetry.md",
    "dist/claude/skills/paper-spine/references/visual-readiness-gate.md",
    "dist/claude/skills/paper-spine/references/scientific-figure-workflow.md",
]

API = "https://api.github.com/repos/{r}/contents/{p}"
RAW = "https://raw.githubusercontent.com/{r}/HEAD/{p}"


def try_api(path):
    for _ in range(3):
        try:
            r = requests.get(API.format(r=REPO, p=path), headers=UA, timeout=30)
            if r.status_code == 200:
                j = r.json()
                if isinstance(j, dict) and j.get("content"):
                    return base64.b64decode(j["content"]).decode("utf-8", "replace")
            elif r.status_code == 404:
                return None
        except Exception:  # noqa: BLE001
            pass
        time.sleep(1.2)
    return None


def try_raw(path):
    for _ in range(2):
        try:
            r = requests.get(RAW.format(r=REPO, p=path), headers={"User-Agent": "hana-audit"}, timeout=30)
            if r.status_code == 200:
                return r.text
            if r.status_code == 404:
                return None
        except Exception:  # noqa: BLE001
            pass
        time.sleep(1.2)
    return None


def main():
    os.makedirs(OUT, exist_ok=True)
    ok = 0
    for p in FILES:
        print("fetch", p)
        txt = try_api(p)
        src = "api"
        if txt is None:
            txt = try_raw(p)
            src = "raw"
        if txt is None:
            print("   FAILED")
            continue
        dst = os.path.join(OUT, p.replace("/", "__"))
        with open(dst, "w", encoding="utf-8") as fh:
            fh.write(txt)
        ok += 1
        print(f"   OK [{src}] {len(txt)} chars -> {os.path.basename(dst)}")
    print(f"done: {ok}/{len(FILES)}")


if __name__ == "__main__":
    main()
