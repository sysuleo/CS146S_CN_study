# CS146S 中文学习项目规则

本文件是本项目的长期约定。后续新增/修改材料时，优先遵守这里的规则。

## 1. 项目目标

把 CS146S 的课程表、阅读材料和课堂实录整理成一套可浏览、可复习、可部署的中文学习资料。

核心入口：

- 课程表：`app/static/schedule.html`
- 学习站：`app/static/study/index.html`
- 当前构建源：`content/study_src/`
- 生成产物：`app/static/study/*.html`

不要直接改 `app/static/study/*.html`，除非只是临时验证。正式内容改 `content/study_src/*.md`，再重新构建。

## 2. 页面结构

每个学习页固定四段，顺序不能变：

1. `## 总结`
2. `## 原文逐段对照翻译`
3. `## 学习者视角`
4. `## 拓展`

要求：

- 总结必须独立成章，不能混在翻译里。
- 原文对照按“英文段落 + 中文段落”交替排列。
- 中文翻译不逐字硬译，保持完整句子和自然语序。
- 学习者视角包含：关键收获、放回课程、反直觉点。
- 拓展包含：思考题、练习、接着读。

## 3. Frontmatter 规范

每个 `content/study_src/*.md` 必须包含：

```yaml
---
title: "中文标题"
original: "原文标题"
week: "1"
slug: "w1-example"
source_url: "https://..."
author: "作者"
date: "2026"
kind: "课堂实录 / 论文 / 工程博客 / 产品文档 / 开源项目"
coverage: "逐段精译 / 全文精译 / 逐段直译"
minutes: "10"
blurb: "首页卡片一句话描述"
---
```

`slug` 必须与文件名一致，必须与课表链接一致。

`coverage` 决定首页状态徽标：

- `逐段精译` / `全文精译`：显示“已精修”
- `核心章节精修`：显示“部分精修”
- `逐段直译`：显示“机翻待精修”

## 4. 翻译规则（信达雅）

优先级：**准确 > 通顺 > 简洁 > 保留原文风格**。

必须做到：

- 保留原文技术论证、数据、例子和结论。
- 不把完整句子拆成碎片；按段落对照，不按单词硬切。
- 中文要像正常技术文章，不要机翻腔。
- 术语首次出现可保留英文，后文保持一致。
- **难翻译的关键词优先保留英文**，不要硬造中文术语；首次出现可括注中文，后文直接用英文。
- 例：`action space`、`harness`、`context window`、`compaction`、`subagent`、`tool call`、`spec`。
- 代码、命令、工具名、文件名保持原样。
- 无法确认的内容不要编造；在页内注明“此处原文不清晰”。
- **原文有图/表时必须保留**：下载到本地，按原文所在 H2/H3 放回对应段落，不得只做文字重写。
- 图注保留原文，并补一句中文说明；不要把图集中堆到页面顶部或末尾。
- **不得改变原文 H2/H3 顺序**。如果要加“总结/学习者视角”，只能放在原文翻译之前或之后，不能重排原文主体。

禁止：

- “克劳德”“编码特工”“代理.md”“代理的人体工”等机翻残留。
- 把 `harness` 译成“线束”。
- 把 `action space` 硬译成“动作空间”。
- 把 `token` 译成“令牌”。
- 把 `AGENTS.md` 译成“代理.md”。
- 用总结代替原文翻译。

推荐术语：

| 英文 | 中文 |
|---|---|
| agent | agent / 智能体（首次可括注） |
| harness | harness / 执行框架 |
| context | 上下文 |
| context window | 上下文窗口 |
| prompt | 提示词 |
| tool call | 工具调用 |
| skill | skill / 技能 |
| subagent | subagent |
| compaction | compaction / 上下文压缩 |
| spec | 规格 |
| code review | 代码审查 |
| pull request | PR |
| merge request | MR |
| token | token |
| repo | 仓库 |
| diff | diff |

## 5. 全文覆盖规则

- 普通文章：正文逐段完整翻译。
- 课堂实录：覆盖技术讲授与技术问答；寒暄、重复表述、无法辨认片段从略。
- 论文：正文完整；参考文献、附录不译，页内注明。
- 超长篇论文允许采用“章节级精译”，但必须覆盖全部章节；逐段机翻只能作为“机器翻译参考”附录，不能冒充逐句精修。
- 产品页：产品说明、用法、示例完整；超长目录/兼容列表可概括，页内注明。

任何省略都必须在页面“阅读说明”里写清楚，不能默默省略。

## 6. PPT 规则

- 来源：Google Slides `export/pdf` 导出。
- 图片目录：`app/static/study/assets/slides/<deck>/<NN>.png`。
- 每张 PPT 单独一行，不与其它页并排。
- 点击图片可打开原尺寸。
- 不靠相似度自动猜；使用 `tools/slides.py` 的逐页锚点映射。
- 锚点必须是原文中唯一、稳定的英文句子。
- 幻灯片顺序必须与讲课顺序一致。
- 标题页/章节页放小节开头；概念页放对应段落前。
- 修改后重新运行 `tools/slides.py` 和 `tools/build.py`。

## 7. 页面 UI 规则

- 左侧目录：桌面粘性、滚动高亮、窄屏折叠。
- 目录必须覆盖 `##` 和 `###` 标题。
- 课堂实录的小节标题要能反映讲课顺序（如“开场与课程安排”“Research：只记录现状”）。
- 首页卡片显示：类型、状态（已精修/机翻待精修）、阅读时长、中文标题、原文标题、一句话描述。
- 不要引入前端框架；保持单文件 HTML + 共享 CSS。

## 8. 构建流程

标准构建：

```bash
python tools/slides.py      # 重新插入 PPT（如涉及课堂实录）
python tools/build.py   # 生成 app/static/study/*.html + 回链课表
python tools/check.py         # 检查本地链接
```

内容规范化：

```bash
python tools/normalize_machine_text.py   # 统一术语/标题
python tools/build.py
```

抓取原文：

```bash
python tools/fetch_readings.py
```

注意：

- `.local/archive/study_src_v1/` 是早期草稿，不再作为构建源。
- `content/study_src/` 是当前唯一构建源。
- `_source/` 放原文提取、PDF、transcript、翻译缓存，不要直接发布。

## 9. 新增一篇材料的流程

1. 在 `_source/` 放原文提取结果。
2. 在 `content/study_src/` 新建 `<slug>.md`，填写 frontmatter。
3. 写“总结 / 原文逐段对照 / 学习者视角 / 拓展”。
4. 如果是课堂实录，准备 PDF 并更新 `tools/slides.py` 映射。
5. 运行 `tools/slides.py`、`tools/build.py`、`tools/check.py`。
6. 在 `README.md` 和 `TODO.md` 更新状态。

## 10. 部署与服务器

本地/服务器启动：

```bash
python -m uvicorn server.app:app --host 0.0.0.0 --port 8787
```

接口：

- `GET /`：学习站首页
- `GET /schedule`：课程表
- `GET /api/health`：健康检查
- `POST /api/jobs`：创建构建单（`{"kind":"rebuild"}`）
- `GET /api/jobs`：任务列表
- `GET /api/jobs/{id}`：任务状态与日志

“建单”在这里指**构建任务单**，不是易协作/内部工单。如果要接内部建单系统，需要另加项目、单号、字段映射。

## 11. 验收清单

- 页面四段结构完整。
- 没有机翻残留术语。
- 所有本地链接和图片存在。
- 课堂实录 PPT 顺序正确、一页一行。
- 首页状态徽标正确。
- `README.md` / `TODO.md` 状态同步。
