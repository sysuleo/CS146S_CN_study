# GitHub Pages 静态托管

读者不需要 FastAPI 也能浏览课程表和学习页。仓库已经附带 `.github/workflows/pages.yml`，推送后由 GitHub Actions 构建并发布 `app/static`。

## 一次性配置（本仓库已启用，以下保留供复刻者参考）

1. 把仓库推送到 GitHub，默认分支使用 `main` 或 `master`。
2. 打开仓库的 **Settings → Pages**。
3. 在 **Build and deployment** 中把 **Source** 设为 **GitHub Actions**。
4. 推送一次代码，或手动运行 **Deploy static study site** 工作流。

本仓库的实际发布地址：

```text
https://oreomolly.cn/CS146S_CN_study/
```

因为账号的 `sysuleo.github.io` 已绑定自定义域名 `oreomolly.cn`，GitHub 会把本项目的站点重定向到 `oreomolly.cn/CS146S_CN_study/`。本仓库名不是 `<用户名>.github.io`，所以不会占用根域。

> 自定义域名只能配置在 `<用户名>.github.io` 这个用户站仓库上，project site 会全部跟随它。因此换域名时只需改用户站的 **Settings → Pages → Custom domain** 一处，本项目仓库不需要 `CNAME` 文件。

## HTTPS 与 DNS

站点已启用 HTTPS，证书由 GitHub Pages 自动签发（Let's Encrypt，`CN=oreomolly.cn`，SAN 含 `oreomolly.cn` 与 `www.oreomolly.cn`）。

域名侧配置（已生效，供复刻者参考）：

- 根域 `oreomolly.cn` 的 A 记录指向 GitHub Pages 当前 IP：`185.199.108.153`、`185.199.109.153`、`185.199.110.153`、`185.199.111.153`
- `www` 通过 CNAME 指向 `sysuleo.github.io`，访问时由 GitHub 301 到根域
- 根域**不要**添加 AAAA 记录：GitHub Pages 自定义域名不提供 IPv6 直连，加了会让部分网络环境下的访问直接失败

> 需要避开的旧配置：GitHub Pages 早期 IP `192.30.252.153`、`192.30.252.154` 只服务 HTTP，证书为 `*.github.com`，指向它们会让 `https://<自定义域名>` 报证书不匹配。把 A 记录改到新 IP 后证书会自动签发，无需在 Pages 设置里反复保存 Custom domain（值未改动时 Save 按钮本就是灰的）。

> 迁移记录：站点原使用 `liuw.tech`，2026-11-21 切换至 `oreomolly.cn`。`liuw.tech` 已不再由 GitHub Pages 提供服务，旧链接会返回 404。

## 发布内容

- `app/static/index.html`：根入口，跳转到 `schedule.html`
- `app/static/schedule.html`：每周课表，同时作为站点首页
- `app/static/study/`：28 个学习页、PPT、原文图表（`study/index.html` 是学习资料索引页）
- `app/static/.nojekyll`：工作流生成，避免 Pages 的 Jekyll 处理

工作流会先运行：

```bash
python tools/build.py
python tools/check.py
```

因此提交前不需要手工同步生成页；推送 Markdown 源文件后，Actions 会重新生成并检查链接。

## 静态版不包含什么

GitHub Pages 只提供静态文件，不支持本项目里的运维接口：

- `/admin` 运维面板
- `POST /api/jobs` 构建任务
- `POST /api/restart` 重启服务
- 通过 `.env` 修改本地端口

这些能力属于本地或 Linux 服务器部署，见 [DEPLOY.md](DEPLOY.md)。如果只是让读者阅读课程内容，GitHub Pages 已足够。

## 更新内容

1. 修改 `content/study_src/*.md` 或 `content/schedule.md`。
2. 本地运行 `python tools/build.py && python tools/check.py`。
3. 提交并推送；GitHub Actions 会自动发布。

不要在 GitHub Pages 上直接修改生成后的 HTML，下一次构建会被覆盖。
