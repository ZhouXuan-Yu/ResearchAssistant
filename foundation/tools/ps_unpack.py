# -*- coding: utf-8 -*-
"""ps_unpack.py - extract the PaperSpine5 skill zip and report structure."""
import os
import zipfile

SRC = r"C:\Users\ZhouXuan\Desktop\OH-WorkSpace\foundation\downloads\paperspine\paperspine5-skill-0.4.0-alpha.1-dev.zip"
DST = r"C:\Users\ZhouXuan\Desktop\OH-WorkSpace\foundation\external\paper-spine-skill"


def main():
    os.makedirs(DST, exist_ok=True)
    with zipfile.ZipFile(SRC) as z:
        names = z.namelist()
        print("entries:", len(names))
        z.extractall(DST)

    total = 0
    for root, dirs, files in os.walk(DST):
        for f in files:
            total += 1
    print("files on disk:", total)

    print("\n--- top level ---")
    for e in sorted(os.listdir(DST)):
        p = os.path.join(DST, e)
        print("  ", e + ("/" if os.path.isdir(p) else ""))

    print("\n--- first 60 entries ---")
    for n in names[:60]:
        print("  ", n)

    sk = None
    for root, dirs, files in os.walk(DST):
        if "SKILL.md" in files:
            sk = os.path.join(root, "SKILL.md")
            break
    print("\n--- SKILL.md location ---")
    print("  ", sk)
    if sk:
        with open(sk, "r", encoding="utf-8", errors="replace") as fh:
            head = fh.read(1200)
        print("--- head ---")
        print(head)


if __name__ == "__main__":
    main()
