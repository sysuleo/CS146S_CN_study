---
title: "OpenSpec：用轻量规格把“做对的事”和“把事做对”分开"
original: "OpenSpec: The spec framework for building the right thing and building it right"
week: "2"
slug: "w2-openspec"
source_url: "https://openspec.dev"
author: "OpenSpec"
date: "2026"
kind: "产品文档"
coverage: "全文精译"
minutes: "5"
blurb: "一个轻量、可配置的规格框架：explore → propose → apply → verify → archive，让团队和 coding agent 围绕同一份规格协作。"
---

## 总结

OpenSpec 想解决的不是“代码怎么写”，而是**在写代码之前和之后，如何让所有人对“要做什么”拥有同一个版本的事实**。

- 规格不是一次性文档，而是团队和 coding agent 共同维护的当前共识。
- 工作流有五步：探索问题、提出变更、实现、验证、归档。
- 它强调两件事：先确认要做的东西是对的，再确认实现和规格一致。
- 规格层与具体 agent 解耦：今天用 Claude Code，明天换 Codex，规格仍然有效。

## 原文逐段对照翻译

> **翻译说明：**原文为产品说明页，以下按原文顺序逐段翻译；兼容性清单过长，正文中概括为“支持主流 agent/IDE”，完整名单保留在原文。

<div class="bilingual-pair">
<p class="src">The spec framework for building the right thing and building it right</p>
<p class="dst">一个用来“做对的事、并把事做对”的规格框架</p>
</div>

<div class="bilingual-pair">
<p class="src">Synopsis: OpenSpec is a lightweight and configurable framework for creating and managing software specifications.</p>
<p class="dst">概要：OpenSpec 是一个轻量、可配置的框架，用于创建和管理软件规格。</p>
</div>

<div class="bilingual-pair">
<p class="src">With OpenSpec, you capture what you want to build in a spec and keep your team and coding agents aligned as the work evolves. We help you refine the requirements, validate that they describe the right thing, and verify that the implementation matches.</p>
<p class="dst">使用 OpenSpec，你可以把“想构建什么”写进规格，并在工作推进过程中让团队和 coding agent 始终对齐。它帮助你细化需求，确认需求描述的是正确的东西，并验证实现是否与规格一致。</p>
</div>

<div class="bilingual-pair">
<p class="src">In essence, OpenSpec helps you build the right thing and build it right.</p>
<p class="dst">本质上，OpenSpec 帮你做到两件事：构建正确的东西，并把它正确地构建出来。</p>
</div>

<div class="bilingual-pair">
<p class="src">Installation: OpenSpec can be installed and used with a wide range of coding agents and IDEs, including Claude Code, Codex, Cursor, GitHub Copilot, Gemini CLI, OpenCode, and many more.</p>
<p class="dst">安装：OpenSpec 支持大量 coding agent 和 IDE，包括 Claude Code、Codex、Cursor、GitHub Copilot、Gemini CLI、OpenCode 等；完整兼容列表见原文。</p>
</div>

<div class="bilingual-pair">
<p class="src">Workflow: /opsx:explore maps the problem and helps you understand the codebase. /opsx:propose drafts proposal.md, specs/, design.md, and tasks.md. /opsx:apply implements tasks from the specification. /opsx:verify checks that the implementation matches the spec. /opsx:archive archives completed changes.</p>
<p class="dst">工作流：`/opsx:explore` 梳理问题、理解代码库；`/opsx:propose` 起草 proposal.md、specs/、design.md、tasks.md；`/opsx:apply` 按规格实现任务；`/opsx:verify` 检查实现是否符合规格；`/opsx:archive` 归档已完成的变更。</p>
</div>

<div class="bilingual-pair">
<p class="src">Each step leaves an inspectable artifact: a proposal for why, specs for what, design for how, tasks for the execution plan, and verification for how correctness is proven.</p>
<p class="dst">每一步都会留下可检查的产物：proposal 说明“为什么做”，specs 说明“做成什么样”，design 说明“怎么做”，tasks 说明“分几步做”，verify 说明“怎么证明做对了”。</p>
</div>

## 学习者视角

### 关键收获

1. **规格是共识，不是文档负担。** 它的价值在于让团队和 agent 对“当前要做什么”有同一份事实。
2. **验证是双向的。** 既要验证实现符合规格，也要在更早的阶段验证规格本身描述的是正确的东西。
3. **归档让规格库保持新鲜。** 完成的变更要从“进行中”变成“历史”，否则规格会腐烂。
4. **规格层应该与 agent 解耦。** 工具会换，规格和变更记录应该留下。

### 放回课程里看

OpenSpec 是 Week 2 “spec-driven development” 的一个具体实现。它和 [Superpowers](w2-superpowers.html) 是两种风格：Superpowers 把方法写成自动触发的 skills，OpenSpec 把方法写成显式的规格工作流。

### 一个反直觉点

很多人认为规格会拖慢 agent。OpenSpec 的假设相反：**没有规格，agent 只会更快地做错事，返工更慢。**

## 拓展

### 思考题

1. 你的项目里，哪些变更值得写规格，哪些不值得？判断标准是什么？
2. 如果 agent 实现了规格，但规格本身是错的，谁来负责？
3. `verify` 应该由人做、agent 做，还是两者都做？

### 练习

选一个最近做过的小功能，补一份 OpenSpec 风格的变更包：

- `proposal.md`：为什么做；
- `specs/`：行为规格；
- `design.md`：关键设计取舍；
- `tasks.md`：可执行任务；
- 一条 verify 清单。

### 接着读

- [Superpowers：用 skills 强制执行开发方法](w2-superpowers.html)
- [Matt Pocock's Skills：用 grill 和共享语言对齐需求](w3-matt-pocock-s-skills.html)
- [AGENTS.md：给 agent 的项目简报](w4-agents-md-factory-docs.html)
