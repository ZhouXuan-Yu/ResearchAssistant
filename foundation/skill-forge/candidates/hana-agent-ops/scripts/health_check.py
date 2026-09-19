#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Hana 科研智能体 · 环境自检（只读，无副作用）
===========================================
用法:
    python health_check.py                 # 打印报告
    python health_check.py --json out.json # 同时导出 JSON

检查项:
  1. Skills    —— SKILL.md 完整性 / frontmatter / 启用与磁盘一致性
  2. Deps      —— 科研与绘图关键 Python 依赖可导入性
  3. Models    —— 模型注册表与关键能力声明（如 deepseek 图像支持）
  4. Memory    —— 记忆目录新鲜度与编译状态
  5. Backup    —— 快照新鲜度
  6. Providers —— provider 配置完整性（不读取任何密钥值）
退出码: 0 = 全绿; 1 = 存在 WARN; 2 = 存在 FAIL
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

HANA_HOME = Path(os.environ.get("HANA_HOME", r"C:\Users\ZhouXuan\.hanako"))
WORKSPACE = Path(os.environ.get("HANA_WORKSPACE", r"C:\Users\ZhouXuan\Desktop\OH-WorkSpace"))
AGENT_ID = os.environ.get("HANA_AGENT_ID", "agent-mu42qzfz")

SKILLS_DIR = HANA_HOME / "skills"
AGENT_DIR = HANA_HOME / "agents" / AGENT_ID
CONFIG_YAML = AGENT_DIR / "config.yaml"
MEMORY_DIR = AGENT_DIR / "memory"
SNAPSHOT_DIR = WORKSPACE / "foundation" / "backup" / "snapshots"
KNOWN_MODELS = HANA_HOME / "artifacts" / "server" / "0.412.7-win32-x64" / "lib" / "known-models.json"

CRITICAL_DEPS = ["matplotlib", "numpy", "pandas", "scipy", "PIL", "seaborn", "plotly"]
OPTIONAL_DEPS = ["scienceplots", "docx", "pptx", "openpyxl", "yaml", "requests"]

results: list[dict] = []


def add(section: str, name: str, status: str, detail: str) -> None:
    results.append({"section": section, "name": name, "status": status, "detail": detail})


def age_days(ts: float) -> float:
    return (time.time() - ts) / 86400.0


# ---------------------------------------------------------------- 1. Skills
def check_skills() -> None:
    if not SKILLS_DIR.exists():
        add("Skills", "skills 目录", "FAIL", f"不存在: {SKILLS_DIR}")
        return

    names_on_disk: dict[str, Path] = {}
    broken: list[str] = []
    for skill_md in SKILLS_DIR.rglob("SKILL.md"):
        head = skill_md.read_text(encoding="utf-8", errors="replace").splitlines()[:10]
        m = next((l for l in head if re.match(r"^\s*name\s*:", l)), None)
        if not m:
            broken.append(str(skill_md.parent.relative_to(SKILLS_DIR)))
            continue
        nm = m.split(":", 1)[1].strip().strip('"').strip("'")
        names_on_disk[nm] = skill_md.parent
    add("Skills", "磁盘技能数", "OK", f"{len(names_on_disk)} 个具名技能，{len(broken)} 个缺 frontmatter")
    if broken:
        add("Skills", "frontmatter 缺失", "WARN", ", ".join(broken[:5]))

    enabled: list[str] = []
    if CONFIG_YAML.exists():
        txt = CONFIG_YAML.read_text(encoding="utf-8", errors="replace")
        in_skills = in_enabled = False
        for line in txt.splitlines():
            if re.match(r"^[^\s#]", line):                 # 顶层键
                if in_enabled:
                    break
                in_skills = bool(re.match(r"^skills\s*:", line))
                continue
            if not in_skills:
                continue
            if re.match(r"^\s+enabled\s*:\s*$", line):
                in_enabled = True
                continue
            if in_enabled:
                m = re.match(r"^\s+-\s+(\S.*?)\s*$", line)
                if m:
                    enabled.append(m.group(1))
                elif line.strip() and not line.lstrip().startswith("#"):
                    break
    add("Skills", "启用条目", "OK", f"{len(enabled)} 条")
    missing = [e for e in enabled if e not in names_on_disk]
    if missing:
        add("Skills", "启用但磁盘无对应", "FAIL", ", ".join(missing[:8]))
    else:
        add("Skills", "启用/磁盘一致性", "OK", "全部命中")


# ---------------------------------------------------------------- 2. Deps
def check_deps() -> None:
    import importlib
    miss_crit, miss_opt = [], []
    for p in CRITICAL_DEPS:
        try:
            importlib.import_module(p)
        except Exception:
            miss_crit.append(p)
    for p in OPTIONAL_DEPS:
        try:
            importlib.import_module(p)
        except Exception:
            miss_opt.append(p)
    add("Deps", "关键依赖", "FAIL" if miss_crit else "OK",
        ("缺失: " + ", ".join(miss_crit)) if miss_crit else f"{len(CRITICAL_DEPS)} 项全部可导入")
    add("Deps", "可选依赖", "WARN" if miss_opt else "OK",
        ("缺失: " + ", ".join(miss_opt)) if miss_opt else "全部可导入")
    add("Deps", "Python 版本", "OK", sys.version.split()[0])


# ---------------------------------------------------------------- 3. Models
def check_models() -> None:
    models_json = HANA_HOME / "models.json"
    if not models_json.exists():
        add("Models", "models.json", "FAIL", "缺失")
        return
    try:
        data = json.loads(models_json.read_text(encoding="utf-8", errors="replace"))
    except Exception as e:
        add("Models", "models.json", "FAIL", f"JSON 解析失败: {e}")
        return
    provs = data.get("providers", {})
    add("Models", "provider 数", "OK", ", ".join(provs.keys()))

    # 关键：DeepSeek 是否声明图像输入（视觉链路前提）
    ds = provs.get("deepseek", {}).get("models", [])
    img_models = [m.get("id") for m in ds if "image" in (m.get("input") or [])]
    add("Models", "deepseek 图像输入声明", "OK" if img_models else "FAIL",
        ("含: " + ", ".join(img_models)) if img_models else "无任何 deepseek 模型声明 image")

    # known-models 能力表是否包含 deepseek-flash 且 image=true
    if KNOWN_MODELS.exists():
        try:
            km = json.loads(KNOWN_MODELS.read_text(encoding="utf-8", errors="replace"))
            entry = km.get("deepseek", {}).get("deepseek-flash")
            if entry is None:
                add("Models", "能力表 deepseek-flash", "WARN", "known-models.json 无该条目（视觉可能被判为不支持图像）")
            elif entry.get("image") is True:
                add("Models", "能力表 deepseek-flash", "OK", "image=true（已打补丁或官方已支持）")
            else:
                add("Models", "能力表 deepseek-flash", "FAIL", "image=false → 图像会被判定为不支持")
        except Exception as e:
            add("Models", "known-models.json", "WARN", f"解析失败: {e}")
    else:
        add("Models", "known-models.json", "WARN", f"未找到: {KNOWN_MODELS}")


# ---------------------------------------------------------------- 4. Memory
def check_memory() -> None:
    if not MEMORY_DIR.exists():
        add("Memory", "记忆目录", "FAIL", f"不存在: {MEMORY_DIR}")
        return
    files = {p.name: p for p in MEMORY_DIR.iterdir() if p.is_file()}
    newest = max((p.stat().st_mtime for p in files.values()), default=0)
    add("Memory", "目录新鲜度", "OK" if age_days(newest) < 2 else "WARN",
        f"最近更新 {age_days(newest):.1f} 天前")
    for f in ("facts.db", "memory.md", "daily-state.json"):
        p = files.get(f)
        add("Memory", f, "OK" if p else "WARN",
            f"{p.stat().st_size} B" if p else "缺失")

    # 扫描最新日志中的记忆报错
    logs = sorted((HANA_HOME / "logs").glob("*.log"), key=lambda p: p.stat().st_mtime, reverse=True)
    if logs:
        tail = logs[0].read_text(encoding="utf-8", errors="replace").splitlines()[-400:]
        errs = [l for l in tail if "[ERROR]" in l and ("memory" in l.lower() or "记忆" in l)]
        add("Memory", "最近日志记忆报错", "OK" if not errs else "FAIL",
            "无" if not errs else f"{len(errs)} 条，例: {errs[-1][:110]}")


# ---------------------------------------------------------------- 5. Backup
def check_backup() -> None:
    if not SNAPSHOT_DIR.exists():
        add("Backup", "快照目录", "FAIL", f"不存在: {SNAPSHOT_DIR}")
        return
    snaps = sorted([d for d in SNAPSHOT_DIR.iterdir() if d.is_dir()], key=lambda d: d.name)
    if not snaps:
        add("Backup", "快照", "FAIL", "无任何快照")
        return
    latest = snaps[-1]
    a = age_days(latest.stat().st_mtime)
    add("Backup", "快照数", "OK", f"{len(snaps)} 份")
    add("Backup", "最新快照", "OK" if a < 7 else "WARN", f"{latest.name}（{a:.1f} 天前）")


# ---------------------------------------------------------------- 6. Providers
def check_providers() -> None:
    """只检查结构与引用形态，不输出任何密钥值。"""
    models_json = HANA_HOME / "models.json"
    if not models_json.exists():
        return
    try:
        data = json.loads(models_json.read_text(encoding="utf-8", errors="replace"))
    except Exception:
        return
    plaintext, refs = [], []
    for pname, p in data.get("providers", {}).items():
        key = p.get("apiKey", "")
        if not key:
            continue
        (refs if key.startswith("hana-runtime-api-key:") or key == "local" else plaintext).append(pname)
    add("Providers", "apiKey 形态", "OK" if not plaintext else "WARN",
        f"引用式 {len(refs)} 个" + (f"；非引用式 {plaintext}" if plaintext else ""))


# ---------------------------------------------------------------- report
def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", help="同时导出 JSON 报告到该路径")
    args = ap.parse_args()

    check_skills()
    check_deps()
    check_models()
    check_memory()
    check_backup()
    check_providers()

    worst = "OK"
    for r in results:
        if r["status"] == "FAIL":
            worst = "FAIL"
            break
        if r["status"] == "WARN" and worst != "FAIL":
            worst = "WARN"

    print(f"# Hana 环境自检报告  {datetime.now(timezone.utc).astimezone().strftime('%Y-%m-%d %H:%M:%S %z')}")
    print(f"# 总体: {worst}\n")
    cur = None
    for r in results:
        if r["section"] != cur:
            cur = r["section"]
            print(f"## {cur}")
        icon = {"OK": "[OK]  ", "WARN": "[WARN]", "FAIL": "[FAIL]"}[r["status"]]
        print(f"  {icon} {r['name']}: {r['detail']}")

    if args.json:
        Path(args.json).write_text(json.dumps({"worst": worst, "results": results},
                                              ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"\n(JSON 已写入 {args.json})")

    return 0 if worst == "OK" else (1 if worst == "WARN" else 2)


if __name__ == "__main__":
    raise SystemExit(main())
