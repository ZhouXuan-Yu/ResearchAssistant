# 已确认贡献（confirmed_contribution）

## Core Contribution

| Field | Content |
|---|---|
| Main Contribution Statement | 提出以"效率来源"而非任务类型为轴的视觉 Transformer 效率化方法四族分类，并配套给出证据强度分级，使不同工作的成本削减机制可直接对照。 |
| Contribution Type | 文献组织方式与证据边界显式化（非新方法、非新读数）。 |
| Reviewer Payoff | 读者可在一次阅读后判断某项效率改进究竟缓解了哪一类瓶颈，并知道当前证据支持到什么程度、在哪一步不能比较。 |

## Why This Contribution Is Needed

| Field | Content |
|---|---|
| Field Problem | 效率型视觉 Transformer 工作数量增长快，但组织与评测口径分裂，进展难以判断。 |
| Specific Gap | 现有组织方式多按任务（分类/检测/分割/复原）划分，掩盖了成本削减来源的实质差异；同时缺少对指标披露完备度的显式记录。 |
| Concrete Challenge | 在只使用公开元数据与摘要的条件下，如何在不做过度解读的前提下给出可核验的分类与边界。 |
| Why Prior Work Leaves It Unresolved | 按任务分类的综述服务检索需求而非机制对照；以性能排序为目的的综述在本证据条件下无法成立。 |

## How This Paper Responds

| Field | Content |
|---|---|
| Design Response | 以效率来源为分类轴建立四族（注意力稀疏化、分组与级联、混合 CNN-Transformer、参数共享与模块重构），并新增指标披露完备度统计。 |
| Evidence Required | 每条归类须可追溯到具体条目；每项统计须可由登记记录逐条回算。 |
| Evidence Available | 24 条真实记录的标题、载体、年份与 DOI/arXiv 标识；其中 6 条含摘要。 |
| Evidence Missing | 18 条无摘要；全部 24 条均未获取全文，故方法细节与实验表格不可知。 |

## Claim Boundary

| Field | Content |
|---|---|
| Strong Claims Allowed | 分类作为"本文提出的组织方式"；披露完备度的元数据层统计；高风险载体占比。 |
| Claims to Soften or Avoid | 任何"某方法更优或更高效"的跨论文比较；任何关于效率与鲁棒性联合缺失的结论。 |
| Novelty Risk | 分类轴并非全新概念，风险在于被视为常识重组；缓解方式是把披露完备度统计作为独立贡献。 |
| Significance Risk | 样本仅 24 条且无全文，若被读作领域总体结论则超出证据；须在摘要与结论双重限定。 |
