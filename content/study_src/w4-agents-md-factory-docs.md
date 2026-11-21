---
title: "AGENTS.md：给 Agent 的一份项目简报"
original: "AGENTS.md: Give Droid durable project instructions, commands, and guardrails"
week: "4"
slug: "w4-agents-md-factory-docs"
source_url: "https://docs.factory.com/harness/agents-md"
author: "Factory"
date: "2026"
kind: "产品文档"
coverage: "全文精译"
minutes: "9"
blurb: "把安装、运行、测试、边界和完成标准写进 AGENTS.md，让每个 agent 会话都从同一份项目简报开始。"
---

## 总结

AGENTS.md 是 agent 每次会话都要带着的“项目简报”：怎么安装、怎么运行、怎么测试、怎么改、怎么验证，以及哪些边界不能碰。

- 在仓库根目录建一个 `AGENTS.md`，只放每次会话都需要的信息。
- 命令优先：安装、开发、测试、类型检查、lint、build，写精确命令。
- 写约定和安全规则：目录结构、生成文件、安全边界、所有权、完成前的证明。
- 规则要具体、可验证，不要写“小心一点”“确保一切正常”。
- 用最窄的持久化表面：`AGENTS.md` 放常驻规则，`SKILL.md` 放按需流程。
- 嵌套 `AGENTS.md` 只在子目录确实有不同规则时使用。
- 上下文有预算：初始加载上限 80,000 字符，动态发现每次工具调用 40,000 字符。

## 原文逐段对照翻译

> **翻译说明：**以下按原文顺序逐段翻译，保留全部规则、示例和限制；中文以自然、准确为目标。

### AGENTS.md 是干什么的

<div class="bilingual-pair">
<p class="src">AGENTS.md gives Droid the project briefing it should carry into every session: how to install, run, test, edit, verify, and stay inside your repository's boundaries. Use it for guidance that should be loaded before Droid writes code. Keep it short, specific, and easy to verify.</p>
<p class="dst">AGENTS.md 给 Droid 一份每次会话都要带着的项目简报：如何安装、运行、测试、编辑、验证，以及如何待在仓库边界内。它适合放“写代码之前就要加载”的指导。要求是：短、具体、容易验证。</p>
</div>

### 创建第一份 AGENTS.md

<div class="bilingual-pair">
<p class="src">Create one root file. Add AGENTS.md at the repository root. Start with one file, then add nested files only where a package, app, or service needs different rules.</p>
<p class="dst">先在仓库根目录建一个文件。从一开始只建一个，只有 package、app 或 service 确实需要不同规则时，才加嵌套文件。</p>
</div>

<div class="bilingual-pair">
<p class="src">Put commands first. List the exact install, development, test, type check, lint, and build commands Droid should run. Add flags or package filters when broad commands are too expensive.</p>
<p class="dst">命令优先。列出精确的安装、开发、测试、类型检查、lint、build 命令。宽泛命令太贵时，加 flag 或 package filter。</p>
</div>

<div class="bilingual-pair">
<p class="src">Add conventions and safety rules. Capture repository layout, generated-file rules, security boundaries, ownership boundaries, and required proof before Droid calls work finished.</p>
<p class="dst">补充约定和安全规则：仓库布局、生成文件规则、安全边界、所有权边界，以及完成前必须提供的证明。</p>
</div>

<div class="bilingual-pair">
<p class="src">Commit it with the project. Project instructions belong in git so every teammate and automation session gets the same operating context.</p>
<p class="dst">和项目一起提交。项目指令属于 git，这样每个同事和自动化会话都拿到同一份操作上下文。</p>
</div>

### 一个示例

<div class="bilingual-pair">
<p class="src">A good AGENTS.md starts with exact commands, a short project layout, coding conventions, and a verification checklist. For example: install with pnpm install, start with pnpm dev, test with pnpm test, typecheck with pnpm typecheck, lint with pnpm lint. Then describe what app/, components/, and lib/ contain, and require tests, typecheck, and lint before calling work finished.</p>
<p class="dst">一份好的 AGENTS.md 从精确命令、简短项目布局、编码约定和验证清单开始。例如：用 `pnpm install` 安装、`pnpm dev` 启动、`pnpm test` 测试、`pnpm typecheck` 类型检查、`pnpm lint` 检查。然后说明 `app/`、`components/`、`lib/` 各放什么，并要求完成前跑测试、类型检查和 lint。</p>
</div>

<div class="bilingual-pair">
<p class="src">Keep human onboarding, screenshots, and contributor background in README.md. Put Droid-specific commands, guardrails, and completion criteria in AGENTS.md.</p>
<p class="dst">人类 onboarding、截图、贡献者背景放 README.md；Droid 专用命令、护栏和完成标准放 AGENTS.md。</p>
</div>

### 应该包含什么

<div class="bilingual-pair">
<p class="src">A good AGENTS.md covers: a short project overview; exact commands for install, run, test, lint, type check, build, and regeneration; a repository map; project-specific conventions that are not obvious from code; testing rules; generated files and how to regenerate them; security rules; and PR expectations.</p>
<p class="dst">好的 AGENTS.md 覆盖：简短项目概览；安装、运行、测试、lint、类型检查、build、重新生成的精确命令；仓库地图；代码里不明显的项目约定；测试规则；生成文件及重新生成方式；安全规则；PR 期望。</p>
</div>

<div class="bilingual-pair">
<p class="src">Prefer concrete rules that change how Droid works: run pnpm test -- path/to/file.test.ts for focused changes; run pnpm test before completing broad refactors; add a regression test for every bug fix when practical. Avoid vague rules that cannot be checked: be careful; make sure everything works.</p>
<p class="dst">优先写能改变行为的规则：局部改动跑 `pnpm test -- path/to/file.test.ts`；大重构完成前跑 `pnpm test`；修 bug 尽量加回归测试。避免无法检查的模糊规则：“小心一点”“确保一切正常”。</p>
</div>

### 选择正确的指令表面

<div class="bilingual-pair">
<p class="src">Use the narrowest durable surface for the job. AGENTS.md and compatible names are for always-on coding instructions, commands, repository conventions, and safety rules. DESIGN.md is for design-system, UX, visual, and interaction guidance. SKILL.md is for reusable workflows, checklists, or domain expertise that should load only when relevant.</p>
<p class="dst">用最窄的持久化表面。`AGENTS.md` 及兼容名放常驻编码指令、命令、仓库约定和安全规则；`DESIGN.md` 放设计系统、UX、视觉和交互指导；`SKILL.md` 放可复用工作流、检查清单或领域知识，只在相关时加载。</p>
</div>

<div class="bilingual-pair">
<p class="src">.factory/commands/* are simple user-invoked prompt or executable shortcuts. .factory/settings.json is for Droid preferences, defaults, and policy settings, parsed as configuration rather than prose. Do not paste long runbooks into AGENTS.md. Link to the source of truth, or move reusable procedures into skills.</p>
<p class="dst">`.factory/commands/*` 放用户调用的 prompt 或可执行快捷方式；`.factory/settings.json` 放偏好、默认值和策略，作为配置解析，而不是散文指令。不要把长 runbook 塞进 AGENTS.md；要么链接到源头，要么把可复用流程移到 skill。</p>
</div>

### 发现与优先级

<div class="bilingual-pair">
<p class="src">When a git root is present, Droid searches from the current working directory up to the git root. At each level, it checks the directory itself and these context directories: .factory/, .agents/, .agent/. Droid also checks personal instruction directories in your home folder: ~/.factory/, ~/.agents/, ~/.agent/.</p>
<p class="dst">有 git root 时，Droid 从当前工作目录向上搜索到 git root。每层检查目录自身和 `.factory/`、`.agents/`、`.agent/`。它也会检查 home 下的个人指令目录：`~/.factory/`、`~/.agents/`、`~/.agent/`。</p>
</div>

<div class="bilingual-pair">
<p class="src">When multiple instruction files apply: the current user request takes priority over standing instructions; nested project files refine root project files for a specific directory tree; project files should override personal defaults; personal files should describe preferences, not requirements that fight repository rules.</p>
<p class="dst">多个指令文件同时生效时：当前用户请求优先于常驻指令；嵌套项目文件细化根项目文件；项目文件覆盖个人默认值；个人文件描述偏好，不应和仓库规则打架。</p>
</div>

### 兼容文件名

<div class="bilingual-pair">
<p class="src">Use AGENTS.md for new guidance. Droid also reads compatible filenames so existing instruction files from other coding tools keep working: agents.md, Agents.md, CLAUDE.md, Claude.md. This is a compatibility set, not a setup checklist. Do not create every file. Duplicating rules across supported filenames spends context without adding signal.</p>
<p class="dst">新指导用 `AGENTS.md`。Droid 也读取兼容名：`agents.md`、`Agents.md`、`CLAUDE.md`、`Claude.md`。这是兼容集合，不是清单；不要创建所有文件。跨文件名重复规则只会浪费上下文，不增加信号。</p>
</div>

### 嵌套指令

<div class="bilingual-pair">
<p class="src">Nested files are useful when a directory tree has different commands, conventions, generated assets, or ownership rules. Use nested files for real differences: a package uses another package manager or test runner; a service has generated code that must not be edited by hand; a frontend area has design-system rules; a deployment or migration path requires extra approval. Do not use nested files to repeat root rules.</p>
<p class="dst">目录树确实有不同命令、约定、生成资源或所有权规则时，嵌套文件才有用。真实差异包括：package 用不同包管理器或测试 runner；service 有不能手改的生成代码；前端区域有设计系统规则；部署/迁移需要额外审批。不要用嵌套文件重复根规则。</p>
</div>

<div class="bilingual-pair">
<p class="src">Reading, editing, listing, or searching files in a directory triggers discovery; shell commands run through Execute do not. For example, editing apps/web/src/page.tsx loads apps/web/AGENTS.md.</p>
<p class="dst">读、编辑、列目录、搜索文件会触发发现；通过 Execute 跑的 shell 命令不会。例如编辑 `apps/web/src/page.tsx` 会加载 `apps/web/AGENTS.md`。</p>
</div>

### 上下文预算

<div class="bilingual-pair">
<p class="src">Instruction files count against the session context. Keep the top of each file dense with the rules Droid most needs. The initial AGENTS-style guideline load limit is 80,000 characters; dynamic guideline discovery per tool call is 40,000 characters. These are caps, not targets. Smaller files are usually better.</p>
<p class="dst">指令文件计入会话上下文。把最重要的规则放在文件顶部。初始 AGENTS 风格指导加载上限 80,000 字符；动态发现每次工具调用 40,000 字符。这是上限，不是目标；更小的文件通常更好。</p>
</div>

### 根模板与嵌套模板

<div class="bilingual-pair">
<p class="src">A root template should include: what the project is; install, run, test, typecheck, lint, and build commands; project layout; conventions; verification steps; and safety rules. A nested template should include local commands, local conventions, and local verification, and state that the root AGENTS.md applies unless this file gives a more specific rule.</p>
<p class="dst">根模板包括：项目是什么；安装、运行、测试、类型检查、lint、build 命令；项目布局；约定；验证步骤；安全规则。嵌套模板包括本地命令、本地约定、本地验证，并说明除非本文件给出更具体规则，否则根 AGENTS.md 仍然适用。</p>
</div>

### 应该避免什么

<div class="bilingual-pair">
<p class="src">Do not use AGENTS.md as a dumping ground. Avoid secrets, credentials, private tokens, or private host names; full copies of long docs that already live elsewhere; stale directory inventories; personal preferences that conflict with project rules; temporary task notes that belong in an issue, PR, or spec; instructions to skip validation without a narrow, explicit reason.</p>
<p class="dst">不要把 AGENTS.md 当垃圾场。避免：密钥、凭证、私有 token、私有主机名；已在别处的长文档全文；会漂移的目录清单；和项目规则冲突的个人偏好；临时任务笔记；没有明确理由就跳过验证的指令。</p>
</div>

<div class="bilingual-pair">
<p class="src">If guidance is useful for one workflow, make it a skill. If it is useful for one project area, put it in a nested AGENTS.md.</p>
<p class="dst">如果指导只对一个工作流有用，做成 skill；如果只对一个项目区域有用，放嵌套 AGENTS.md。</p>
</div>

## 学习者视角

### 关键收获

1. **AGENTS.md 是“常驻项目简报”，不是知识库。** 只放每次会话都需要的规则。
2. **命令优先。** agent 最需要知道的是“怎么跑起来、怎么验证”。
3. **具体可验证 > 模糊正确。** “确保一切正常”没有行为价值。
4. **用最窄的表面。** 常驻规则、按需流程、命令、配置，各有位置。
5. **上下文预算真实存在。** 80k/40k 是上限，不是目标；小文件更好。

### 放回课程里看

这篇是 Week 4 的基础材料。它和 [Writing a Good CLAUDE.md](w4-writing-a-good-claude-md.html) 讲同一件事的不同侧面：一个讲结构与表面，一个讲“少即是多”。

### 一个反直觉点

很多人把 AGENTS.md 写成“项目百科”。官方建议相反：**它是给 agent 的操作简报，不是给人看的永久文档。** 描述性内容往往不改变 agent 行为。

## 拓展

### 思考题

1. 你的 AGENTS.md 里，有多少行是“描述项目”，有多少行是“改变行为”？
2. 哪些规则应该从根文件移到嵌套文件或 skill？
3. 如果 AGENTS.md 超过 300 行，你会先删什么？
4. 为什么“跨文件名重复规则”是浪费上下文？

### 练习

审计你的 AGENTS.md：

- 标出每条规则属于“命令 / 布局 / 约定 / 安全 / 验证 / PR”；
- 删除所有无法验证的规则；
- 把只对某个目录有用的规则移到嵌套文件；
- 把只对某个工作流有用的规则移到 skill；
- 把最重要的 10 条放到文件顶部。

### 接着读

- [Writing a Good CLAUDE.md：少即是多](w4-writing-a-good-claude-md.html)
- [Steering Claude Code：七种指令机制怎么选](w4-steering-claude-code.html)
- [Making Ergonomic Repositories：把仓库变成 agent 原生](w5-making-ergonomic-repositories.html)
