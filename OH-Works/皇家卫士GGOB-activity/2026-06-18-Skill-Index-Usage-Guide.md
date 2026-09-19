# 📚 技能索引使用实战指南

> 基于 SKILL_INDEX.md 的92个技能，整理最实用的查找技巧和工作流
> 创建时间：2026-06-18 23:25

---

## 🎯 快速查找技能的三个技巧

### 技巧一：Ctrl+F 关键词搜索
当不确定技能位置时，直接搜索：
- **编程问题**：搜 `review`、`test`、`error`、`simplify`
- **设计问题**：搜 `color`、`font`、`layout`、`responsive`
- **规划问题**：搜 `plan`、`requirement`、`council`
- **文档问题**：搜 `docx`、`xlsx`、`pptx`、`pdf`

### 技巧二：场景速查优先
索引底部的「任务场景速查」是最高效入口：
```
"我要写一个新功能" → requirements-architect → planning-with-files → karpathy-guidelines → tdd-workflow → codex-ralph-loop → verification-loop
```
直接按链条调用，比逐个查找快3倍。

### 技巧三：分层决策逻辑
1. **核心层（C/D/P/T/M）**：每次任务至少扫一眼，确认适用性
2. **支援层（S）**：任务开始时查，匹配子任务
3. **参考层（R）**：特定场景触发时查
4. **归档层（A）**：基本不查，除非需要历史版本

---

## 🔧 五种常见任务完整工作流

### 工作流1：从零开发一个功能
```
1. requirements-architect（澄清需求）
2. planning-with-files（拆解任务）
3. karpathy-guidelines（约束编码风格）
4. tdd-workflow（测试驱动）
5. codex-ralph-loop（迭代直到完成）
6. verification-loop（全面验证）
7. code-review-excellence（最终审查）
```

### 工作流2：设计一个完整页面
```
1. frontend-design（选定美学锚点）
2. ui-ux-pro-max（配色/字体/布局数据库）
3. ui-design（布局和网格系统）
4. component-patterns（组件设计）
5. responsive-design（响应式适配）
6. web-typography（排版细节）
7. webdesign-review（最终评审）
```

### 工作流3：生产上线前检查
```
1. production-audit（生产就绪审计）
2. verification-loop（构建/测试/安全）
3. e2e-testing（端到端测试）
4. error-handling（错误处理验证）
5. ai-regression-testing（AI代码回归测试）
```

### 工作流4：处理Office文档
```
1. 识别文件类型 → 对应技能
   - .docx → docx
   - .xlsx/.csv → xlsx
   - .pptx → pptx-generator 或 ppt-master
   - .pdf → pdf
2. 如需AI辅助 → ppt-master（PPT专用）
3. 如需格式转换 → office-documents（通用）
```

### 工作流5：Agent调试与优化
```
1. agent-introspection-debugging（四阶段自调试）
2. strategic-compact（上下文压缩）
3. iterative-retrieval（渐进式检索）
4. meta-theory（治理调度）
5. continuous-learning-v2（自动学习）
```

---

## 🔄 索引维护最佳实践

### 安装新技能时的同步清单
```bash
# 1. 安装到HanaAgent
install_skill → C:\Users\ZhouXuan\.hanako\skills\

# 2. 读取SKILL.md提取name和description

# 3. 判断归属层级和分类
   - 核心编程？→ C编号
   - 核心设计？→ D编号
   - 支援层？→ S编号
   - 参考层？→ R编号

# 4. 插入到对应表格
# 5. 更新场景速查（如适用）
# 6. 更新"最后更新"日期
# 7. 同步到其他平台
   - Codex: C:\Users\ZhouXuan\.codex\skills\
   - Claude Code: C:\Users\ZhouXuan\.claude\skills\
   - OpenClaw: C:\Users\ZhouXuan\.openclaw\skills\
   - Hermes: C:\Users\ZhouXuan\.hermes\skills\

# 8. 更新Obsidian仓库
   - E:\Obsidian仓库\ZhouXuan私人领域\skill使用\03-索引与维护\平台技能对照表.md
   - E:\Obsidian仓库\ZhouXuan私人领域\skill使用\03-索引与维护\安装记录.md
```

### 定期维护建议
- **每周**：检查是否有技能可以升级层级（参考→支援、支援→核心）
- **每月**：清理归档层，删除超过3个月未使用的技能
- **每季度**：重新评估场景速查链路，补充新场景

---

## 📊 技能统计与分布

当前索引统计：
- **总计**：92个技能
- **核心层**：19个（C6 + D6 + P4 + T3 + M3）
- **支援层**：45个（S1-S45）
- **参考层**：18个（R1-R18）
- **归档层**：4个（A1-A4）
- **场景速查**：9条完整工作流

### 分类分布
| 分类 | 数量 | 占比 |
|------|------|------|
| 🔧 编程开发 | 28 | 30.4% |
| 🎨 UI/UX设计 | 24 | 26.1% |
| 📋 项目规划 | 8 | 8.7% |
| 📄 文档办公 | 7 | 7.6% |
| 🧪 测试质量 | 6 | 6.5% |
| 🧠 Agent元技能 | 12 | 13.0% |
| 🏢 业务设计 | 4 | 4.3% |
| 📚 学习知识 | 3 | 3.3% |

---

## 💡 高级使用技巧

### 技巧1：技能组合创造新能力
例如：`frontend-design` + `color-theory` + `web-typography` = 完整视觉设计系统

### 技巧2：用council解决决策卡点
当有2-3个方案难以抉择时：
```
council（四角色决策） → 架构师+怀疑者+实用主义+批评者
```

### 技巧3：用teach系统化学习新领域
```
teach（多会话学习） → 基于ZPD理论自动调整难度
```

### 技巧4：用caveman节省token
长会话token膨胀时：
```
caveman（极简模式） → 砍掉75%废话，保留技术精度
```

---

## 🚀 下一步行动建议

1. **熟悉场景速查**：记住9条常用工作流，遇到任务直接套用
2. **建立个人快捷方式**：把最常用的5个技能编号记在便签上
3. **定期回顾**：每周花5分钟看看索引，发现新的技能组合可能
4. **贡献优化**：发现索引不清晰的地方，直接编辑SKILL_INDEX.md

---

> 索引不是目录，是作战地图。知道每个技能在哪只是开始，知道怎么组合才是关键。
>
> *最后更新：2026-06-18 23:25 · 基于 SKILL_INDEX.md v2026-06-13*