---
title: "分层代码审查：让 AI 读大部分代码，人只管风险"
original: "Layered Code Review and Risk-Based Human Oversight"
week: "6"
slug: "w6-layered-code-review-and-risk-based-human-oversight"
source_url: "https://x.com/addyosmani/status/2114604912520921136"
author: "Claude Code 团队"
date: "2026"
kind: "工程实践"
coverage: "全文精译"
minutes: "14"
blurb: "Claude 写了约 90% 的 Claude Code 代码。合并 PR 翻倍、回滚率下降 40%，他们怎么审查？"
---

## 总结

Claude 写了 Claude Code 约 90% 的代码。团队没有放弃代码审查，而是把大部分“读代码”自动化，把人的注意力留给风险。

- 审查目标不是“有人读过吗”，而是“这个改动可能出什么问题，哪种检查能抓住它”。
- 六层检查 + 回滚：pre-PR 验证、每 PR AI review、可阻断安全审查、自动检查、风险分级人工审批、merge queue/feature flag/分批发布。
- Pre-PR 验证能把输出质量提高 2–3 倍。
- 每个 PR 先过 Claude review；发现由多个 agent 并行找、投票确认、过滤风格噪音。
- 人工审批按风险分级；agent 审批不算人工审批；一个 approval 只对一个 commit 有效。
- 审查必须收敛：曾有一个 PR 在 agent 作者和 agent reviewer 之间循环 50 多次。
- 人的价值在“该不该做、架构、危险代码、验证证明、承担责任”。

## 原文逐段对照翻译

> **翻译说明：**以下按原文顺序逐段翻译，保留六层流程、指标和实施建议；中文以自然、准确为目标。

<figure class="article-figure">
<a href="https://pbs.twimg.com/media/HVgF5M4bIAAvLxh?format=webp&name=large" target="_blank" rel="noopener noreferrer"><img src="https://pbs.twimg.com/media/HVgF5M4bIAAvLxh?format=webp&name=large" alt="Layered code review cover"></a>
<figcaption>原文封面图（X 原图）：Layered Code Review and Risk-Based Human Oversight。</figcaption>
</figure>

### 重新思考审查目标

<div class="bilingual-pair">
<p class="src">We previously mentioned that Claude writes about 90 percent of the code for Claude Code. So how do we do code review at this scale? Between June and September, we saw more than double the number of pull requests merged, while the share of pull requests that had to be reverted fell by more than 40 percent.</p>
<p class="dst">我们之前提到，Claude 写了 Claude Code 约 90% 的代码。那这个规模下怎么做代码审查？6 月到 9 月，合并的 PR 数量翻倍以上，而需要回滚的 PR 比例下降 40% 以上。</p>
</div>

<div class="bilingual-pair">
<p class="src">We didn't stop doing code review. Instead, we've automated the majority of reading and tuned it to optimize for human time and effort. We've also made significant investments into improving the speed and ease of reverting mistakes.</p>
<p class="dst">我们没有停止代码审查，而是把大部分“阅读”自动化，并围绕人的时间和精力做优化。同时，我们投入大量精力提升回滚的速度和便利性。</p>
</div>

<div class="bilingual-pair">
<p class="src">Code review serves two purposes: detect and correct bugs before they ship, and develop a shared understanding of the codebase. We view "did someone read the code?" as an imprecise measure of "what could go wrong with this change, and what check—automated or human—is the right one to catch it?"</p>
<p class="dst">代码审查有两个目的：发布前发现并修复 bug；建立对代码库的共同理解。我们把“有人读过代码吗”换成更精确的问题：**这个改动可能出什么问题，哪种检查——自动或人工——能抓住它？**</p>
</div>

<div class="bilingual-pair">
<p class="src">Traditionally, code review was a check performed after the fact. Instead, we've integrated code review into the workflow. It's more like a spellcheck that you continuously do while writing. The majority of changes have already been reviewed and corrected by Claude before a human is asked to take a look.</p>
<p class="dst">传统审查是事后检查；我们把审查嵌入工作流，更像写作时持续做的拼写检查。大多数改动在人类看之前，已经被 Claude 审查和修正过至少一次。</p>
</div>

### 人的时间是双向成本

<div class="bilingual-pair">
<p class="src">Human time is a dual-sided cost. Not only do we count the time people spend doing code review, but also the time that they spend fixing bugs that are introduced by bad code. If we reduce the first without reducing the second, we're not really saving human time.</p>
<p class="dst">人的时间是双向成本：既包括做审查的时间，也包括修坏代码引入的 bug 的时间。如果只减少前者、不减少后者，并没有真正节省人的时间。</p>
</div>

<div class="bilingual-pair">
<p class="src">Our goal is that the majority of pull requests should merge with a maximum of one person in the loop, without an increase in reverts or incidents. We track median human approvals per PR, human comments, and how long a PR waits on a person. Revert and incident rates are guardrails.</p>
<p class="dst">目标是大多数 PR 最多一个人参与就能合并，同时不增加回滚或事故。我们跟踪每个 PR 的人工 approval 中位数、人工评论数、PR 等待人的时间；回滚率和事故率作为护栏。</p>
</div>

### 六层检查 + 回滚

<div class="bilingual-pair">
<p class="src">Layer 1: Pre-PR verification. Most of our review is done before we create a PR. We ask Claude to do something runnable, such as running tests, the build, or comparing a screenshot to the design. Instead of saying the task is done, we ask it to show us the result. Then a subagent reviews the diff with fresh context.</p>
<p class="dst">第 1 层：Pre-PR 验证。大多数审查发生在创建 PR 之前。让 Claude 做可运行的事：跑测试、build、把截图和设计对比。不要让它说“完成了”，要它展示结果。然后一个 fresh context 的 subagent 审查 diff。</p>
</div>

<div class="bilingual-pair">
<p class="src">Boris Cherny estimates that a verification process improves the quality of Claude's output by a factor of two to three. The verification process can be a bash command, a test suite, or testing the app in a browser or phone simulator.</p>
<p class="dst">Boris Cherny 估计，验证流程能把 Claude 输出质量提高 2–3 倍。验证可以是一条 bash 命令、一套测试，或在浏览器/手机模拟器里测试 app。</p>
</div>

<div class="bilingual-pair">
<p class="src">If the automated reviewer is consistently flagging the same issue, we fix it at the source—via the skill itself, a lint rule, or updating CLAUDE.md and REVIEW.md. CLAUDE.md gives Claude context about the project; REVIEW.md tells the reviewer what matters in that part of the code.</p>
<p class="dst">如果自动 reviewer 反复标同一个问题，就从源头修：改 skill、加 lint rule，或更新 `CLAUDE.md` / `REVIEW.md`。CLAUDE.md 给 Claude 项目上下文；REVIEW.md 告诉 reviewer 这部分代码什么最重要。</p>
</div>

<div class="bilingual-pair">
<p class="src">Layer 2: AI review on every pull request. Every PR receives a Claude review before a human review. The diff is analyzed against the entire codebase and the intent of the PR. It checks that the change addresses the issue, fits the larger system, and does not break other parts of the codebase. For a bug fix, it tries to find the root cause.</p>
<p class="dst">第 2 层：每个 PR 的 AI review。每个 PR 在人工 review 前先过 Claude。diff 会和整个代码库、PR 意图一起分析，检查改动是否解决问题、是否适配系统、是否破坏其他部分；如果是 bug fix，还要找根因。</p>
</div>

<div class="bilingual-pair">
<p class="src">Findings are vetted by multiple other agents: multiple agents run in parallel to hunt for bugs; a separate vote decides if a finding is valid; style/diagnostics/cleanup findings are filtered out; remaining findings are ordered by severity and marked Important, Nit, or Pre-existing.</p>
<p class="dst">发现由多个 agent 并行寻找、投票确认；风格/诊断/清理类 finding 被过滤；剩余 finding 按严重级别排序，标记为 Important、Nit、Pre-existing。</p>
</div>

<div class="bilingual-pair">
<p class="src">Layer 3: Security review that can block. No PR can be merged while there is an open finding from code review or security review. The author can fix it or close the thread with a short reason. A finding will be auto-closed if a subsequent commit addresses it.</p>
<p class="dst">第 3 层：可阻断的安全审查。只要代码审查或安全审查还有 open finding，PR 就不能合并。作者可以修，或带简短理由关闭 thread；后续 commit 解决问题时自动关闭。</p>
</div>

<div class="bilingual-pair">
<p class="src">Layer 4: Automated checks that block. Standard checks include lint, type checks, tests on all platforms, and build. A typical CLI PR can have dozens of checks run before anyone looks at it. The PR template asks how the change was tested and how to revert it.</p>
<p class="dst">第 4 层：可阻断的自动检查。标准检查包括 lint、类型检查、所有平台测试、build。一个典型 CLI PR 在任何人看之前可能跑几十个检查。PR 模板要求说明怎么测试、怎么回滚。</p>
</div>

<div class="bilingual-pair">
<p class="src">Layer 5: Human approval, scaled by risk. The tier is determined by the change, not the author. Some paths always require another approval: anything marked sensitive by owners, and any CI workflow file. Only authors on the trusted list receive relaxed review requirements. Agent approvals don't count as human approvals.</p>
<p class="dst">第 5 层：按风险分级的人工审批。级别由改动决定，不是作者。敏感路径、CI workflow 文件永远需要额外 approval；只有 trusted list 上的作者享受宽松审查；agent approval 不算人工 approval。</p>
</div>

<div class="bilingual-pair">
<p class="src">A PR approval is only good for one commit. If a new commit lands that can't be trusted, the PR must be reapproved. Layer 6: Merge queue, feature flags, and staged rollouts. The merge queue ensures checks run on main with the change applied, preventing two successful PRs from merging into a broken main.</p>
<p class="dst">一个 approval 只对一个 commit 有效；新 commit 不可信时必须重新 approval。第 6 层：merge queue、feature flag、分批发布。Merge queue 确保检查在 main 上、应用改动后跑一遍，避免两个成功 PR 合出 broken main。</p>
</div>

<div class="bilingual-pair">
<p class="src">Layer 7: Fast feedback and rollback. Some bad merges will inevitably get through. Feature flags can be disabled without deploying. Claude Code runs a weekly on-call rotation, and incident reviews ask which layer should have caught the problem.</p>
<p class="dst">第 7 层：快速反馈与回滚。总会有坏 merge 漏过。Feature flag 可以不开新版本就关闭；Claude Code 有每周 on-call；事故复盘会问“哪一层本该抓住”。</p>
</div>

<figure class="article-figure">
<a href="https://pbs.twimg.com/media/HVf9yKZbwAAQXG9.jpg" target="_blank" rel="noopener noreferrer"><img src="https://pbs.twimg.com/media/HVf9yKZbwAAQXG9.jpg" alt="Code review journey 1"></a>
<figcaption>原文图（X 原图）：一个改动从作者环境到生产的审查路径 1。</figcaption>
</figure>

<figure class="article-figure">
<a href="https://pbs.twimg.com/media/HVf-M9yawAAIxYF.jpg" target="_blank" rel="noopener noreferrer"><img src="https://pbs.twimg.com/media/HVf-M9yawAAIxYF.jpg" alt="Code review journey 2"></a>
<figcaption>原文图（X 原图）：审查路径 2。</figcaption>
</figure>

<figure class="article-figure">
<a href="https://pbs.twimg.com/media/HVf_D--bcAAPXY-.jpg" target="_blank" rel="noopener noreferrer"><img src="https://pbs.twimg.com/media/HVf_D--bcAAPXY-.jpg" alt="Code review journey 3"></a>
<figcaption>原文图（X 原图）：审查路径 3。</figcaption>
</figure>

### 让 reviewer 变好

<div class="bilingual-pair">
<p class="src">We use incidents as an evaluation metric. The team collected incident-causing PRs, their fix-forwards and reverts, and had engineers verify each bug. The review system is evaluated daily against this collection. Every incident adds to the collection.</p>
<p class="dst">我们用事故做评估集：收集导致事故的 PR、fix-forward、revert，让工程师验证每个 bug；review 系统每天对这套集合评估；每次事故都加入集合。</p>
</div>

<div class="bilingual-pair">
<p class="src">To measure noise, we observe how humans react to review comments: fixed, rejected, clarified as intentional, or decided it didn't matter. We also run the review system on known-clean PRs and observe false positives.</p>
<p class="dst">衡量噪音要看人对评论的反应：修了、拒绝、澄清为有意、认为不重要。还会在已知干净的 PR 上跑，观察误报。</p>
</div>

<div class="bilingual-pair">
<p class="src">The review process must converge. We observed one PR in our CLI project cycle more than fifty times overnight due to back-and-forth between the agent author and agent reviewer. When we ran git blame on what the review system kept flagging, about 59% was code that had been there since its first pass.</p>
<p class="dst">审查必须收敛。我们观察到一个 CLI PR 过夜循环 50 多次，因为 agent 作者和 agent reviewer 来回拉扯。对反复被标记的代码做 `git blame`，约 59% 是第一次 review 就存在的旧代码。</p>
</div>

<div class="bilingual-pair">
<p class="src">We updated re-review to: limit the number of cycles; after three cycles ask the author to re-evaluate the approach; limit re-review to just the new diff after initial cycles; specify the class of bugs so the author can correct all of them; avoid re-reporting issues already observed.</p>
<p class="dst">我们改进了 re-review：限制循环次数；3 轮后要求作者重新评估方案；初始轮次后只 review 新 diff；指定 bug 类别让作者一次修完；避免重复报告已观察的问题。</p>
</div>

<figure class="article-figure">
<a href="https://pbs.twimg.com/media/HVf_nM4aIAAKyCq.jpg" target="_blank" rel="noopener noreferrer"><img src="https://pbs.twimg.com/media/HVf_nM4aIAAKyCq.jpg" alt="Reviewer improvement 1"></a>
<figcaption>原文图（X 原图）：如何让 reviewer 变好 1。</figcaption>
</figure>

<figure class="article-figure">
<a href="https://pbs.twimg.com/media/HVgAB3aaYAApPEZ.jpg" target="_blank" rel="noopener noreferrer"><img src="https://pbs.twimg.com/media/HVgAB3aaYAApPEZ.jpg" alt="Reviewer improvement 2"></a>
<figcaption>原文图（X 原图）：如何让 reviewer 变好 2。</figcaption>
</figure>

### 人在回路里

<div class="bilingual-pair">
<p class="src">Human reviewers are still essential for: deciding whether to build something at all; auditing dangerous code such as billing, auto-updater, and CI workflows; architecture review; verifying proofs; and taking responsibility. A person answers for every change that ships, whoever typed it.</p>
<p class="dst">人类 reviewer 仍然不可替代：决定“该不该建”；审计计费、auto-updater、CI workflow 等危险代码；架构审查；验证证明；承担责任。每个上线的改动都要有人负责，不管是谁敲的。</p>
</div>

<div class="bilingual-pair">
<p class="src">If the bulk of reading is done by machines, what becomes the way to learn the codebase? We don't have a formal mechanism. When anyone wants to learn a piece of the codebase, they ask Claude to generate an explainer about that exact slice. It only takes a few minutes and is always up to date.</p>
<p class="dst">如果大部分阅读由机器完成，人怎么学习代码库？我们没有正式机制。想学某块代码时，让 Claude 生成针对该切片的 explainer，几分钟就好，而且总是最新。</p>
</div>

<div class="bilingual-pair">
<p class="src">"You land it, you own it." If you merge a small or medium change and something goes wrong, the general expectation is that you fix it yourself. Small changes are easy to review and revert; everything can be reverted; blast radius sets the bar; regressions are surfaced quickly by telemetry.</p>
<p class="dst">“你 land，你 own。”合并小/中改动后出问题，通常你自己修。小改动容易 review 和回滚；一切可回滚；blast radius 决定审查门槛；回归会被 telemetry 快速暴露。</p>
</div>

<figure class="article-figure">
<a href="https://pbs.twimg.com/media/HVgAZymawAAx2IG.jpg" target="_blank" rel="noopener noreferrer"><img src="https://pbs.twimg.com/media/HVgAZymawAAx2IG.jpg" alt="Team context"></a>
<figcaption>原文图（X 原图）：团队如何学习代码库。</figcaption>
</figure>

### 怎么落地

<div class="bilingual-pair">
<p class="src">Before the pull request: give the agent a checklist of checks it can run; set up formatters and linters via hooks; run /code-review and /security-review locally; create a REVIEW.md and track recurring review issues. On every PR: enforce CI, update the PR template with Testing, Risk, and How to revert.</p>
<p class="dst">PR 之前：给 agent 可运行的检查清单；用 hooks 跑 formatter/linter；本地跑 `/code-review` 和 `/security-review`；建 `REVIEW.md` 跟踪反复问题。每个 PR：强制 CI；模板加 Testing、Risk、How to revert。</p>
</div>

<div class="bilingual-pair">
<p class="src">Approval: define risk levels by change, not author; start strict; reserve lenient paths for trusted authors; bot approvals cannot satisfy required approval; dismiss approvals when new commits are pushed; designate humans for auth, billing, CI, release workflows, and installers.</p>
<p class="dst">Approval：按改动而非作者定义风险级别；先严格；宽松路径只给 trusted authors；bot approval 不能替代 required approval；新 commit 要 dismiss approval；auth、billing、CI、release、installer 由人审批。</p>
</div>

<div class="bilingual-pair">
<p class="src">Merging and post-merge: set up a merge queue; experiment with feature flags; launch to internal users first; roll out in stages; create a one-step revert mechanism; build evals by logging incidents and reverts; rescore the reviewer whenever you change prompts, tools, or model.</p>
<p class="dst">合并后：merge queue；feature flags；先内部用户；分批发布；一键回滚；用事故/revert 建 eval 集；每次改 prompt/tool/model 都重新评分 reviewer。</p>
</div>

## 学习者视角

### 关键收获

1. **审查的目标是风险匹配，不是“读过”。** 人类注意力应该花在高风险处。
2. **验证流程是质量杠杆。** 让 agent 展示结果而不是声称完成，能提升 2–3 倍质量。
3. **Agent 审查会制造噪音和循环。** 必须有多 agent 投票、过滤、收敛机制。
4. **Agent approval 不能替代人类责任。** 责任必须落到一个人。
5. **回滚能力是审查系统的一部分。** feature flag、revert、merge queue 让快速修错成为可能。
6. **人的价值转向判断和证明。** 该不该做、架构、危险代码、验证证据。

### 放回课程里看

这篇是 Week 6 的核心：它展示“agent 写大部分代码”之后，审查系统如何重新设计。它和 [Coordinating Specialist Review Agents](w6-coordinating-specialist-review-agents-at-scale.html) 是同一问题的两种实现：一个讲 Anthropic 内部流程，一个讲 Cloudflare 的编排架构。

### 一个反直觉点

他们发现 review 系统反复标记的代码中，约 59% 是第一次 review 就存在的旧代码。多轮 review 往往不是在发现新 bug，而是在反复找旧问题。**审查必须收敛。**

## 拓展

### 思考题

1. 你的团队现在哪一层最薄弱？
2. 如果 agent 作者和 agent reviewer 循环，你会用什么规则强制收敛？
3. 哪些改动必须人类审批？能否用“改动风险”而不是“作者级别”来定义？
4. “你 land，你 own”在你的团队文化里成立吗？

### 练习

为一个 agent 参与开发的 repo 设计审查流程：

- 列出六层检查；
- 为每层定义“抓住什么 bug”；
- 定义风险分级规则；
- 设计一个 review 轮次上限；
- 写一条“完成前必须提供的证明”。

### 接着读

- [Coordinating Specialist Review Agents at Scale：七类审查 agent 的编排](w6-coordinating-specialist-review-agents-at-scale.html)
- [Beyond the Diff：代码审查 agent 的五个改进](w6-beyond-the-diff-context-testing-and-model-selection.html)
- [Making Ergonomic Repositories：agent 原生代码库](w5-making-ergonomic-repositories.html)
