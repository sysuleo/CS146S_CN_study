---
title: "课堂实录：从 Vibe Coding 到 RePPIT 规格驱动开发（9/29）"
original: "CS146S Lecture Transcript — September 29, 2026"
week: "2"
slug: "w2-lecture-9-29-transcript"
source_url: "https://themodernsoftware.dev/materials/9-29-26-transcript.txt"
author: "Mihail Eric"
date: "2026-09-29"
kind: "课堂实录"
coverage: "逐段精译"
minutes: "22"
blurb: "为什么复杂代码库不能只靠 vibe coding，以及 RePPIT 五步如何把需求、方案、计划、实现和验证串起来。"
---

## 总结

这节课的核心问题是：**当代码库大到几十万行，直接对着聊天框说“帮我加个功能”为什么不够？**

- Vibe coding 适合小改动，但复杂任务需要先理解代码库，再提方案、做计划、实现和验证。
- RePPIT 是五步流程：Research、Propose、Plan、Implement、Test。
- Research 只描述代码库“现在是什么”，不提出改进；产物是一份压缩后的代码库理解文档。
- Propose 要给出两个真正不同的方案，而不是同一个方案换皮。
- Plan 的关键是明确“做什么”和“不做什么”，最好细到文件、行号和验证方式。
- 人类最该介入的两个位置，是意图/架构决策和代码审查。
- 上下文管理要结合压缩阈值、清空会话和模型选择；早期思考用强模型，后期实现可以用轻模型。

## 原文逐段对照翻译

> **翻译说明：**以下按讲课顺序逐段对照翻译，覆盖技术讲授与技术问答；课程行政、重复表述和现场寒暄从略。中文以准确、自然为目标。

<div class="slide-block"><p class="slide-block-title">对应 PPT · Slide 1</p><div class="slide-strip"><figure class="slide"><a class="slide-link" href="assets/slides/9-29/01.png" target="_blank" rel="noopener noreferrer"><img src="assets/slides/9-29/01.png" alt="9-29 slide 1" loading="lazy"></a><figcaption>Slide 1</figcaption></figure></div></div>

### 课程安排与 OSS 合作项目

<div class="slide-block"><p class="slide-block-title">对应 PPT · Slide 2</p><div class="slide-strip"><figure class="slide"><a class="slide-link" href="assets/slides/9-29/02.png" target="_blank" rel="noopener noreferrer"><img src="assets/slides/9-29/02.png" alt="9-29 slide 2" loading="lazy"></a><figcaption>Slide 2</figcaption></figure></div></div>

<div class="bilingual-pair">
<p class="src">Today we're also officially announcing the OSS Partners program, which is one of the most exciting things about this iteration of the class. We have a lot of partners building cool software that we get to contribute to, and contributing is part of your assignments.</p>
<p class="dst">今天还要正式公布 OSS 合作项目，这是本期课程最令人兴奋的部分之一。我们联系了很多正在做优秀软件的公司，大家可以向这些项目贡献代码，而贡献本身就是课程作业的一部分。</p>
</div>

<div class="bilingual-pair">
<p class="src">Put your preferences in the form. We'll do something like a stable matching problem, matching people against their rankings so that every partner gets students working on the project and you get as high up your preference list as possible. There will be a swap in the middle of the quarter, so you won't be with one partner for the entire quarter.</p>
<p class="dst">大家把偏好填进表格。我们会用类似“稳定匹配”的方式，根据双向排名做分配：每个合作方都能分到学生，大家也尽量去到自己更靠前的志愿。期中会换一次合作方，所以每个人至少会接触两个项目。</p>
</div>

<div class="bilingual-pair">
<p class="src">Part of the exercise is going through the process of onboarding onto multiple substantial codebases. You'll have two opportunities, and I think we're targeting at least four contributions. The due dates for each OSS contribution are in the class schedule.</p>
<p class="dst">这项练习的目的之一，是让大家体验如何进入多个真实的大型代码库。你们会有两次机会，目标是至少完成四次贡献。每次贡献的截止时间都写在课程表里。</p>
</div>

<div class="bilingual-pair">
<p class="src">When you say these partners are providing developer or maintainer support, what does that look like? At the very least, each has a dedicated maintainer you can interact with if issues come up. They'll primarily be responsible for reviewing PRs and making sure things get shipped into the codebases.</p>
<p class="dst">有同学问：合作方提供的维护者支持具体是什么？至少每家都会有一位固定维护者，遇到问题时可以直接沟通。他们主要负责 review PR，确保贡献真正合进代码库。</p>
</div>

### 为什么 Vibe Coding 不够

<div class="slide-block"><p class="slide-block-title">对应 PPT · Slide 3</p><div class="slide-strip"><figure class="slide"><a class="slide-link" href="assets/slides/9-29/03.png" target="_blank" rel="noopener noreferrer"><img src="assets/slides/9-29/03.png" alt="9-29 slide 3" loading="lazy"></a><figcaption>Slide 3</figcaption></figure></div></div>

<div class="bilingual-pair">
<p class="src">Today's focus is advanced prompting and context engineering for complex codebases. One of our goals is to take very good software developers with strong theoretical foundations and academic backgrounds and give them the tools to succeed in the real world.</p>
<p class="dst">今天的主题是：在复杂代码库里做高级提示和上下文工程。课程的目标之一，是把理论功底很好的软件工程师带到真实工程环境里，让他们掌握能落地的工具和方法。</p>
</div>

<div class="slide-block"><p class="slide-block-title">对应 PPT · Slide 4</p><div class="slide-strip"><figure class="slide"><a class="slide-link" href="assets/slides/9-29/04.png" target="_blank" rel="noopener noreferrer"><img src="assets/slides/9-29/04.png" alt="9-29 slide 4" loading="lazy"></a><figcaption>Slide 4</figcaption></figure></div></div>

<div class="bilingual-pair">
<p class="src">One of the biggest things you have to learn is how to operate coding agents at a scale beyond a handful of local files. We're talking about hundreds or thousands of files across millions of lines of code, at something like Google scale. Once you hit that scale, you run into the inherent context window limitations of coding agents.</p>
<p class="dst">你们必须学会的一件事，是在远超“几个本地文件”的规模上操作 coding agent。那是几百上千个文件、几百万行代码，接近 Google 那种体量。到了这个规模，上下文窗口的硬限制就会暴露出来。</p>
</div>

<div class="bilingual-pair">
<p class="src">Some have up to a million tokens, but not all tokens are created equal. You probably have fewer than a million that you can use for meaningful work before performance degrades. That means you have to be more thoughtful when working on complex software where a lot of code and context could be ingested by the agent.</p>
<p class="dst">有些模型号称支持一百万 token，但 token 和 token 并不等价。真正能用于有效工作的，往往远少于一 million；超过某个点，性能就会下降。所以在复杂软件里，你得更有意识地决定：到底把哪些代码和上下文喂给 agent。</p>
</div>

<div class="slide-block"><p class="slide-block-title">对应 PPT · Slide 10</p><div class="slide-strip"><figure class="slide"><a class="slide-link" href="assets/slides/9-29/10.png" target="_blank" rel="noopener noreferrer"><img src="assets/slides/9-29/10.png" alt="9-29 slide 10" loading="lazy"></a><figcaption>Slide 10</figcaption></figure></div></div>

<div class="slide-block"><p class="slide-block-title">对应 PPT · Slide 11</p><div class="slide-strip"><figure class="slide"><a class="slide-link" href="assets/slides/9-29/11.png" target="_blank" rel="noopener noreferrer"><img src="assets/slides/9-29/11.png" alt="9-29 slide 11" loading="lazy"></a><figcaption>Slide 11</figcaption></figure></div></div>

<div class="bilingual-pair">
<p class="src">We'll focus on REPIT: research, propose, plan, implement, and test. Those are the five steps. We'll work through what each means, and I'll share other frameworks that touch on similar ideas. You can try them and pick what you like.</p>
<p class="dst">今天重点讲 RePPIT：research（研究）、propose（提方案）、plan（做计划）、implement（实现）、test（测试）。我们会逐步拆开这五步，也会介绍其他类似框架。你可以都试试，再挑适合自己的。</p>
</div>

<div class="slide-block"><p class="slide-block-title">对应 PPT · Slide 5</p><div class="slide-strip"><figure class="slide"><a class="slide-link" href="assets/slides/9-29/05.png" target="_blank" rel="noopener noreferrer"><img src="assets/slides/9-29/05.png" alt="9-29 slide 5" loading="lazy"></a><figcaption>Slide 5</figcaption></figure></div></div>

<div class="slide-block"><p class="slide-block-title">对应 PPT · Slide 6</p><div class="slide-strip"><figure class="slide"><a class="slide-link" href="assets/slides/9-29/06.png" target="_blank" rel="noopener noreferrer"><img src="assets/slides/9-29/06.png" alt="9-29 slide 6" loading="lazy"></a><figcaption>Slide 6</figcaption></figure></div></div>

<div class="bilingual-pair">
<p class="src">Does anyone remember when "vibe coding" was coined? It came from a tweet by Andrej Karpathy. The idea was: what if we do this thing called vibe coding, don't even think about it, and just say, "Jesus, take the wheel"? It's cool and makes for a popular tweet. But to solve hard problems in difficult codebases, we need to go a level beyond vibe coding.</p>
<p class="dst">还有人记得“vibe coding”这个词是怎么来的吗？它来自 Andrej Karpathy 的一条推文，大意是：别想太多，直接“交给上帝”，让模型带着你写。这个说法很酷，也很容易传播。但要在复杂代码库里解决真正困难的问题，必须比 vibe coding 再往前走一层。</p>
</div>

### 例子：给 Mint Clone 加趋势图

<div class="slide-block"><p class="slide-block-title">对应 PPT · Slide 7</p><div class="slide-strip"><figure class="slide"><a class="slide-link" href="assets/slides/9-29/07.png" target="_blank" rel="noopener noreferrer"><img src="assets/slides/9-29/07.png" alt="9-29 slide 7" loading="lazy"></a><figcaption>Slide 7</figcaption></figure></div></div>

<div class="bilingual-pair">
<p class="src">Here's a thought exercise: how would you build a Mint clone? Mint was a consumer expense-tracking app. You could input your budget, connect your credit cards, track expenses, and see how much you were spending on different things. Let's go one step further: imagine we already have a fully fleshed-out Mint clone and need to extend it.</p>
<p class="dst">先做一个思想实验：如果让你做一个 Mint，你会怎么做？Mint 是一款面向消费者的记账应用，可以设预算、连信用卡、追踪支出，并查看各类别花了多少钱。我们再往前走一步：假设已经有一个功能完整的 Mint clone，现在要给它加功能。</p>
</div>

<div class="slide-block"><p class="slide-block-title">对应 PPT · Slide 8</p><div class="slide-strip"><figure class="slide"><a class="slide-link" href="assets/slides/9-29/08.png" target="_blank" rel="noopener noreferrer"><img src="assets/slides/9-29/08.png" alt="9-29 slide 8" loading="lazy"></a><figcaption>Slide 8</figcaption></figure></div></div>

<div class="slide-block"><p class="slide-block-title">对应 PPT · Slide 9</p><div class="slide-strip"><figure class="slide"><a class="slide-link" href="assets/slides/9-29/09.png" target="_blank" rel="noopener noreferrer"><img src="assets/slides/9-29/09.png" alt="9-29 slide 9" loading="lazy"></a><figcaption>Slide 9</figcaption></figure></div></div>

<div class="bilingual-pair">
<p class="src">To do that at production scale, we have to be methodical about how we write code using coding agents. First, you have to understand an unfamiliar codebase, especially one you haven't contributed to or written yourself. You need to find your way around it and know enough to direct your agent.</p>
<p class="dst">要在生产规模上完成这件事，就必须有方法地使用 coding agent。第一步是理解一个陌生的代码库，尤其是你既没写过、也没贡献过的项目。你需要在里面找到方向，掌握足够的信息去指挥 agent。</p>
</div>

<div class="bilingual-pair">
<p class="src">Then you need to propose solutions. If I gave you a task in a codebase you didn't write and knew nothing about, how would you approach it? You'd propose some solutions, identify the most promising one, implement it, and test it. Some of you might say, "We do test-driven development. Don't you start with tests and work back to the solution?" That's fine; it works here too.</p>
<p class="dst">接下来是提出方案。如果我给你一个完全陌生代码库里的任务，你会怎么入手？通常是先提出几种做法，挑出最有希望的一种，再实现、测试。有人可能会问：不是应该 TDD，先写测试再倒推实现吗？当然可以，顺序不是死的，核心环节不变。</p>
</div>

<div class="bilingual-pair">
<p class="src">I'll show you a minimalist Mint clone and its current state. Then we'll extend it with a new feature: a trend line showing spending by category over time. This app was vibe coded. I'm not a frontend developer. I know enough to be dangerous, but not enough to be useful.</p>
<p class="dst">我先给大家看一个极简版 Mint 的现状，然后加一个功能：按类别展示支出随时间变化的趋势线。顺便承认，这个 app 是 vibe coding 出来的。我不是前端工程师，懂一点但不多，属于“能闯祸但不能干活”的水平。</p>
</div>

### Research：只记录现状

<div class="slide-block"><p class="slide-block-title">对应 PPT · Slide 12</p><div class="slide-strip"><figure class="slide"><a class="slide-link" href="assets/slides/9-29/12.png" target="_blank" rel="noopener noreferrer"><img src="assets/slides/9-29/12.png" alt="9-29 slide 12" loading="lazy"></a><figcaption>Slide 12</figcaption></figure></div></div>

<div class="bilingual-pair">
<p class="src">The first step is research. This is an opportunity to seed the agent's context with useful information about the codebase without feeding it all the raw code. We're distilling the codebase into a consolidated representation that gives the coding agent enough to start making proposals about solutions.</p>
<p class="dst">第一步是 research。它的作用，是在不把全部原始代码塞进去的前提下，先给 agent 播种一份有用的代码库上下文。换句话说，把代码库蒸馏成一份浓缩表示，让 agent 有足够信息去提出方案。</p>
</div>

<div class="bilingual-pair">
<p class="src">The research phase is responsible only for documenting what exists in the codebase. It isn't responsible for implementation or proposing a solution. Its job is to define the behavioral contracts that exist today. The prompt is explicit: only document what exists today; don't suggest improvements.</p>
<p class="dst">Research 阶段只负责记录代码库里已经存在的东西，不负责实现，也不负责提方案。它的任务是描述当前的行为契约。提示词写得很明确：只记录今天已经存在的事实，不要提改进建议。</p>
</div>

<div class="bilingual-pair">
<p class="src">It might read mentioned files, decompose the request into research areas, and work through checklists. The important thing is the artifact at the end: a structured research document describing what the agent learned about components or areas of the codebase, potentially with references to code.</p>
<p class="dst">它会读取相关文件，把任务拆成若干研究区域，再按清单逐项推进。最重要的是最后留下的产物：一份结构化的研究文档，说明 agent 对各个组件或代码区域理解了什么，并尽可能给出代码位置引用。</p>
</div>

<div class="bilingual-pair">
<p class="src">That document serves two purposes. One is to seed the coding agent, because subsequent steps build on it. The other is to help my own understanding. I want to know enough to be useful. I don't need every detail, but I need a mental model to discern good from bad.</p>
<p class="dst">这份文档有两个用途。第一，给后续步骤提供上下文，后面的 propose 和 plan 都建立在它之上。第二，帮我自己建立理解。我不需要掌握每个细节，但必须有足够的心智模型，能判断 agent 的方案是好是坏。</p>
</div>

<div class="bilingual-pair">
<p class="src">If there's existing documentation, do you ingest it, scrap it, or find a middle ground? It depends entirely on how good the documentation is. If it's well maintained and accurately represents the codebase, I'd recommend reusing it and adjusting the skills to take it as a starting point. Given a choice between ingesting bad docs and starting from scratch, I'd start from scratch.</p>
<p class="dst">如果项目里已有文档，是直接读、丢掉，还是折中？完全取决于文档质量。如果维护得好、准确反映代码，就复用它，把 skill 改成以它为输入。如果文档已经过期，我宁愿让 agent 从代码重新建立理解，也不要让它被错误信息带偏。</p>
</div>

### Propose：两个真正不同的方案

<div class="bilingual-pair">
<p class="src">Next comes "propose." So far, we have a generic document describing the state of the codebase. It says nothing about the feature we're trying to build. We're now going to get more opinionated. The feature is a trend line showing spending by category over time.</p>
<p class="dst">接下来是 propose。前面那份文档只描述代码库现状，还没有涉及我们要做的功能。从这里开始，方案要变得有立场。我们的目标是：加一条按类别展示支出趋势的线。</p>
</div>

<div class="bilingual-pair">
<p class="src">The "make proposals" step is another skill. Given the consolidated representation of the codebase, take the feature and propose two distinct solutions. You can ask for three or four, but I've seen diminishing returns beyond two. These proposals are grounded in the existing research document.</p>
<p class="dst">“提方案”也是一个 skill：基于前面那份浓缩的代码库表示，围绕功能给出两个真正不同的方案。你当然可以要三个、四个，但超过两个通常收益递减。所有方案都必须扎根在 research 文档上，而不是凭空发挥。</p>
</div>

<div class="bilingual-pair">
<p class="src">The important parts are the context for each proposal, an overview of the solution, key changes, trade-offs, validation, and open questions. This phase and the next are where you should be most involved as the user and expert deciding on the agent's behavior.</p>
<p class="dst">每个方案要包含：背景、方案概述、关键改动、取舍、验证方式和开放问题。这个阶段以及下一步的 plan，是人类最应该深度参与的地方——你要以产品和技术专家的身份，决定 agent 往哪个方向走。</p>
</div>

<div class="bilingual-pair">
<p class="src">I can see two proposals here and their trade-offs. One is server-side, with a multi-series upload response. The other works with the uploaded transactions on the client. That feels more lightweight, with purely frontend changes. For a live demo, the less I can mess with the backend, the better. I'll pick proposal two.</p>
<p class="dst">这里有两个方案。一个是服务端方案，上传接口返回多序列数据；另一个是在客户端直接处理已上传的交易记录，只改前端，感觉更轻。对现场 demo 来说，少动后端就是少惹麻烦，所以我选第二个。</p>
</div>

<div class="bilingual-pair">
<p class="src">Outside a live demo, I'd look at this closely. What are the trade-offs? What do I care about? As the technical person who understands the product requirements, system requirements, and system limitations, I choose among the proposals and proceed.</p>
<p class="dst">如果不在 demo 环境，我会认真比较：各自的取舍是什么？我最在意什么？作为理解产品需求、系统要求和系统限制的技术负责人，最终方案要由我来选，而不是让 agent 替我拍板。</p>
</div>

<div class="bilingual-pair">
<p class="src">I've found a point of diminishing returns. If you're familiar with PCA in machine learning, I want principal components that are orthogonal to each other: one axis and another perpendicular axis. I mainly want to force the agent to identify two different regions of the solution space.</p>
<p class="dst">两个方案之后，收益就明显递减了。可以借用机器学习里的 PCA 来理解：我希望两个方案像两个正交的主成分，分别覆盖解空间的不同方向。目的就是逼 agent 去看两个真正不同的区域，而不是在同一个点上反复润色。</p>
</div>

### Plan：把“做什么”和“不做什么”写清楚

<div class="bilingual-pair">
<p class="src">We're now at the plan phase. We've made two proposals, reviewed them diligently, and committed to one. Now we're forming a plan. Here's my skill. It essentially says: here's a design document template; fill it in based on the proposal.</p>
<p class="dst">现在进入 plan。两个方案已经比较过，也选定了一个，接下来要形成实施计划。我的 skill 很简单：给 agent 一份设计文档模板，让它基于选中的方案把内容填完整。</p>
</div>

<div class="bilingual-pair">
<p class="src">The design document includes the current state of the codebase, functional and nonfunctional requirements, design decisions and trade-offs, and the technical design. There's some code-level detail so I can get into the weeds. The template also covers testing, which tests to run, observability, and future considerations.</p>
<p class="dst">设计文档包括：代码库现状、功能与非功能需求、设计决策与取舍、技术设计。里面会保留一些代码级细节，方便我深入检查。模板还覆盖测试计划、要跑哪些测试、可观测性，以及未来考虑。</p>
</div>

<div class="bilingual-pair">
<p class="src">One of the most valuable things is explicitly calling out what's outside the scope of the implementation. For this feature, here's what's not going to happen. I put those items under future considerations and say, "Don't touch this. Only implement the work in scope. Defer everything else."</p>
<p class="dst">最有价值的部分之一，是明确写出“这次不做什么”。我会把范围外的事项放进 future considerations，并直接告诉 agent：不要碰这些，只实现本次范围内的内容，其他全部推迟。这样能有效防止它跑偏。</p>
</div>

<div class="bilingual-pair">
<p class="src">Making that explicit helps prevent the agent from going off the rails and doing unrelated work. At this stage, I'd be very involved in reviewing what's here. Are the service boundaries good? Are we modularizing the codebase appropriately? What are the data models?</p>
<p class="dst">把这些写清楚，可以防止 agent 擅自做无关重构。到了这一步，我会非常认真地审阅计划：服务边界合理吗？模块划分合适吗？数据模型是什么？这些判断不能外包给 agent。</p>
</div>

<div class="bilingual-pair">
<p class="src">I do less validation on the research side than I used to, because agents have become very good at reading code and distilling it into a consolidated representation. Research is effectively compression of information, and I think agents are very good at that. I'm more concerned with implementation than research.</p>
<p class="dst">现在我对 research 结果的验证比过去少，因为 agent 读代码、提炼信息的能力已经很强。Research 本质上是信息压缩，而这是模型擅长的。我更担心的是后面的实现，而不是研究阶段。</p>
</div>

### Implement + Test：让 agent 自己验证行为

<div class="bilingual-pair">
<p class="src">While it's implementing, I want to show the incredibly sophisticated implementation prompt. It barely needs to be a prompt: it essentially just tells the agent to implement the plan. Meanwhile, Cursor is working through the plan and adding what it needs.</p>
<p class="dst">实现阶段的提示词其实非常朴素，几乎只有一句：按计划实现。真正干活的是 agent。此时 Cursor 正在按计划推进，补上需要改的代码。</p>
</div>

<div class="bilingual-pair">
<p class="src">It's implicitly opening a browser, interacting with the app, creating synthetic data, and trying to upload it through the CSV interface. It's combining implementation and testing in one step. This wasn't true six months ago, but now it's good enough to say, after implementing something, "I should probably test this myself and verify what was generated."</p>
<p class="dst">它还会自己打开浏览器、操作应用、造合成数据，并通过 CSV 上传验证。实现和测试被合在了一起。半年前这还不太现实，现在 agent 已经会在写完代码后主动想：我应该自己跑一遍，确认生成的东西真的能用。</p>
</div>

<div class="bilingual-pair">
<p class="src">That's a behavioral check: I upload a CSV, and I should see the new feature generated. At least visually, it seems complete. There's another set of concerns: performance, quality, readability, and so on. Those aspects beyond the behavioral contract fall under code review.</p>
<p class="dst">这属于行为验证：上传一个 CSV，应该能看到新功能出现。至少从视觉上看，它是完整的。至于性能、代码质量、可读性等问题，属于行为契约之外的范畴，要交给代码审查。</p>
</div>

### 代码审查与上下文管理

<div class="bilingual-pair">
<p class="src">I'll show you a simple code review skill. It checks the diff and outputs "must fix," "recommended fixes," and "consider," like red, yellow, and green. This particular skill combines security, performance, style, consistency, and edge cases.</p>
<p class="dst">这里有一个简单的 code review skill：检查 diff，把问题分成“必须修”“建议修”“可以考虑”三档，类似红黄绿。这个示例把安全、性能、风格、一致性和边界情况都放在了一个 skill 里。</p>
</div>

<div class="bilingual-pair">
<p class="src">In practice, people often use four or five agents, each handling one area, such as security or performance. When you open a PR on GitHub, an action runs those agents, and a coordinating agent combines their outputs. You get one report with checks on architecture, style, consistency, and so on.</p>
<p class="dst">真实团队通常会用四五个 agent，各自负责一个领域，比如安全、性能。PR 提交到 GitHub 后，Action 触发这些 agent，再由一个协调 agent 汇总结果，最后给出一份覆盖架构、风格、一致性等维度的综合报告。</p>
</div>

<div class="slide-block"><p class="slide-block-title">对应 PPT · Slide 13</p><div class="slide-strip"><figure class="slide"><a class="slide-link" href="assets/slides/9-29/13.png" target="_blank" rel="noopener noreferrer"><img src="assets/slides/9-29/13.png" alt="9-29 slide 13" loading="lazy"></a><figcaption>Slide 13</figcaption></figure></div></div>

<div class="bilingual-pair">
<p class="src">When do you clear context? You didn't mention compaction, but I'll include it too. When do you use a stronger model? Some of this is more art than science, but people are increasingly studying these choices.</p>
<p class="dst">什么时候该清空上下文？什么时候该用更强的模型？这些问题目前更像经验，而不是严格科学，但已经有人在系统研究。</p>
</div>

<div class="bilingual-pair">
<p class="src">This was a solid blog post studying compaction, when to do it, how it affects cost, and how many tokens you should accumulate before compacting. One takeaway was somewhere between 250,000 and 450,000 tokens, depending on the model.</p>
<p class="dst">有一篇研究 compaction 的文章，分析了什么时候压缩、对成本有什么影响、积累到多少 token 再压缩比较合适。一个结论是：根据模型不同，大约在 25 万到 45 万 token 之间。</p>
</div>

<div class="bilingual-pair">
<p class="src">As for clearing the context: I did something in this demo that I wouldn't recommend. After making and selecting a proposal, I would normally clear the context. Otherwise, both proposals remain there even though you've committed to one. That can confuse the agent about which it's implementing.</p>
<p class="dst">关于清空上下文：我在 demo 里做了一个不太推荐的操作。选完方案后，正常应该清空上下文；否则两个方案都还留在窗口里，agent 可能搞不清你到底让它实现哪一个。</p>
</div>

<div class="bilingual-pair">
<p class="src">Use a very good model for the early stages. The later stages don't need to be as powerful. Implementation and even testing can use lighter-weight models. For research, proposals, and planning, use a strong model, because that's where most of the thinking happens.</p>
<p class="dst">早期阶段用强模型，后期不一定需要。实现甚至测试可以用更轻的模型。Research、propose、plan 尽量用强模型，因为真正的思考主要发生在那里。</p>
</div>

### 任务复杂度阶梯

<div class="slide-block"><p class="slide-block-title">对应 PPT · Slide 14</p><div class="slide-strip"><figure class="slide"><a class="slide-link" href="assets/slides/9-29/14.png" target="_blank" rel="noopener noreferrer"><img src="assets/slides/9-29/14.png" alt="9-29 slide 14" loading="lazy"></a><figcaption>Slide 14</figcaption></figure></div></div>

<div class="bilingual-pair">
<p class="src">There's an open question: when should you use vanilla prompting, and when should you switch to a heavier approach? You can use simple prompting: talk to ChatGPT and say, "Jesus, take the wheel." You can make a single plan by going straight into plan mode in Claude. You can research and then plan. Or you can repeat research and planning several times.</p>
<p class="dst">还有一个关键问题：什么时候直接普通对话就行，什么时候该上重流程？你可以直接对 ChatGPT 说“交给你了”；也可以在 Claude 里进一次 plan mode；也可以先 research 再 plan；还可以把 research 和 plan 反复迭代几轮。</p>
</div>

<div class="slide-block"><p class="slide-block-title">对应 PPT · Slide 15</p><div class="slide-strip"><figure class="slide"><a class="slide-link" href="assets/slides/9-29/15.png" target="_blank" rel="noopener noreferrer"><img src="assets/slides/9-29/15.png" alt="9-29 slide 15" loading="lazy"></a><figcaption>Slide 15</figcaption></figure></div></div>

<div class="bilingual-pair">
<p class="src">Something like a copy change or a small fix can be handled by talking to Claude or Codex. You'll be fine. For small features spanning multiple files, start thinking about making a plan. As complexity increases to medium-sized features, and certainly to a big refactor or migration, you'll want multiple steps of research, proposals, and planning, with separate sessions and subagents.</p>
<p class="dst">改文案、小修复，直接和 Claude 或 Codex 说就行。跨多个文件的小功能，至少先做个计划。到了中型功能，尤其是大重构、大迁移，就需要多轮 research、propose、plan，分 session，必要时上 subagent。</p>
</div>

<div class="slide-block"><p class="slide-block-title">对应 PPT · Slide 16</p><div class="slide-strip"><figure class="slide"><a class="slide-link" href="assets/slides/9-29/16.png" target="_blank" rel="noopener noreferrer"><img src="assets/slides/9-29/16.png" alt="9-29 slide 16" loading="lazy"></a><figcaption>Slide 16</figcaption></figure></div></div>

<div class="bilingual-pair">
<p class="src">For very large projects in my day-to-day work, I break them into multiple issues, use separate agents for each issue, and stack the issues so agents build on one another's work. At that point, I'm much more thoughtful about the issue descriptions.</p>
<p class="dst">在日常工作里遇到超大项目，我会把它拆成多个 issue，每个 issue 交给一个 agent，再把 issue 串成栈，让后一个 agent 接着前一个的成果做。到这一步，issue 描述本身就要写得很讲究。</p>
</div>

### Superpowers 与 OpenSpec

<div class="slide-block"><p class="slide-block-title">对应 PPT · Slide 17</p><div class="slide-strip"><figure class="slide"><a class="slide-link" href="assets/slides/9-29/17.png" target="_blank" rel="noopener noreferrer"><img src="assets/slides/9-29/17.png" alt="9-29 slide 17" loading="lazy"></a><figcaption>Slide 17</figcaption></figure></div></div>

<div class="bilingual-pair">
<p class="src">Superpowers is effectively the framework I described on steroids. It has 300,000 stars. It's a more involved but solid approach to thoughtful planning, outlining specs, and brainstorming with the agent. OpenSpec is another framework you can check out through the slides.</p>
<p class="dst">Superpowers 可以看作我今天讲的方法的“加强版”，有 30 万 star。它更重，但在规划、写规格、和 agent 做 brainstorming 方面非常完整。OpenSpec 则是另一个值得看的框架，幻灯片里有链接。</p>
</div>

<div class="slide-block"><p class="slide-block-title">对应 PPT · Slide 18</p><div class="slide-strip"><figure class="slide"><a class="slide-link" href="assets/slides/9-29/18.png" target="_blank" rel="noopener noreferrer"><img src="assets/slides/9-29/18.png" alt="9-29 slide 18" loading="lazy"></a><figcaption>Slide 18</figcaption></figure></div></div>

<div class="bilingual-pair">
<p class="src">At its core, the repository is just a set of skills. Look at what's provided: brainstorming, writing plans, executing plans, code review, and more. They're the things we've been talking about. This whole 300,000-star repository is a set of skills.</p>
<p class="dst">Superpowers 的核心其实只是一组 skills：brainstorming、写计划、执行计划、代码审查等等。都是我们今天讲的东西。这个 30 万 star 的仓库，本质上就是一套 skills 集合。</p>
</div>

## 学习者视角

### 关键收获

1. **复杂任务的第一原则是“先理解”。** 不了解代码库就直接让 agent 写，等于把方向判断也外包了。
2. **Research 和 Propose 要分开。** 一个只描述现状，一个才提出改变；混在一起会让 agent 把假设当事实。
3. **两个正交方案足够。** 方案不是越多越好，关键是覆盖解空间的不同方向。
4. **Plan 的“不做什么”比“做什么”更能防止跑偏。**
5. **验证要验证行为。** 单测之外，浏览器/端到端检查能抓住“代码看起来对但行为不对”。
6. **人类的杠杆在意图、架构和审查。** 实现越自动化，这三件事越重要。

### 放回课程里看

这节课把 [OpenSpec](w2-openspec.html)、[Superpowers](w2-superpowers.html) 和 [Context Tax](w2-the-context-tax-when-to-compact.html) 串成了一条真实工作流。它也是后面 Week 6 代码审查的铺垫。

### 一个反直觉点

讲师对 research 的验证反而最少。他的判断是：读代码、压缩信息是模型现在最擅长的事；真正容易出问题的是实现和测试。所以人的注意力应该后移，而不是平均分配。

## 拓展

### 思考题

1. 你最近做的一个功能，属于复杂度阶梯的哪一级？用的流程匹配吗？
2. 为什么两个正交方案通常比四个“换皮方案”更有价值？
3. 你的 plan 里有没有明确写“不做什么”？如果没有，agent 跑偏过吗？
4. 如果 research 文档本身有错，后面的 propose 和 plan 会怎样被放大？

### 练习

选一个中等功能，按 RePPIT 走一遍：

- 写一份只描述现状的 research 文档；
- 提两个真正不同的方案；
- 选一个，写设计文档，明确范围外事项；
- 实现后用浏览器或端到端测试验证行为；
- 做一次代码审查。

### 接着读

- [OpenSpec：规格工作流](w2-openspec.html)
- [Superpowers：完整开发方法论](w2-superpowers.html)
- [课堂实录 10/1：MCP 与 Code Mode](w2-lecture-10-1-transcript.html)
