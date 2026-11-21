---
title: "课堂实录：MCP、工具设计与 Code Mode（10/1）"
original: "CS146S Lecture Transcript — October 1, 2026"
week: "2"
slug: "w2-lecture-10-1-transcript"
source_url: "https://themodernsoftware.dev/materials/10-1-26-transcript.txt"
author: "Mihail Eric"
date: "2026-10-01"
kind: "课堂实录"
coverage: "逐段精译"
minutes: "20"
blurb: "MCP 如何把 M×N 变成 M+N，为什么工具膨胀会拖垮上下文，以及 Code Mode 如何用 search + execute 省下 90% token。"
---

## 总结

这节课回答了三个问题：**MCP 到底解决什么问题、为什么大多数 MCP server 的工具设计是错的、以及如何用 Code Mode 把工具数量压下来。**

- MCP 把 M 个模型与 N 个服务之间的 M×N 连接，变成 M+N。
- 术语要分清：host、client、server、tool。
- 第一次请求时，client 用 `tools/list` 发现工具，host 把 schema 注入上下文。
- 工具膨胀是默认结果：早期 GitHub MCP 有 110–150 个工具，Cursor 只能加载 88 个。
- 好工具按“用户想完成的结果”设计，而不是把 API endpoint 一对一包成工具。
- 工具的参数、类型、docstring、错误信息、命名，全都是给模型看的上下文。
- Code Mode 只暴露 search + execute，让模型写代码按需调用工具，token 可降 90% 以上。

## 原文逐段对照翻译

> **翻译说明：**以下按讲课顺序逐段对照翻译，覆盖技术讲授与技术问答；课程行政、重复表述和现场寒暄从略。中文以准确、自然为目标。

<div class="slide-block"><p class="slide-block-title">对应 PPT · Slide 1</p><div class="slide-strip"><figure class="slide"><a class="slide-link" href="assets/slides/10-1/01.png" target="_blank" rel="noopener noreferrer"><img src="assets/slides/10-1/01.png" alt="10-1 slide 1" loading="lazy"></a><figcaption>Slide 1</figcaption></figure></div></div>

### 课程要求：AI Slop 直接 0 分

<div class="slide-block"><p class="slide-block-title">对应 PPT · Slide 2</p><div class="slide-strip"><figure class="slide"><a class="slide-link" href="assets/slides/10-1/02.png" target="_blank" rel="noopener noreferrer"><img src="assets/slides/10-1/02.png" alt="10-1 slide 2" loading="lazy"></a><figcaption>Slide 2</figcaption></figure></div></div>

<div class="bilingual-pair">
<p class="src">One hard requirement for grading: if you're going to put up an AI-slop PR, that's not going to work. The maintainers are being gracious with their time. They're making themselves available to review our code, PRs, and contributions. Review your code and make sure you're not just slop-grenading your teammates.</p>
<p class="dst">评分有一条硬性要求：提交 AI 垃圾 PR 是行不通的。合作方的维护者是自愿拿出时间帮我们 review 代码和 PR 的。你要先自己 review，别把一堆没消化的东西直接丢给队友。</p>
</div>

<div class="bilingual-pair">
<p class="src">For this assignment, AI slop gets a zero. That's a hard line in the sand, and we'll defer to the maintainers on it. You can use AI coding agents to generate your PRs, of course. You should; that's the whole point of the class. But you shouldn't think, "This is due in an hour," write something, submit it, and put it on Gradescope.</p>
<p class="dst">这次作业，AI slop 直接 0 分，没有商量余地，最终以维护者的判断为准。当然可以用 AI 生成 PR，这本来就是课程的目的；但不能因为“一小时后截止”就随便写点东西交上去。</p>
</div>

<div class="slide-block"><p class="slide-block-title">对应 PPT · Slide 3</p><div class="slide-strip"><figure class="slide"><a class="slide-link" href="assets/slides/10-1/03.png" target="_blank" rel="noopener noreferrer"><img src="assets/slides/10-1/03.png" alt="10-1 slide 3" loading="lazy"></a><figcaption>Slide 3</figcaption></figure></div></div>

### MCP 是什么

<div class="slide-block"><p class="slide-block-title">对应 PPT · Slide 4</p><div class="slide-strip"><figure class="slide"><a class="slide-link" href="assets/slides/10-1/04.png" target="_blank" rel="noopener noreferrer"><img src="assets/slides/10-1/04.png" alt="10-1 slide 4" loading="lazy"></a><figcaption>Slide 4</figcaption></figure></div></div>

<div class="bilingual-pair">
<p class="src">LLMs today are pretrained systems. To a large extent, what they've learned in their parameters is static information: a point-in-time snapshot of the data they were trained on. When we want to use them in a modern context, reacting to things happening in the world and to the most up-to-date versions of systems, we need to extend their functionality beyond the pretrained weights.</p>
<p class="dst">今天的 LLM 是预训练系统。参数里学到的知识，很大程度上是静态的——训练数据在某个时间点的快照。要让它对现实世界正在发生的事、对系统的最新状态作出反应，就必须把能力扩展到预训练权重之外。</p>
</div>

<div class="slide-block"><p class="slide-block-title">对应 PPT · Slide 5</p><div class="slide-strip"><figure class="slide"><a class="slide-link" href="assets/slides/10-1/05.png" target="_blank" rel="noopener noreferrer"><img src="assets/slides/10-1/05.png" alt="10-1 slide 5" loading="lazy"></a><figcaption>Slide 5</figcaption></figure></div></div>

<div class="bilingual-pair">
<p class="src">MCP stands for Model Context Protocol. It's an open protocol developed by Anthropic. It allows systems, such as wrappers around APIs, to provide relevant context to AI models in a way that generalizes across the underlying system or API. In the simplest terms, MCP provides a standard format and protocol for exposing tools to LLMs.</p>
<p class="dst">MCP 全称 Model Context Protocol，是 Anthropic 提出的开放协议。它让各种系统——通常是 API 的封装——以统一方式向 AI 模型提供上下文，而不必为每个底层系统单独适配。最简单的说法是：MCP 定义了“把工具暴露给 LLM”的标准格式和协议。</p>
</div>

<div class="bilingual-pair">
<p class="src">These aren't just tools we develop locally, but tools from third-party services or systems. If you're interacting with Gmail or DoorDash, you don't want to build the integration yourself and expose it to your LLM. Ideally, the service provider exposes it through MCP, and you just connect.</p>
<p class="dst">这些工具不只来自本地，也来自第三方服务。要接 Gmail 或 DoorDash，你不应该自己从头写集成再暴露给模型。更合理的做法是：服务方通过 MCP 暴露能力，你直接接上。</p>
</div>

### 从 M×N 到 M+N

<div class="slide-block"><p class="slide-block-title">对应 PPT · Slide 6</p><div class="slide-strip"><figure class="slide"><a class="slide-link" href="assets/slides/10-1/06.png" target="_blank" rel="noopener noreferrer"><img src="assets/slides/10-1/06.png" alt="10-1 slide 6" loading="lazy"></a><figcaption>Slide 6</figcaption></figure></div></div>

<div class="bilingual-pair">
<p class="src">Traditionally, when we wanted to connect coding agents or LLMs to third-party services, we had to build connectors for every point-to-point solution. If you had M LLMs or coding agents on one side and N services on the other, you needed M × N connectors between the hosts or agents and the underlying tools.</p>
<p class="dst">过去要把 LLM 或 coding agent 接到第三方服务，只能做点对点连接器。假设一边有 M 个模型/agent，另一边有 N 个服务，那就需要 M×N 个连接器。</p>
</div>

<div class="slide-block"><p class="slide-block-title">对应 PPT · Slide 7</p><div class="slide-strip"><figure class="slide"><a class="slide-link" href="assets/slides/10-1/07.png" target="_blank" rel="noopener noreferrer"><img src="assets/slides/10-1/07.png" alt="10-1 slide 7" loading="lazy"></a><figcaption>Slide 7</figcaption></figure></div></div>

<div class="bilingual-pair">
<p class="src">MCP provides a more efficient way to do this. We don't have to reimplement the standard pieces common across connectors, including authentication, error handling, rate limiting, and many of the things we'd otherwise have to think about when building an API connector.</p>
<p class="dst">MCP 把这些通用部分标准化了：认证、错误处理、限流，以及其他每个 API 连接器都要重复处理的琐事，都不必在每个连接里重写一遍。</p>
</div>

<div class="slide-block"><p class="slide-block-title">对应 PPT · Slide 8</p><div class="slide-strip"><figure class="slide"><a class="slide-link" href="assets/slides/10-1/08.png" target="_blank" rel="noopener noreferrer"><img src="assets/slides/10-1/08.png" alt="10-1 slide 8" loading="lazy"></a><figcaption>Slide 8</figcaption></figure></div></div>

<div class="bilingual-pair">
<p class="src">As long as the LLM side knows how to speak MCP and the connector side speaks the other side of the protocol, you don't have to recreate all those aspects. You handle those pieces once. The value is going from M × N to M + N.</p>
<p class="dst">只要模型侧会说 MCP，服务侧实现协议的另一端，这些通用能力就只需要做一次。连接数量从 M×N 降为 M+N。M 和 N 越大，收益越明显。</p>
</div>

### Host、Client、Server、Tool

<div class="slide-block"><p class="slide-block-title">对应 PPT · Slide 9</p><div class="slide-strip"><figure class="slide"><a class="slide-link" href="assets/slides/10-1/09.png" target="_blank" rel="noopener noreferrer"><img src="assets/slides/10-1/09.png" alt="10-1 slide 9" loading="lazy"></a><figcaption>Slide 9</figcaption></figure></div></div>

<div class="bilingual-pair">
<p class="src">The host is what we mean when we say Cursor or Claude Desktop. The MCP client is effectively a library sitting on the host. The protocol defines the client, and the client maintains a stateful session per server.</p>
<p class="dst">Host 指的是 Cursor、Claude Desktop 这类宿主程序。MCP client 是运行在 host 里的客户端库，负责按协议维护与每个 server 的有状态会话。</p>
</div>

<div class="bilingual-pair">
<p class="src">A server is a wrapper around a third-party or first-party tool. With third-party tools, you usually interact over the wire through a protocol such as HTTP. If you're building your own MCP server, you'll often keep it local. Your coding agent can then talk to it through stdio.</p>
<p class="dst">Server 是对第三方或第一方工具的封装。接第三方服务时，通常通过网络协议（比如 HTTP）通信；自己写 MCP server 时，一般跑在本地，agent 通过 stdio 和它对话。</p>
</div>

<div class="bilingual-pair">
<p class="src">The last term is "tool." In MCP, think of a tool almost like an API, with big air quotes. It's not exactly an API, but it is a callable function you expose to a client of the protocol.</p>
<p class="dst">最后是 tool。可以把 MCP 里的工具近似理解成 API，但要打个大引号：它不是严格的 REST API，而是你通过协议暴露给 client 的可调用函数。</p>
</div>

### 一次 MCP 调用的流程

<div class="slide-block"><p class="slide-block-title">对应 PPT · Slide 10</p><div class="slide-strip"><figure class="slide"><a class="slide-link" href="assets/slides/10-1/10.png" target="_blank" rel="noopener noreferrer"><img src="assets/slides/10-1/10.png" alt="10-1 slide 10" loading="lazy"></a><figcaption>Slide 10</figcaption></figure></div></div>

<div class="bilingual-pair">
<p class="src">At a high level, when you're interacting with an MCP server, the client typically starts with discovery. The client asks an MCP server, or a set of servers, "What tools are available to me?" That's the first line here: the client calls tools/list.</p>
<p class="dst">一次典型交互从“发现”开始。client 会问一个或多个 MCP server：“你有哪些工具？”对应协议里的 `tools/list` 调用。</p>
</div>

<div class="bilingual-pair">
<p class="src">The servers return JSON describing each tool: its name, summary, and JSON schema. The host then injects that information into the model's context. A user request triggers the model. If the model decides it should use an MCP tool, it emits a structured tool call based on the definitions it received.</p>
<p class="dst">server 返回 JSON，描述每个工具的名称、简介和 JSON schema。host 把这些信息注入模型上下文。用户请求触发模型后，模型如果决定使用某个工具，就根据收到的定义发出结构化的 tool call。</p>
</div>

<div class="bilingual-pair">
<p class="src">The local or remote MCP server executes the call, returns the response, and the conversation resumes. In this toy example, we've connected three third-party services through MCP servers: Gmail, S3, and DoorDash. The user asks the system to summarize emails from Jack.</p>
<p class="dst">本地或远程 server 执行调用，返回结果，对话继续。课堂上的玩具例子接了 Gmail、S3、DoorDash 三个服务，用户说“帮我总结 Jack 的邮件”。</p>
</div>

<div class="bilingual-pair">
<p class="src">The important thing is that we didn't implement them. They're third-party servers defined by developers elsewhere. We've authenticated to those servers through OAuth, and discovery returns the tools we can use. The LLM identifies Gmail as relevant and returns a structured tool call.</p>
<p class="dst">关键点是：这些 server 不是我们写的，而是第三方开发者提供的。我们通过 OAuth 完成认证，discovery 返回可用工具。模型判断 Gmail 相关，于是发出对应的工具调用。</p>
</div>

### 工具膨胀：MCP 最大的坑

<div class="bilingual-pair">
<p class="src">By default, you get all the tools. If you remember the Claude harness trace I showed, it was around 10,000 lines of JSONL. The actual conversation, including prompts, was maybe 600 or 700 lines. The rest was all the available tools: schemas, expected arguments, and names.</p>
<p class="dst">默认情况下，所有工具都会暴露。还记得之前展示的 Claude harness trace 吗？整个 JSONL 大约一万行，真正的对话只有六七百行，其余全是工具定义：schema、参数、名称。</p>
</div>

<div class="bilingual-pair">
<p class="src">This is a considerable limitation of MCP. With the naive version, you'll hit tool issues very quickly. Part of the problem is saturating your context. The other part is confusing the LLM. Past a certain number of tokens, it's hard to reason about that many tools.</p>
<p class="dst">这是 MCP 的一个重大限制。用最朴素的方式接工具，很快就会出问题：一方面上下文被塞满，另一方面模型被大量工具搞糊涂。token 超过某个量级后，让它同时推理几十上百个工具会非常困难。</p>
</div>

<div class="bilingual-pair">
<p class="src">In the early days, people naively built servers with a one-to-one mapping from API endpoints to MCP tools. If you connected to the GitHub MCP server, there were something like 150 tools. You could use one server, and that was about it. There wasn't room for much else.</p>
<p class="dst">早期大家很自然地按“一个 API endpoint 对应一个 MCP 工具”来做。GitHub MCP server 一接上就有 150 个左右的工具，光这一个 server 就快把上下文占满了，别的服务几乎放不下。</p>
</div>

<div class="bilingual-pair">
<p class="src">I remember when Cursor only allowed 88 tools in the IDE. You couldn't even load some servers in their entirety. GitHub alone gave you something like 120 to 150 tools. It wasn't a good system.</p>
<p class="dst">Cursor 有一段时间在 IDE 里只允许 88 个工具。有些 server 甚至没法完整加载，GitHub 一个就 120 到 150 个。那套系统并不好用。</p>
</div>

### 设计原则一：按结果设计，而不是按端点

<div class="slide-block"><p class="slide-block-title">对应 PPT · Slide 11</p><div class="slide-strip"><figure class="slide"><a class="slide-link" href="assets/slides/10-1/11.png" target="_blank" rel="noopener noreferrer"><img src="assets/slides/10-1/11.png" alt="10-1 slide 11" loading="lazy"></a><figcaption>Slide 11</figcaption></figure></div></div>

<div class="bilingual-pair">
<p class="src">You shouldn't think of an MCP server as just a REST API wrapper. LLMs reason about the context you provide. API endpoints were designed for human consumption, and sometimes not even particularly well for humans. That isn't necessarily the best way for an LLM to consume the information.</p>
<p class="dst">不要把 MCP server 只当成 REST API 的包装。模型是靠你提供的上下文来推理的，而 API endpoint 是为人设计的，有时连人都觉得难用，更不一定适合模型消费。</p>
</div>

<div class="bilingual-pair">
<p class="src">A one-to-one mapping leaves something on the table. There are plenty of bad APIs and endpoints that work but are hard for an LLM to reason about because they're too granular. If you have a get-X tool for every possible resource, the API definitions alone might saturate the context window.</p>
<p class="dst">一对一映射会浪费能力。很多 API 能用，但太细碎，模型很难推理。如果每种资源都有一个 `get-X`，光工具定义就可能把上下文窗口塞满。</p>
</div>

<div class="bilingual-pair">
<p class="src">The suggested practice is to design tool definitions around outcomes rather than individual operations. Consider two ways of doing the same thing. Option one is "send payment to this user's email." You provide the email, send the payment, and you're done.</p>
<p class="dst">推荐做法是围绕“结果”设计工具，而不是围绕“单个操作”。比如给某个邮箱付款：好设计是一个 `send_payment_to_email`，传入邮箱和金额，内部把后续步骤都处理掉。</p>
</div>

<div class="bilingual-pair">
<p class="src">Option two follows a more traditional API-to-tool mapping. The API only defined "send payment to account." You first have to get the email from the user ID, list the accounts for that email, and then send the payment using the account ID. That's three tool calls you have to get right in succession.</p>
<p class="dst">坏设计是照搬 API：接口只提供“给账户付款”。你得先从 user ID 拿到邮箱，再用邮箱列出账户，最后用 account ID 付款。三次调用必须依次做对，每一步都可能出错。</p>
</div>

<div class="bilingual-pair">
<p class="src">This approach focuses on the semantics of what we want LLMs to do. Traditional APIs weren't necessarily designed around semantics; they were designed to expose or modify each piece of data.</p>
<p class="dst">区别就在于：前者按“我们想让模型完成什么”来设计，后者按“系统里有哪些数据操作”来设计。传统 API 关心的是暴露和修改数据，不一定关注意图。</p>
</div>

### 设计原则二：一切写给模型看

<div class="bilingual-pair">
<p class="src">Another practice is being explicit about arguments. Type annotations, docstrings, and function names are all part of the context the LLM uses to reason about what to do. A lazy approach in Python might be to use *args and **kwargs everywhere. It works, but it's confusing for an LLM.</p>
<p class="dst">另一个原则是把参数写清楚。类型标注、docstring、函数名，都会进入模型上下文，影响它怎么推理。Python 里图省事可以用 `*args`、`**kwargs`，代码能跑，但模型很难判断到底该传什么。</p>
</div>

<div class="bilingual-pair">
<p class="src">A common early failure was a mismatch between the arguments and the tool call. The model selected the right tool but supplied the wrong arguments. We weren't strict enough about telling it what needed to be true of the function call.</p>
<p class="dst">早期最常见的问题之一，就是工具选对了、参数传错了。原因往往是我们没有把“这个调用需要满足什么条件”说清楚。</p>
</div>

<div class="bilingual-pair">
<p class="src">Avoid massive, untyped dictionaries. You can use a dictionary, but use Pydantic or type annotations to describe it. That gives the LLM a more meaningful hint than arbitrary inputs. Instructions are context, docstrings are context, and every annotation is context.</p>
<p class="dst">不要用巨大、无类型的字典。可以用 dict，但要用 Pydantic 或类型标注描述结构。指令是上下文，docstring 是上下文，每一个类型标注也是上下文。</p>
</div>

<div class="bilingual-pair">
<p class="src">That includes error messages. Even something as benign as raising a generic Exception instead of a ValueError, NameError, or a custom error type matters. Opt for specific or custom error types. They provide hints that help the LLM interpret errors and debug.</p>
<p class="dst">错误信息也一样。抛一个泛泛的 `Exception`，和抛 `ValueError`、`NameError` 或自定义错误，对模型的意义完全不同。越具体的错误类型，越能帮助模型理解问题并调试。</p>
</div>

### 设计原则三：先铺开，再看 trace 合并

<div class="bilingual-pair">
<p class="src">In practice, it's hard to predict the optimal semantics to expose to an LLM. Often, you're not very thoughtful about tool design initially. You go a little crazy to get high coverage and support every case you can think of. Then you realize you have 100 tools and need to reduce that number.</p>
<p class="dst">现实中很难一开始就预测出最优的工具语义。通常的做法是：先尽量铺开，覆盖各种能想到的场景；等发现工具到了 100 个、模型开始混乱，再回头做减法。</p>
</div>

<div class="bilingual-pair">
<p class="src">At that point, you consolidate. You look at the LLM's traces and identify common patterns. For example, you might have separate tools for searching meetings, transcripts, and Slack threads. One way to consolidate them is to make a search_resource tool, with the resource to search as a parameter.</p>
<p class="dst">合并时要看 trace，找常见模式。比如原来有搜会议、搜转录、搜 Slack 三个工具，可以合并成一个 `search_resource(resource_type, query)`，把“搜什么”变成参数。</p>
</div>

<div class="bilingual-pair">
<p class="src">When you designed the first tools, you might not even have supported Slack or email. How could you predict that you'd need something general-purpose across channels? Usually, you start eagerly, throw things at the wall, and see what sticks. Then the LLM gets confused, so you consolidate. It's refactoring.</p>
<p class="dst">设计第一批工具时，你可能还没接 Slack 或邮件，根本想不到需要一个跨渠道的通用搜索。所以流程通常是：先积极试，看看什么有效；模型开始混乱后，再重构、合并。这和代码重构是一个道理。</p>
</div>

<div class="bilingual-pair">
<p class="src">If you know it will be broadly exposed, think carefully about the design, the consumers, and the different classes of consumers. If it's only for yourself, you can probably get away with less rigorous practices. Software engineering is what happens when you add time and people to programming.</p>
<p class="dst">如果工具要广泛分发，就要认真考虑设计、消费者和不同用户类型；如果只给自己用，可以宽松一些。有句话说得很好：软件工程，是“编程”加上“时间和人”之后才发生的事。</p>
</div>

### Code Mode：Search + Execute

<div class="slide-block"><p class="slide-block-title">对应 PPT · Slide 12</p><div class="slide-strip"><figure class="slide"><a class="slide-link" href="assets/slides/10-1/12.png" target="_blank" rel="noopener noreferrer"><img src="assets/slides/10-1/12.png" alt="10-1 slide 12" loading="lazy"></a><figcaption>Slide 12</figcaption></figure></div></div>

<div class="bilingual-pair">
<p class="src">The basic approach is to create a meta MCP server between you and the other servers. It exposes just two tools: search and execute. Search finds relevant servers, tools, and definitions. Execute performs the operation after you've searched and narrowed down the relevant candidates.</p>
<p class="dst">现代做法之一，是在 agent 和其他 server 之间放一个 meta server，只暴露两个工具：search 和 execute。search 负责找到相关 server、工具和定义；execute 在筛选之后执行操作。</p>
</div>

<div class="bilingual-pair">
<p class="src">The agent calls search to find relevant tools and their definitions. The execute step uses generated deterministic code to perform the operation. This middle layer dynamically generates code that strings tools or functions together. Instead of making the LLM work through each individual tool call, these two meta tools support generating the code needed for the operation.</p>
<p class="dst">Agent 先调 search 找工具和定义；execute 则用动态生成、确定性的代码完成任务。中间层会把多个工具或函数串起来，而不是让模型一步一步发几十个 tool call。</p>
</div>

<div class="bilingual-pair">
<p class="src">First, it massively reduces context because you no longer load every available tool into the context window at once. Second, because you interact through search and execute, the interface is agnostic to how many servers you have. An arbitrary number of MCP servers can be indexed for search.</p>
<p class="dst">好处有两个：第一，不必一次把所有工具塞进上下文，token 大幅下降；第二，接口与 server 数量解耦，不管你接了多少个 server，都可以被索引和搜索。</p>
</div>

<div class="bilingual-pair">
<p class="src">Some studies of this technique report more than 90% token reduction. It has different names in industry, but one term to remember is "code mode": generating tool calls and issuing server requests through code.</p>
<p class="dst">有些研究报告说，这种做法的 token 降幅超过 90%。行业里叫法不一，记住一个词就行：Code Mode——用代码生成来发起工具调用和 server 请求。</p>
</div>

<div class="slide-block"><p class="slide-block-title">对应 PPT · Slide 13</p><div class="slide-strip"><figure class="slide"><a class="slide-link" href="assets/slides/10-1/13.png" target="_blank" rel="noopener noreferrer"><img src="assets/slides/10-1/13.png" alt="10-1 slide 13" loading="lazy"></a><figcaption>Slide 13</figcaption></figure></div></div>

<div class="bilingual-pair">
<p class="src">Suppose the request is, "Find a Jira ticket and update it with information from Google Drive." Under the hood, a block of code is generated dynamically from that request. It searches the available tools and filters them based on the request.</p>
<p class="dst">比如请求是：“找一个 Jira ticket，用 Google Drive 里的内容更新它。”系统会先动态生成一段代码，搜索可用工具，再根据请求过滤出 Jira 和 Drive 相关的工具。</p>
</div>

<div class="bilingual-pair">
<p class="src">Imagine the search returned tools for searching Jira with JQL, getting Google Workspace Drive content, and updating a Jira ticket. A second block of code is dynamically generated to string those operations together. That block is executed as a process, not by the LLM itself.</p>
<p class="dst">假设搜索返回了三个工具：用 JQL 搜 Jira、读取 Drive 内容、更新 Jira ticket。第二步再生成一段代码，把这三个操作串起来，作为进程执行，而不是让模型自己一步步调用。</p>
</div>

<div class="bilingual-pair">
<p class="src">We never loaded the full tool set into the model's context. Code was generated and run, typically in a VM, returning the relevant tools and passing the results along. The filtering can be semantic or lexical. Here, it's lexical: the LLM recognizes Jira and Google Drive and generates JavaScript to filter on those keywords.</p>
<p class="dst">整个过程中，完整工具集从未进入模型上下文。代码在 VM 里生成并执行，只把相关工具和结果传下去。过滤可以语义，也可以词法；例子用的是词法：模型看到 Jira 和 Google Drive，就生成按关键词过滤的 JavaScript。</p>
</div>

### MCP Gateway 与收尾

<div class="slide-block"><p class="slide-block-title">对应 PPT · Slide 14</p><div class="slide-strip"><figure class="slide"><a class="slide-link" href="assets/slides/10-1/14.png" target="_blank" rel="noopener noreferrer"><img src="assets/slides/10-1/14.png" alt="10-1 slide 14" loading="lazy"></a><figcaption>Slide 14</figcaption></figure></div></div>

<div class="bilingual-pair">
<p class="src">MCP gateways are a separate topic, especially for team use. We also have a whole lecture on agent skills next week, so we'll go much deeper then. We're at time, and I want to leave room for our guests.</p>
<p class="dst">MCP gateway 是另一个话题，尤其是团队使用场景；下周还有一整节 agent skills 的课，会讲得更深。今天就到这里，把时间留给嘉宾。</p>
</div>

### 课后附页：Agent Skills 预告（本堂课未展开）

> 本堂课 transcript 在 MCP Gateway 处结束，随后交给 Factory workshop。以下 3 页来自同一份 Slides，但课堂没有展开讲授，因此没有对应的原文与翻译，仅作为后续课程预告保留。

<div class="slide-block"><p class="slide-block-title">对应 PPT · Slide 15</p><div class="slide-strip"><figure class="slide"><a class="slide-link" href="assets/slides/10-1/15.png" target="_blank" rel="noopener noreferrer"><img src="assets/slides/10-1/15.png" alt="10-1 slide 15" loading="lazy"></a><figcaption>Slide 15</figcaption></figure></div></div>

<div class="slide-block"><p class="slide-block-title">对应 PPT · Slide 16</p><div class="slide-strip"><figure class="slide"><a class="slide-link" href="assets/slides/10-1/16.png" target="_blank" rel="noopener noreferrer"><img src="assets/slides/10-1/16.png" alt="10-1 slide 16" loading="lazy"></a><figcaption>Slide 16</figcaption></figure></div></div>

<div class="slide-block"><p class="slide-block-title">对应 PPT · Slide 17</p><div class="slide-strip"><figure class="slide"><a class="slide-link" href="assets/slides/10-1/17.png" target="_blank" rel="noopener noreferrer"><img src="assets/slides/10-1/17.png" alt="10-1 slide 17" loading="lazy"></a><figcaption>Slide 17</figcaption></figure></div></div>

## 学习者视角

### 关键收获

1. **MCP 的价值是标准化连接。** 认证、错误、限流只实现一次，连接数从乘法变成加法。
2. **工具膨胀是默认结果。** 一对一映射 API 会把上下文撑爆，必须主动设计。
3. **按结果设计工具。** 一个“给邮箱付款”胜过“查用户→查邮箱→查账户→付款”四次调用。
4. **工具定义就是提示词。** 参数类型、docstring、错误类型、命名，都会影响模型行为。
5. **Code Mode 是上下文工程的极致。** 只暴露 search + execute，让模型写代码按需调用。
6. **工具集是迭代出来的。** 先铺开、看 trace、合并，不要指望一次设计完美。

### 放回课程里看

这节课是 Week 2 MCP 的原理与设计课。它和 [Enterprise MCP](w2-enterprise-mcp-cloudflare.html) 互补：课堂讲协议与工具设计，Cloudflare 讲企业治理和 Code Mode 落地。

### 一个反直觉点

很多人以为 MCP 的价值是“工具更多”。这节课的结论相反：**MCP 用不好，最大的问题就是工具太多。** Code Mode 甚至把成百上千个工具压成两个。

## 拓展

### 思考题

1. 你现在的 MCP server 里，有多少工具可以合并成“结果导向”的工具？
2. 为什么“工具选对了但参数传错”如此常见？你会怎么改 schema？
3. Code Mode 让模型生成代码执行，安全边界应该怎么划？
4. 词法过滤会漏掉什么？语义过滤的代价是什么？

### 练习

选一个你熟悉的 API，设计两版 MCP 工具集：

- 版本 A：一对一 endpoint 映射；
- 版本 B：按结果导向合并。

比较工具数量、schema、完成一个典型任务的调用次数、出错点和上下文 token 估算。

### 接着读

- [Enterprise MCP：企业级 MCP 与 Code Mode](w2-enterprise-mcp-cloudflare.html)
- [I Still Prefer MCP Over Skills：连接层 vs 说明书](w4-i-still-prefer-mcp-over-skills.html)
- [课堂实录 9/29：RePPIT 与规格驱动开发](w2-lecture-9-29-transcript.html)
