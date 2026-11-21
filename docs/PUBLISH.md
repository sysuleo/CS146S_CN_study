# GitHub Pages 静态托管

读者不需要 FastAPI 也能浏览课程表和学习页。仓库已经附带 `.github/workflows/pages.yml`，推送后由 GitHub Actions 构建并发布 `app/static`。

## 一次性配置

1. 把仓库推送到 GitHub，默认分支使用 `main` 或 `master`。
2. 打开仓库的 **Settings → Pages**。
3. 在 **Build and deployment** 中把 **Source** 设为 **GitHub Actions**。
4. 推送一次代码，或手动运行 **Deploy static study site** 工作流。

发布地址通常是：

```text
https://<用户名>.github.io/<仓库名>/
```

如果仓库名是 `<用户名>.github.io`，地址则是：

```text
https://<用户名>.github.io/
```

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
