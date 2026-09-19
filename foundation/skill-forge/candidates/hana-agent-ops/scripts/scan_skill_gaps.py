#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
技能缺口扫描器（只读）
=====================
挖掘会话记录，统计：用户意图关键词 / 工具调用 / 已装技能被提及情况，
产出"哪些反复出现的需求可能没有被现成技能覆盖"的候选清单。

这是"技能自进化"的探测端：它不自动创建技能，只产出证据，
由 Agent 判断 + 用户批准后，才进入起草与安装。

用法:
  python scan_skill_gaps.py                       # 默认扫 agent-mu42qzfz 近 30 天
  python scan_skill_gaps.py --days 60 --top 30
  python scan_skill_gaps.py --out gap-report.md
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

HANA_HOME = Path(os.environ.get("HANA_HOME", r"C:\Users\ZhouXuan\.hanako"))
WORKSPACE = Path(os.environ.get("HANA_WORKSPACE", r"C:\Users\ZhouXuan\Desktop\OH-WorkSpace"))

# 科研场景意图词表（可扩展）
INTENT_LEXICON = {
    "文献检索": ["检索", "查文献", "搜文献", "文献综述", "研究现状", "related work"],
    "论文精读": ["精读", "读论文", "paper card", "阅读器", "逐段", "翻译论文"],
    "引用核验": ["引用", "参考文献", "doi", "citation", "核验引文", "文献真伪"],
    "统计审查": ["统计", "p值", "效应量", "置信区间", "显著性", "样本量", "功效"],
    "科研绘图": ["画图", "绘图", "图", "figure", "配图", "多面板", "制图", "可视化"],
    "论文写作": ["写作", "润色", "proposal", "开题", "摘要", "引言", "讨论", "投稿"],
    "审稿返修": ["审稿", "返修", "reviewer", "回复意见", "rebuttal"],
    "实验管理": ["实验", "复现", "数据集", "标注", "benchmark", "baseline"],
    "知识组织": ["知识图谱", "本体", "ontology", "实体", "关系抽取", "schema"],
    "智能体工程": ["智能体", "agent", "多智能体", "路由", "工具调用", "评测"],
    "环境运维": ["环境", "自检", "健康", "备份", "回滚", "配置", "安装", "skill"],
}


def load_enabled_skills() -> set[str]:
    cfg = HANA_HOME / "agents" / "agent-mu42qzfz" / "config.yaml"
    names: set[str] = set()
    if cfg.exists():
        txt = cfg.read_text(encoding="utf-8", errors="replace")
        in_skills = in_enabled = False
        for line in txt.splitlines():
            if re.match(r"^[^\s#]", line):
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
                    names.add(m.group(1))
                elif line.strip():
                    break
    return names


def iter_session_files(agent: str, days: int) -> list[Path]:
    root = HANA_HOME / "agents" / agent / "sessions"
    if not root.exists():
        root = HANA_HOME / "agents"
    cutoff = time.time() - days * 86400
    out = []
    for p in root.rglob("*.jsonl"):
        try:
            if p.stat().st_mtime >= cutoff:
                out.append(p)
        except OSError:
            pass
    return out


def extract_text(content) -> str:
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = []
        for b in content:
            if isinstance(b, dict):
                if b.get("type") in ("text", "input_text") and isinstance(b.get("text"), str):
                    parts.append(b["text"])
        return "\n".join(parts)
    return ""


def tool_names(content) -> list[str]:
    out = []
    if isinstance(content, list):
        for b in content:
            if isinstance(b, dict) and b.get("type") in ("tool_use", "toolCall", "tool_call"):
                out.append(b.get("name") or b.get("toolName") or "?")
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--agent", default="agent-mu42qzfz")
    ap.add_argument("--days", type=int, default=30)
    ap.add_argument("--top", type=int, default=25)
    ap.add_argument("--out", default=None)
    args = ap.parse_args()

    enabled = load_enabled_skills()
    files = iter_session_files(args.agent, args.days)

    intent_hits = Counter()
    tool_freq = Counter()
    skill_mentions = Counter()
    user_msgs: list[str] = []

    for f in files:
        try:
            for line in f.read_text(encoding="utf-8", errors="replace").splitlines():
                if not line.strip():
                    continue
                try:
                    o = json.loads(line)
                except Exception:
                    continue
                msg = o.get("message")
                if not isinstance(msg, dict):
                    continue
                role = msg.get("role")
                content = msg.get("content")
                if role == "user":
                    t = extract_text(content)
                    if t:
                        user_msgs.append(t)
                        for cat, kws in INTENT_LEXICON.items():
                            if any(k.lower() in t.lower() for k in kws):
                                intent_hits[cat] += 1
                elif role == "assistant":
                    for tn in tool_names(content):
                        tool_freq[tn] += 1
                    t = extract_text(content)
                    for s in enabled:
                        if s in t:
                            skill_mentions[s] += 1
        except OSError:
            continue

    ts = datetime.now(timezone.utc).astimezone().strftime("%Y-%m-%d %H:%M:%S %z")
    lines = []
    lines.append(f"# 技能缺口扫描报告  {ts}")
    lines.append("")
    lines.append(f"- 扫描会话文件：{len(files)} 个（近 {args.days} 天）")
    lines.append(f"- 采集用户消息：{len(user_msgs)} 条")
    lines.append(f"- 已装启用技能：{len(enabled)} 个")
    lines.append("")
    lines.append("## 1. 意图分布（用户消息命中次数）")
    lines.append("")
    lines.append("| 意图 | 命中 | 粗判覆盖 |")
    lines.append("|---|---|---|")
    for cat, n in intent_hits.most_common():
        lines.append(f"| {cat} | {n} | {coverage_guess(cat, enabled)} |")
    lines.append("")
    lines.append("## 2. 工具调用频次")
    lines.append("")
    lines.append("| 工具 | 次数 |")
    lines.append("|---|---|")
    for t, n in tool_freq.most_common(args.top):
        lines.append(f"| {t} | {n} |")
    lines.append("")
    lines.append("## 3. 已装技能被提及次数（近似的使用信号）")
    lines.append("")
    if skill_mentions:
        lines.append("| 技能 | 提及 |")
        lines.append("|---|---|")
        for s, n in skill_mentions.most_common(args.top):
            lines.append(f"| {s} | {n} |")
    else:
        lines.append("（本窗口内未在助手文本中发现技能名，说明多为隐式使用）")
    lines.append("")
    lines.append("## 4. 候选缺口（高命中意图中未被现成技能明确覆盖者）")
    lines.append("")
    gaps = [c for c, _ in intent_hits.most_common() if coverage_guess(c, enabled).startswith("弱")]
    if gaps:
        for g in gaps:
            lines.append(f"- **{g}**：命中 {intent_hits[g]} 次，覆盖偏弱 → 值得评估是否需要自建技能")
    else:
        lines.append("（无明显缺口）")
    lines.append("")
    lines.append("> 说明：本报告是**证据**，不是结论。技能是否该自建，由 Agent 结合具体会话内容判断，并经用户批准。")

    report = "\n".join(lines)
    print(report)
    out = Path(args.out) if args.out else (WORKSPACE / "foundation" / "skill-forge" / "gap-report.md")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(report, encoding="utf-8")
    print(f"\n(报告已写入 {out})")
    return 0


def coverage_guess(cat: str, enabled: set[str]) -> str:
    m = {
        "文献检索": ["nature-academic-search", "nature-literature-pipeline", "deep-research"],
        "论文精读": ["nature-reader", "nature-paper-card", "paper-deep-reading"],
        "引用核验": ["nature-ref-verifier", "nature-citation"],
        "统计审查": ["nature-statistics"],
        "科研绘图": ["scipilot-figure-skill", "nature-figure"],
        "论文写作": ["nature-writing", "nature-polishing", "researchwrite"],
        "审稿返修": ["nature-reviewer", "academic-paper-reviewer", "nature-response"],
        "实验管理": ["nature-experiment-log"],
        "知识组织": ["understand-knowledge"],
        "智能体工程": [],
        "环境运维": [],
    }
    have = [s for s in m.get(cat, []) if s in enabled]
    return ("较强: " + ", ".join(have)) if len(have) >= 2 else (
        ("部分: " + ", ".join(have)) if have else "弱/无")


if __name__ == "__main__":
    raise SystemExit(main())
