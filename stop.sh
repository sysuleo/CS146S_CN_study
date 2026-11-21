#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

if [ -f .env ]; then
  set -a
  . ./.env
  set +a
fi

PORT="${PORT:-8787}"
PID_FILE=".local/server.pid"

if [ -f "$PID_FILE" ]; then
  PID="$(cat "$PID_FILE")"
  if [ -n "$PID" ] && kill -0 "$PID" 2>/dev/null \
    && ps -p "$PID" -o args= | grep -q "uvicorn app.server:app"; then
    kill "$PID"
    rm -f "$PID_FILE"
    echo "stopped pid $PID (port $PORT)"
    exit 0
  fi
  rm -f "$PID_FILE"
fi

if command -v lsof >/dev/null 2>&1; then
  PIDS="$(lsof -ti tcp:"$PORT" || true)"
  if [ -n "$PIDS" ]; then
    kill $PIDS
    echo "stopped port $PORT"
    exit 0
  fi
fi

pkill -f "uvicorn app.server:app" || true
echo "stop signal sent"
