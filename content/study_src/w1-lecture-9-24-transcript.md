---
title: "课堂实录：生产级 Coding Agent 的 Harness 解剖（9/24）"
original: "CS146S Lecture Transcript — September 24, 2026"
week: "1"
slug: "w1-lecture-9-24-transcript"
source_url: "https://themodernsoftware.dev/materials/9-24-26-transcript.txt"
author: "Mihail Eric"
date: "2026-09-24"
kind: "课堂实录"
coverage: "逐段精译"
minutes: "20"
blurb: "从 200 行 demo 到生产级 harness：工具、system prompt、CLAUDE.md、plan mode、skills、subagents 与 compaction。"
---

## 总结

这节课从周二那个“200 行代码就能跑”的 demo 出发，回答一个更实际的问题：**既然核心循环并不复杂，为什么生产级 coding agent 还要在外面套这么多东西？**

- 核心循环始终很简单：接收请求、调用模型、执行工具、把结果放回上下文，然后继续。
- 真正复杂的是 harness：工具列表、system prompt、CLAUDE.md、plan mode、skills、subagents、hooks、compaction。
- 工具定义本身就是提示词。名字、描述、参数类型、docstring、错误类型，都会进入模型上下文。
- MCP 是“原语”，负责一次外部调用；skill 是“流程”，把多次调用、脚本和提示词串起来。
- 工具并非越多越好。早期 GitHub MCP 有上百个工具，直接把上下文撑爆；更合理的做法是提供少数几个能力很强的“瑞士军刀”。
- system prompt 在变短，harness 在变薄，行业趋势是把更多能力交给模型本身。

## 原文逐段对照翻译

> **翻译说明：**以下按讲课顺序逐段对照翻译，覆盖本堂课的技术讲授与技术问答；课程寒暄、重复表述和无法辨认的现场片段从略。中文以准确、自然为目标，不逐字硬译，也不把完整句子硬拆成碎片。

### 开场与课程安排

<div class="slide-block"><p class="slide-block-title">对应 PPT · Slide 1</p><div class="slide-strip"><figure class="slide"><a class="slide-link" href="assets/slides/9-24/01.png" target="_blank" rel="noopener noreferrer"><img src="assets/slides/9-24/01.png" alt="9-24 slide 1" loading="lazy"></a><figcaption>Slide 1</figcaption></figure></div></div>

<div class="bilingual-pair">
<p class="src">Welcome back. We have a quick one-two here with Tuesdays and Thursdays, so I'm glad to see everyone again, or at least most of the folks. Let's dive into it.</p>
<p class="dst">欢迎回来。周二和周四两节课挨得很近，很高兴又见到大家，至少见到了大多数人。我们直接开始。</p>
</div>

<div class="slide-block"><p class="slide-block-title">对应 PPT · Slide 2</p><div class="slide-strip"><figure class="slide"><a class="slide-link" href="assets/slides/9-24/02.png" target="_blank" rel="noopener noreferrer"><img src="assets/slides/9-24/02.png" alt="9-24 slide 2" loading="lazy"></a><figcaption>Slide 2</figcaption></figure></div></div>

<div class="bilingual-pair">
<p class="src">I want to start with some logistics for people who are here for the first time, as well as a few updates for those who were here on Tuesday. First, I believe Isaac put out the final project specifications. That's the capstone for the quarter. There are roughly four milestones along the way, including a proposal and some intermediate milestones, to get you looking at things before the last week of the quarter, when people start getting really crazy with the vibe coding.</p>
<p class="dst">先讲一些课程安排，既照顾第一次来的同学，也补充周二已经到场的人需要知道的信息。第一，Isaac 应该已经发布了期末项目说明。这是本季度的大作业，整个过程大约有四个节点，包括开题提案和若干中间里程碑。这样安排，是为了避免大家拖到最后一周才开始疯狂 vibe coding。</p>
</div>

<div class="bilingual-pair">
<p class="src">We're allowing up to one additional partner in the class for this project. You can have one human partner and as many coding agents as you want. A swarm of them, in fact. That's all fair game. You can also do it by yourself. A lot of people choose to, and I think that's acceptable, maybe even appropriate these days, given how powerful coding agents are.</p>
<p class="dst">这个项目最多允许一位人类搭档，coding agent 则不限数量，开一整群也没问题。当然，你也可以独立完成。很多人会选择单干；考虑到现在 coding agent 的能力，这不仅可接受，甚至可能更合适。</p>
</div>

<div class="bilingual-pair">
<p class="src">One thing I forgot to mention last time: in addition to the other perks of the class, such as the OSS partners whose projects we'll get to contribute to and the guest speakers coming in, we're also getting credits from a bunch of providers. These include a lot of the top coding agent startups and companies. That includes Claude, Claude Code credits, Factory credits, and xAI credits. Devin is included too. Windsurf and Devin are part of the same company, Cognition.</p>
<p class="dst">上次还有一件事没提：除了 OSS 合作项目和嘉宾讲座，课程还拿到了一批厂商的计算额度，覆盖不少头部 coding agent 公司，包括 Claude Code、Factory、xAI，以及 Cognition 旗下的 Devin 和 Windsurf。大家尽情写代码、跑 agent，不用先烧自己的信用卡。</p>
</div>

<div class="bilingual-pair">
<p class="src">We also mentioned the OSS partner component of the class. We'll explain exactly what form that takes next week. A few of the partners are so excited about being in the class that they're actually going to come in. They'll walk through their projects and, in some cases, do virtual or in-person office hours.</p>
<p class="dst">我们还提到过课程的 OSS 合作项目，下周会具体说明参与方式。有些合作方非常积极，会亲自来课堂介绍项目，部分还会安排线上或线下的 office hours。</p>
</div>

<div class="bilingual-pair">
<p class="src">A lot of people have asked about applications to get off the waitlist. The prerequisites are the minimum set I think you need to be successful in the class. There are ways to get exceptions, usually for people who didn't do their undergraduate work at Stanford but took equivalent courses elsewhere and can demonstrate that. The application deadline is the 27th, which I think is Sunday.</p>
<p class="dst">很多人问候补名单的申请。先修要求并不高，但我认为这是顺利完成课程所需的最低基础。也可以申请例外，通常适用于本科不在斯坦福、但在其他学校修过同等课程并能证明的人。申请截止到 27 号，应该是周日。</p>
</div>

<div class="bilingual-pair">
<p class="src">Today we're going deeper into some of the topics we touched on last week—or rather, two days ago. Toward the end of Tuesday's class, we went through a demonstration showing that, in about 150 to 200 lines of code, you can build the bare bones of a coding agent. It can interpret user requests, edit code and files, and generate things of some complexity, starting with “Hello, world.”</p>
<p class="dst">今天我们会深入上周——准确说是两天前——提到的一些主题。周二课程的后半段，我们演示了如何用大约 150 到 200 行代码搭出一个 coding agent 的骨架：它能理解用户请求、编辑代码和文件，也能生成一些有复杂度的东西，虽然只是从“Hello, world”开始。</p>
</div>

### 从 200 行 demo 到生产级 harness

<div class="slide-block"><p class="slide-block-title">对应 PPT · Slide 3</p><div class="slide-strip"><figure class="slide"><a class="slide-link" href="assets/slides/9-24/03.png" target="_blank" rel="noopener noreferrer"><img src="assets/slides/9-24/03.png" alt="9-24 slide 3" loading="lazy"></a><figcaption>Slide 3</figcaption></figure></div></div>

<div class="bilingual-pair">
<p class="src">Tuesday was a proof of concept: look what you can do in 200 lines of code. Today, I want to bring us up to the modern day in coding agents and their harnesses. We're going to dissect the anatomy of a state-of-the-art coding agent and see what's happening under the hood.</p>
<p class="dst">周二那节课只是一个概念验证：看看 200 行代码能做到什么。今天我们要回到当下，拆开一个现代 coding agent，看看它内部到底是怎么运转的。</p>
</div>

<div class="slide-block"><p class="slide-block-title">对应 PPT · Slide 4</p><div class="slide-strip"><figure class="slide"><a class="slide-link" href="assets/slides/9-24/04.png" target="_blank" rel="noopener noreferrer"><img src="assets/slides/9-24/04.png" alt="9-24 slide 4" loading="lazy"></a><figcaption>Slide 4</figcaption></figure></div></div>

<div class="bilingual-pair">
<p class="src">We'll be able to see everything except the intelligence layer, which is the model. The model is private: some big set of two-trillion-plus-parameter models sitting on servers distributed around the world. We can't see that, but we can see the harness around it.</p>
<p class="dst">除了智能层本身，也就是模型，其余部分我们都能看到。模型是黑盒：那是一批参数规模超过两万亿、部署在全球服务器上的庞然大物。我们看不到它内部，但可以看到包在它外面的那层 harness。</p>
</div>

<div class="slide-block"><p class="slide-block-title">对应 PPT · Slide 5</p><div class="slide-strip"><figure class="slide"><a class="slide-link" href="assets/slides/9-24/05.png" target="_blank" rel="noopener noreferrer"><img src="assets/slides/9-24/05.png" alt="9-24 slide 5" loading="lazy"></a><figcaption>Slide 5</figcaption></figure></div></div>

<div class="bilingual-pair">
<p class="src">Two days ago, we went through the core execution loop of a coding agent. You have a user interacting with a coding agent harness, such as Claude, Windsurf, or Devin. The harness passes the request to the model, the model decides whether to call a tool, the tool runs, and the result goes back into context.</p>
<p class="dst">两天前我们讲过 coding agent 的核心执行循环：用户通过 Claude Code、Windsurf、Devin 这类 harness 发出请求；harness 把请求交给模型；模型判断要不要调用工具；工具执行后，结果重新进入上下文；循环继续，直到任务完成。</p>
</div>

### Harness 的标准组件

<div class="slide-block"><p class="slide-block-title">对应 PPT · Slide 6</p><div class="slide-strip"><figure class="slide"><a class="slide-link" href="assets/slides/9-24/06.png" target="_blank" rel="noopener noreferrer"><img src="assets/slides/9-24/06.png" alt="9-24 slide 6" loading="lazy"></a><figcaption>Slide 6</figcaption></figure></div></div>

<div class="slide-block"><p class="slide-block-title">对应 PPT · Slide 7</p><div class="slide-strip"><figure class="slide"><a class="slide-link" href="assets/slides/9-24/07.png" target="_blank" rel="noopener noreferrer"><img src="assets/slides/9-24/07.png" alt="9-24 slide 7" loading="lazy"></a><figcaption>Slide 7</figcaption></figure></div></div>

<div class="bilingual-pair">
<p class="src">A lot goes into the harness around the intelligence of an LLM. A few components are now fairly standard: the system prompt; custom configuration; tools; skills; subagents; hooks; compaction; and session persistence.</p>
<p class="dst">围绕模型智能的 harness，包含的东西其实很多。现在比较标准的组件包括：system prompt、自定义配置、工具、skills、subagents、hooks、上下文压缩，以及会话持久化。</p>
</div>

<div class="bilingual-pair">
<p class="src">In Claude's case, there are about 40 built-in tools that you get when you download and use Claude Code. These are capabilities the Anthropic team has decided the coding agent should have access to. I'd go a step further: the model has been optimized to use those tools.</p>
<p class="dst">以 Claude Code 为例，安装后大约自带 40 个工具。这些是 Anthropic 认为 coding agent 应该具备的能力。更进一步说，模型在训练阶段就针对这些工具做过优化——工具和模型是配套设计的。</p>
</div>

### 工具定义本身就是提示词

<div class="bilingual-pair">
<p class="src">One thing I want to highlight before we get into an example: you can think of a tool as a function. Everything in its definition—the description, comments, name, and full signature—becomes part of your prompt. It gets injected into the context.</p>
<p class="dst">在进入例子之前，先强调一点：你可以把工具理解成一个函数。它的全部定义——描述、注释、名称、完整签名——都会成为提示词的一部分，被注入上下文。</p>
</div>

<div class="bilingual-pair">
<p class="src">When you're writing a function to expose as a tool to a coding agent, being clear and consistent in the Python docstring is incredibly important. So is being clear about the argument types. All of that gets surfaced to the LLM, and it's what the LLM uses to understand what to do and when to use the tool.</p>
<p class="dst">所以，给 agent 写工具函数时，docstring 必须清楚、一致，参数类型也必须明确。这些东西最终都会呈现给模型，模型正是靠它们判断“这个工具是干什么的、什么时候该用、参数怎么传”。</p>
</div>

<div class="slide-block"><p class="slide-block-title">对应 PPT · Slide 8</p><div class="slide-strip"><figure class="slide"><a class="slide-link" href="assets/slides/9-24/08.png" target="_blank" rel="noopener noreferrer"><img src="assets/slides/9-24/08.png" alt="9-24 slide 8" loading="lazy"></a><figcaption>Slide 8</figcaption></figure></div></div>

<div class="bilingual-pair">
<p class="src">We said we'd start with tools, so let's dive into the tool lists. Below the user and assistant messages, there's a tools block in the intercepted request. The tools are explicitly listed in this component. The tools object is a list, and each entry is a dictionary.</p>
<p class="dst">我们先从工具列表看起。在拦截到的请求里，用户消息和助手消息下面有一个 tools 字段，所有工具都在这里显式列出。它是一个列表，每一项是一个字典，描述一个工具的名称、用途和参数结构。</p>
</div>

<div class="bilingual-pair">
<p class="src">One example is the agent tool. It lets you launch a new agent to handle complex, multistep tasks, and the description explains that agent's capabilities. There's also a schema that you can think of as the function signature for this tool.</p>
<p class="dst">比如 Agent 工具，它允许主 agent 启动一个新的 agent 来处理复杂的多步任务；工具描述会说明这个子 agent 能做什么。下面的 schema 则可以理解为这个工具的“函数签名”，规定它可以接收哪些参数。</p>
</div>

<div class="bilingual-pair">
<p class="src">It's a lot of stuff. MCP came first, and skills were introduced later. One reason for introducing skills was progressive disclosure: bringing information into the context when it's relevant to the LLM.</p>
<p class="dst">这里的上下文负担很重。MCP 出现得更早，skills 是后来才加入的。引入 skills 的一个重要原因，就是“渐进式披露”：只有当信息与当前任务相关时，才把它加载进上下文。</p>
</div>

### MCP 与 skills 的分工

<div class="bilingual-pair">
<p class="src">Here, we're dropping in all the tools. Every MCP server you've loaded, including third-party servers, appears in this block. Every time you send a request, it gets that set of tools. Skills, by contrast, initially include only a small amount of metadata describing what the skill does.</p>
<p class="dst">但工具不一样：你加载的每一个 MCP server，包括第三方 server，都会出现在这个 tools 块里。你每发一次请求，模型都会收到这一整套工具定义。skills 则相反，会话开始时只加载少量元数据，说明这个 skill 大致做什么；等真正需要时，才把正文拉进来。</p>
</div>

<div class="bilingual-pair">
<p class="src">MCP is a primitive. You can think of an MCP tool almost like an API call: an input-output mechanism. When we talk about skills, we're codifying procedures: multiple steps, multiple tool calls, and prompts between calls.</p>
<p class="dst">MCP 是底层原语。你可以把 MCP 工具近似理解成一次 API 调用：给定输入，返回输出。skill 则是把流程固化下来：它可能包含多个步骤、多次工具调用，以及步骤之间的提示词和判断。</p>
</div>

<div class="bilingual-pair">
<p class="src">So, tools: there are about 40 built in, and depending on how many MCP servers you add, that can grow to a lot more. One reason Claude Code became so popular around December of last year was its minimalist harness. For a long time, it had a restrictive set of tools that could still do almost everything.</p>
<p class="dst">工具方面：Claude Code 自带约 40 个，接入的 MCP server 越多，总数还会继续增长。Claude Code 去年十二月前后之所以受欢迎，一个重要原因就是 harness 足够克制。很长一段时间里，它的工具数量不多，但几乎什么都能做。</p>
</div>

### 少而强的工具

<div class="bilingual-pair">
<p class="src">Examples of powerful tools include Bash and SQL. You can do complex operations by giving an LLM access to the file system and a CLI. They stripped down a lot of what had become bloated.</p>
<p class="dst">Bash 和 SQL 就是典型的“强力工具”。只要把文件系统和命令行交给模型，它就能组合出非常复杂的操作。Claude Code 做的事情，是把过去臃肿的工具集大幅削减，只留下少数几个通用能力。</p>
</div>

### System prompt 与 CLAUDE.md

<div class="slide-block"><p class="slide-block-title">对应 PPT · Slide 9</p><div class="slide-strip"><figure class="slide"><a class="slide-link" href="assets/slides/9-24/09.png" target="_blank" rel="noopener noreferrer"><img src="assets/slides/9-24/09.png" alt="9-24 slide 9" loading="lazy"></a><figcaption>Slide 9</figcaption></figure></div></div>

<div class="bilingual-pair">
<p class="src">For anyone who isn't familiar, a system prompt is effectively a blueprint for the LLM's behavior. It's a block of text that defines aspects of the harness and its behavior, including guardrails and information about the environment. The harness injects this static text without you saying anything.</p>
<p class="dst">system prompt 可以理解为模型行为的“蓝图”。它是一段由 harness 自动注入的静态文本，定义模型在这个环境里应该如何行动，包括安全边界、可用能力、环境信息等。你不需要开口，它就已经在上下文里了。</p>
</div>

<div class="bilingual-pair">
<p class="src">The first block says, “You are Claude Code, Anthropic's official CLI for Claude.” That's the harness telling the LLM, in natural language, what it is as a system. The second block is where the more substantial instructions are.</p>
<p class="dst">第一段很简单：“你是 Claude Code，Anthropic 官方提供的 Claude 命令行工具。”这是 harness 在用自然语言告诉模型“你现在是什么系统”。第二段才是更实质的指令，包含行为规范、安全注意事项、环境信息等。</p>
</div>

<div class="bilingual-pair">
<p class="src">This is a much shorter system prompt. Until the last month or two, it was around 200 to 250 lines. Much of it explained things like how to use Git and issue tasks. Those were instructions considered important to give the model explicitly, but they seem less necessary now.</p>
<p class="dst">现在的 system prompt 已经短了很多。直到一两个月前，它还有 200 到 250 行，很多内容是在教模型怎么用 Git、怎么拆任务。过去这些必须明说，现在模型自己已经掌握了，显式写进去反而显得多余。</p>
</div>

<div class="slide-block"><p class="slide-block-title">对应 PPT · Slide 10</p><div class="slide-strip"><figure class="slide"><a class="slide-link" href="assets/slides/9-24/10.png" target="_blank" rel="noopener noreferrer"><img src="assets/slides/9-24/10.png" alt="9-24 slide 10" loading="lazy"></a><figcaption>Slide 10</figcaption></figure></div></div>

<div class="bilingual-pair">
<p class="src">CLAUDE.md is a user-controlled counterpart to the system prompt. The system prompt is static, set by the harness, and injected behind the scenes. CLAUDE.md is also injected, but we control it.</p>
<p class="dst">CLAUDE.md 则是用户可以控制的“另一半 system prompt”。system prompt 由 harness 固定写好，在后台注入；CLAUDE.md 同样会被注入，但内容由我们自己决定。</p>
</div>

<div class="bilingual-pair">
<p class="src">In general, the consensus on CLAUDE.md or AGENTS.md is that it's helpful to include some directions for running the code, such as tests and starting the server, but not too many. It's a fine line. If you include too much, you overconstrain the system.</p>
<p class="dst">关于 CLAUDE.md 或 AGENTS.md，目前比较一致的看法是：写一些“怎么跑代码”的说明是有帮助的，比如怎么跑测试、怎么启动服务，但不要写太多。这个度很难拿捏——写过头，就会把系统约束得太死。</p>
</div>

### Plan mode、skills 与 subagents

<div class="slide-block"><p class="slide-block-title">对应 PPT · Slide 11</p><div class="slide-strip"><figure class="slide"><a class="slide-link" href="assets/slides/9-24/11.png" target="_blank" rel="noopener noreferrer"><img src="assets/slides/9-24/11.png" alt="9-24 slide 11" loading="lazy"></a><figcaption>Slide 11</figcaption></figure></div></div>

<div class="bilingual-pair">
<p class="src">Plan mode is a mode you can use when talking to these agents, specifically for designing specifications and working through harder tasks. It's a way to develop specs and go back and forth with the user to clarify requirements and architecture.</p>
<p class="dst">Plan mode 是专门处理复杂任务的模式：先不写代码，而是和用户来回讨论，把需求、规格和架构澄清，再形成计划。它把“想清楚”从“写代码”里单独拆了出来。</p>
</div>

<div class="bilingual-pair">
<p class="src">Claude's prompt describes a workflow for generating plans. Phase one is understanding the user's requirements, and there's even a point where you kick off agents to explore the codebase. Phase two is design. Then there's a review phase, a final plan, and instructions to exit plan mode when you're done.</p>
<p class="dst">Claude 的 plan mode 提示词定义了一套流程：第一阶段理解需求，必要时还会启动子 agent 去探索代码库；第二阶段做设计；之后是审查、产出最终计划，最后退出 plan mode。整个过程的产物是一份可执行的计划文件。</p>
</div>

<div class="slide-block"><p class="slide-block-title">对应 PPT · Slide 12</p><div class="slide-strip"><figure class="slide"><a class="slide-link" href="assets/slides/9-24/12.png" target="_blank" rel="noopener noreferrer"><img src="assets/slides/9-24/12.png" alt="9-24 slide 12" loading="lazy"></a><figcaption>Slide 12</figcaption></figure></div></div>

<div class="bilingual-pair">
<p class="src">At their core, skills describe a written procedure. That can include multiple tool calls and scripts stitched together with prompts, allowing more elaborate tasks. Skills can be invoked proactively based on the context, or explicitly by the user.</p>
<p class="dst">skill 的本质，是把一套流程写成文字：它可以包含多次工具调用、脚本，以及穿插其间的提示词，从而完成更复杂的任务。调用方式有两种：用户可以显式点名，agent 也可以在上下文合适时主动触发。</p>
</div>

<div class="slide-block"><p class="slide-block-title">对应 PPT · Slide 13</p><div class="slide-strip"><figure class="slide"><a class="slide-link" href="assets/slides/9-24/13.png" target="_blank" rel="noopener noreferrer"><img src="assets/slides/9-24/13.png" alt="9-24 slide 13" loading="lazy"></a><figcaption>Slide 13</figcaption></figure></div></div>

<div class="bilingual-pair">
<p class="src">Subagents let you delegate parts of a task. You have a main orchestrator agent, the main control loop in Claude Code, and you can invoke helpers or workers with their own fresh context windows. That lets you parallelize work and define specific behaviors for different tasks.</p>
<p class="dst">subagent 用来把任务的一部分委派出去。主 agent 负责整体编排，维持主控制循环；它可以启动若干拥有独立上下文的“助手”或“工人”。这样既能并行处理，也能为不同类型的子任务定义专门的行为。</p>
</div>

<div class="bilingual-pair">
<p class="src">When those workers finish, they return their outputs to the main agent. The benefit is that each subagent starts with a fresh context rather than inheriting all the context of the parent. Its exploration happens outside the main control flow, and the result is brought back when it's done.</p>
<p class="dst">子 agent 完成后，只把结果交回主 agent。好处在于：它从一个干净的上下文开始，不必继承父会话的全部历史；探索过程发生在主线之外，结束以后只把结论带回来。这是控制上下文规模的一种手段。</p>
</div>

<div class="slide-block"><p class="slide-block-title">对应 PPT · Slide 14</p><div class="slide-strip"><figure class="slide"><a class="slide-link" href="assets/slides/9-24/14.png" target="_blank" rel="noopener noreferrer"><img src="assets/slides/9-24/14.png" alt="9-24 slide 14" loading="lazy"></a><figcaption>Slide 14</figcaption></figure></div></div>

<div class="bilingual-pair">
<p class="src">There are also hooks, which I'll touch on only briefly. The last big topic is compaction. You may have heard that term.</p>
<p class="dst">此外还有 hooks，这里只简单带过。最后一个大主题是 compaction，你可能已经听过这个词。</p>
</div>

### Compaction 与 model-vs-harness

<div class="slide-block"><p class="slide-block-title">对应 PPT · Slide 15</p><div class="slide-strip"><figure class="slide"><a class="slide-link" href="assets/slides/9-24/15.png" target="_blank" rel="noopener noreferrer"><img src="assets/slides/9-24/15.png" alt="9-24 slide 15" loading="lazy"></a><figcaption>Slide 15</figcaption></figure></div></div>

<div class="bilingual-pair">
<p class="src">When your context gets increasingly long, compaction is a way to consolidate and summarize it, reducing context bloat. Compaction happens in one of two ways: automatically, when you're about to exceed the context window; or manually, when you invoke it yourself.</p>
<p class="dst">当上下文越来越长时，compaction 会把它整理、压缩成摘要，减轻上下文膨胀。触发方式有两种：一是接近窗口上限时自动发生；二是用户主动调用。压缩后的摘要会取代原来的历史，成为模型之后看到的上下文。</p>
</div>

<div class="slide-block"><p class="slide-block-title">对应 PPT · Slide 16</p><div class="slide-strip"><figure class="slide"><a class="slide-link" href="assets/slides/9-24/16.png" target="_blank" rel="noopener noreferrer"><img src="assets/slides/9-24/16.png" alt="9-24 slide 16" loading="lazy"></a><figcaption>Slide 16</figcaption></figure></div></div>

<div class="bilingual-pair">
<p class="src">There are a lot of bells and whistles around the core loop, but the trend is toward simplicity. We still want fewer, more powerful tools. Harness designers are relying more on the capabilities of the underlying model rather than having the harness do the heavy lifting for difficult tasks.</p>
<p class="dst">核心循环周围有很多“花活”，但大趋势是简化：工具要少而强，harness 要尽量薄。设计者越来越倾向于依赖模型本身的能力，而不是让 harness 去替模型完成困难的部分。</p>
</div>

<div class="bilingual-pair">
<p class="src">That's a big question in agent design: do you invest in the model or the harness? Right now, we're at a point where people want the harness to be as simple and concise as possible. You can still do interesting things in it; just be careful about blowing up the context.</p>
<p class="dst">这引出了 agent 设计里的一个大问题：到底该投资模型，还是投资 harness？行业一直在两者之间摇摆。至少现在，主流倾向是让 harness 尽量简单、克制；harness 当然还能做很多事，但前提是别把上下文撑爆。</p>
</div>

<div class="bilingual-pair">
<p class="src">We'll talk about something called the “dumb zone.” It's an informal name for when the LLM starts getting less effective. We'll discuss how to avoid it, and many context-engineering principles come into play there.</p>
<p class="dst">后面还会讲到所谓的“dumb zone”。这不是正式术语，而是大家用来形容“上下文太长以后，模型开始变笨”的那个区间。如何避免它，正是 context engineering 要解决的问题。</p>
</div>

<div class="slide-block"><p class="slide-block-title">对应 PPT · Slide 17</p><div class="slide-strip"><figure class="slide"><a class="slide-link" href="assets/slides/9-24/17.png" target="_blank" rel="noopener noreferrer"><img src="assets/slides/9-24/17.png" alt="9-24 slide 17" loading="lazy"></a><figcaption>Slide 17</figcaption></figure></div></div>

## 学习者视角

### 关键收获

1. **Harness 才是 agent 的工程主体。** 模型负责推理，harness 负责把工具、上下文、权限、记忆和恢复机制组织起来。
2. **工具定义就是提示词。** docstring、类型、命名、错误信息，都会影响模型是否会正确调用工具。
3. **MCP 和 skill 分属两层。** MCP 提供一次外部调用，skill 编排多步流程。
4. **上下文预算是硬约束。** 工具列表、system prompt、CLAUDE.md、MCP server 都在争夺同一块窗口。
5. **“少而强”优于“多而碎”。** Bash、SQL 这类通用工具，往往比几十个细碎 endpoint 更有效。

### 放回课程里看

这节课是 Week 1 的“现场版架构图”。它和 [Dive into Claude Code](w1-dive-into-claude-code.html) 互补：论文给结构，课堂给 trace 和具体例子。

### 一个反直觉点

很多人以为工具越多，agent 越强。实际情况往往相反：**工具越多，模型越难选，上下文越脏，行为越不稳定。**

## 拓展

### 思考题

1. 如果只能给 agent 三个工具，你会选哪三个？为什么？
2. system prompt 变短说明了什么？哪些能力应该交给模型，哪些必须留在 harness？
3. CLAUDE.md 应该写“项目是什么”，还是“怎么操作”？边界在哪里？
4. subagent 和 compaction 都在解决上下文问题，它们各自适合什么场景？

### 练习

抓一次你自己的 coding agent trace，回答：

- 本次请求里，工具定义占了多少 token？
- system prompt 占了多少？
- 哪些工具这次完全没用到？
- 如果把工具列表减半，模型行为可能怎么变？

### 接着读

- [Dive into Claude Code：完整设计空间](w1-dive-into-claude-code.html)
- [课堂实录 9/29：RePPIT 与规格驱动开发](w2-lecture-9-29-transcript.html)
- [课堂实录 10/1：MCP 与 Code Mode](w2-lecture-10-1-transcript.html)
