# 本地运行与部署

> 只想在线阅读，不需要部署服务器：直接访问 <https://liuw.tech/CS146S_CN_study/>，或使用 [GitHub Pages 静态托管](PUBLISH.md)。本文件适用于本地跑一份、二次构建，以及需要 `/admin` 和构建任务 API 的自托管场景（Linux / Windows / Docker）。

## 1. 直接启动

```bash
cd CS146S
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt

cp .env.example .env
# 修改 PORT / STUDY_API_TOKEN
chmod +x start.sh stop.sh restart.sh
./start.sh
```

`start.sh` 默认后台运行，日志在 `.local/server.log`，PID 在 `.local/server.pid`。`./stop.sh` 停止，`./restart.sh` 重启；前台调试使用 `FOREGROUND=1 ./start.sh`。

访问：

- `http://服务器:8787/` 学习站
- `http://服务器:8787/schedule` 课程表
- `http://服务器:8787/admin` 运维面板

端口由 `.env` 的 `PORT` 控制，默认 8787。

## 2. systemd

```ini
[Unit]
Description=CS146S Study Site
After=network.target

[Service]
Type=simple
WorkingDirectory=/opt/cs146s
EnvironmentFile=/opt/cs146s/.env
ExecStart=/opt/cs146s/.venv/bin/python -m uvicorn app.server:app --host 0.0.0.0 --port ${PORT}
Restart=always
RestartSec=3
User=www-data

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now cs146s
```

设置 `STUDY_ALLOW_RESTART=1` 后，`/admin` 的“重启服务”按钮会退出进程，由 systemd 重新拉起。

## 3. Docker

```bash
cp .env.example .env
docker compose up --build -d
```

`PORT` 同时控制容器内监听端口和宿主机映射端口。

## 4. Nginx 反向代理（可选）

```nginx
location / {
    proxy_pass http://127.0.0.1:8787;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
}
```

## 5. 本地跑一份（Windows / 构建 / 验收）

只想在本地看效果或改内容，不走 systemd / Nginx 时用这一节。

### Windows PowerShell

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt

Copy-Item .env.example .env
.\start.ps1
```

默认地址 `http://127.0.0.1:8787/`；`/schedule` 课程表、`/admin` 运维面板、`/api/health` 健康检查。

### 构建与验收

```bash
python tools/slides.py    # 按逐页锚点插入课堂 PPT
python tools/build.py     # 由 content/study_src 生成学习页并回链课表
python tools/check.py     # 检查本地链接、页面结构和资源数量
```

也可以用 Makefile：

```bash
make build     # 只重建页面
make full      # PPT + 页面 + 检查
make check     # 只做检查
make docker    # 启动 Docker
```

当前验收结果：

```text
local links: 554, missing: 0
index cards: 28
study pages: 28
schedule study links: 29
schedule 中译 chips: 25
```

### 内容源与生成物

- 内容源：`content/study_src/*.md`
- 课表源：`content/schedule.md` 与 `data/syllabus2026.json`
- 生成物：`app/static/study/*.html`

不要直接修改生成后的学习页。先改 Markdown 源文件，再运行构建脚本；否则下一次构建会覆盖手工修改。

### 修改端口

端口只在一个地方配置：

```bash
# .env
HOST=0.0.0.0
PORT=9000
```

```bash
./restart.sh
# 或
docker compose up --build -d
```

`PORT` 同时控制服务监听端口和 Docker 宿主机映射端口。

## 6. 运维接口

`app/server.py` 提供静态站和最小的运维接口：

| 接口 | 用途 |
|---|---|
| `GET /api/health` | 返回服务状态、端口和学习页数量 |
| `POST /api/jobs` | 创建构建任务，`kind` 取 `rebuild`、`sync` 或 `full` |
| `GET /api/jobs` | 查看最近任务 |
| `GET /api/jobs/{id}` | 查看任务状态与日志尾部 |
| `POST /api/restart` | 退出进程，交给 systemd 或 Docker 重新拉起 |

说明：

- 这里的“建单”指**站点构建任务**，不是易协作或内部工单。
- 开启 `STUDY_ALLOW_RESTART=1` 后，`/api/restart` 才会生效。
- 设置 `STUDY_API_TOKEN` 后，创建任务和重启需要携带 `X-API-Token`。
- 后台任务日志写入 `.local/jobs/`，不会进入 Git。
