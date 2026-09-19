# -*- coding: utf-8 -*-
"""env_probe.py - check rendering/drawing toolchain availability."""
import importlib
import shutil
import sys

print("python:", sys.version.split()[0])
print("=" * 60)
print("[1] external binaries")
for exe in ("pdflatex", "xelatex", "tectonic", "pandoc", "latexmk", "bibtex", "soffice", "libreoffice", "dot"):
    print(f"  {exe:12s}: {shutil.which(exe) or '-'}")

print("=" * 60)
print("[2] python packages")
for mod in ("matplotlib", "numpy", "pandas", "docx", "jinja2", "PIL", "yaml", "requests",
            "scipy", "seaborn", "scienceplots", "fitz", "reportlab", "markdown"):
    try:
        m = importlib.import_module(mod)
        v = getattr(m, "__version__", "?")
        print(f"  {mod:14s}: OK  {v}")
    except Exception as exc:  # noqa: BLE001
        print(f"  {mod:14s}: MISSING ({type(exc).__name__})")

print("=" * 60)
print("[3] fonts available to matplotlib (CJK check)")
try:
    import matplotlib
    matplotlib.use("Agg")
    from matplotlib import font_manager
    names = sorted({f.name for f in font_manager.fontManager.ttflist})
    cjk = [n for n in names if any(k in n for k in ("Noto", "SimHei", "Song", "Hei", "YaHei", "Ming", "Kai", "Source Han", "EB Garamond", "JetBrains"))]
    print("  sampled candidates:", cjk[:20])
    print("  total families:", len(names))
except Exception as exc:  # noqa: BLE001
    print("  unavailable:", type(exc).__name__, exc)
