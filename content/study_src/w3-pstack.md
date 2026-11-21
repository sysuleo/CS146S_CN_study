---
title: "pstack：反 Slop 的工程纪律"
original: "pstack: the same skills I use every day to ship high quality code at Cursor"
week: "3"
slug: "w3-pstack"
source_url: "https://github.com/cursor/plugins/tree/main/pstack"
author: "poteto"
date: "2026"
kind: "开源项目"
coverage: "全文精译"
minutes: "12"
blurb: "不是让 AI 写得更多，而是写得更少、更可验证。23 个 playbook 把 Cursor 变成一支有工程纪律的团队。"
---

## 总结

pstack 的立场：速度不是目标，深度才是。先在一个 agent 上做深、做对、做到可验证，再谈并行。

- 目标不是最大化代码行数，而是写更少、更高质量的代码。
- 核心入口是 `/poteto-mode`：读取任务，匹配 23 个 playbook 之一，再按步骤调用其他 skill。
- 默认按模型强项分工：代码委派给 Grok，最难改动、写作和判断交给 Opus 5.5。
- playbook 覆盖调查、修 bug、性能、取证、功能、重构、原型、review、shipping、autonomous run、orchestrate 等。
- 核心哲学：先复现、再修；先测量、再优化；先证明、再宣布完成。

## 原文逐段对照翻译

> **翻译说明：**以下按原文顺序翻译核心理念、playbook、skills 和模型分工；完整安装命令与 23 个 playbook 的细节保留在原文。

### 为什么是 pstack

<div class="bilingual-pair">
<p class="src">There's a growing sense that AI writes too much slop code. I agree. I don't want to ship like a team of twenty slop artists. Throughput without quality is not a goal I aspire to. If you want to go fast, go deep first.</p>
<p class="dst">越来越多人觉得 AI 写了太多 slop code。我同意。我不想让团队像二十个 slop artist 一样出货。没有质量的吞吐量不是我的目标。想快，先做深。</p>
</div>

<div class="bilingual-pair">
<p class="src">pstack is my answer. These are the same skills I use every day to ship high quality code at Cursor. This turns cursor into a real engineering team. The goal is not to maximize LOC; in fact, it's the opposite. pstack helps you write less, but higher quality code.</p>
<p class="dst">pstack 是我的答案。这些是我在 Cursor 每天用来交付高质量代码的 skills。它把 Cursor 变成一支真正的工程团队。目标不是最大化代码行数，恰恰相反：pstack 帮你写得更少，但质量更高。</p>
</div>

<div class="bilingual-pair">
<p class="src">pstack gives you fearless parallelism. When you can go deep on one agent and trust it to write good, verifiable code, you can truly parallelize with confidence. Start multiple agents up with poteto-mode and trust that they'll apply rigorous engineering principles to their work.</p>
<p class="dst">pstack 给你“无所畏惧的并行”。当你能在一个 agent 上做深，并相信它写出可验证的好代码，你才能真正有信心地并行。开多个 agent，用 poteto-mode，相信它们会应用严格的工程原则。</p>
</div>

### `/poteto-mode`：23 个 playbook 的入口

<div class="bilingual-pair">
<p class="src">Use /poteto-mode at the start of a task. It reads your request, picks from a set of playbooks, and runs the other skills as the steps need them. When invoked it matches your task to a playbook and opens a todo list whose first items are its steps, copied in verbatim.</p>
<p class="dst">任务开始时用 `/poteto-mode`。它读取请求，从一组 playbook 里选一个，再在步骤需要时调用其他 skills。调用后，它把任务匹配到 playbook，并打开 todo list，把 playbook 的步骤逐字复制进去。</p>
</div>

<div class="bilingual-pair">
<p class="src">The 23 playbooks cover investigation, bug fix, perf, hillclimb, runtime forensics, trace forensics, feature, refactoring, prototype, visual parity, authoring a skill, eval, babysit, shipping, autonomous run, orchestrate, autopilot-full, autopilot-stack, session pickup, pause safely, multi-phase plan, worktree cleanup, and opening a PR.</p>
<p class="dst">23 个 playbook 覆盖：调查、修 bug、性能、hillclimb、运行时取证、trace 取证、功能、重构、原型、视觉对齐、编写 skill、eval、babysit、shipping、autonomous run、orchestrate、autopilot-full、autopilot-stack、接管会话、安全暂停、多阶段计划、worktree 清理、开 PR。</p>
</div>

<div class="bilingual-pair">
<p class="src">Examples: /poteto-mode this PR has a subtle bug where the scroll drifts every 750ms even when idle. Repro first, then fix and verify. Or: /poteto-mode I'm going to bed. Land the stack even if CI flakes. I want everything merged by morning.</p>
<p class="dst">例子：`/poteto-mode 这个 PR 有个微妙的 bug：即使 idle，滚动也每 750ms 漂移。先复现，再修并验证。` 或者：`/poteto-mode 我要睡了。即使 CI 抖动也把 stack land 掉，早上前全部合并。`</p>
</div>

### 专项 skills

<div class="bilingual-pair">
<p class="src">/how gives a walkthrough of how a subsystem works. /why discovers available MCPs and queries source control, issue tracker, docs, chat, infra observability, error tracking, and analytics. /blast-radius asks what else a small-looking change could break, with the one fact it's safe proven by running code, not asserted.</p>
<p class="dst">`/how` 讲清一个子系统怎么工作；`/why` 查询版本控制、issue tracker、文档、聊天、可观测性、错误追踪、分析等证据，解释为什么这样设计；`/blast-radius` 分析小改动可能破坏什么，并用运行代码证明“为什么安全”，而不是口头断言。</p>
</div>

<div class="bilingual-pair">
<p class="src">/architect settles caller usage, types, and module shape before writing code that crosses a function boundary. /arena runs N parallel attempts at the same thing, then grabs the best parts of each. /swarm runs N parallel workers across different slices, then aggregates one report.</p>
<p class="dst">`/architect` 在跨函数边界写代码前，先确定调用方、类型和模块形状；`/arena` 对同一任务做 N 个并行尝试，再挑最好的部分；`/swarm` 让 N 个 worker 跑不同切片，最后汇总一份报告。</p>
</div>

<div class="bilingual-pair">
<p class="src">/interrogate has different models try to break a diff, keeping only findings a run proves. /tdd writes the failing test first, then fixes it. /unslop removes AI tells from writing. /teach actually helps you understand a change or subsystem, not just get a summary.</p>
<p class="dst">`/interrogate` 让不同模型尝试攻破一个 diff，只保留被运行证明的发现；`/tdd` 先写失败测试再修；`/unslop` 清理 AI 味写作；`/teach` 帮你真正理解一个改动或子系统，而不只是摘要。</p>
</div>

### 模型分工

<div class="bilingual-pair">
<p class="src">Out of the box, the mode splits work by model strength: code delegates (feature, refactoring, bug fix, perf, hillclimb) go to grok, while the hardest changes, prose, and judgment go to opus 5.5. The default panel is opus 5.5 / grok. /setup-pstack changes any of it.</p>
<p class="dst">默认按模型强项分工：代码委派（feature、refactoring、bug fix、perf、hillclimb）给 Grok；最难的改动、写作和判断给 Opus 5.5。默认组合是 Opus 5.5 / Grok；`/setup-pstack` 可以改。</p>
</div>

<div class="bilingual-pair">
<p class="src">Every frontier model has strengths and weaknesses. Use any model with pstack. Many of my skills use multi-model workflows to take advantage of each model's unique strengths.</p>
<p class="dst">每个前沿模型都有强项和弱项。pstack 可以用任何模型；我的很多 skills 采用多模型工作流，利用各自的长处。</p>
</div>

### 怎么开始

<div class="bilingual-pair">
<p class="src">Two steps: run /setup-pstack, pick a reasoning budget, and choose which models you want; use /poteto-mode whenever you're doing anything that requires rigor. If you're stuck or unsure which skill fits, ask /poteto-help.</p>
<p class="dst">两步：运行 `/setup-pstack`，选 reasoning budget 和模型；做任何需要严谨的事时用 `/poteto-mode`。卡住或不知道用哪个 skill，就问 `/poteto-help`。</p>
</div>

## 学习者视角

### 关键收获

1. **反 slop 不是反 AI，而是反无验证的产出。** 所有 playbook 都围绕可复现、可测量、可证明。
2. **入口比工具列表重要。** 23 个 playbook 很多，但用户只需要记住 `/poteto-mode`。
3. **模型分工是成本与质量的平衡。** 不是所有任务都值得用最强模型。
4. **并行建立在信任上。** 先让一个 agent 做深，再复制这套纪律到多个 agent。
5. **“证明”是核心 artifact。** `/blast-radius` 要求用运行代码证明安全。

### 放回课程里看

pstack 是 Week 3 的工程化代表：skills 从“提示词集合”升级为“可路由、可组合、可验证的工作流系统”。它和 [Superpowers](w2-superpowers.html) 的区别是：Superpowers 更偏方法论，pstack 更偏日常工程 playbook + 模型分工。

### 一个反直觉点

pstack 的目标不是“让 agent 写更多代码”，而是“让 agent 写更少但更好的代码”。它甚至把“少写”当成质量指标。

## 拓展

### 思考题

1. 23 个 playbook 里，哪三个最适合你当前的工作？为什么？
2. 如果团队只用一种模型，pstack 的模型分工思想还适用吗？
3. “先复现再修”在什么情况下会被跳过？代价是什么？
4. `/blast-radius` 要求“用运行代码证明”，这和“让模型解释”有什么区别？

### 练习

为你自己的项目设计一个 `/mode` 入口：

- 列出 5 个最常用的 playbook；
- 为每个 playbook 写 3–5 个步骤；
- 指定每步需要调用的 skill；
- 设计一个“完成前必须证明”的检查。

### 接着读

- [Superpowers：完整开发方法论](w2-superpowers.html)
- [Matt Pocock's Skills：小型、可组合的工程技能](w3-matt-pocock-s-skills.html)
- [Steering Claude Code：技能、规则、hooks 的分工](w4-steering-claude-code.html)
