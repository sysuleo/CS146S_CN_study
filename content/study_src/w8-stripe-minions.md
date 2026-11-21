---
title: "Stripe Minions：一次运行、端到端交付的 Coding Agent"
original: "Minions: Stripe’s one-shot, end-to-end coding agents"
week: "8"
slug: "w8-stripe-minions"
source_url: "https://stripe.dev/blog/minions-stripes-one-shot-end-to-end-coding-agents"
author: "Alistair Gray / Stripe"
date: "2026-02-09"
kind: "工程博客"
coverage: "全文精译"
minutes: "10"
blurb: "每周 1,000+ 个 PR 由 Minions 全自动产出：10 秒 devbox、400+ MCP 工具、本地 lint、最多两轮 CI，以及为什么 Stripe 必须自建。"
---

## 总结

Stripe 的 Minions 是**完全无人值守、一次运行完成任务**的 coding agents。

- 每周有 1,000+ 个合并 PR 完全由 Minions 产出；代码经过人类 review，但没有人类手写代码。
- 典型流程：Slack 消息 → devbox 里运行 agent → 改代码、跑测试 → 推送分支 → 开 PR。
- Stripe 没有直接用现成 agent：代码库有数亿行、Ruby + Sorbet 栈、大量内部库，还有金融合规约束。
- 每个 Minion 跑在预热的 devbox 上，10 秒启动，隔离生产资源和互联网，可以直接并行。
- 核心 agent loop 基于 Block 的 goose fork，并把 agent 循环和确定性步骤（git、lint、测试）交错起来。
- 通过内部 MCP server Toolshed 访问 400+ 工具；本地 lint 5 秒内完成，CI 最多跑两轮。
- 目标不是“让 agent 多跑几轮”，而是把反馈尽量左移，第一次就做对。

## 原文逐段对照翻译

> **翻译说明：**以下按原文顺序翻译全文；原文 3 张正文截图已下载到本地并按原位置插入。文章元数据（栏目、阅读时长、分享按钮等）、文末相关文章、导航和订阅模块从略。

### 引言

<div class="bilingual-pair">
<p class="src">Across the industry, agentic coding has gone from new and exciting to table stakes, and as underlying models continue to improve, unattended coding agents have gone from possibility to reality.</p>
<p class="dst">在整个行业里，agentic coding 已经从新鲜事变成基本功；随着底层模型持续进步，无人值守的 coding agents 也从可能性变成了现实。</p>
</div>

<div class="bilingual-pair">
<p class="src">Minions are Stripe’s homegrown coding agents. They’re fully unattended and built to one-shot tasks. Over a thousand pull requests merged each week at Stripe are completely minion-produced, and while they’re human-reviewed, they contain no human-written code.</p>
<p class="dst">Minions 是 Stripe 自研的 coding agents。它们完全无人值守，目标是一次运行完成整个任务。Stripe 每周有 1,000+ 个合并 PR 完全由 Minions 产出；这些代码会经过人类 review，但不包含人类手写的代码。</p>
</div>

<div class="bilingual-pair">
<p class="src">Our developers can still plan and collaborate with agents such as Claude and Cursor, but in a world where one of our most constrained resources is developer attention, unattended agents allow for parallelization of tasks.</p>
<p class="dst">开发者仍然可以用 Claude、Cursor 这类 agent 做规划和协作；但在开发者注意力是最稀缺资源之一的环境里，无人值守 agent 让任务可以并行推进。</p>
</div>

<div class="bilingual-pair">
<p class="src">A typical minion run starts in a Slack message and ends in a pull request which passes CI and is ready for human review, with no interaction in between. We frequently see engineers spinning up multiple minions in parallel, to enable them to parallelize the completion of many different tasks. This can be particularly helpful during an on-call rotation to effectively resolve many small issues that might arise.</p>
<p class="dst">一次典型的 Minion 运行从 Slack 消息开始，到一个通过 CI、可供人类 review 的 PR 结束，中间不需要任何交互。我们经常看到工程师并行启动多个 Minions，把许多不同任务同时推进；在 on-call 轮值期间，这对快速处理大量小问题尤其有用。</p>
</div>

<div class="bilingual-pair">
<p class="src">In the first part of this blog post miniseries, we’ll show you how our engineers use minions and what they can do. In Part 2, we’ll dive into the implementation under the hood and how we built them.</p>
<p class="dst">在这个系列的第一篇里，我们展示工程师如何使用 Minions、它们能做什么；第二篇会深入实现细节，讲我们是怎么把它们建起来的。</p>
</div>

### 为什么自建

<div class="bilingual-pair">
<p class="src">Vibe coding a prototype from scratch is fundamentally different from contributing code to Stripe’s codebase.</p>
<p class="dst">从零 vibe coding 一个原型，和给 Stripe 的代码库贡献代码，是两件根本不同的事。</p>
</div>

<div class="bilingual-pair">
<p class="src">Stripe’s codebase encompasses hundreds of millions of lines of code across a few large repositories. Most of our backend is written in Ruby (not Rails) with Sorbet typing, a relatively uncommon stack. Throughout, our code uses a vast number of homegrown libraries that are unique to Stripe and therefore natively unfamiliar to LLMs.</p>
<p class="dst">Stripe 的代码库分布在几个大型仓库里，总计数亿行代码。大部分后端用 Ruby（不是 Rails）加 Sorbet 类型系统，这是一个相对少见的栈。代码里还使用了大量 Stripe 自研库，LLM 天然不熟悉。</p>
</div>

<div class="bilingual-pair">
<p class="src">The stakes are high: this code moves well over $1 trillion per year of payment volume live in production. Simultaneously, Stripe has many intricate real-world dependencies on financial institutions and regulatory and compliance obligations that our code must honor.</p>
<p class="dst">风险很高：这些代码在生产环境承载每年超过 1 万亿美元的支付量。同时，Stripe 与金融机构、监管和合规义务之间有大量复杂的现实依赖，代码必须遵守。</p>
</div>

<div class="bilingual-pair">
<p class="src">LLM agents are incredibly good at building software from scratch when there are relatively few constraints on a system. However, iterating on any codebase of the scale, complexity, and maturity of Stripe’s is inherently much harder. Humans must build sophisticated mental models to make effective changes in our repos, and enabling agents to develop the correct intuitions and use the correct tools within the confines of their context windows is challenging.</p>
<p class="dst">当系统约束较少时，LLM agents 非常擅长从零构建软件。但在 Stripe 这种规模、复杂度和成熟度的代码库里迭代，本质上难得多。人类需要建立复杂的心智模型才能有效改动我们的仓库；要让 agent 在有限的上下文窗口里形成正确直觉、使用正确工具，非常困难。</p>
</div>

<div class="bilingual-pair">
<p class="src">Over the years, Stripe has invested in developer productivity foundations that support our unique constraints at all stages in the development lifecycle—source control, environments, code generation, CI, and much more—and so our custom minion harness tightly integrates with that tooling. Minions use the same developer tooling that equally enables Stripe’s human engineers to effectively operate at our scale: if it’s good for humans, it’s good for LLMs, too.</p>
<p class="dst">多年来，Stripe 在开发者生产力基础设施上投入很多，覆盖开发生命周期的各个阶段——版本控制、环境、代码生成、CI 等——我们的 Minion harness 与这些工具紧密集成。Minions 使用的就是让 Stripe 人类工程师能在这种规模下工作的同一套工具：对人类好用的东西，对 LLM 也好用。</p>
</div>

### 使用 Minion 是什么体验

<div class="bilingual-pair">
<p class="src">There are several different entry points for minions, designed to integrate as ergonomically as possible with where Stripes are. While we provide CLI and web interfaces for initiating minions, engineers will most frequently start one from Slack. By tagging our Slack app, engineers can kick off a minion directly from the thread discussing a change, and it’ll be able to access the entire thread and any links included as context.</p>
<p class="dst">Minions 有多个入口，设计目标是尽量贴合 Stripe 员工的工作场景。我们提供 CLI 和 Web 界面，但工程师最常从 Slack 发起：在讨论改动的线程里 @ 我们的 Slack app，Minion 就能拿到整个线程和其中的链接作为上下文。</p>
</div>

<div class="bilingual-pair">
<p class="src">If you’re an engineer working on internal tools, you might kick off a minion with a message like this:</p>
<p class="dst">如果你在做内部工具，可能会用这样的消息启动一个 Minion：</p>
</div>

<figure class="article-figure">
<a href="assets/figures/w8-stripe/image1.png" target="_blank" rel="noopener noreferrer"><img src="assets/figures/w8-stripe/image1.png" alt="A Slack message invoking a minion run"></a>
<figcaption>原文截图：一条启动 Minion 运行的 Slack 消息。</figcaption>
</figure>

<div class="bilingual-pair">
<p class="src">Minions can also be invoked from inside other internal applications at Stripe. Our internal docs platform, feature flag platform, and internal ticketing UI all integrate with minions. For example, when our CI systems detect flaky tests, we create automated tickets that prompt users to fix the problem with a minion.</p>
<p class="dst">Minions 也能从 Stripe 其他内部应用里调用。内部文档平台、feature flag 平台和内部 ticket UI 都集成了 Minions。比如 CI 检测到 flaky test 时，我们会自动创建 ticket，提示用户用 Minion 修复。</p>
</div>

<figure class="article-figure">
<a href="assets/figures/w8-stripe/image2.png" target="_blank" rel="noopener noreferrer"><img src="assets/figures/w8-stripe/image2.png" alt="A flaky test ticket with a button to start a minion"></a>
<figcaption>原文截图：一个 flaky test ticket，带有“启动 Minion 修复”的按钮。</figcaption>
</figure>

<div class="bilingual-pair">
<p class="src">While the minion works, or after the fact, engineers can see the decisions and actions the minion took in a web UI.</p>
<p class="dst">Minion 运行期间或结束后，工程师可以在 Web UI 里查看它做了哪些决策和操作。</p>
</div>

<figure class="article-figure">
<a href="assets/figures/w8-stripe/image3.png" target="_blank" rel="noopener noreferrer"><img src="assets/figures/w8-stripe/image3.png" alt="An example of the web interface for managing minion runs"></a>
<figcaption>原文截图：管理 Minion 运行的 Web 界面示例。</figcaption>
</figure>

<div class="bilingual-pair">
<p class="src">Once it has completed its task, a minion creates a branch, pushes it to CI, and prepares a pull request following Stripe’s PR template. If the code looks good, the engineer opens the PR and requests a review from another Stripe engineer. If not, they can give the minion further instructions, and it will push updated code to the branch when it’s done.</p>
<p class="dst">任务完成后，Minion 会创建分支、推送到 CI，并按 Stripe 的 PR 模板准备 PR。如果代码看起来不错，工程师就打开 PR，请另一位 Stripe 工程师 review；如果不行，可以给 Minion 进一步指令，它完成后会把更新推到同一分支。</p>
</div>

<div class="bilingual-pair">
<p class="src">Engineers can also iterate on a completed minion run manually once it’s completed. While our North Star is a pull request produced without any human code, a minion run that’s not entirely correct is often still an excellent starting point for an engineer’s focused work.</p>
<p class="dst">Minion 完成后，工程师也可以手动继续迭代。我们的 North Star 是产出不含任何人类代码的 PR；但即使一次运行不完全正确，它往往仍是工程师继续专注修改的好起点。</p>
</div>

### Minion 如何工作

<div class="bilingual-pair">
<p class="src">There are many stages to a minion, and in the second part of this miniseries, we’ll have more details about how minions work. Many of the details are Stripe-specific, but we do think that there are some generalizable lessons. To whet your appetite, here’s a brief chronological tour.</p>
<p class="dst">一个 Minion 包含很多阶段，本系列第二篇会讲更多细节。很多细节是 Stripe 特有的，但我们认为其中有一些可推广的经验。先按时间顺序快速走一遍。</p>
</div>

<div class="bilingual-pair">
<p class="src">A minion run starts in an isolated developer environment—or “devbox”—which are the same type of machine that Stripe engineers write code on. Devboxes are pre-warmed so one can be spun up in 10 seconds, with Stripe code and services pre-loaded. They’re isolated from production resources and the internet, so we can run minions on devboxes without human permission checks. This also gives parallelization without the overhead of something like git worktrees, which wouldn’t scale at Stripe.</p>
<p class="dst">Minion 运行从隔离的开发者环境——“devbox”——开始，它和 Stripe 工程师写代码用的是同一类机器。Devbox 预热过，10 秒就能启动，Stripe 代码和服务已经预加载。它们与生产资源和互联网隔离，所以可以在没有人工权限检查的情况下运行 Minions。这也带来了并行能力，而不用承担 git worktree 那类在 Stripe 规模下无法扩展的开销。</p>
</div>

<div class="bilingual-pair">
<p class="src">The core agent loop runs on a fork of Block’s coding agent goose, one of the first widely used coding agents, which we forked early on. We’ve customized the orchestration flow in an opinionated way to interleave agent loops and deterministic code—for git operations, linters, testing, and so on—so that minion runs mix the creativity of an agent with the assurance that they’ll always complete Stripe-required steps like linters.</p>
<p class="dst">核心 agent loop 跑在 Block 的 coding agent goose 的一个 fork 上。Goose 是最早被广泛使用的 coding agents 之一，我们很早就 fork 了它。我们用一种有明确取舍的方式定制了编排流程，把 agent loop 和确定性代码交错起来——git 操作、linter、测试等——这样 Minion 既保留 agent 的创造力，又能保证一定会执行 Stripe 要求的步骤，比如 lint。</p>
</div>

<div class="bilingual-pair">
<p class="src">In general, minions read the same coding agent rule files that human-operated tools such as Cursor and Claude Code do, consuming several different agent rule file formats. However, it would be impractical for Stripe to have many unconditional rules, so almost all agent rules at Stripe are conditionally applied based on subdirectories.</p>
<p class="dst">一般来说，Minions 读取的 coding agent 规则文件，和 Cursor、Claude Code 这类人类操作工具读取的一样，支持多种 agent 规则文件格式。但 Stripe 不可能维护大量无条件规则，所以几乎所有 agent 规则都按子目录条件生效。</p>
</div>

<div class="bilingual-pair">
<p class="src">Minions are connected to MCP, which provides a common language for networkable LLM function calling. This is how they gather context like internal documentation, ticket details, build statuses, code intelligence via Sourcegraph search, and more. Indeed, we deterministically run relevant MCP tools over likely-looking links before a minion run even starts, to better hydrate the context.</p>
<p class="dst">Minions 接入了 MCP，它为可网络化的 LLM function calling 提供了共同语言。Minion 通过 MCP 获取内部文档、ticket 详情、构建状态、Sourcegraph 代码搜索等上下文。实际上，在 Minion 运行开始前，我们会确定性地对看起来相关的链接调用相关 MCP 工具，提前补足上下文。</p>
</div>

<div class="bilingual-pair">
<p class="src">Since MCP is a common language for all agents at Stripe, not just minions, we built a central internal MCP server called Toolshed, which hosts more than 400 MCP tools spanning internal systems and SaaS platforms we use at Stripe. Minions and other agents have connectivity to configurable but curated subsets of the full breadth of tools.</p>
<p class="dst">因为 MCP 是 Stripe 所有 agent（不只 Minions）的共同语言，我们建了一个中心化内部 MCP server，叫 Toolshed，托管 400+ 个 MCP 工具，覆盖 Stripe 使用的内部系统和 SaaS 平台。Minions 和其他 agents 可以连接这些工具中可配置、经过筛选的子集。</p>
</div>

<div class="bilingual-pair">
<p class="src">Minions are built with the goal of one-shotting their tasks, but if they don’t, then it’s key to give agents feedback. We do this via several automated layers of tests that minions can iterate against. The first line of defense is an automated local executable, which uses heuristics to select and automatically run selected lints on each git push. This takes less than five seconds.</p>
<p class="dst">Minions 的目标是一次完成任务；如果做不到，给 agent 反馈就非常关键。我们通过多层自动测试让 Minion 迭代。第一道防线是一个自动本地可执行程序，它用启发式规则在每次 git push 时选择并运行相关 lint，耗时不到 5 秒。</p>
</div>

<div class="bilingual-pair">
<p class="src">We seek to “shift feedback left” when thinking about developer productivity. That means that it’s best for humans and agents if any lint step that would fail in CI is enforced in the IDE or on a git push, and presented to the engineer immediately.</p>
<p class="dst">在考虑开发者生产力时，我们追求“把反馈左移”。也就是说，任何会在 CI 失败的 lint，最好在 IDE 或 git push 时就强制执行，并立刻呈现给工程师——这对人和 agent 都更好。</p>
</div>

<div class="bilingual-pair">
<p class="src">If the local testing doesn’t catch anything, CI selectively runs tests from Stripe’s battery of tests—there are over three million of them—upon a push. Many of our tests have autofixes for failures, which we automatically apply. If a test failure has no autofix, we send it back to the minion to try and fix.</p>
<p class="dst">如果本地测试没抓到问题，CI 会在 push 后从 Stripe 的测试库里选择性运行测试——我们的测试超过 300 万个。很多测试失败带有 autofix，我们会自动应用；如果没有 autofix，就把失败发回给 Minion 尝试修复。</p>
</div>

<div class="bilingual-pair">
<p class="src">Since CI runs cost tokens, compute, and time, we only have at most two rounds of CI. If tests fail after an initial push, we prompt the minion to fix failing tests and push a second time, but are then done. There’s a balancing act between speed and completeness here, and there are diminishing marginal returns for an LLM to run many rounds of a full CI loop. We feel this guidance of “often one, at most two, CI runs—and only after we’ve fixed everything we can locally” strikes a good balance.</p>
<p class="dst">CI 会消耗 token、算力和时间，所以我们最多只跑两轮。第一次 push 后测试失败，会提示 Minion 修复并再 push 一次，然后结束。这里要在速度和完整性之间平衡；让 LLM 反复跑完整 CI 的边际收益会递减。我们认为“通常一轮、最多两轮 CI，而且只在本地能修的都修完之后”是一个不错的平衡。</p>
</div>

<div class="bilingual-pair">
<p class="src">In short, minions are set up with the same tools we give human engineers and the necessary context to follow Stripe best practices in the code they write. And engineers can and do invoke them ergonomically as part of their normal job duties.</p>
<p class="dst">简而言之，Minions 配备了和人类工程师相同的工具，以及遵循 Stripe 最佳实践所需的上下文。工程师可以在日常工作里顺手调用它们。</p>
</div>

### 下一步

<div class="bilingual-pair">
<p class="src">Minions have already reimagined what it’s like to code at Stripe. The industry is still exploring what the future of agentic coding will look like, but we’re sure that the unattended code agent use case will remain among the most exciting applications of agents.</p>
<p class="dst">Minions 已经重新定义了在 Stripe 写代码的体验。行业仍在探索 agentic coding 的未来，但我们确信，无人值守 coding agent 会一直是最令人兴奋的应用之一。</p>
</div>

<div class="bilingual-pair">
<p class="src">In Part 2, we’ll dive more deeply into how we implemented minions. Interested in working with, or on, minions? We’re hiring.</p>
<p class="dst">第二篇会深入讲 Minions 的实现。有兴趣使用或参与构建 Minions？我们正在招聘。</p>
</div>

<div class="bilingual-pair">
<p class="src">Alistair is a software engineer on the Leverage team. The Leverage team builds surprisingly delightful internal products that Stripes can leverage to supercharge their productivity.</p>
<p class="dst">Alistair 是 Leverage 团队的软件工程师。Leverage 团队构建令人惊喜的内部产品，帮助 Stripe 员工提升生产力。</p>
</div>

## 学习者视角

### 关键收获

1. **自建的理由是“约束”。** Stripe 的 Ruby/Sorbet 栈、自研库、金融合规和数亿行代码，决定了通用 agent 不够用。
2. **Devbox 是并行化的基础。** 10 秒预热、隔离生产、无人工权限检查，才能让多个 Minions 同时跑。
3. **Agent + 确定性步骤交错。** 让 agent 负责创造性改动，同时强制 git、lint、测试这些必须步骤。
4. **反馈左移。** 5 秒本地 lint 比 CI 失败后再回传更便宜；CI 最多两轮，避免边际收益递减。
5. **工具要为人设计，也为 agent 设计。** Minions 复用人类工程师的工具链，降低了维护两套体系的成本。

### 放回课程里看

这篇是 Week 8 的“自建 harness”代表：它解释了为什么通用 coding agent 在大型、成熟、强约束代码库里不够用，以及如何用 devbox、MCP 和 CI 反馈闭环把 agent 变成可靠的生产工具。和 [Spotify Honk](w8-spotify-background-coding-agent.html) 相比，Stripe 更强调“一次运行完成”和“执行环境隔离”；和 [Ramp Inspect](w8-ramp-background-agent.html) 相比，Stripe 更强调与现有 CI/测试体系的深度集成。

### 一个反直觉点

很多人以为提高 agent 成功率要靠“多跑几轮”。Stripe 的结论是：**最多两轮 CI，更多轮次的边际收益递减；真正有效的是把 lint 和测试反馈尽量左移，让第一轮就足够好。**

## 拓展

### 思考题

1. 为什么 Stripe 不直接用 Cursor/Claude Code，而是 fork goose 做自己的 harness？
2. Devbox 隔离生产资源和互联网，带来了哪些安全收益和限制？
3. “最多两轮 CI”在什么情况下会不够？你会怎么调整规则？
4. 如果你的代码库没有 300 万测试，如何设计一个更轻量的反馈闭环？

### 练习

为一个“一次运行完成”的 agent 设计执行环境：

- 需要预加载什么（代码、依赖、服务、缓存）；
- 启动时间目标是多少；
- 哪些操作必须确定性执行（git、lint、测试、格式化）；
- 本地反馈和 CI 反馈各覆盖什么；
- 最多允许多少轮 CI，为什么；
- 如何记录 agent 的决策和操作。

### 接着读

- [Spotify Honk：1,500+ PR 的迁移 agent](w8-spotify-background-coding-agent.html)
- [Ramp Inspect：自建后台 agent 的架构](w8-ramp-background-agent.html)
- [LangChain Robin：开源软件工厂](w8-langchain-robin.html)
