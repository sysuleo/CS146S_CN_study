# Linux 部署

> 只想让读者在线阅读，不需要部署服务器：使用 [GitHub Pages 静态托管](PUBLISH.md)。本文件适用于需要 `/admin` 和构建任务 API 的自托管场景。

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
