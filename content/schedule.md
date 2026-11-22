# CS146S: The Modern Software Developer（Fall 2026）每周课表

来源：<https://themodernsoftware.dev/> 的 Syllabus 分页（页面为前端 Tab，无独立 syllabus URL）

> 中文学习站：<study/index.html>（25 篇阅读材料 + 3 篇课堂实录的中文精译、学习者总结与延伸练习）

## 课程信息

- 学校：Stanford University
- 学分：3 units
- 时间：周二、周四 17:30–18:20
- 地点：周二 370-370；周四 STLC 111
- 先修：CS111/CS161 同等编程经验，建议有 CS221/229
- 讲师：Mihail Eric（Instructor）
- 助教：Isaac Kan（Head TA）、Vijay Daita、Patrick Hua
- Office Hours：Mihail Eric 仅预约；Isaac Kan 周二 16:00–17:00 Coda 地下层；Vijay Daita 周三 18:00–19:00 Coda 3 层；Patrick Hua 周四 13:00–14:00 Gates 4 层

## 每周课表

| 周次 | 周二（含材料） | 周四（含材料） | 主题 | 阅读 |
|---|---|---|---|---|
| Week 1（9/22、9/24） | 课程介绍 + 用 200 行代码实现 Claude Code<br>[Slides](https://docs.google.com/presentation/d/1uztIhjHAG6O_9QOD1N_3wdhwhABml1fANXEN2dGwdbg/edit?usp=drive_link) · [完成版代码](https://drive.google.com/file/d/1DxKa_autBOu9s8DvItodgUAwH_pBg7aR/view?usp=drive_link) | 顶尖 coding agent 如何设计：深入其系统提示词<br>[Slides](https://docs.google.com/presentation/d/1RZu-p18Qybbgm8WVP2RH04ESc4Bn377B-T9j5-TBFdQ/edit?usp=drive_link) · [Prompts](https://drive.google.com/drive/folders/1c6_atVW0RrqEBWsNIscG2KNwCiuPxWQG?usp=drive_link) · [Transcript](https://themodernsoftware.dev/materials/9-24-26-transcript.txt) | Coding Agent 内部机制 | [Building a Coding Agent](https://youtube.com/watch?v=s7ZzkdvCMDY)<br>[Lessons from Building Claude Code](https://x.com/trq212/status/2027463795355095314?s=20)<br>[Dive into Claude Code](https://arxiv.org/pdf/2604.14228) |
| Week 2（9/29、10/1） | 高级提示技巧 + agentic 开发框架（RePPIT、spec-driven development）<br>[Slides](https://docs.google.com/presentation/d/17brqoQQZHF3K82WgYaV6urAV3Q7iIwyGUBYRvSuY8QY/edit?usp=sharing) · [Transcript](https://themodernsoftware.dev/materials/9-29-26-transcript.txt) | MCP 与 tool calling 完整入门（理论、配置、进阶工具设计）<br>[Slides](https://docs.google.com/presentation/d/1q2cB1a7P4XsR0UJqE0RmtZFeggNOLdPaSnOpbBVewHA/edit?usp=sharing) · [Skills](https://drive.google.com/drive/folders/1aEHCXzZKkokuA4AYjD_2i6OrcM5iQosW?usp=drive_link) · [Transcript](https://themodernsoftware.dev/materials/10-1-26-transcript.txt) | 高级上下文工程 | [The Context Tax: When to Compact](https://langwatch.ai/blog/context-tax-when-to-compact)<br>[OpenSpec](https://openspec.dev)<br>[Superpowers](https://github.com/obra/superpowers)<br>[Enterprise MCP (Cloudflare)](https://blog.cloudflare.com/enterprise-mcp) |
| Week 3（10/6、10/8） | Agent Skills（含 web skills）<br>[Slides](https://docs.google.com/presentation/d/15bPu5c-i8D8McTh6l7SpUPk2n9M_Y-CdDQLfyzL8RD8/edit?usp=sharing) | 嘉宾：Lee Robinson（Model Behavior @ SpaceX）<br>[个人主页](https://leerob.com) · [Slides](https://drive.google.com/file/d/1b8WiBk_lcB3ue-jZMLijSUMLj6SDiF6Z/view?usp=drive_link) · [视频](https://www.youtube.com/watch?v=L1OBRtfPS34) | Agent Skills 与 CLI | [pstack](https://github.com/cursor/plugins/tree/main/pstack)<br>[Matt Pocock's Skills](https://github.com/mattpocock/skills)<br>[browse.sh](https://browse.sh) |
| Week 4（10/13、10/15） | 定制 Agent 配置（CLAUDE.md、AGENTS.md、hooks）<br>[Slides](https://docs.google.com/presentation/d/152VaUifBKH4T6hxd6fCKKM9kJTSAuBmkF8zSYwuTYAo/edit?usp=sharing) | 嘉宾：Boris Cherny（Creator of Claude Code @ Anthropic）<br>[个人主页](https://borischerny.com) | 定制 Agent 与代码仓库 | [I Still Prefer MCP Over Skills](https://david.coffee/i-still-prefer-mcp-over-skills)<br>[AGENTS.md (Factory Docs)](https://docs.factory.com/harness/agents-md)<br>[Steering Claude Code](https://claude.com/resources/articles/steering-claude-code-skills-hooks-rules-subagents-and-more)<br>[Writing a Good CLAUDE.md](https://hlyr.dev/blog/writing-a-good-claude-md) |
| Week 5（10/20、10/22） | 让仓库达到 Agent-ready（结构、文档、检查）<br>[Slides](https://docs.google.com/presentation/d/1yCxocmUrGIN7IrC42WB6NW08PtYYFLe1ombDj3Ay6_8/edit?usp=drive_link) | 嘉宾：Eno Reyes（CTO @ Factory）<br>[个人主页](https://www.linkedin.com/in/enoreyes) · [Slides](https://drive.google.com/file/d/1Nbi1QEdiLXFBFAu1lRKkTkd85QRGpWOx/view?usp=drive_link) | Agent-Ready 代码库 | [Making Codebases Agent Ready](https://www.youtube.com/watch?v=ShuJ_CN6zr4)<br>[Making Ergonomic Repositories](https://x.com/trybasis/status/2056881705269580023) |
| Week 6（10/27、10/29） | Agentic code review：最佳实践与架构<br>[Slides](https://docs.google.com/presentation/d/1u8WYtFj0O9yc4H4JX9D4URYKhDzvrAGKLzn38DXSrak/edit?usp=drive_link) | 嘉宾：Silas Alberti（Chief Research Officer @ Cognition）<br>[个人主页](https://sil.as) | Agent 代码审查 | [Layered Code Review and Risk-Based Human Oversight](https://x.com/addyosmani/status/2114604912520921136)<br>[Coordinating Specialist Review Agents at Scale](https://blog.cloudflare.com/ai-code-review)<br>[Beyond the Diff: Context, Testing, and Model Selection](https://greptile.com/blog/how-to-build-a-code-review-agent) |
| Week 7（11/3、11/5） | **停课：学校假期** | 嘉宾：Isaac Evans（CEO @ Semgrep）<br>[个人主页](https://www.linkedin.com/in/isaacevans) | 安全（Security） | — |
| Week 8（11/10、11/12） | Background agents：异步启动任务<br>[Slides](https://docs.google.com/presentation/d/1R8Pr3RNAFQiw8mHKbXopOhxi_h9zuEeUKrJkxCZ5Fio/edit?usp=sharing) | 嘉宾：Rajesh Bhatia（Senior Director @ Cloudflare）<br>[个人主页](https://www.linkedin.com/in/rajeshbh) | 后台 Agent | [Spotify: From Migration Scripts to Agent Fleets](https://engineering.atspotify.com/2025/11/spotifys-background-coding-agent-part-1)<br>[Stripe: From Slack Message to Review-Ready PR](https://stripe.dev/blog/minions-stripes-one-shot-end-to-end-coding-agents)<br>[Ramp: Giving Agents the Tools to Prove Their Work](https://builders.ramp.com/post/why-we-built-our-background-agent)<br>[LangChain: Inside an Open-Source Software Factory](https://github.com/langchain-ai/open-swe) |
| Week 9（11/17、11/19） | 软件工厂与自改进的软件系统（The Software Factory and self-improving software systems）<br>[Slides](https://docs.google.com/presentation/d/1hxlLspHQ2WOs2tZmCN3gdDi7dfbbRorxzPr65HyyE6Y/edit?usp=sharing) | 嘉宾：Michele Catasta（President @ Replit）<br>[个人主页](https://www.linkedin.com/in/michelecatasta) | The Software Factory | [From Issue to Pull Request: A Warp Factory Example](https://github.com/warpdotdev/warp-factory-examples/tree/main/examples/02-sdlc-issue-to-pr)<br>[The Software Factory](https://software-factory.dev)<br>[OpenInspect](https://openinspect.dev)<br>[WarpBench: Evaluating Coding Agents](https://warp.dev/factories/benchmarks/warpbench) |
| Week 10（12/1、12/3） | Building the AI-native team（MCP portal、LLM gateway、组织模式、成本优化、模型路由） | Software taste and what's left for humans | The AI-Native Team + The Future | — |

## 每周主题细目

### Week 1: The Internals of Coding Agents

- LLM 到底是什么，以及 agent loop 在底层如何运转
- 核心工具集（read、write、edit、bash）与任务如何在其中流转
- 生产级 coding agent 如何组织 system prompt 与 tool definitions
- 资料：
  - [Building a Coding Agent](https://youtube.com/watch?v=s7ZzkdvCMDY)
  - [Lessons from Building Claude Code](https://x.com/trq212/status/2027463795355095314?s=20)
  - [Dive into Claude Code](https://arxiv.org/pdf/2604.14228)

### Week 2: Advanced Context Engineering

- 高级提示技巧及各自适用场景
- RePPIT（Research、Propose、Plan、Implement、Test）与 spec-driven development
- MCP 基础：servers、clients、tools、transport
- 面向 agent 使用体验的工具设计
- 资料：
  - [The Context Tax: When to Compact](https://langwatch.ai/blog/context-tax-when-to-compact)
  - [OpenSpec](https://openspec.dev)
  - [Superpowers](https://github.com/obra/superpowers)
  - [Enterprise MCP (Cloudflare)](https://blog.cloudflare.com/enterprise-mcp)

### Week 3: Agent Skills and CLI

- Skill 是什么，以及 SKILL.md + scripts 如何编码一套工作流
- Web skills 与在代码仓库之外扩展 agent 能力
- 在 CLI 中高效工作
- 资料：
  - [pstack](https://github.com/cursor/plugins/tree/main/pstack)
  - [Matt Pocock's Skills](https://github.com/mattpocock/skills)
  - [browse.sh](https://browse.sh)

### Week 4: Customizing Your Agent and Repository

- CLAUDE.md 与 AGENTS.md：什么内容放在哪里
- 用 hooks 做 lint gate、测试执行与护栏
- Subagent 模式（planner / implementer / reviewer）
- 资料：
  - [I Still Prefer MCP Over Skills](https://david.coffee/i-still-prefer-mcp-over-skills)
  - [AGENTS.md (Factory Docs)](https://docs.factory.com/harness/agents-md)
  - [Steering Claude Code](https://claude.com/resources/articles/steering-claude-code-skills-hooks-rules-subagents-and-more)
  - [Writing a Good CLAUDE.md](https://hlyr.dev/blog/writing-a-good-claude-md)

### Week 5: Agent-Ready Codebases

- 什么样的仓库算 agent-ready：结构、文档、测试与检查
- 评估与审计仓库的 readiness
- 真实仓库中阻碍 agent 的常见缺口
- 资料：
  - [Making Codebases Agent Ready](https://www.youtube.com/watch?v=ShuJ_CN6zr4)
  - [Making Ergonomic Repositories](https://x.com/trybasis/status/2056881705269580023)

### Week 6: Agentic Code Review

- AI review 擅长捕获什么、容易漏掉什么
- 审查架构与自定义规则
- 如何把 AI review 嵌入团队的 PR 流程
- 资料：
  - [Layered Code Review and Risk-Based Human Oversight](https://x.com/addyosmani/status/2114604912520921136)
  - [Coordinating Specialist Review Agents at Scale](https://blog.cloudflare.com/ai-code-review)
  - [Beyond the Diff: Context, Testing, and Model Selection](https://greptile.com/blog/how-to-build-a-code-review-agent)

### Week 7: Security

- SAST / SCA、依赖与密钥泄露类漏洞
- Prompt injection 与 agent 特有攻击面
- Agent 辅助的漏洞分诊与修复
- 周二 11/3 为学校假期停课；周四 11/5 为 Semgrep CEO Isaac Evans 嘉宾课

### Week 8: Background Agents

- 异步、云端委派的 agents
- 管理并行 agent fleet
- Issue-to-PR 流水线与触发器（Slack、Linear、GitHub）
- 周二 11/10 讲背景 agent；周四 11/12 为 Cloudflare 嘉宾 Rajesh Bhatia

### Week 9: The Software Factory

- 软件工厂作为一种运营模式
- 自运行、自改进的软件系统
- 部署后运行与保护 agents
- 周二 11/17 讲软件工厂与自改进软件系统（无嘉宾）；周四 11/19 嘉宾 Michele Catasta（President @ Replit）

### Week 10: The AI-Native Team + The Future

- MCP portal 与集中化、带权限的工具访问
- LLM gateway、模型路由与成本优化
- 组织级落地模式
- 软件品味与人类判断的持久价值
- 周二 12/1 讲 AI-native team 建设（MCP portal、LLM gateway、组织模式、成本优化、模型路由）；周四 12/3 讲软件品味与留给人类的工作

## 说明

- 根页面为 Fall 2026；`https://themodernsoftware.dev/fall2025` 是 Fall 2025 归档，课表内容不同。
- Fall 2026 的 Syllabus 中作业栏为空；上表只整理已公布的讲次、主题与阅读。
- 带 `gated` 标记的 Slides 需要 Stanford 账号权限。
