# -*- coding: utf-8 -*-
"""html2pdf_edge.py - print a local HTML file to PDF via headless Edge/Chrome.

Fallback for the broken office_html-to-pdf helper (missing packaged font css).
Usage: python html2pdf_edge.py <input.html> <output.pdf>
"""
import os
import subprocess
import sys

CANDIDATES = [
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe"),
]


def find_browser():
    for c in CANDIDATES:
        if os.path.exists(c):
            return c
    return None


def main():
    if len(sys.argv) < 3:
        print("usage: python html2pdf_edge.py <in.html> <out.pdf>")
        return 1
    src, dst = os.path.abspath(sys.argv[1]), os.path.abspath(sys.argv[2])
    if not os.path.exists(src):
        print("input missing:", src)
        return 1
    br = find_browser()
    if not br:
        print("NO_BROWSER_FOUND")
        return 2
    print("browser:", br)

    if os.path.exists(dst):
        os.remove(dst)

    url = "file:///" + src.replace("\\", "/")
    cmd = [
        br,
        "--headless=new",
        "--disable-gpu",
        "--no-sandbox",
        "--no-pdf-header-footer",
        "--virtual-time-budget=8000",
        f"--print-to-pdf={dst}",
        url,
    ]
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8",
                       errors="replace", timeout=180)
    print("rc =", r.returncode)
    if r.stderr:
        print("stderr:", r.stderr.strip()[:300])

    if not os.path.exists(dst):
        print("PDF NOT PRODUCED")
        return 3
    size = os.path.getsize(dst)
    with open(dst, "rb") as fh:
        head = fh.read(5)
    print(f"output: {dst}  {size} bytes  header={head!r}")
    return 0 if head.startswith(b"%PDF") else 4


if __name__ == "__main__":
    sys.exit(main())
