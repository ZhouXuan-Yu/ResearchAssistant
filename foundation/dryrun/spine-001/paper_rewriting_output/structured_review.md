# Structured Peer Review

- Manuscript: `final_paper/manuscript.md`（评审时版本：修订前）
- Sections: 8
- Total findings: 23（CRITICAL 2 / MAJOR 6 / MINOR 15）
- 评审者：独立子代理（只读），逐字原文见 `reviewer_audit.md`
- 处置状态：全部已核验并按批修订，映射表见 `DRILL-STATUS.md` 第 5 节

> 每条 finding 均给出位置、证据状态与具体改法，而不是"建议改进"。
> 本文件为科研助手依评审原文整理的结构化版本；评审者原文未被改写，保留于 `reviewer_audit.md`。

## Reviewer Personas

### Methods Reviewer (journal)
- **Context:** Target venue type: journal（本演练未指定具体载体）
- **Standards:** Focus on originality, method rigor, evidence strength, reproducibility, and fit for the target journal.
- **Style:** Scene-aware structured review.

### Contribution Reviewer (journal)
- **Context:** Target venue type: journal
- **Standards:** Assess the contribution's significance, differentiation from prior work, citation credibility, and alignment with journal standards.
- **Style:** Scene-aware structured review.

### Clarity Reviewer (journal)
- **Context:** Target venue type: journal
- **Standards:** Evaluate structure clarity, argument coherence, figure/table quality, and adherence to journal conventions.
- **Style:** Scene-aware structured review.

---

## Findings

| ID | Severity | What | Evidence | Revision Command |
|---|---|---|---|---|
| S1 | CRITICAL | 摘要与 §4 称"3 条同时报告参数量、算力与精度"，与自身证据库 E-A 冲突（无一条三项俱全） | 冲突 | 按 E-A 台账改为字段覆盖表述，明写"三项俱全 0 条" |
| E1 | CRITICAL | 同稿"16 条无摘要"与"18 条仅元数据"并存 | 冲突 | §2、§5 统一为 18（6+18=24） |
| T1 | MAJOR | 图注称计数"可由 source_index.md 逐条回算"，而该文件在评审时不含被回算数据 | 缺失 | 恢复书目表；图注改为按面分别指明回算源 |
| I2 | MAJOR | "逐条回算"是可审计性承诺，当时无法兑现 | 缺失 | 先建 E-A 台账再作声明，或删除该声明 |
| S2 | MAJOR | 把"未获取摘要"等同于"未披露" | 弱 | CL-2 降为受限样本事实，正文加限定 |
| T3 | MAJOR | 载体构成在 research_dossier 与正文/E-B1 间互斥 | 冲突 | 以书目表实点为准统一为 2/2/5/6/6/3 |
| T4 | MAJOR | 披露完备度 3/1/2/18 无逐条台账 | 缺失 | 建 E-A 逐条台账（需摘要原文） |
| E2 | MAJOR | §5 缺 GAP-4 | 缺失 | 补 GAP-4 条目 |
| S3 | MINOR | 由 6 条推及"该体裁"，且 GAP-2 把 6 条误写为 24 条 | 弱 | 降为迹象并修 GAP-2 表述 |
| S4 | MINOR | 点云/视频/skeleton 的"视觉"边界未交代 | 缺失 | §2 增加范围边界声明 |
| S5 | MINOR | §4 小标题把 6 条子集结论写成一般结论 | 弱 | 加"在有摘要子集内"限定 |
| E3 | MINOR | 摘要负结果表述未带 6 条限定 | 弱 | 结论补样本限定 |
| E4 | MINOR | §1 区间引注止于 R21，书目至 R24 | 冲突 | 改为 R01–R24 |
| E5 | MINOR | "缩减一半以上"依赖未言明的分级标准 | 弱 | 明写"仅保留顶会正刊与期刊（7 条）" |
| T2/I6 | MINOR | 年份分布与书目表不符 | **评审时证据被污染** | 恢复书目表后实点一致；为三处补年份字段 |
| T5 | MAJOR | 部署延迟在三处定性不一 | 冲突 | E-C/CL-5/GAP-3 统一为推断 |
| T6 | MINOR | CL-1 依赖标为 E-B1（与分类无关） | 冲突 | 改为 E-A + 标题层归类 |
| T7 | MINOR | results_validation 引用不可执行回算源 | 冲突 | 改指 E-A 台账，注明未做逐条映射 |
| T8 | MINOR | 标题年份 2020 起，数据 2021 起 | 冲突 | 改为 2021–2026 |
| T9 | MINOR | E-A3 出自 R18，正文未引 | 缺失 | 台账标注来源记录 |
| I1 | MAJOR | 全稿引用零核验，且该 FAIL 未写入局限 | 缺失 | 运行标识核验（本轮已由 0 条修到 18 条通过） |
| I3 | MINOR | 剔除的 5 条与检索式未列出 | 缺失 | 当时未留档，无法追补（已登记） |
| I4 | MINOR | 载体风险标为"事实"；R24 定性无来源 | 弱 | CL-4 降为"判断"并注明标准 |
| I5 | MINOR | 书目表混排正文未引条目，未声明性质 | 缺失 | 表首注明"纳入语料全集" |

---

## Editor Synthesis

### Points of Agreement
- 骨架可用：以效率来源为轴的四族分类 + 证据强度分级，作为"文献组织方式"的贡献可辩护。
- Claim Boundary 写得克制，正文确未写入跨论文性能比较，GAP-5 未被写成结论。

### Points of Disagreement
- 评审者把 T2/I6 判为数据缺陷；核验后确认其成因是评审时 `source_index.md` 已被
  `reference_inventory.py` 覆盖，恢复书目表后实点与图一致。该分歧不影响其余发现。

### Revision Priority
1. S1 摘要核心数字与证据库冲突（阻断级，且已进摘要）
2. E1 同稿计数不一致（阻断级）
3. T1/I2 可回算声明无法兑现
4. T4 披露完备度无逐条台账
5. T3 载体构成互斥
6. E2 GAP-4 缺失

**Overall score:** 52/100（评审时版本）
**Recommendation:** Major Revision

> 本演练稿足以证明独立评审门控有效：它拦下的不是措辞问题，而是"摘要数字与自身证据库正面冲突"
> "同稿计数不一致""声称可回算而源文件不含数据"这三类。若此类问题被放行，说明门控只做了格式校验。
