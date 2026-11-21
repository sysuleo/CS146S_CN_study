---
title: "从构建 Claude Code 中学到的工具设计经验"
original: "Lessons from Building Claude Code"
week: "1"
slug: "w1-lessons-from-building-claude-code"
source_url: "https://x.com/trq212/status/2027463795355095314?s=20"
author: "Thariq"
date: "2026"
kind: "X 长帖"
coverage: "全文精译"
minutes: "8"
blurb: "工具不是越多越好。Claude Code 团队如何通过提问、任务、搜索三类工具，塑造 agent 的行为和上下文。"
---

## 总结

这篇文章讲的是：**给 coding agent 设计工具，不是把 API 一个个包成函数，而是在设计它的action space。**

- 工具应该贴合模型当前的能力；模型变强后，曾经必要的工具可能变成限制。
- `AskUserQuestion` 经过三次迭代，最后选择“独立工具 + 阻塞式 UI”，而不是改输出格式。
- `TodoWrite` 最终被 `Task` 取代：前者让模型保持轨道，后者让多个 subagent 协作。
- 搜索工具让 Claude 自己构建上下文；progressive disclosure 让它按需逐层发现信息。
- 工具设计是艺术加科学，必须持续实验、读输出、观察模型如何犯错。

## 原文逐段对照翻译

> **翻译说明：**以下按原文顺序逐段翻译，保留作者的全部技术论证和例子；中文以自然、准确为目标。

<figure class="article-figure">
<a href="assets/figures/w1-lessons/cover.png" target="_blank" rel="noopener noreferrer"><img src="assets/figures/w1-lessons/cover.png" alt="Lessons from Building Claude Code"></a>
<figcaption>原文封面图。原文：Lessons from Building Claude Code: Seeing like an Agent.</figcaption>
</figure>

### action space：给人挑工具，也给 agent 挑工具

<div class="bilingual-pair">
<p class="src">One of the hardest parts of building an agent harness is constructing its action space. Claude acts through Tool Calling, but there are a number of ways tools can be constructed in the Claude API with primitives like bash, skills and recently code execution.</p>
<p class="dst">构建 agent harness 最难的部分之一，是设计它的action space。Claude 通过 Tool Calling 行动，但在 Claude API 里，工具有很多种构造方式：bash、skills，以及最近的 code execution。</p>
</div>

<div class="bilingual-pair">
<p class="src">Given all these options, how do you design the tools of your agent? Do you need just one tool like code execution or bash? What if you had 50 tools, one for each use case your agent might run into?</p>
<p class="dst">面对这些选择，你该怎么设计 agent 的工具？是只给一个 code execution 或 bash 这样的通用工具，还是给 50 个工具、每个场景一个？</p>
</div>

<div class="bilingual-pair">
<p class="src">To put myself in the mind of the model I like to imagine being given a difficult math problem. What tools would you want in order to solve it? It would depend on your own skills. Paper would be the minimum, but you'd be limited by manual calculations. A calculator would be better, but you would need to know how to operate the more advanced options. The fastest and most powerful option would be a computer, but you would have to know how to use it to write and execute code.</p>
<p class="dst">作者喜欢用“解一道难题”来代入模型的视角：你会想要什么工具？这取决于你自己的能力。纸笔是最低配置，但只能手算；计算器更好，但你得会用高级功能；最快最强的是电脑，但前提是你会写代码、会执行代码。</p>
</div>

<div class="bilingual-pair">
<p class="src">This is a useful framework for designing your agent. You want to give it tools that are shaped to its own abilities. But how do you know what those abilities are? You pay attention, read its outputs, experiment. You learn to see like an agent.</p>
<p class="dst">这就是设计 agent 工具的好框架：工具要贴合它自己的能力。但你怎么知道它现在具备什么能力？答案是观察输出、做实验、读它失败的方式——也就是学会“像 agent 一样看问题”。</p>
</div>

### AskUserQuestion：让 agent 更会提问

<figure class="article-figure">
<a href="assets/figures/w1-lessons/elicitation.png" target="_blank" rel="noopener noreferrer"><img src="assets/figures/w1-lessons/elicitation.png" alt="Improving elicitation"></a>
<figcaption>原文图：AskUserQuestion / elicitation 的设计。原文配图。</figcaption>
</figure>

<div class="bilingual-pair">
<p class="src">When building the AskUserQuestion tool, our goal was to improve Claude's ability to ask questions, often called elicitation. While Claude could just ask questions in plain text, we found answering those questions felt like they took an unnecessary amount of time. How could we lower this friction and increase the bandwidth of communication between the user and Claude?</p>
<p class="dst">做 `AskUserQuestion` 工具时，目标是提升 Claude 的提问能力，也就是所谓的 elicitation。Claude 当然可以用自然语言直接问，但用户回答起来很慢。团队想降低摩擦，提高人机沟通的带宽。</p>
</div>

<div class="bilingual-pair">
<p class="src">Attempt #1: Editing the ExitPlanTool. The first thing we tried was adding a parameter to the ExitPlanTool to have an array of questions alongside the plan. This was the easiest thing to implement, but it confused Claude because we were simultaneously asking for a plan and a set of questions about the plan.</p>
<p class="dst">第一次尝试：改 `ExitPlanTool`。他们在退出计划模式的工具里加了一个问题数组。实现最简单，但 Claude 被搞糊涂了：它同时要给出计划，又要问关于计划的问题；如果用户回答和计划冲突怎么办？</p>
</div>

<div class="bilingual-pair">
<p class="src">Attempt #2: Changing Output Format. Next we tried modifying Claude's output instructions to serve a slightly modified markdown format that it could use to ask questions. While this was the most general change we could make, it was not guaranteed. Claude would append extra sentences, omit options, or use a different format altogether.</p>
<p class="dst">第二次尝试：改输出格式。让 Claude 输出一种特殊 Markdown，例如“问题 + 方括号选项”，前端再解析成 UI。这个方案最通用，但不保证稳定：Claude 会多写句子、漏掉选项，或者干脆换一种格式。</p>
</div>

<div class="bilingual-pair">
<p class="src">Attempt #3: The AskUserQuestion Tool. Finally, we landed on creating a tool that Claude could call at any point, but it was particularly prompted to do so during plan mode. When the tool triggered we would show a modal to display the questions and block the agent's loop until the user answered.</p>
<p class="dst">第三次尝试：做成独立工具。最终方案是 `AskUserQuestion`：Claude 可以在任何时候调用，但在 plan mode 下会被特别提示去调用。工具触发后，前端弹出模态框展示问题，并阻塞 agent 循环，直到用户回答。</p>
</div>

<div class="bilingual-pair">
<p class="src">This tool allowed us to prompt Claude for a structured output and it helped us ensure that Claude gave the user multiple options. Most importantly, Claude seemed to like calling this tool and we found its outputs worked well. Even the best designed tool doesn't work if Claude doesn't understand how to call it.</p>
<p class="dst">这个方案强制了结构化输出，保证给出多个选项，还能被 Agent SDK、skills 复用。最重要的是，Claude 自己“愿意”调用它。再好的工具，如果模型不知道怎么调用，也等于不存在。</p>
</div>

### 从 TodoWrite 到 Task：能力变了，工具也要变

<figure class="article-figure">
<a href="assets/figures/w1-lessons/attempt3.png" target="_blank" rel="noopener noreferrer"><img src="assets/figures/w1-lessons/attempt3.png" alt="AskUserQuestion tool"></a>
<figcaption>原文图：AskUserQuestion 工具的最终形态。原文配图。</figcaption>
</figure>

<figure class="article-figure">
<a href="assets/figures/w1-lessons/tasks.png" target="_blank" rel="noopener noreferrer"><img src="assets/figures/w1-lessons/tasks.png" alt="Tasks and todos"></a>
<figcaption>原文图：从 TodoWrite 到 Task 的能力演进。原文配图。</figcaption>
</figure>

<div class="bilingual-pair">
<p class="src">When we first launched Claude Code, we realized that the model needed a Todo list to keep it on track. To do this we gave Claude the TodoWrite tool. But even then we often saw Claude forgetting what it had to do. To adapt, we inserted system reminders every 5 turns.</p>
<p class="dst">Claude Code 刚发布时，模型需要一个 Todo 列表来保持轨道，于是有了 `TodoWrite`。但模型经常忘记自己要做什么，团队只好每 5 轮插入一次系统提醒，把目标重新告诉它。</p>
</div>

<div class="bilingual-pair">
<p class="src">But as models improved, they not only did not need to be reminded of the Todo List but could find it limiting. Being sent reminders of the todo list made Claude think that it had to stick to the list instead of modifying it. We also saw Opus 4.5 get much better at using subagents, but how could subagents coordinate on a shared Todo List?</p>
<p class="dst">模型变强后，问题反过来了：它不再需要被提醒，提醒反而让它以为必须严格遵守列表、不敢修改。同时，Opus 4.5 更擅长使用 subagent，但多个 subagent 如何共享一份 Todo？</p>
</div>

<div class="bilingual-pair">
<p class="src">Seeing this, we replaced TodoWrite with the Task Tool. Whereas Todos were about keeping the model on track, Tasks were more about helping agents communicate with each other. Tasks could include dependencies, share updates across subagents and the model could alter and delete them.</p>
<p class="dst">于是 `TodoWrite` 被 `Task` 取代。Todo 是“让模型别跑偏”，Task 是“让 agent 之间能沟通”：任务可以有依赖、可以共享更新、可以被修改和删除。</p>
</div>

<div class="bilingual-pair">
<p class="src">As model capabilities increase, the tools that your models once needed might now be constraining them. It's important to constantly revisit previous assumptions on what tools are needed. This is also why it's useful to stick to a small set of models to support that have a fairly similar capabilities profile.</p>
<p class="dst">模型能力提升后，曾经帮助它的工具可能变成约束。团队要不断重新审视旧假设，也要尽量只支持一组能力相近的模型，避免为每个模型维护一套工具。</p>
</div>

### 搜索接口：让 agent 自己构建上下文

<div class="bilingual-pair">
<p class="src">When Claude Code first came out, we used a RAG vector database to find context for Claude. While RAG was powerful and fast it required indexing and setup and could be fragile across a host of different environments. More importantly, Claude was given this context instead of finding the context itself.</p>
<p class="dst">Claude Code 最早用 RAG 向量数据库找上下文。RAG 很快，但需要索引、配置，在不同环境里容易变脆；更重要的是，上下文是“被给”的，不是 Claude 自己找的。</p>
</div>

<div class="bilingual-pair">
<p class="src">But if Claude could search on the web, why not search your codebase? By giving Claude a Grep tool, we could let it search for files and build context itself. This is a pattern we've seen as Claude gets smarter: it becomes increasingly good at building its context if it's given the right tools.</p>
<p class="dst">既然 Claude 能搜网页，为什么不能搜代码库？给它一个 `Grep` 工具，它就能自己找文件、自己拼上下文。模型越聪明，只要工具合适，它构建上下文的能力就越强。</p>
</div>

<div class="bilingual-pair">
<p class="src">When we introduced Agent Skills we formalized the idea of progressive disclosure, which allows agents to incrementally discover relevant context through exploration. Claude could read skill files and those files could then reference other files that the model could read recursively.</p>
<p class="dst">引入 Agent Skills 后，团队把“渐进式披露”正式化了：agent 先读 skill 文件，skill 再引用其他文件，模型可以递归地读下去，逐层发现需要的信息。</p>
</div>

<div class="bilingual-pair">
<p class="src">For example, we noticed that Claude did not know enough about how to use Claude Code. We could have put all of this information in the system prompt, but users rarely asked about this, so it would have added context rot. Instead, we built the Claude Code Guide subagent.</p>
<p class="dst">例如，Claude 原本不太了解 Claude Code 自身怎么用。把所有文档塞进 system prompt 会污染上下文，因为用户很少问这些。团队最后做了 `Claude Code Guide` subagent：用户问 Claude Code 自身时，由它去查文档并返回答案。</p>
</div>

<div class="bilingual-pair">
<p class="src">Claude Code currently has around 20 tools, and we are constantly asking ourselves if we need all of them. The bar to add a new tool is high, because this gives the model one more option to think about.</p>
<p class="dst">Claude Code 长期维持在约 20 个工具，团队不断问自己“真的都需要吗”。新增工具的门槛很高，因为每多一个工具，模型就多一层决策负担。</p>
</div>

### 这是艺术，不是科学

<figure class="article-figure">
<a href="assets/figures/w1-lessons/art.png" target="_blank" rel="noopener noreferrer"><img src="assets/figures/w1-lessons/art.png" alt="An art not a science"></a>
<figcaption>原文图：工具设计是艺术，不是科学。原文配图。</figcaption>
</figure>

<div class="bilingual-pair">
<p class="src">If you were hoping for a set of rigid rules on how to build your tools, unfortunately that is not this guide. Designing the tools for your models is as much an art as it is a science. It depends heavily on the model you're using, the goal of the agent and the environment it's operating in.</p>
<p class="dst">如果你想要一套死规则，这篇文章给不了。工具设计既是科学也是艺术，取决于模型、agent 目标和运行环境。</p>
</div>

<div class="bilingual-pair">
<p class="src">Experiment often, read your outputs, try new things. See like an agent.</p>
<p class="dst">多实验、多读输出、多试新东西。学会像 agent 一样看问题。</p>
</div>

## 学习者视角

### 关键收获

1. **工具是行为塑形器。** 给什么工具，agent 就会形成什么工作方式。
2. **结构化交互优于解析自然语言。** `AskUserQuestion` 的价值在于把提问变成可渲染、可复用、可阻塞的协议。
3. **工具会过期。** TodoWrite 不是设计错了，而是模型能力变了。
4. **上下文获取应尽量交给 agent。** Grep、skills、progressive disclosure 都在把“找信息”的责任转给模型。
5. **少而精的工具集是刻意选择。** 每增加一个工具，模型就多一层选择成本。

### 放回课程里看

这篇是 Week 1 的核心：它把 agent loop 落到了具体工具设计。可以配合 [Dive into Claude Code](w1-dive-into-claude-code.html) 一起读：前者讲“为什么这样设计工具”，后者讲“这些工具如何嵌进完整架构”。

### 一个反直觉点

很多人以为工具越多，agent 越强。这篇文章的结论相反：**工具越多，选择成本越高，行为越不稳定。** 重要的是工具的形状，不是数量。

## 拓展

### 思考题

1. 如果你的 agent 经常“不问清楚就开干”，你会改 prompt、改输出格式，还是新增一个提问工具？
2. 你项目里有哪些“TodoWrite 式”的工具，其实已经被模型能力淘汰了？
3. Progressive disclosure 和 RAG 各自的适用边界是什么？

### 练习

为一个“代码审查 agent”设计 5 个以内的工具：

- 每个工具能用一句话说明“什么时候调用”；
- 至少一个负责“向人提问”；
- 至少一个负责“让 agent 自己找上下文”；
- 写下你刻意不提供的工具，以及原因。

### 接着读

- [Dive into Claude Code：完整设计空间](w1-dive-into-claude-code.html)
- [The Context Tax：上下文成本与压缩](w2-the-context-tax-when-to-compact.html)
- [Steering Claude Code：七种指令机制](w4-steering-claude-code.html)
