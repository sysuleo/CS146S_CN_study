---
title: "Ramp Inspect：为什么我们要自建后台 Coding Agent"
original: "Why We Built Our Own Background Agent"
week: "8"
slug: "w8-ramp-background-agent"
source_url: "https://builders.ramp.com/post/why-we-built-our-background-agent"
author: "Zach Bruggeman / Jason Quense / Rahul Sengottuvelu / Ramp"
date: "2026-01-12"
kind: "工程博客"
coverage: "全文精译"
minutes: "14"
blurb: "Ramp 自建 Inspect 的完整架构：Modal sandbox、OpenCode、Durable Objects、多人会话，以及 Slack/Web/Chrome 三个入口。"
---

## 总结

Ramp 的 Inspect 是一个**协作式后台 coding agent**，目标不是“让 agent 能写代码”，而是让它像 Ramp 工程师一样能验证自己的工作。

- 后端任务能跑测试、查 telemetry、读 feature flag；前端任务能截图、给 live preview。
- 每个会话跑在 Modal sandbox 里，预装完整开发环境，启动快、可并行、不占本地机器。
- 仓库镜像每 30 分钟构建一次；会话从快照启动，最多落后 30 分钟。
- Agent 基于 OpenCode：server-first、typed SDK、插件系统，便于做多客户端。
- 控制面用 Cloudflare Durable Objects，每个会话一个 SQLite；Agents SDK 处理实时流。
- 支持多人同时在一个 session 里工作，prompt 会记录作者；PR 用用户自己的 GitHub token 创建。
- 客户端覆盖 Slack、Web、Chrome 扩展；约 30% 合并到前后端仓库的 PR 由 Inspect 编写。

## 原文逐段对照翻译

> **翻译说明：**以下按原文顺序翻译全文；原文 6 张配图已下载到本地并按原位置插入。页面里的代码/工具名保持原样，页面导航和页脚从略。

<figure class="article-figure">
<a href="assets/figures/w8-ramp/hero.png" target="_blank" rel="noopener noreferrer"><img src="assets/figures/w8-ramp/hero.png" alt="Ramp Inspect"></a>
<figcaption>原文头图：Ramp 的协作式后台 coding agent Inspect。</figcaption>
</figure>

### 引言

<div class="bilingual-pair">
<p class="src">Built for Ramp’s engineers. Now open to yours. Meet Inspect, our collaborative coding agent.</p>
<p class="dst">为 Ramp 工程师而建，现在也向你的团队开放。认识一下 Inspect，我们的协作式 coding agent。</p>
</div>

<div class="bilingual-pair">
<p class="src">Request early access.</p>
<p class="dst">申请早期访问。</p>
</div>

<div class="bilingual-pair">
<p class="src">We built our own background coding agent: Inspect. Inspect writes the code like any other coding agent, but closes the loop on verifying its work by having all the context and tools needed to prove it, as a Ramp engineer would.</p>
<p class="dst">我们自建了后台 coding agent：Inspect。它像其他 coding agent 一样写代码，但会像 Ramp 工程师那样，拿到所有需要的上下文和工具，把“验证自己的工作”这一步闭环。</p>
</div>

<div class="bilingual-pair">
<p class="src">For backend work, it can run tests, review telemetry, and query feature flags. For frontend, it visually verifies its work and gives users screenshots and live previews. Agents should have agency, and so we made sure Inspect is never limited by missing context or tools, but only by model intelligence itself.</p>
<p class="dst">做后端时，它能跑测试、看 telemetry、查 feature flag；做前端时，它能可视化验证自己的改动，给用户截图和 live preview。Agent 应该有能动性，所以我们确保 Inspect 不会被缺失的上下文或工具限制，只受模型智能本身限制。</p>
</div>

<div class="bilingual-pair">
<p class="src">Each session runs in a sandboxed VM on Modal with everything an engineer would have locally: Vite, Postgres, Temporal, the works. It’s wired into Sentry, Datadog, LaunchDarkly, Braintrust, GitHub, Slack, and Buildkite. It supports all frontier models, MCPs, custom tools, and skills that encode how we ship at Ramp. This also lets builders of all backgrounds, contribute with the tooling and setup an engineer would.</p>
<p class="dst">每个会话跑在 Modal 的 sandbox VM 里，带有工程师本地会有的一切：Vite、Postgres、Temporal 等。它接入了 Sentry、Datadog、LaunchDarkly、Braintrust、GitHub、Slack 和 Buildkite，支持所有前沿模型、MCP、自定义工具，以及编码 Ramp 交付方式的 skills。这也让不同背景的构建者，能用工程师级别的工具和环境做贡献。</p>
</div>

<div class="bilingual-pair">
<p class="src">Because Inspect sessions are fast to start and effectively free to run, you can use them without rationing local checkouts or worktrees. A builder can kick off multiple versions of the same prompt, and just see which one lands. They can try different approaches or swap models without thinking twice. There’s no limit to how many sessions you can have running concurrently, and your laptop doesn’t need to be involved at all.</p>
<p class="dst">因为 Inspect 会话启动快、运行成本几乎可以忽略，你不用再节省本地 checkout 或 worktree。一个构建者可以对同一个 prompt 启动多个版本，看哪个效果最好；也可以毫不犹豫地试不同方法或换模型。并发会话数量没有限制，而且完全不需要用到你的笔记本。</p>
</div>

<div class="bilingual-pair">
<p class="src">This also means you can capture ideas the moment you have them. Notice a bug while winding down for the night? Kick off a session, talk to it if you want (we added voice), and check the PR in the morning.</p>
<p class="dst">这也意味着有想法的那一刻就能抓住。晚上收工前发现一个 bug？启动一个会话，想说话就直接说（我们加了语音），第二天早上看 PR。</p>
</div>

<div class="bilingual-pair">
<p class="src">The interface understands that people rely on a rich variety of workflows. You can chat with Inspect in Slack and send it screenshots, use the Chrome extension to highlight specific changes to elements, prompt it on the web interface, discuss on the Pull Request, and even drop into a web-based VS Code editor to make manual changes. All changes are synced to the session, so you never lose your work while switching around. Plus, every session is multiplayer. Send your session to any colleague, and they can help take it home.</p>
<p class="dst">界面理解人们的工作流多种多样。你可以在 Slack 里和 Inspect 聊天、发截图；用 Chrome 扩展高亮具体元素改动；在 Web 界面写 prompt；在 PR 里讨论；甚至进入 Web 版 VS Code 手动修改。所有改动都会同步到会话，切换界面不会丢工作。另外，每个会话都是多人协作的：把 session 发给任何同事，对方都能接着帮你完成。</p>
</div>

<div class="bilingual-pair">
<p class="src">We want Inspect sessions to be fast, and session speed should only be limited by model-provider time-to-first-token. Everything else, like cloning and installing, is done before you start your session. When background agents are fast, they’re strictly better than local: same intelligence, more power, and unlimited concurrency. You can go home and let Inspect cook (and if you’re so inclined, resume after dinner from your couch and mobile phone).</p>
<p class="dst">我们希望 Inspect 会话足够快，速度只应该受模型提供商的 time-to-first-token 限制。clone、安装等其他步骤都在会话开始前完成。后台 agent 一旦够快，就严格优于本地：同样的智能、更强的算力、无限的并发。你可以回家让 Inspect 继续干活（如果愿意，晚饭后在沙发上用手机接着看）。</p>
</div>

<div class="bilingual-pair">
<p class="src">Internal adoption charts have been vertical: ~30% of all pull requests merged to our frontend and backend repos are written by Inspect. It only took a couple months for us to reach this level of usage, and it continues to grow. We didn’t force anyone to use Inspect over their own tools. We built to people’s needs, created virality loops through letting it work in public spaces, and let the product do the talking.</p>
<p class="dst">内部采用曲线几乎是垂直的：合并到我们前端和后端仓库的 PR 中，约 30% 由 Inspect 编写。达到这个使用率只用了几个月，而且还在增长。我们没有强迫任何人放弃自己的工具改用 Inspect；我们按人的需求构建，让它在公共空间里工作形成传播闭环，然后让产品自己说话。</p>
</div>

<div class="bilingual-pair">
<p class="src">We think anyone should be able to build this. Owning the tooling lets you build something significantly more powerful than an off-the-shelf tool will ever be. After all, it only has to work on your code. To make this easy to replicate, we’ve written a spec of what we’ve built so far. Paste the link to this post into a coding agent and let it begin building.</p>
<p class="dst">我们认为任何人都应该能构建这样的东西。拥有自己的工具链，能做出比现成产品强得多的东西——毕竟它只需要为你的代码工作。为了方便复现，我们把目前构建的东西写成了一份 spec。把本文链接粘给 coding agent，就可以让它开始搭。</p>
</div>

<div class="bilingual-pair">
<p class="src">Update: Inspect is now open to teams outside Ramp. Read the launch announcement.</p>
<p class="dst">更新：Inspect 现在已向 Ramp 之外的团队开放。可以阅读发布公告。</p>
</div>

### Sandbox

<div class="bilingual-pair">
<p class="src">At the core of a hosted coding agent is the execution environment. Whenever you start a new coding session, you want to spin up a new sandbox that has a full development environment. This will allow the agent to work effectively, by having access to all the tools a human would have, while also being isolated from other work. It’s also crucial that time-to-first-token is as fast as possible.</p>
<p class="dst">托管式 coding agent 的核心是执行环境。每次启动新会话，都要拉起一个带完整开发环境的 sandbox，让 agent 拥有和人类一样的工具，同时与其他工作隔离。另一个关键是 time-to-first-token 要尽可能快。</p>
</div>

<div class="bilingual-pair">
<p class="src">The key challenge is spinning up full dev environments quickly. Modal solves this: it's a cloud platform for AI infrastructure we use across Ramp. Their sandboxes start near instantly, and file system snapshots allow us to freeze and restore state later. With Modal Sandboxes, we take the following approach:</p>
<p class="dst">关键挑战是快速拉起完整开发环境。Modal 解决了这个问题：它是我们在 Ramp 广泛使用的 AI 基础设施云平台。它的 sandbox 几乎瞬间启动，文件系统快照让我们可以冻结状态并在之后恢复。使用 Modal Sandboxes，我们采用下面的做法：</p>
</div>

<div class="bilingual-pair">
<p class="src">We have an image registry, defining an image for each code repository.</p>
<p class="dst">我们有一个 image registry，为每个代码仓库定义镜像。</p>
</div>

<div class="bilingual-pair">
<p class="src">We build these images every 30 minutes, meaning that we clone the repository, install any runtime dependencies, and do any initial setup and build commands.</p>
<p class="dst">每 30 分钟构建一次镜像：clone 仓库、安装运行时依赖、执行初始 setup 和 build 命令。</p>
</div>

<div class="bilingual-pair">
<p class="src">If you use GitHub: You will need to have a GitHub app, and generate a new app installation token on each clone, so that it can clone the repository without knowing what user will consume it.</p>
<p class="dst">如果使用 GitHub：需要一个 GitHub app，并在每次 clone 时生成新的 app installation token，这样 clone 时不需要知道最终是哪个用户来使用。</p>
</div>

<div class="bilingual-pair">
<p class="src">As git operations are not tied to a GitHub user, you will simply update the git config’s user.name and user.email when committing and pushing the changes.</p>
<p class="dst">由于 git 操作不绑定某个 GitHub 用户，提交和 push 时只需更新 git config 的 user.name 和 user.email。</p>
</div>

<div class="bilingual-pair">
<p class="src">We save a snapshot of the image in this completed state.</p>
<p class="dst">在这个完成状态下保存镜像快照。</p>
</div>

<div class="bilingual-pair">
<p class="src">When we later start the session, we spin up a new sandbox that starts from this stored snapshot. This ensures that at most, the repository is 30 minutes out of date. This makes the synchronization with the latest code in the repository much faster, as there’s only up to 30 minutes of changes to sync.</p>
<p class="dst">之后启动会话时，从保存的快照拉起新 sandbox。这样仓库最多落后 30 分钟，与最新代码同步也快得多，因为最多只需要同步 30 分钟内的改动。</p>
</div>

<div class="bilingual-pair">
<p class="src">When the agent is finished making changes, we take another snapshot, and restore to it later if the sandbox has exited and the user sends a follow up.</p>
<p class="dst">Agent 改完后，我们再拍一个快照；如果 sandbox 已退出、用户又发来后续消息，就从该快照恢复。</p>
</div>

<figure class="article-figure">
<a href="assets/figures/w8-ramp/take-screenshot.png" target="_blank" rel="noopener noreferrer"><img src="assets/figures/w8-ramp/take-screenshot.png" alt="Inspect sandbox and screenshot workflow"></a>
<figcaption>原文图：Inspect 的 sandbox 与截图验证流程。</figcaption>
</figure>

<div class="bilingual-pair">
<p class="src">You now need to set up an agent to do work in the sandbox. We strongly recommend using OpenCode, an open source coding agent. We believe it has critical advantages over other agents:</p>
<p class="dst">接下来要在 sandbox 里配置 agent。我们强烈推荐 OpenCode——一个开源 coding agent。我们认为它相比其他 agents 有几个关键优势：</p>
</div>

<div class="bilingual-pair">
<p class="src">It is structured as a server first, with its TUI and desktop app just being clients on top. You want the ability to create as many custom clients as possible down the line, as you want to put your coding agent wherever your team works. OpenCode was the strongest technical implementation we found, as it has a fully typed SDK, and comprehensive plugin system.</p>
<p class="dst">它首先是 server 架构，TUI 和桌面应用只是上层客户端。你之后会希望创建尽可能多的自定义客户端，把 coding agent 放到团队工作的每个地方。OpenCode 是我们找到的最强技术实现，有完整类型的 SDK 和全面的插件系统。</p>
</div>

<div class="bilingual-pair">
<p class="src">If something is unclear from the documentation, you can simply ask the AI to read the code of OpenCode itself, and figure out exactly what the behaviour should be. This is something we believe is highly underrated in development with AI. You want it to be as easy as possible for the agent to understand how it works, without it hallucinating what it believes is its own behaviour. As such, having the code as its source of truth is extremely powerful.</p>
<p class="dst">如果文档里有什么不清楚，可以直接让 AI 读 OpenCode 自己的代码，弄清真实行为。我们认为这在 AI 开发里被严重低估：你要让 agent 尽可能容易理解工具如何工作，而不是让它对自己行为的想象产生幻觉。因此，把代码作为事实来源非常强大。</p>
</div>

<div class="bilingual-pair">
<p class="src">If you build something great, you will get the OpenCode team to work with you.</p>
<p class="dst">如果你做出了很棒的东西，OpenCode 团队会愿意和你合作。</p>
</div>

<div class="bilingual-pair">
<p class="src">Some optimizations you should add for increased speed:</p>
<p class="dst">为了进一步提升速度，建议加入这些优化：</p>
</div>

<div class="bilingual-pair">
<p class="src">Warm the sandbox for your session as soon as a user starts to type their prompt. This lets it start cloning the latest changes, and doing any initial setup in the newly created sandbox before the user has even hit enter. If your spin up is fast, it can be ready before the user finishes typing, making the prompt feel as fast as it would on a local machine. You can also keep a pool of warm sandboxes for any high-volume repositories, so they’re already there before you start. Just ensure to expire and recreate the pool as new image builds come in.</p>
<p class="dst">用户一开始输入 prompt，就预热会话 sandbox。这样可以在用户按下回车前就开始同步最新改动、做初始 setup。如果启动够快，用户还没打完字环境就绪，体验会像本地一样快。对于高频仓库，还可以维护一个 warm sandbox 池，让环境提前存在；但要记得在新镜像构建后让旧池过期并重建。</p>
</div>

<div class="bilingual-pair">
<p class="src">Allow your agent to start reading files immediately, even if the sync from the latest base branch is not complete yet. In a large enough repository, it is unlikely that an incoming prompt is going to modify a file changed in the last 30 minutes. As such, you can let it start researching immediately, and avoid any latency from git here. However, ensure that you block file edits until synchronization is complete. OpenCode makes this easy for you, as you can write a plugin that listens to the tool.execute.before event, and block any write or edit calls until the sync is done.</p>
<p class="dst">允许 agent 立刻开始读文件，即使与最新 base branch 的同步还没完成。在足够大的仓库里，新 prompt 很少会刚好改到最近 30 分钟变过的文件。因此可以让它马上开始研究，避免 git 同步延迟。但要确保同步完成前阻止文件编辑。OpenCode 很容易做到：写一个插件监听 <code>tool.execute.before</code> 事件，在同步完成前拦截所有 write/edit 调用。</p>
</div>

<div class="bilingual-pair">
<p class="src">Move as much as you can to the build step for your repository images. Thoroughly investigate what you need to do to have a complete development environment, and do literally everything you can do beforehand. Even things like running your app and test suite once are helpful, as these may write cached files that a second run will make use of. It doesn’t matter if your image build is long, as users are just using the last built image, and therefore will not see how long this step took.</p>
<p class="dst">尽量把能提前做的事情都移到仓库镜像的 build 阶段。彻底研究完整开发环境需要什么，把所有能预先做的都做掉。哪怕是先跑一次应用和测试套件也有帮助，因为它们可能写下缓存文件供第二次运行使用。镜像构建慢没关系，用户使用的是上一次构建好的镜像，不会感受到这一步的耗时。</p>
</div>

<div class="bilingual-pair">
<p class="src">You should decide if you want follow up prompts that are sent during an execution to be inserted as soon as possible, or queued to be run after the current prompt is complete. We chose to queue them, as we found it not only easier to manage, but also helpful for sending over thoughts on next steps while the AI is still working. Be sure to build a mechanism to also allow an agent to be stopped mid-way.</p>
<p class="dst">你要决定：执行期间发来的后续 prompt，是尽快插入当前执行，还是排队等当前 prompt 完成后再跑。我们选择排队，因为更容易管理，也方便在 AI 工作时先把下一步想法发过去。同时一定要有中途停止 agent 的机制。</p>
</div>

<figure class="article-figure">
<a href="assets/figures/w8-ramp/child.png" target="_blank" rel="noopener noreferrer"><img src="assets/figures/w8-ramp/child.png" alt="Inspect spawning child sessions"></a>
<figcaption>原文图：Inspect 可以自行派生新的子会话。</figcaption>
</figure>

<div class="bilingual-pair">
<p class="src">Amongst many tools you could build for your agent, a crucial tool is one that allows it to spawn sessions itself. Don’t be afraid of the possibility of it spawning too many agents; frontier models are smart enough to contain themselves. Create a tool that starts a new session, and a tool that lets it read the status of any session, so it can check in periodically while the main session still does work. Prompt engineer this so you can either do research tasks (especially across different repositories), or create many smaller pull requests for one major task.</p>
<p class="dst">在你能为 agent 构建的众多工具里，一个关键工具是“让它自己派生会话”。不要害怕它派出太多 agent；前沿模型足够聪明，能自我约束。提供一个启动新会话的工具，以及一个读取任意会话状态的工具，让它能周期性查看进度，同时主会话继续工作。再通过 prompt 设计，让它既能做研究任务（尤其是跨仓库研究），也能把一个大任务拆成多个小 PR。</p>
</div>

### API

<div class="bilingual-pair">
<p class="src">You want to build an API that is going to be able to support input from a variety of clients, whether that be a chat interface, a Slack bot, a Chrome extension, or any other input you can think of in the future. You want the state to be synchronized across all clients. You also want to build multiplayer support, which we’ll explain shortly.</p>
<p class="dst">你需要一个能支持多种客户端输入的 API：聊天界面、Slack bot、Chrome 扩展，或未来任何输入方式。所有客户端的状态要同步；还要支持多人协作，下面会解释。</p>
</div>

<div class="bilingual-pair">
<p class="src">The best system we found for this was Cloudflare’s Durable Objects. Every session gets its own SQLite database. This ensures high performance, even when you have hundreds of sessions running in parallel, as no one session can impact another. This is particularly important given that the agent will be streaming tokens to you in real time, so you will likely receive hundreds of updates in a very short time frame.</p>
<p class="dst">我们找到的最合适系统是 Cloudflare 的 Durable Objects。每个会话有自己的 SQLite 数据库，即使同时有数百个会话，性能也不会互相影响。考虑到 agent 会实时流式输出 token，短时间内可能收到数百条更新，这一点尤其重要。</p>
</div>

<div class="bilingual-pair">
<p class="src">Cloudflare also provides its Agents SDK, which we found was particularly useful for handling the real-time streaming between the sandbox, the API, and any attached clients. It provides helpful abstractions over the WebSockets Hibernation API, which allows for sockets to stay open without incurring compute costs during idle periods.</p>
<p class="dst">Cloudflare 还提供 Agents SDK，我们发现它特别适合处理 sandbox、API 和各个客户端之间的实时流。它对 WebSockets Hibernation API 做了有用抽象，让 socket 可以保持打开，同时在空闲期间不产生计算成本。</p>
</div>

<figure class="article-figure">
<a href="assets/figures/w8-ramp/multiplayer.png" target="_blank" rel="noopener noreferrer"><img src="assets/figures/w8-ramp/multiplayer.png" alt="Inspect multiplayer session"></a>
<figcaption>原文图：Inspect 的多人协作会话。</figcaption>
</figure>

<div class="bilingual-pair">
<p class="src">We believe that multiplayer is a mission-critical feature, and something we have not seen in any other product yet. The idea behind multiplayer should be that any number of people can work in one session together, just as they would in a branch of code. Each person’s prompt that causes code changes should be attributed to them. This is useful for a variety of scenarios:</p>
<p class="dst">我们认为多人协作是关键功能，而且目前还没在其他产品里见过。它的理念是：任意数量的人可以一起在一个会话里工作，就像在同一个代码分支上协作。每个人引发代码改动的 prompt 都应该归因到本人。这在很多场景里有用：</p>
</div>

<div class="bilingual-pair">
<p class="src">Teaching non-engineering builders, such as product managers and designers, how to effectively utilize the AI for their own work. Doing live QA sessions with your team, as each person can queue up changes they find in real-time, instead of writing a ticket to do it later. Reviewing another person’s pull request, asking the AI to quickly make requested changes instead of just commenting them and waiting for the original author to pick them up.</p>
<p class="dst">教非工程构建者（比如产品经理和设计师）如何有效用 AI 完成自己的工作；和团队做 live QA，每个人可以实时把自己发现的问题排进会话，而不是事后写 ticket；review 别人的 PR 时，直接让 AI 快速改掉请求的变更，而不是只留评论等原作者来处理。</p>
</div>

<div class="bilingual-pair">
<p class="src">If you build a system that synchronizes across clients, multiplayer support should be nearly free to add. Just ensure your data model does not strongly tie a session to only one author at a time, and be sure to pass authorship info to each prompt that’s sent to the coding agent.</p>
<p class="dst">如果系统本身已经做跨客户端同步，多人支持几乎可以免费加上。只要数据模型不要把 session 强绑定到单一作者，并把作者信息随每个 prompt 传给 coding agent。</p>
</div>

<div class="bilingual-pair">
<p class="src">You will need to add authentication. Consider using GitHub authentication if your code lives in GitHub, as this will give you a user token that you can then use to open a pull request on behalf of the user. This is strongly preferred over having it open pull requests as the app itself. In the latter scenario, this would allow for any user to approve their own changes. You do not want to knowingly create a vector for unreviewed code to go into the codebase.</p>
<p class="dst">你需要认证。如果代码在 GitHub 上，考虑用 GitHub 认证，这样能拿到用户 token，以用户身份开 PR。这比用 app 自身身份开 PR 好得多：后者会让任何用户都能批准自己的改动，等于有意制造一条未 review 代码进入代码库的通道。</p>
</div>

<div class="bilingual-pair">
<p class="src">Our setup is to have the sandbox push the changes (updating the git user as previously mentioned), and then send an event to the API with the branch name and session ID. The API will then use the user’s GitHub token to call GitHub’s pull request API. You should also set up a GitHub webhook to listen for branch and pull request events, so you can keep track of when a pull request is updated, merged, or closed.</p>
<p class="dst">我们的做法是：sandbox push 改动（如前所述更新 git 用户），然后向 API 发送带分支名和 session ID 的事件；API 用用户的 GitHub token 调 GitHub 的 PR API。还应配置 GitHub webhook 监听分支和 PR 事件，跟踪 PR 的更新、合并和关闭。</p>
</div>

### 客户端

<div class="bilingual-pair">
<p class="src">Client choices should be to taste, focusing on where your organization primarily works. These are just our most effective clients. As you have now built a generic sandbox and API for remote coding, you can build any client on top.</p>
<p class="dst">客户端选择取决于你的组织主要在哪里工作。下面只是我们最有效的几个。既然已经建好了通用的远程 coding sandbox 和 API，上面可以接任何客户端。</p>
</div>

#### Slack

<div class="bilingual-pair">
<p class="src">Choose whatever team communication tool your company uses. We believe this is extremely effective, as it not only lets you quickly tackle issues from a variety of sources, but also introduces a virality loop. As people in your organization use it, others will see it, and they’ll learn how to use it themselves.</p>
<p class="dst">选择你公司使用的团队沟通工具。我们认为了解这个入口非常有效：它既能快速处理各种来源的问题，也形成传播闭环——组织里有人用，其他人就会看到，并学会自己用。</p>
</div>

<figure class="article-figure">
<a href="assets/figures/w8-ramp/slack.png" target="_blank" rel="noopener noreferrer"><img src="assets/figures/w8-ramp/slack.png" alt="Inspect Slack client"></a>
<figcaption>原文图：Inspect 的 Slack 客户端。</figcaption>
</figure>

<div class="bilingual-pair">
<p class="src">Slack’s APIs are not hard to start with, as they have a plethora of client libraries. Your goal here is to make it as seamless as possible to use. Do not force the user to learn syntax to use a chat bot. They should just be able to chat with it, and it should figure it out.</p>
<p class="dst">Slack API 不难上手，客户端库很多。目标是让使用尽可能无缝。不要强迫用户学习某种语法才能用聊天机器人；他们应该能直接聊，机器人自己理解。</p>
</div>

<div class="bilingual-pair">
<p class="src">A critical piece is to build a classifier to determine what repository to work in. Take the user’s incoming message, any thread context (if sent in a thread), and the channel’s name. Give that to a fast model (we use GPT 5.2 with no reasoning), along with descriptions of every repository your coding agent can access. Be sure to give it hints on the most common repositories, and example classifications. Be sure to include an “unknown” option, so the AI can ask the user if unsure. You may need to tweak this at first, but this significantly lowers the barrier for entry.</p>
<p class="dst">一个关键部分是分类器：判断该在哪个仓库工作。把用户消息、线程上下文（如果是在线程里）和频道名，连同所有可访问仓库的描述，交给一个快速模型（我们用不带 reasoning 的 GPT 5.2）。给它常见仓库的提示和分类示例，并且一定要有 “unknown” 选项，让 AI 不确定时反问用户。初期可能需要调，但这会显著降低使用门槛。</p>
</div>

<div class="bilingual-pair">
<p class="src">The Slack bot should also be very clear when it’s working vs. when it’s done. Give the agent a Slack message tool, so it can post updates about what it’s doing at important inflection points. Use Block Kit to design an appealing layout, such as including metadata about the repository and working status as context blocks.</p>
<p class="dst">Slack bot 要清楚区分“正在工作”和“已完成”。给 agent 一个 Slack 消息工具，让它在关键节点发布进展；用 Block Kit 设计好看的布局，比如把仓库元数据和工作状态放在 context block 里。</p>
</div>

<div class="bilingual-pair">
<p class="src">Most importantly: Since this is your own Slack bot, we recommend adding your own emojis for the bot to use. It’s a lot more fun than just using generic emojis.</p>
<p class="dst">最重要的是：既然这是你自己的 Slack bot，建议给它加自定义 emoji。比只用通用 emoji 有趣得多。</p>
</div>

#### Web

<div class="bilingual-pair">
<p class="src">You should have a polished web client, so users can work on sessions from anywhere. Ensure it works well on both desktop and mobile. If you use Cloudflare’s Agents SDK, you’ll have easy constructs for handling the real-time streaming.</p>
<p class="dst">应该有一个精致的 Web 客户端，让用户在任何地方处理会话，并确保桌面和手机都好用。如果用 Cloudflare Agents SDK，处理实时流会容易很多。</p>
</div>

<div class="bilingual-pair">
<p class="src">What matters more here is some additional functionality you can expose uniquely in the interface: A hosted VS Code instance, which runs inside of the sandbox, so people can make manual changes without having to clone the repository locally. A streamed desktop view, so you can work alongside the agent for web projects, having it perform computer use to navigate and verify its changes visually. It can also take before and after screenshots, which you can append to the pull request descriptions.</p>
<p class="dst">更重要的是在界面里暴露一些独特能力：一个跑在 sandbox 里的托管 VS Code，让人不用本地 clone 就能手动改代码；一个流式桌面视图，让你在 Web 项目里和 agent 并肩工作，让它用 computer use 导航并可视化验证改动；它还能拍前后对比截图，附到 PR 描述里。</p>
</div>

<div class="bilingual-pair">
<p class="src">As well, you should build a statistics page. Include your entire organization’s usage, particularly surfacing how many sessions result in a merged pull request. This is the most important metric to track, as merged pull requests indicate that the agent is producing valuable work. Show these as metrics over time, so you can inspire more growth. A live “humans prompting” count is a good gauge as well, which we base on the number of users that have sent a prompt in the last 5 minutes.</p>
<p class="dst">还应该做统计页：展示全组织使用情况，尤其突出有多少 session 最终产生了合并 PR。这是最重要的指标，因为合并 PR 才说明 agent 产出了有价值的工作。把这些指标按时间展示，能推动增长。一个实时的“正在 prompt 的人数”也很好用，我们按最近 5 分钟发过 prompt 的用户数计算。</p>
</div>

#### Chrome 扩展

<div class="bilingual-pair">
<p class="src">To inspire usage across more non-engineering users, you should build a Chrome extension that allows you to make changes to any React app visually. Use the Chrome extension sidebar API to build a chat interface that also includes a screenshot tool. However, instead of sending the actual image (which consumes many tokens), it should use the DOM and React internals to get the full tree of elements in the selected area. We built our own, to tie directly into our React app and its debugging internals, but if you need a starting point, you could use something like React Grab.</p>
<p class="dst">为了让更多非工程用户用起来，应该做一个 Chrome 扩展，让你可视化修改任何 React 应用。用 Chrome 扩展 sidebar API 做聊天界面，并带截图工具。但不要发送真实图片（很耗 token），而是用 DOM 和 React internals 获取选中区域的完整元素树。我们自建了扩展，直接接入自己的 React 应用和调试内部结构；如果需要起点，可以用 React Grab 这类工具。</p>
</div>

<figure class="article-figure">
<a href="assets/figures/w8-ramp/extension.png" target="_blank" rel="noopener noreferrer"><img src="assets/figures/w8-ramp/extension.png" alt="Inspect Chrome extension"></a>
<figcaption>原文图：Inspect 的 Chrome 扩展。</figcaption>
</figure>

<div class="bilingual-pair">
<p class="src">To distribute this extension, you can use a managed device policy. This allows you to avoid the Chrome Web Store entirely, and also will increase adoption by putting it in your team’s browsers. You’ll need to stand up an extension update server; these return a pretty simple manifest and the CRX. Follow the attached link to build a compliant server. Then, you’ll set the ExtensionInstallForcelist MDM property, pointing it to your extension update server.</p>
<p class="dst">分发扩展可以用托管设备策略，这样完全绕过 Chrome Web Store，也能直接装进团队浏览器、提高采用率。你需要搭一个扩展更新服务器，返回简单的 manifest 和 CRX；按链接里的说明构建合规服务器。然后设置 MDM 属性 <code>ExtensionInstallForcelist</code>，指向你的扩展更新服务器。</p>
</div>

## 学习者视角

### 关键收获

1. **验证闭环是差异化。** Inspect 不只会写代码，还能跑测试、看 telemetry、查 feature flag、截图验证前端。
2. **环境启动速度决定产品形态。** 预构建镜像 + 快照 + warm pool，让 session 快到可以并行、可以随手启动。
3. **OpenCode 的 server-first 架构适合多客户端。** Slack、Web、Chrome 扩展都只是同一套 API 的客户端。
4. **多人协作应该是一等能力。** 数据模型不能把 session 绑死在一个作者上，prompt 要带作者信息。
5. **PR 要用用户身份创建。** 用 app 身份开 PR 会让用户能批准自己的改动，是安全反模式。

### 放回课程里看

这篇是 Week 8 的“产品化后台 agent”代表：它把 sandbox、API、客户端和安全模型讲得很完整。和 [Stripe Minions](w8-stripe-minions.html) 对比，Ramp 更强调多人协作、可视化验证和多入口；和 [Spotify Honk](w8-spotify-background-coding-agent.html) 对比，Ramp 更强调“从零自建一套通用后台 agent 基础设施”。

### 一个反直觉点

很多人以为后台 agent 的核心是模型。Ramp 的工程重点却大量花在**环境预热、文件系统快照、同步策略和反馈闭环**上：模型只应该受 time-to-first-token 限制，其他延迟都应该在会话开始前解决。

## 拓展

### 思考题

1. 为什么仓库镜像每 30 分钟构建一次，而不是每次会话都重新 clone/install？
2. 允许 agent 在同步完成前读文件、但阻止写文件，解决了什么权衡？
3. 多人 session 的 prompt 归因为什么重要？如果做错会有什么后果？
4. 为什么用用户 GitHub token 开 PR 比用 app 身份更安全？

### 练习

为你的团队设计一个后台 agent 的 session 架构：

- 镜像/快照策略（多久构建一次、如何恢复）；
- sandbox 启动优化（warm pool、提前 clone、缓存）；
- 同步与写操作的保护顺序；
- API 状态模型（每 session 一个 DB？如何广播流？）；
- 多人协作与作者归因；
- 至少两个客户端入口和它们的认证方式。

### 接着读

- [Stripe Minions：一次运行、端到端交付](w8-stripe-minions.html)
- [Spotify Honk：Fleet Management + coding agent](w8-spotify-background-coding-agent.html)
- [LangChain Robin：开源软件工厂](w8-langchain-robin.html)
