# GitHub Pages 静态托管

读者不需要 FastAPI 也能浏览课程表和学习页。仓库已经附带 `.github/workflows/pages.yml`，推送后由 GitHub Actions 构建并发布 `app/static`。

## 一次性配置（本仓库已启用，以下保留供复刻者参考）

1. 把仓库推送到 GitHub，默认分支使用 `main` 或 `master`。
2. 打开仓库的 **Settings → Pages**。
3. 在 **Build and deployment** 中把 **Source** 设为 **GitHub Actions**。
4. 推送一次代码，或手动运行 **Deploy static study site** 工作流。

本仓库的实际发布地址：

```text
http://liuw.tech/CS146S_CN_study/
```

因为账号的 `sysuleo.github.io` 已绑定自定义域名 `liuw.tech`，GitHub 会把本项目的站点重定向到 `liuw.tech/CS146S_CN_study/`。本仓库名不是 `<用户名>.github.io`，所以不会占用根域。

## HTTPS 与 DNS

`liuw.tech` 的 A 记录目前指向 GitHub Pages 的旧 IP（`192.30.252.153`、`192.30.252.154`）：这些 IP 只服务 HTTP，证书是 `*.github.com`，所以 `https://liuw.tech` 会报证书不匹配。

把根域 A 记录改为 GitHub Pages 当前 IP：

```text
185.199.108.153
185.199.109.153
185.199.110.153
185.199.111.153
```

`www` 保持 CNAME 到 `sysuleo.github.io`。DNS 生效后，到 `sysuleo/sysuleo.github.io` 的 **Settings → Pages** 重新保存一次 Custom domain，等待 GitHub 签发 Let's Encrypt 证书，随后勾选 **Enforce HTTPS**。证书就绪后，访问地址即可升级为 `https://liuw.tech/CS146S_CN_study/`。

## 发布内容

- `app/static/index.html`：根入口，跳转到 `study/`
- `app/static/schedule.html`：课程表
- `app/static/study/`：28 个学习页、PPT、原文图表
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
