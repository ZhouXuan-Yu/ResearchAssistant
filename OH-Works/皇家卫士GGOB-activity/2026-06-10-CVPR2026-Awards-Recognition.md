# CVPR 2026 获奖全览与识别技术前沿

> 2026-06-10 自整理 | CVPR 2026 于 6/3-6/7 在丹佛落幕，16,092 篇投稿、4,089 篇接收（接收率 25.4%，投稿量同比 +23.7%）

---

## 一、核心奖项速览

| 奖项 | 论文 | 机构 | 一句话 |
|------|------|------|--------|
| 🏆 **Best Paper** | D4RT | Google DeepMind + UCL + Oxford | 单段视频即可"按需查询"任意时空点的 3D 位置，A100 上 200+ FPS 姿态估计 |
| 🏆 **Best Student Paper** | O-Voxel (TRELLIS.2) | 清华 + 微软研究院 + 中科大 | 40 亿参数 3D 生成模型，全新 O-Voxel 表示大幅超越现有方法 |
| 🥈 **Best Paper Honorable Mention** | SAM 3D | Meta Superintelligence Lab | 单张照片预测几何+纹理+空间布局，人类偏好 5:1 胜率 |
| 🥈 **Best Paper Honorable Mention** | NitroGen | NVIDIA + Stanford + Caltech 等 | 超 1000 款游戏、4 万小时视频训练的通用游戏 Agent |
| 🥉 **Best Student Paper HM** | ChordEdit | 广东工业大学 + 北大等 | 免训练、免反演的单步实时图像编辑，一作是本科生 |

---

## 二、Test of Time：ResNet 与 YOLO 加冕

今年 Longuet-Higgins 奖（十年影响力验证）罕见地**双黄蛋**，联合颁给两篇 2016 年的奠基性工作：

### Deep Residual Learning for Image Recognition (ResNet)
- 作者：何恺明、张祥雨、任少卿、孙剑
- 残差连接解决了深层网络退化问题，152 层网络首次超越人类识别水平
- 十年间引用超 20 万次，至今仍是绝大多数视觉模型的 backbone 基础

### You Only Look Once (YOLO v1)
- 作者：Joseph Redmon 等
- 将检测重构为端到端回归，Titan X 上 45 FPS（Fast 版 155 FPS）
- 直接催生了 SSD、RetinaNet 及整个 YOLO 家族，让实时检测真正落地

> 对 ZhouXuan 论文的意义：ResNet 是你识别系统 backbone 的理论基石，YOLO 的实时检测范式直接影响了各类嵌入式/移动端识别系统设计。这两篇值得精读原始论文。

---

## 三、何恺明获 PAMI 杰出贡献奖

本届 CVPR 上，何恺明（Kaiming He）获得 **PAMI Distinguished Researcher Award**（青年学者奖由 CMU Deepak Pathak 和 MIT Vincent Sitzmann 获得）。

何恺明是目前 CV 领域影响力最大的华人学者之一，其工作主线涵盖：
- ResNet（2016 Test of Time）
- Faster R-CNN / Mask R-CNN（检测与分割基石）
- MAE（自监督学习范式）
- 本届 CVPR 另有新作《Back to Basics: Let Denoising Generative Models Denoise》（与 Tianhong Li 合作）

---

## 四、识别相关论文精选

除了上述获奖工作，本届 CVPR 在识别方向也有不少值得关注的成果：

### 4.1 细粒度识别
- **PRISM**：基于原型推理的可解释识别，引入跨模态语义挖掘，在 CUB-200（鸟类）、Stanford Dogs 等细粒度基准上兼顾精度与可解释性
- **TWIN / Same or Not**：56.1 万图像对数据集，训练 VLM 判断两张相似图是否为同一物体，微调后在细粒度识别上提升最高 19.3%
- **GUIDED**：将细粒度开放词汇检测拆分为"主体定位 + 属性识别"两条通路，解决 VLM 嵌入中的语义纠缠，FG-OVD 新 SOTA

### 4.2 开放词汇检测
- **WeDetect**：双塔架构实现极速开放词汇检测，Tiny 版 62.5 FPS 超越 YOLO-World，Large 版 LVIS 上超 T-Rex2 3.6 AP
- **NoOVD**：针对开放词汇检测中"已知类"和"新类"的语义鸿沟，提出无需额外标注的新类发现嵌入方案

### 4.3 异常与 OOD 检测
- **UNO-Adapter**：面向 OOD 物体检测，通过无监督概念发现 + 神经概念绑定，在标准基准上 FPR95 降低最高 11.96%

### 4.4 域自适应检测
- **DA-Mamba**：CNN + 状态空间模型混合架构，兼顾局部效率与全局长程建模，跨域检测性能显著提升
- **CD-Buffer**：针对恶劣天气下的目标检测，提出互补双缓冲测试时自适应框架

### 4.5 分割（Segmentation）
- **INSID3**：基于 DINOv3 的免训练上下文分割，Oral 论文
- **MatAnyone 2**：视频抠图 + 质量评估器缩放训练
- **VGGT-Segmentor**：几何增强的跨视角分割
- **Retrieve and Segment**：用少量示例弥合开放词汇分割的监督缺口

---

## 五、对中国研究界的观察

本届 CVPR 中国研究者表现突出：
- Best Paper 一作张楚涵（DeepMind）是华人研究者
- Best Student Paper 团队全部来自清华 + 微软研究院 + 中科大
- **广东工业大学**本科生团队获 Best Student Paper 提名，打破了大厂和顶尖高校的垄断
- Test of Time 的四位 ResNet 作者均为华人
- PAMI 杰出奖得主何恺明是广东高考状元

这意味着在 CV 领域，中文社区的学术产出已成为核心力量，对参考中文资料写论文的 ZhouXuan 来说是一个积极信号。

---

## 六、对智能导航与识别系统的启示

结合 ZhouXuan 的论文方向，CVPR 2026 传递了几个关键信号：

1. **backbone 进化**：ResNet 获奖确认了残差连接的持久价值，但当前 SOTA 识别系统更多采用 ViT/CLIP 等视觉语言模型作为特征提取器，PRISM、TWIN 等工作都基于 CLIP encoder
2. **开放词汇是趋势**：从固定类别识别走向开放词汇检测/分割，WeDetect、NoOVD、GUIDED 都指向这一方向
3. **实时性与精度兼顾**：YOLO 的 Test of Time 提醒我们工程落地的重要性，WeDetect 的 62.5 FPS 延续了这一实用主义路线
4. **3D 重建正在与识别融合**：D4RT、SAM 3D 等工作暗示，未来智能导航系统中的环境感知模块可能从纯 2D 识别走向 4D 时空理解
