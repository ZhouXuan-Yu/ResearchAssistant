# MCP 能力登记（MCP Capabilities Registry）

> 建立：2026-09-18｜维护：agent-mu42qzfz｜状态：**2 个连接器运行中，均已按 Agent 授权**
> 本文件登记 **MCP 工具**。MCP 工具不是技能（Skill），两者分类体系独立：
> - 技能：`skill-taxonomy.yaml`（144 项，由 `check_taxonomy.py` 校验）
> - MCP：本文件

## 调用约定（重要）

MCP 工具的真实调用名为 **`mcp_<connector>_<tool>`**，例如：

| 连接器 | 工具名 | 实际调用名 |
|---|---|---|
| zotero | `zotero_search_items` | `mcp_zotero_zotero_search_items` |
| academic-search | `search_papers` | `mcp_academic-search_search_papers` |

**用短名调用会报 `Tool <name> not found`。** 这是 2026-09-18 排查 40 分钟的真凶，已入经验库。

---

## 连接器 1：`academic-search`（本机技能自带）

- **来源**：`skills/nature-academic-search/mcp-server/`（随技能分发，非外部依赖）
- **传输**：stdio，`uv run --no-project --directory <mcp-server> --with ...`
- **工具数**：16
- **免密钥可用**：CrossRef、PubMed（缺 email 时报错降级）、arXiv
- **需配置**：Scopus / ScienceDirect（需 pybliometrics 本地配置 + Elsevier 配额）

### 工具清单

| 组 | 工具 | 用途 |
|---|---|---|
| 通用检索 | `search_papers` | 跨 CrossRef/PubMed/arXiv 检索，返回合并结果 + 分源错误 |
| | `get_paper_by_id` | DOI / PMID / arXiv ID 自动识别取元数据 |
| | `get_citation` | 生成格式化引用（apa/nature/ieee/harvard/vancouver/chicago/mla） |
| | `lookup_mesh` | MeSH 主题词查询 |
| Scopus | `search_scopus`、`get_scopus_abstract`、`get_scopus_citation_overview`、`search_scopus_authors`、`get_scopus_author`、`search_scopus_affiliations`、`get_scopus_affiliation`、`search_scopus_serial_titles`、`get_scopus_serial_title`、`get_scopus_plumx_metrics` | 需 Elsevier 配置 |
| ScienceDirect | `search_sciencedirect`、`get_sciencedirect_article_metadata` | 需 Elsevier 配置 |

### 已知缺陷与补丁

- **缺陷**：`sources/arxiv.py` 在 defusedxml 0.7.1 下启动即崩（`AttributeError: module 'defusedxml.ElementTree' has no attribute 'Element'`），导致连接器 `exited (1)`、工具数 0。
- **补丁（已应用）**：`arxiv.py` 顶部加 `from __future__ import annotations`（令类型注解惰性求值）。
- **脆弱点**：补丁改的是第三方源码，**技能重装会丢失**。周检须复查。

---

## 连接器 2：`zotero`（Zotero 本地库）

- **命令**：`C:\Users\ZhouXuan\.local\bin\zotero-mcp.exe`，`ZOTERO_LOCAL=true`，`ZOTERO_MCP_TOOLSETS=all`
- **工具数**：53
- **库现状（2026-09-18 实测）**：My Library **1 条目**、**0 collection**、语义库 2 文档、PDF 覆盖率 100%。**库基本是空的。**

### 工具分组（按科研用途）

| 组 | 工具 | 科研价值 |
|---|---|---|
| **引文图** | `find_related_papers` | 走 OpenAlex 取后向参考 + 前向引用，标注本库是否已有 → 综述扩展的核心 |
| **引用评价** | `scite_enrich_item`、`scite_enrich_search`、`scite_check_retractions` | 引用语境（支持/反驳）+ **撤稿/更正检测** |
| 库内检索 | `search_items`、`advanced_search`、`search_by_tag`、`search_by_citation_key`、`semantic_search`、`get_recent` | 语义检索需先 `update_search_database` |
| 元数据 | `get_item_metadata`、`update_item`、`batch_update`、`add_item`、`add_item_relation`、`export_bibliography` | BibTeX / CSL 引用导出 |
| 全文阅读 | `read_pdf_pages`（文本/图像/区域裁剪）、`get_pdf_outline`、`get_item_fulltext`、`get_attachment_path` | 定向读页，避免整篇上下文爆炸 |
| 标注 | `get_annotations`、`create_annotation`、`update_annotation`、`delete_annotation`、`get_page_layout` | 拉真实阅读痕迹 |
| 笔记 | `get_notes`、`manage_note`、`synthesize_annotations` | 把全库高亮聚成综述素材 |
| 集合 | `create_collection`、`update_collection`、`delete_collection`、`set_item_collections`、`search_collections` | 建项目文献目录 |
| 去重 | `find_duplicates`、`merge_duplicates` | |
| 全文覆盖 | `library_coverage` | 列出缺 PDF 的条目及 DOI |
| 附件 | `attach_file`、`set_item_parent` | |
| 库管理 | `list_libraries`、`switch_library`、`list_feeds`、`get_feed_items` | |
| 写入授权 | `write_capabilities`、`authorize_local_writes` | 本地写入需 Zotero 10+ 弹窗授权 |

### 注意事项

- 写入类工具需**可写后端**：本地写入（Zotero 10+ 弹窗）或 Web API key。当前未确认可用。
- `delete_annotation` 为**不可撤销删除**，`delete_collection` 为硬删除（Zotero API 不回收站）→ 归入高风险动作，须先确认。
- `get_item_fulltext` 单次 10K+ tokens，禁止用于检索，只用于定向精读。
- **scite 依赖境外网络可达性**：无代理时 `scite.ai` / `api.scite.ai` 会超时（实测 20s 超时），工具报 `MCP request "tools/call" timed out`。这是**网络问题不是工具故障**，启用代理后即恢复（实测 HTTP 200 / 1.1s）。注意系统代理 `ProxyEnable=0`，实际靠 TUN 透明转发，无需重启连接器。

---

## 路由角色

| 功能组 | MCP 承担 | 替代/补充的原设计 |
|---|---|---|
| B 文献检索 | `academic-search.*` | 取代原"仅通用网页搜索"的方案；免密钥即用 |
| B 综述扩展 | `zotero.find_related_papers` + `zotero.library_coverage` | 新增能力，原设计无 |
| D 引用核验 | `academic-search.get_paper_by_id`（真伪）+ `zotero.scite_*`（语境/撤稿） | 与 `nature-ref-verifier` 技能互补：技能管流程，MCP 管数据源 |

---

## 未配置项（待办）

| 项 | 影响 | 解除条件 |
|---|---|---|
| `PUBMED_EMAIL` / `NCBI_API_KEY` | PubMed 源检索报错降级 | 填入邮箱（可选 NCBI key 提高限速） |
| Scopus / ScienceDirect | 10 + 2 个工具不可用 | 需 Elsevier 订阅 + pybliometrics 配置 |
| Zotero 库内容 | 库仅 1 条目，检索无实际收益 | 录入文献（研究阶段动作） |
| Zotero 写入后端 | 无法建 collection / 写标注 | Zotero 10+ 本地写入授权，或 Web API key |
