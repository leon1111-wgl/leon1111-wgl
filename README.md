<a href="https://leon1111-wgl.github.io/leon1111-wgl/"><img src="site/assets/profile-banner.svg" width="100%" alt="Leon Wang — MSc student at HKU, working on AI. Click to enter my website." /></a>

<p align="center">
  <a href="https://leon1111-wgl.github.io/leon1111-wgl/"><strong>ENTER MY WEBSITE ↗</strong></a> &nbsp; / &nbsp;
  <a href="#about-me">About me</a> &nbsp; / &nbsp;
  <a href="#featured-project">Project</a> &nbsp; / &nbsp;
  <a href="#selected-research">Research</a> &nbsp; / &nbsp;
  <a href="#learning-portals">Courses</a> &nbsp; / &nbsp;
  <a href="mailto:zetongw6@gmail.com">Contact</a>
</p>

## About me

I am an MSc student at the University of Hong Kong, working on AI. My interests include multimodal models, LLM agents, long-video understanding and generation, and efficient video inference. I enjoy turning complex ideas into clear, practical learning resources.

| Currently exploring | How I work |
| :--- | :--- |
| Multimodal models and LLM agents | Connect model outputs to verifiable evidence |
| Long-video understanding and generation | Build datasets and evaluate models carefully |
| Efficient video inference | Explain ideas through stories, formulas and examples |

**Tools & interests** · Python · Java · C · Multimodal evaluation · lmms-eval · Instruction tuning · Knowledge distillation · Model quantization

## Featured project

### [CreditLens · 企业信用复核与证据智能](https://github.com/leon1111-wgl/creditlens)

把官方财务披露转成可追溯事实，校验数字口径，记录核查依据，再交给独立复核身份确认。当前 v0.4 包含微软与苹果的官方披露案例、42 项 PDF 原页事实、期限分区与周历口径校验、API-key 与租户约束、事件记录及 86 项测试与 15 个财务控制回归场景；通用多模态文档理解、真实模型评测与预测是后续研究主线。

`Financial evidence` · `Review workflow` · `Risk factors` · `Evaluation` · `FastAPI`

可在本地运行，无需 GPU。FinQA dev 883 题页内证据 Recall@5 为 82.43%，并非端到端回答准确率。可选模型接口已实现，真实模型质量与微调尚未评测。

[源码与复现](https://github.com/leon1111-wgl/creditlens) · [通俗制作报告](https://github.com/leon1111-wgl/creditlens/tree/main/docs/iterations) · [研究设计](https://github.com/leon1111-wgl/creditlens/blob/main/docs/08-document-ai-and-governance.md)

### [LoopDesk · 证据优先的企业客服 Agent](https://leon1111-wgl.github.io/loopdesk/)

把客服大模型做成能上线的系统：回答逐句对照知识库和业务数据校验，超额退款暂停等人工审批，模型故障时转人工或引用政策原文，坐席的每一次纠错都会变成知识补丁和回归测试。

`Agent 工具调用` · `RAG` · `人工审批` · `证据校验` · `回归评测` · `FastAPI + React`

在线演示是控制台的静态构建，数据录制自真实后端的离线运行（虚构数据），可以切换顾客、坐席、管理员浏览。完整版本在本地运行，可接入豆包、混元、DeepSeek 等模型。

**[打开在线演示 ↗](https://leon1111-wgl.github.io/loopdesk/)** · [源码与运行说明](https://github.com/leon1111-wgl/loopdesk) · [案例：一位顾客的退款](https://github.com/leon1111-wgl/loopdesk/blob/main/docs/CASE_STUDY.md)

### [EstateGuard · 社区智能巡检](https://leon1111-wgl.github.io/estateguard/)

将电梯搬运、通道占用和停车线索整理成可复核的物业事件。浏览器运行真实轻量视觉模型，分析本地图片或短视频，通过区域与时间规则形成候选，再记录人工判断并导出交接单。

`浏览器端视觉推理` · `场景规则` · `事件复核` · `中文工作台`

素材在本地处理，无需账户或 API key。当前是通用物体模型与规则基线；专门的违规行为识别仍需领域数据验证。

**[打开中文工作台 ↗](https://leon1111-wgl.github.io/estateguard/)** · [源码与运行说明](https://github.com/leon1111-wgl/estateguard) · [场景与实现案例](https://github.com/leon1111-wgl/estateguard/blob/main/docs/CASE_STUDY.md)

### [FinScope — Earnings Quality & Financial Resilience](https://leon1111-wgl.github.io/finscope/)

Does reported profit have cash-flow support? Review real SEC accounts, compare six companies, inspect AI anomaly cues and test a downside scenario. Export a research brief with formulas, assumptions and source evidence.

`Python` · `Machine learning` · `SEC financial evidence` · `Browser scenarios`

Use it online without an account or Python installation. Official annual filings and Treasury rates carry explicit source dates. The original synthetic forecasting lab remains a separate research track.

**[START A COMPANY REVIEW ↗](https://leon1111-wgl.github.io/finscope/)** · [Source code and setup](https://github.com/leon1111-wgl/finscope) · [Worked case](https://github.com/leon1111-wgl/finscope/blob/main/docs/CASE_STUDY.md)

## Selected research

**[Seeing Is Believing: Grounding Long-Video Understanding in Spatio-Temporal Visual Evidence](https://ojs.aaai.org/index.php/AAAI/article/view/38031)**

`AAAI 2026` · `Co-first author` · Long-video understanding

Long videos require answers that can be checked against visual evidence. This work introduces EV²-Bench and DynamicSelect to study evidence-grounded understanding and efficient video processing.

My contributions included benchmark construction, temporal and visual evidence annotation, model evaluation, and evidence scoring using temporal IoU, text similarity, and bipartite matching.

[Read the paper ↗](https://ojs.aaai.org/index.php/AAAI/article/view/38031) · [Research on my website ↗](https://leon1111-wgl.github.io/leon1111-wgl/#research)

## Background & experience

- **The University of Hong Kong** · MSc · 2026 - Present. Working on AI. Enrolled September 2026.
- **The University of Sydney** · Studied Finance and Computer Science · 2023–2026. Dalyell Scholar.
- **Zhejiang University** · Exchange study · Dec 2024 - Jan 2025. Short-term exchange experience.

- **Long-video research**, EV²-Bench & model evaluation · 2025 - 2026. Contributed to dataset construction and reproducible evaluation with lmms-eval, structured model outputs, and evidence precision, recall, and F1.
- **AI Algorithm Intern**, Shenzhen Beidou Applied Technology Research Institute · 2025. Worked on video data preparation, annotation consistency checks, and model fine-tuning, distillation, quantization, and deployment validation for safety monitoring.

**Languages** · Mandarin Chinese and English (IELTS 7.5)

## Learning portals

Choose a card to enter the teaching website. Follow **story → concept → formula → worked example**. All five courses have English and Chinese editions. Follow algorithms in Python, objects in Java and systems in C. Trace the output, work through the mathematics and compare alternatives.

<a href="https://leon1111-wgl.github.io/leon1111-wgl/python-zero-to-practice/index.html"><img src="site/assets/profile-python.svg" width="100%" alt="Python — Zero to Practice. Open the Chinese self-study handbook." /></a>

**Python — Zero to Practice** · Chinese handbook · 19 learning units · 105 runnable examples · 114 self-study exercises · 4 complete projects.

[Read online ↗](https://leon1111-wgl.github.io/leon1111-wgl/python-zero-to-practice/index.html) · [Download the complete learning kit ↓](https://leon1111-wgl.github.io/leon1111-wgl/downloads/Python-Zero-to-Practice.zip) · [Browse the source](site/python-zero-to-practice/)

**New to Python or AI?** [Start here in English](https://leon1111-wgl.github.io/leon1111-wgl/ai/start.en.html) · [Start here in Chinese](https://leon1111-wgl.github.io/leon1111-wgl/ai/start.zh.html) · [Python examples](https://leon1111-wgl.github.io/leon1111-wgl/downloads/guoliang-python-examples.zip) · [All Python, Java and C examples](https://leon1111-wgl.github.io/leon1111-wgl/downloads/guoliang-code-examples.zip)

**Build with C:** [COMP2017 guided path](https://leon1111-wgl.github.io/leon1111-wgl/courses/comp2017.html#study-plan) · [Three complete engineering projects](https://leon1111-wgl.github.io/leon1111-wgl/courses/comp2017.html#projects) · [Download project source](https://leon1111-wgl.github.io/leon1111-wgl/downloads/COMP2017-projects.zip)

**Keep learning:** [Explore the guided extensions](https://leon1111-wgl.github.io/leon1111-wgl/#extensions-library). Follow complete bilingual cases on memory ownership, algorithm choices, logic, model evaluation, vision and multimodal retrieval. Predict the output, run the program and check each step.

<table>
<tr>
<td width="50%" align="center"><a href="https://leon1111-wgl.github.io/leon1111-wgl/#learning"><img src="site/assets/profile-foundations.svg" width="100%" alt="Computer science — open five courses, knowledge maps and one-page cheatsheets" /></a><br /><a href="https://leon1111-wgl.github.io/leon1111-wgl/#learning"><strong>Open the course library ↗</strong></a><p>5 courses · 121 topics</p></td>
<td width="50%" align="center"><a href="https://leon1111-wgl.github.io/leon1111-wgl/#ai"><img src="site/assets/profile-ai.svg" width="100%" alt="AI field guides — open four learning paths with English and Chinese versions" /></a><br /><a href="https://leon1111-wgl.github.io/leon1111-wgl/#ai"><strong>Open the bilingual AI guides ↗</strong></a><p>4 guides · 64 bilingual topics</p></td>
</tr>
</table>

<details>
<summary><strong>Go straight to a course</strong></summary>

### Computer science foundations

| Course | English | Chinese | Reference |
| :--- | :--- | :--- | :--- |
| INFO1113 | [Object-Oriented Programming in Java](https://leon1111-wgl.github.io/leon1111-wgl/courses/info1113.html) | [Read ZH](https://leon1111-wgl.github.io/leon1111-wgl/courses/info1113.zh.html) | [One-page PDF](https://leon1111-wgl.github.io/leon1111-wgl/downloads/INFO1113-cheatsheet.pdf) |
| COMP2017 | [Systems Programming: C, Processes & Concurrency](https://leon1111-wgl.github.io/leon1111-wgl/courses/comp2017.html) | [Read ZH](https://leon1111-wgl.github.io/leon1111-wgl/courses/comp2017.zh.html) | [One-page PDF](https://leon1111-wgl.github.io/leon1111-wgl/downloads/COMP2017-cheatsheet.pdf) |
| COMP2123 | [Algorithm Design and Analysis](https://leon1111-wgl.github.io/leon1111-wgl/courses/comp2123.html) | [Read ZH](https://leon1111-wgl.github.io/leon1111-wgl/courses/comp2123.zh.html) | [One-page PDF](https://leon1111-wgl.github.io/leon1111-wgl/downloads/COMP2123-cheatsheet.pdf) |
| COMP2022 | [Models of Computation: Languages, Machines & Logic](https://leon1111-wgl.github.io/leon1111-wgl/courses/comp2022.html) | [Read ZH](https://leon1111-wgl.github.io/leon1111-wgl/courses/comp2022.zh.html) | [One-page PDF](https://leon1111-wgl.github.io/leon1111-wgl/downloads/COMP2022-cheatsheet.pdf) |
| COMP3308 | [Artificial Intelligence: Search, Reasoning & Learning](https://leon1111-wgl.github.io/leon1111-wgl/courses/comp3308.html) | [Read ZH](https://leon1111-wgl.github.io/leon1111-wgl/courses/comp3308.zh.html) | [One-page PDF](https://leon1111-wgl.github.io/leon1111-wgl/downloads/COMP3308-cheatsheet.pdf) |

### AI field guides

| Guide | English | Chinese |
| :--- | :--- | :--- |
| Machine Learning | [Read EN](https://leon1111-wgl.github.io/leon1111-wgl/ai/ml.en.html) | [Read ZH](https://leon1111-wgl.github.io/leon1111-wgl/ai/ml.zh.html) |
| Deep Learning | [Read EN](https://leon1111-wgl.github.io/leon1111-wgl/ai/dl.en.html) | [Read ZH](https://leon1111-wgl.github.io/leon1111-wgl/ai/dl.zh.html) |
| Computer Vision: From Pixels to Perception | [Read EN](https://leon1111-wgl.github.io/leon1111-wgl/ai/vision.en.html) | [Read ZH](https://leon1111-wgl.github.io/leon1111-wgl/ai/vision.zh.html) |
| Multimodal AI | [Read EN](https://leon1111-wgl.github.io/leon1111-wgl/ai/multimodal.en.html) | [Read ZH](https://leon1111-wgl.github.io/leon1111-wgl/ai/multimodal.zh.html) |

[Download the complete cheatsheet collection](https://leon1111-wgl.github.io/leon1111-wgl/downloads/guoliang-cheatsheet-collection.pdf)

</details>

<p align="center"><sub>Leon · Research, ideas & learning in public.</sub><br /><a href="https://leon1111-wgl.github.io/leon1111-wgl/"><strong>Explore my personal website ↗</strong></a></p>
