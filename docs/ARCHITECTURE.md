# 目录结构

```text
.
├─ app/
│  ├─ server.py              # FastAPI 静态站 + 构建任务 API
│  └─ static/
│     ├─ index.html          # GitHub Pages 根入口，跳转到 study/
│     ├─ schedule.html       # 课程表
│     ├─ admin.html          # 运维面板
│     └─ study/              # 学习站页面与资源
├─ content/
│  ├─ study_src/             # 学习页 Markdown 源文件
│  └─ schedule.md            # 课表 Markdown
├─ data/
│  └─ syllabus2026.json      # 官方 Syllabus 结构化数据
├─ tools/
│  ├─ build.py               # 生成学习站并回链课表
│  ├─ slides.py              # 逐页锚点插入 PPT
│  ├─ check.py               # 本地链接检查
│  └─ sync_syllabus.py       # 同步官网 Syllabus
├─ docs/                     # 部署与架构说明
├─ .github/workflows/        # GitHub Pages 发布
├─ .local/                   # 原始抓取、缓存、预览、任务日志（不提交）
├─ start.sh / stop.sh / restart.sh
├─ Dockerfile / docker-compose.yml
└─ README.md
```

## 构建链

1. `tools/sync_syllabus.py` 从 `.local/source/syllabus-latest.json` 同步 `data/syllabus2026.json`。
2. `tools/slides.py` 按逐页锚点插入 PPT。
3. `tools/build.py` 从 `content/study_src/` 生成 `app/static/study/`，并回链 `app/static/schedule.html`。
4. `tools/check.py` 检查本地链接。

## API

- `GET /api/health`
- `POST /api/jobs` `{kind: rebuild|sync|full}`
- `GET /api/jobs/{id}`
- `POST /api/restart`（需要 `STUDY_ALLOW_RESTART=1`）
