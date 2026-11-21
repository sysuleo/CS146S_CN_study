#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

if [ -f .env ]; then
  set -a
  . ./.env
  set +a
fi

export HOST="${HOST:-0.0.0.0}"
export PORT="${PORT:-8787}"
PYTHON_BIN="${PYTHON:-python3}"
LOG_FILE=".local/server.log"
PID_FILE=".local/server.pid"

mkdir -p .local

if [ "${FOREGROUND:-0}" = "1" ]; then
  exec "$PYTHON_BIN" -m uvicorn app.server:app --host "$HOST" --port "$PORT"
fi

if command -v lsof >/dev/null 2>&1 && [ -n "$(lsof -ti tcp:"$PORT" || true)" ]; then
  echo "port $PORT is already in use; run ./restart.sh or ./stop.sh first" >&2
  exit 1
fi

if command -v setsid >/dev/null 2>&1; then
  setsid nohup "$PYTHON_BIN" -m uvicorn app.server:app --host "$HOST" --port "$PORT" \
    >> "$LOG_FILE" 2>&1 < /dev/null &
else
  nohup "$PYTHON_BIN" -m uvicorn app.server:app --host "$HOST" --port "$PORT" \
    >> "$LOG_FILE" 2>&1 < /dev/null &
fi
PID=$!
echo "$PID" > "$PID_FILE"
sleep 1

if ! kill -0 "$PID" 2>/dev/null; then
  echo "failed to start; see $LOG_FILE" >&2
  tail -n 20 "$LOG_FILE" >&2 || true
  rm -f "$PID_FILE"
  exit 1
fi

echo "started pid=$PID port=$PORT log=$LOG_FILE"
