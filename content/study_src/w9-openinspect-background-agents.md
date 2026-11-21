---
title: "Background Agents：让整个团队都能把想法变成 PR"
original: "Background Agents - Let Your Whole Team Ship Code"
week: "9"
slug: "w9-openinspect-background-agents"
source_url: "https://openinspect.dev"
author: "OpenInspect"
date: "2026"
kind: "产品文档"
coverage: "全文精译"
minutes: "6"
blurb: "一个开源、可自托管的后台 agent 框架：PM、设计师和工程师都能从 Slack、Web、VS Code 发起会话，直接产出可 review 的 PR。"
---

## 总结

这个页面介绍的是一套**面向整个团队的后台 coding agent 基础设施**，而不是只给工程师用的本地工具。

- 入口不止 IDE：Slack、Chrome 扩展、Web 版 VS Code、手机都可以发起和接管会话。
- 每个会话自带完整环境：仓库已 clone、依赖已安装、数据库已 seed、dev server 已启动。
- 目标是把“提 ticket 等排期”变成“直接产出一个可 review 的 PR”。
- 支持多人协作：分享 session URL，PM、设计师、工程师可以在同一个会话里补充上下文。
- 架构分三层：Cloudflare Workers + Durable Objects 控制面、Modal sandbox 数据面、Next.js Web 客户端。
- 开源、可自托管，MIT License。

## 原文逐段对照翻译

> **翻译说明：**原文是 Background Agents 的产品落地页。以下按页面顺序翻译产品定位、工作流、协作方式、指标和架构；顶部导航从略，页面里的 UI mock 文案用中文集中说明，避免把演示数据误当成真实运行状态。

### 产品定位

<div class="bilingual-pair">
<p class="src">Background Agents. An open framework for background coding agents.</p>
<p class="dst">Background Agents：一套用于后台 coding agents 的开放框架。</p>
</div>

<div class="bilingual-pair">
<p class="src">From code to tests to merged PR—automatically. Kick off a session at midnight, review the PR over breakfast.</p>
<p class="dst">从代码到测试再到已合并的 PR，全程自动。半夜启动一个会话，早餐时 review PR。</p>
</div>

<div class="bilingual-pair">
<p class="src">View on GitHub. Open source &amp; self-hostable.</p>
<p class="dst">在 GitHub 上查看。开源，可自托管。</p>
</div>

### 界面示例

<p><strong>界面示意：</strong>首屏展示的是一个示意性的 sessions dashboard：三个 agent 正在运行、一个新建会话表单，以及示例任务，比如把移动端 checkout 按钮调大、更新 header 品牌色、给 API 加 rate limiting。</p>

<p><strong>界面示意：</strong>示例会话状态包括“已运行 12 分钟”“已运行 8 分钟”“2 小时前完成”；每个任务旁边会显示仓库和发起人。</p>

### 让整个团队交付代码

<div class="bilingual-pair">
<p class="src">Let your whole team ship code. Not just engineers.</p>
<p class="dst">让你的整个团队都能交付代码，而不只是工程师。</p>
</div>

<div class="bilingual-pair">
<p class="src">PMs can fix their own bugs instead of filing tickets. Designers can tweak UI without waiting for eng cycles. Anyone with an idea can turn it into a PR. The barrier between "I wish this worked differently" and a merged pull request disappears.</p>
<p class="dst">PM 可以自己修 bug，而不是提交 ticket 等排期；设计师可以自己调 UI，不用等工程周期；任何有想法的人都能把它变成 PR。“我希望这里不一样”和“已合并的 PR”之间的壁垒消失了。</p>
</div>

<p><strong>界面示意：</strong>在 Slack 的 product-requests 频道里，PM 提出把移动端 checkout 按钮调大并占满宽度。后台 agent 回复说会更新移动端 checkout 样式，随后报告 PR #847 已准备好 review。</p>

### 零配置

<div class="bilingual-pair">
<p class="src">Zero Setup. Anyone can start. No configuration required.</p>
<p class="dst">零配置。任何人都能开始，不需要额外配置。</p>
</div>

<div class="bilingual-pair">
<p class="src">Contributors don't need local environments, package managers, or database setup. Every session comes pre-configured with your full stack—so anyone with an idea can turn it into working code.</p>
<p class="dst">贡献者不需要本地环境、包管理器或数据库配置。每个会话都预配置好完整技术栈，所以任何有想法的人都能把它变成可运行的代码。</p>
</div>

<p><strong>界面示意：</strong>环境面板显示仓库已 clone、依赖已安装、数据库已 seed、dev server 已运行，环境 8 秒内就绪。</p>

### 跳过 Ticket 队列

<div class="bilingual-pair">
<p class="src">Skip the Ticket Queue. Requests become PRs, not backlogs.</p>
<p class="dst">跳过 Ticket 队列。请求直接变成 PR，而不是进入 backlog。</p>
</div>

<div class="bilingual-pair">
<p class="src">Stop waiting for eng cycles. When a PM spots a bug or a designer wants a tweak, they can ship it themselves. The agent handles the code—your team just reviews and merges.</p>
<p class="dst">不用再等工程排期。PM 发现 bug、设计师想调整时，可以自己交付。agent 负责代码，团队只需要 review 和合并。</p>
</div>

<p><strong>界面示意：</strong>PR 列表展示了两个由 background-agent 发起的改动：PM 提交的移动端 checkout 尺寸修复，以及设计师提交的 header 品牌色更新。</p>

### 无限并发

<div class="bilingual-pair">
<p class="src">Unlimited Concurrency. Scale your team without scaling headcount.</p>
<p class="dst">无限并发。不增加人头，也能扩展团队产能。</p>
</div>

<div class="bilingual-pair">
<p class="src">Every team member can run parallel sessions. PMs exploring fixes, designers iterating on visuals, engineers prototyping—all at once. No local machines required, no bottlenecks on who can work.</p>
<p class="dst">每个团队成员都能并行跑会话：PM 探索修复方案、设计师迭代视觉、工程师做原型，全部同时进行。不需要本地机器，也不会因为“谁能用机器”而卡住。</p>
</div>

<p><strong>界面示意：</strong>会话面板显示团队里有 8 个活跃会话，包括移动端按钮、header 颜色、API rate limiting，以及另外 5 个。</p>

### 在任何地方工作

<div class="bilingual-pair">
<p class="src">Work From Anywhere. Meet agents where you work.</p>
<p class="dst">在任何地方工作。在你习惯的工具里直接使用 agent。</p>
</div>

<div class="bilingual-pair">
<p class="src">Start a session from Slack. Refine it in the web UI. Make a quick edit in VS Code. Review on your phone. Everything stays synced, so you never lose context switching between surfaces.</p>
<p class="dst">从 Slack 发起会话，在 Web UI 里细化，在 VS Code 里快速改一笔，在手机上 review。所有状态保持同步，切换界面不会丢上下文。</p>
</div>

<div class="bilingual-pair">
<p class="src">Slack: start sessions with screenshots. Chrome Extension: highlight visual changes directly. Web-based VS Code: make manual edits without cloning.</p>
<p class="dst">Slack：带截图发起会话。Chrome 扩展：直接高亮视觉改动。Web 版 VS Code：不用 clone 就能手动编辑。</p>
</div>

### 内置多人协作

<div class="bilingual-pair">
<p class="src">Multiplayer Built In. Every session is collaborative.</p>
<p class="dst">内置多人协作。每个会话都是协作空间。</p>
</div>

<div class="bilingual-pair">
<p class="src">Share a session URL with a colleague. Let them prompt alongside you, make changes, or take it home. Designers can request visual tweaks. PMs can file bugs directly. Anyone can contribute.</p>
<p class="dst">把 session URL 分享给同事，让对方一起写 prompt、改代码，或者把会话接过去继续做。设计师可以提视觉调整，PM 可以直接报 bug，任何人都能贡献。</p>
</div>

<p><strong>界面示意：</strong>协作面板展示了一个多人会话：有人要求把按钮调大，有人补了边界测试，agent 最后报告按钮已更新、所有测试通过。</p>

### 只为你的代码工作

<div class="bilingual-pair">
<p class="src">It only has to work for your code. Off-the-shelf agents try to work everywhere and excel nowhere. When you own the tooling, you encode exactly how your team ships. That's significantly more powerful than any generic tool.</p>
<p class="dst">它只需要为你的代码工作。通用 agent 试图在任何地方都能用，结果哪里都不够好。当你拥有自己的工具链，就能把团队的交付方式编码进去，这比任何通用工具都强得多。</p>
</div>

<div class="bilingual-pair">
<p class="src">30% of PRs at teams using background agents come from non-engineers. Minutes from idea to pull request, not sprints. Zero local setup required for any contributor.</p>
<p class="dst">使用后台 agent 的团队里，30% 的 PR 来自非工程师。从想法到 PR 只需要几分钟，而不是几个 sprint。任何贡献者都不需要本地配置。</p>
</div>

### 异步设计

<div class="bilingual-pair">
<p class="src">Async by design. Capture ideas the moment you have them.</p>
<p class="dst">异步设计。有想法的那一刻就能启动。</p>
</div>

<div class="bilingual-pair">
<p class="src">Notice a bug while winding down? Kick off a session, describe what you want, and check the PR tomorrow morning. Agents work while you sleep.</p>
<p class="dst">下班前发现一个 bug？启动会话、描述需求，第二天早上直接看 PR。agent 在你睡觉时继续工作。</p>
</div>

### 架构

<div class="bilingual-pair">
<p class="src">Architecture. Built on modern infrastructure.</p>
<p class="dst">架构。建立在现代基础设施之上。</p>
</div>

<div class="bilingual-pair">
<p class="src">Control Plane: Cloudflare Workers + Durable Objects for session management, WebSocket streaming, and GitHub integration.</p>
<p class="dst">控制面：Cloudflare Workers + Durable Objects，负责会话管理、WebSocket 流式传输和 GitHub 集成。</p>
</div>

<div class="bilingual-pair">
<p class="src">Data Plane: Modal-powered sandboxed environments running autonomous coding agents with full dev tooling.</p>
<p class="dst">数据面：基于 Modal 的 sandbox 环境，运行带完整开发工具的自主 coding agents。</p>
</div>

<div class="bilingual-pair">
<p class="src">Web Client: Next.js application with GitHub OAuth for monitoring and managing your coding agents.</p>
<p class="dst">Web 客户端：Next.js 应用，使用 GitHub OAuth 来监控和管理 coding agents。</p>
</div>

<div class="bilingual-pair">
<p class="src">Let everyone ship like your best engineers. Open source. Self-hostable. Ready for your whole team. MIT License.</p>
<p class="dst">让每个人都能像最好的工程师一样交付。开源、可自托管、面向整个团队。MIT License。</p>
</div>

## 学习者视角

### 关键收获

1. **后台 agent 的产品边界是“入口”和“环境”。** 谁能发起、在哪里发起、环境是否开箱即用，决定了非工程师能不能真正参与。
2. **PR 是比 ticket 更好的工作单位。** 需求直接变成可 review 的改动，减少排队和转述损耗。
3. **多人协作需要 session 作为共享上下文。** 不是把任务分配给一个人，而是让多个人围绕同一个会话补充信息。
4. **控制面和数据面分离。** Cloudflare 负责会话与 GitHub 集成，Modal 负责隔离执行环境，职责清晰。
5. **自托管是差异化的一部分。** 团队可以把“自己怎么交付”编码进工具，而不是适配通用产品。

### 放回课程里看

这篇是 Week 9 的“团队入口”视角：Week 8 讨论后台 agent 如何异步执行，这篇进一步问“谁可以发起任务、在哪里发起、如何协作”。它和 [Warp Factory](w9-warp-factory-issue-to-pr.html) 形成对照：Warp 用多入口 + 多 runner 构建工程流水线，OpenInspect 用 session + sandbox 降低参与门槛。

### 一个反直觉点

很多人以为后台 agent 的价值是“工程师不用盯着跑”。这个产品的重点其实是**让非工程师也能直接产出 PR**：PM 和设计师不再只是提需求的人，而是可以自己完成第一版改动的人。

## 拓展

### 思考题

1. 如果 PM 和设计师都能直接开 PR，代码 review 的重点会发生什么变化？
2. “每个会话预配置完整环境”需要哪些基础设施？最大的安全风险是什么？
3. 多人协作 session 和传统 pair programming 有什么相同点和不同点？
4. 为什么控制面适合用 Durable Objects，而执行面适合用 sandbox？

### 练习

为你的团队设计一个后台 agent 入口：

- 哪些角色可以发起会话；
- 从哪些界面发起（Slack / Web / IDE / 手机）；
- 每个会话需要预配置什么环境；
- 哪些操作必须人工批准；
- 如何把 session 链接给同事接手；
- 用什么指标判断“非工程师也能安全交付”。

### 接着读

- [Software Factory：10 天软件工厂实验](w9-software-factory.html)
- [Warp Factory 示例：从 Issue 到 PR](w9-warp-factory-issue-to-pr.html)
- [WarpBench：用内部 benchmark 优化 agent 成本](w9-warpbench.html)
