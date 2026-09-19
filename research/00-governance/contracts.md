# 阶段契约规范（Stage Contracts v1.0）

| 项 | 值 |
|---|---|
| 状态 | **P0 冻结草案**（2026-09-19） |
| 作用 | 定义 8 个科研阶段之间的**唯一交接形式**。有契约才能串联，有契约才能拆开单用。 |
| 校验器 | `foundation/tools/check_contracts.py` |
| 样例 | `foundation/dryrun/spine-001/contracts/`（3 条，由演练产物实填） |
| 上位文档 | `foundation/RESEARCH-OS-EXPANSION-PLAN.md` §3 |
| 编排依据 | `research-os-router`（A–M 功能组 + G1–G5 门禁） |

---

## 1. 设计原则

1. **只认文件，不认对话**：阶段之间不靠上下文交接，一切以契约文件为准。
2. **契约即准入**：上游契约存在且校验通过，下游才允许执行；否则必须显式选择 `请求上游` / `降级自给（标注证据较弱）` / `拒绝执行`。
3. **自主度随身携带**：契约里必须写 `autonomy`，越界即拒。
4. **空缺即事实**：凡是没做的，写进 `unresolved`，不写"待补充"这类含糊词，也不留空。
5. **不发明字段**：新字段先进本文件升版本号，再改校验器。

---

## 2. 字段规范

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `contract_version` | str | ✓ | 契约格式版本，当前 `"1.0"` |
| `stage` | enum | ✓ | `S1`…`S8` |
| `phase` | enum | ✓ | `Creation` / `Writing` / `Validation` / `Dissemination` |
| `autonomy` | enum | ✓ | `人主导` / `需人确认` / `可高自主` |
| `produced_by` | str | ✓ | 产出该阶段产物的技能名 |
| `produced_at` | ISO8601 | ✓ | 产出时间（带时区） |
| `subject` | str | ○ | 任务标识（项目/演练名） |
| `upstream` | list[enum] | ✓ | 依赖的上游阶段，可为 `[]` |
| `inputs` | list[str] | ✓ | 消费的文件路径（相对项目根） |
| `artifacts` | list[str] | ✓ | 产出物路径（相对项目根），不可为空 |
| `claims` | list[str] | ○ | 涉及的断言编号（如 `CL-1`） |
| `gates` | map[str→enum] | ✓ | 自检门结果，取值 `pass` / `fail` / `n_a` / **`blocked`** |
| `reproducibility` | map | ✓ | `data_version` / `code_commit` / `seed` 三个键必须存在 |
| `verification` | map | ○ | `checked` / `unresolved` / `notes` |
| `unresolved` | list[str] | ✓ | 未解决项，无则 `[]` |
| `next` | str | ○ | 下游阶段提示 |

### 阶段与相位的对应（校验器强制）

| stage | phase | 自主度下限 |
|---|---|---|
| S1 选题生成 | Creation | **人主导** |
| S2 文献综述与检索 | Creation | 可高自主 |
| S3 编码与实验 | Creation | **人主导** |
| S4 表与图 | Creation | 可高自主 |
| S5 稿件撰写 | Writing | **需人确认** |
| S6 同行评审 | Validation | 可高自主 |
| S7 返修与回复 | Validation | **需人确认** |
| S8 传播 | Dissemination | 可高自主 |

> "自主度下限"含义：S1/S3 不得声明为"可高自主"或"需人确认"；S5/S7 不得声明为"可高自主"。
> 依据：Kong et al., arXiv:2605.18661 —— AI 在"真正新颖的想法、研究级实验、科学判断"上不可靠。

---

## 3. 校验规则（`check_contracts.py`）

1. **必填字段**齐全，类型正确。
2. `stage` 与 `phase` 必须符合 §2 对照表。
3. `autonomy` 必须 ≥ 该阶段的下限（见上表）。
4. `artifacts` 非空，且每个路径在 `--base` 下**真实存在**（不存在即 FAIL，不允许"计划产出"）。
5. `gates` 非空，取值合法；出现任一 `fail` 即整体 FAIL。
   **`blocked`** 的含义是“尝试过且已定位阻塞原因”，允许存在，但必须在 `unresolved` 里写下来（校验器强制）。
   三态分工：`pass` = 做了且通过；`fail` = 做了且没过；`n_a` = 不适用于本阶段；`blocked` = 该做但被外部因素卡住。
6. **S3 特则**：`reproducibility` 的 `data_version` / `code_commit` / `seed` 三者必须非空，且不得为 `n/a`；否则 FAIL（此即"可复现门"）。
7. `unresolved` 必须存在（可为空列表）——强制作者对"没做什么"表态。

---

## 4. 示例（S2，由演练产物实填）

```yaml
contract_version: "1.0"
stage: S2
phase: Creation
autonomy: 可高自主
produced_by: nature-academic-search + mcp_academic-search
produced_at: "2026-09-19T16:20:00+08:00"
subject: "spine-001 演练：高效视觉 Transformer 方法学图谱"
upstream: []
inputs: []
artifacts:
  - foundation/dryrun/spine-001/paper_rewriting_output/reference_materials/source_index.md
  - foundation/dryrun/spine-001/paper_rewriting_output/evidence_bank.md
  - foundation/dryrun/spine-001/paper_rewriting_output/source_inventory.md
claims: [CL-1, CL-2, CL-3, CL-4, CL-5]
gates:
  reference_identity: n_a
  inclusion_recomputable: pass
  no_fabrication: pass
reproducibility:
  data_version: "n/a（materials_only，无实验数据）"
  code_commit: "n/a"
  seed: "n/a"
verification:
  checked: 24
  unresolved: 7
  notes: "25 行 / 24 唯一源；6 条仅存 arXiv 标识，1 条 DOI 标题匹配 67%"
unresolved:
  - "6 条 arXiv 记录未逐条解析核验（citation_quality_audit 记为 pending）"
  - "1 条 DOI（IBAST）标题相似度 0.67，身份存疑"
  - "剔除的 5 条未留档，纳入口径不可外部复核"
next: S4
```

> `reference_identity: n_a` 说明：该门在演练当时未设独立门禁，身份核验由 S4 之前的引用质量审计承担，故此处记 `n_a` 而非 `pass` —— **不把没做的写成通过**。

---

## 5. 版本与变更

| 版本 | 日期 | 变更 |
|---|---|---|
| 1.0 | 2026-09-19 | 首版冻结：15 字段、阶段-相位对照、7 条校验规则 |

变更流程：改本文件 → 升 `contract_version` → 同步 `check_contracts.py` → 用 3 条样例回归。
