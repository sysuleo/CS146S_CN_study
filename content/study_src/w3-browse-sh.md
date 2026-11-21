---
title: "browse.sh：给 Agent 的浏览器 CLI 与技能目录"
original: "browse.sh: The open web catalog / A browser CLI for your AI Agents"
week: "3"
slug: "w3-browse-sh"
source_url: "https://browse.sh"
author: "Browserbase"
date: "2026"
kind: "产品文档"
coverage: "全文精译"
minutes: "7"
blurb: "一个 CLI 统一浏览器原语、网站技能、网络/控制台观测和云端会话，让 agent 用更少 token 操作网页。"
---

## 总结

给 AI agent 用的浏览器 CLI：一个命令，统一 skills、浏览器原语、调试和云会话。

- 底层浏览器原语：click、scroll、type、hover、press、screenshot。
- 网站技能目录：`browse skills add <domain>`，安装后 agent 知道该网站的选择器和 API。
- 可以实时 tail 网络请求和控制台，agent 能看到页面到底做了什么。
- 本地用 Chromium；加 `cloud` 前缀切换到 Browserbase 云会话。
- 官方称，预置 DOM 选择器和 XHR 请求可把 token 成本降低 50 倍。

## 原文逐段对照翻译

> **翻译说明：**以下按原文顺序翻译产品说明、CLI 示例和工作流；站点目录条目为结构化数据，正文中概括展示，完整目录见原文。

### 它是什么

<div class="bilingual-pair">
<p class="src">The open web catalog. A browser CLI for your AI Agents. One CLI for skills, browser primitives, debugging, and cloud sessions, designed to be driven by AI Agents.</p>
<p class="dst">一个开放的 Web 目录，也是给 AI agent 用的浏览器 CLI。一个命令统一 skills、浏览器原语、调试和云会话，专为 AI agent 驱动而设计。</p>
</div>

<div class="bilingual-pair">
<p class="src">Give AI Agents the skills to automate websites from the open web catalog. Suggested DOM selectors and XHR requests cut token costs by 50x.</p>
<p class="dst">让 agent 使用开放目录里的“网站技能”来自动化网站。预置的 DOM 选择器和 XHR 请求，可以把 token 成本降低 50 倍。</p>
</div>

### 底层浏览器原语

<div class="bilingual-pair">
<p class="src">Drive any page with low-level primitives: click, scroll, type, hover, press. Address elements by selector or by the AI Agent's accessibility refs.</p>
<p class="dst">用底层原语操作任意页面：click、scroll、type、hover、press。元素可以用 CSS selector，也可以用 agent 的可访问性 ref 定位。</p>
</div>

<div class="bilingual-pair">
<p class="src">browse click "input#search"; browse type "Apartments in SF"; browse select @8 "Single family unit"; browse press "Enter"; browse mouse scroll 50 50 10 10; browse screenshot.</p>
<p class="dst">示例命令：`browse click "input#search"`、`browse type "Apartments in SF"`、`browse select @8 "Single family unit"`、`browse press "Enter"`、`browse mouse scroll 50 50 10 10`、`browse screenshot`。</p>
</div>

### 网站技能目录

<div class="bilingual-pair">
<p class="src">browse skills add alltrails.com; browse skills add recreation.gov; browse skills add weather.gov; browse skills add plugshare.com; browse skills add ramp.com.</p>
<p class="dst">用 `browse skills add <domain>` 安装网站技能，例如 AllTrails、Recreation.gov、Weather.gov、PlugShare、Ramp。</p>
</div>

<div class="bilingual-pair">
<p class="src">Once installed, the skill gives the agent suggested DOM selectors, key XHR/API requests, operation steps, and the shape of returned data. This avoids re-discovering the page structure every session.</p>
<p class="dst">安装后，skill 会给 agent 提供推荐 DOM 选择器、关键 XHR/API 请求、操作步骤和返回数据结构。这样就不必每次会话都重新摸索页面结构。</p>
</div>

### 网络与控制台观测

<div class="bilingual-pair">
<p class="src">Tail the network and console of any browse session in real time. AI Agents (and you) see exactly what the page did: GET /api/listings 200 124 ms; POST /api/filter 200 84 ms; warnings and errors from the console.</p>
<p class="dst">实时 tail 任意 browse 会话的网络和控制台，agent 和你都能看到页面到底做了什么：`GET /api/listings 200 124 ms`、`POST /api/filter 200 84 ms`，以及控制台的 warning/error。</p>
</div>

<div class="bilingual-pair">
<p class="src">This matters because the agent is not just "clicking"; it can verify what request the click triggered and what error the page reported. Observability is part of reliability.</p>
<p class="dst">这很重要：agent 不只是“点了一下”，还能验证点击触发了什么请求、页面报了什么错。可观测性是可靠性的一部分。</p>
</div>

### 本地与云端

<div class="bilingual-pair">
<p class="src">All CLI commands work natively with local Chromium. Switch to remote sessions on Browserbase's Platform by prefixing any command with cloud: browse cloud sessions create; browse cloud search "..."; browse cloud fetch "https://...".</p>
<p class="dst">所有命令默认在本地 Chromium 上运行。加 `cloud` 前缀即可切换到 Browserbase 云会话：`browse cloud sessions create`、`browse cloud search "..."`、`browse cloud fetch "https://..."`。</p>
</div>

### 技能目录的结构

<div class="bilingual-pair">
<p class="src">Catalog entries usually include domain, skill name, method (api / browser / fetch / hybrid / cli), region, and a capability description. Examples: Ticketmaster find-ticket API, FlightAware track-flight fetch, Glassdoor get-company-reviews browser, Amazon search-products browser, Airbnb search-listings browser, 12306 find-trains hybrid.</p>
<p class="dst">目录条目通常包括：域名、技能名、方法（api / browser / fetch / hybrid / cli）、地区、能力描述。例如 Ticketmaster 查票、FlightAware 查航班、Glassdoor 查公司评论、Amazon 搜商品、Airbnb 搜房源、12306 查火车。</p>
</div>

<div class="bilingual-pair">
<p class="src">This is not a generic browser agent; it is a library of skills accumulated per website. The agent does not need to guess the site structure every time.</p>
<p class="dst">这不是通用浏览器 agent，而是按网站沉淀的技能库。agent 不需要每次猜网站结构。</p>
</div>

## 学习者视角

### 关键收获

1. **浏览器 agent 的瓶颈是“网站知识”，不是点击能力。** 知道该调哪个 API、该选哪个 DOM，比会点击重要得多。
2. **技能目录是 context engineering。** 预置选择器和 XHR，把“探索成本”从每次会话转移到一次安装。
3. **观测能力是可靠性的前提。** 网络和控制台 tail 让 agent 能验证动作。
4. **本地/云端切换是部署灵活性。** 同一套命令，既能本地跑，也能云端并行。
5. **网站技能会腐烂。** 网站改版、API 变更、反爬升级，都需要维护。

### 放回课程里看

browse.sh 是 Week 3 “Agent Skills and CLI” 的产品化案例：CLI 原语 + 网站技能 + 观测。它和 [pstack](w3-pstack.html) 的区别是：pstack 管工程流程，browse.sh 管网页操作。

### 一个反直觉点

很多人以为浏览器 agent 的关键是“更聪明的视觉模型”。browse.sh 的答案是：**预置网站知识，减少模型需要看和猜的东西。**

## 拓展

### 思考题

1. 什么情况下应该用 API 技能，什么情况下必须用浏览器技能？
2. 网站技能腐烂后，如何自动发现并修复？
3. 让 agent 直接调用网站内部 API，可能带来哪些合规和稳定性风险？
4. 如果目标网站有反爬，browse.sh 的方案会如何失效？

### 练习

选一个你常用的网站，写一份最小“网站技能”：

- 目标 URL；
- 3 个关键选择器；
- 1 个关键 XHR 请求；
- 成功/失败的判断条件；
- 一次完整的操作脚本。

### 接着读

- [pstack：工程 playbook 与模型分工](w3-pstack.html)
- [Matt Pocock's Skills：小型可组合技能](w3-matt-pocock-s-skills.html)
- [Enterprise MCP：企业级工具治理](w2-enterprise-mcp-cloudflare.html)
