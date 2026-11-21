import json
import os
import subprocess
import sys
import threading
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path

from fastapi import FastAPI, Header, HTTPException, Request
from fastapi.responses import FileResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

ROOT = Path(__file__).resolve().parent.parent
STATIC = ROOT / "app" / "static"
STUDY = STATIC / "study"
JOBS = ROOT / ".local" / "jobs"
JOBS.mkdir(parents=True, exist_ok=True)

app = FastAPI(title="CS146S Study Server", version="2.0.0")
app.mount("/study", StaticFiles(directory=STUDY, html=True), name="study")

_lock = threading.Lock()
_current_job = {"id": None}

COMMANDS = {
    "rebuild": ["tools/build.py"],
    "sync": ["tools/sync_syllabus.py", "tools/build.py"],
    "full": ["tools/slides.py", "tools/build.py", "tools/check.py"],
}


class JobRequest(BaseModel):
    kind: str = "rebuild"
    note: str = ""


def now():
    return datetime.now(timezone.utc).isoformat()


def job_path(job_id):
    return JOBS / f"{job_id}.json"


def log_path(job_id):
    return JOBS / f"{job_id}.log"


def write_job(job):
    job_path(job["id"]).write_text(
        json.dumps(job, ensure_ascii=False, indent=2), encoding="utf-8"
    )


def read_job(job_id):
    path = job_path(job_id)
    if not path.exists():
        raise HTTPException(status_code=404, detail="job not found")
    return json.loads(path.read_text(encoding="utf-8"))


def run_job(job_id, kind):
    job = read_job(job_id)
    job["status"] = "running"
    job["started_at"] = now()
    write_job(job)
    log = log_path(job_id)
    try:
        with log.open("w", encoding="utf-8") as handle:
            for script in COMMANDS[kind]:
                handle.write(f"$ python {script}\n")
                handle.flush()
                process = subprocess.run(
                    [sys.executable, script],
                    cwd=ROOT,
                    stdout=handle,
                    stderr=subprocess.STDOUT,
                    text=True,
                )
                handle.write(f"\n[exit {process.returncode}] {script}\n")
                handle.flush()
                if process.returncode != 0:
                    raise RuntimeError(f"{script} exited with {process.returncode}")
        job["status"] = "success"
    except Exception as exc:
        job["status"] = "failed"
        job["error"] = str(exc)
        with log.open("a", encoding="utf-8") as handle:
            handle.write(f"\nERROR: {exc}\n")
    finally:
        job["finished_at"] = now()
        write_job(job)
        with _lock:
            _current_job["id"] = None


def require_token(token):
    expected = os.environ.get("STUDY_API_TOKEN")
    if expected and token != expected:
        raise HTTPException(status_code=401, detail="invalid api token")


@app.get("/")
def index():
    return RedirectResponse(url="/study/", status_code=307)


@app.get("/schedule")
def schedule():
    return FileResponse(STATIC / "schedule.html")


@app.get("/schedule.html")
def schedule_html():
    return FileResponse(STATIC / "schedule.html")


@app.get("/CS146S-Fall2026-课表.html")
def schedule_alias():
    return RedirectResponse(url="/schedule", status_code=307)


@app.get("/admin")
def admin():
    return FileResponse(STATIC / "admin.html")


@app.get("/admin.html")
def admin_html():
    return FileResponse(STATIC / "admin.html")


@app.get("/api/health")
def health(request: Request):
    return {
        "ok": True,
        "time": now(),
        "port": request.url.port or os.environ.get("PORT", "8787"),
        "configured_port": os.environ.get("PORT", "8787"),
        "running_job": _current_job["id"],
        "study_pages": sum(
            1 for path in STUDY.glob("*.html") if path.name != "index.html"
        ),
        "static_root": str(STATIC),
    }


@app.post("/api/jobs")
def create_job(request: JobRequest, x_api_token: str | None = Header(default=None)):
    require_token(x_api_token)
    if request.kind not in COMMANDS:
        raise HTTPException(
            status_code=400, detail=f"kind must be one of {sorted(COMMANDS)}"
        )
    with _lock:
        if _current_job["id"]:
            raise HTTPException(
                status_code=409,
                detail=f"job {_current_job['id']} is already running",
            )
        job_id = time.strftime("%Y%m%d-%H%M%S") + "-" + uuid.uuid4().hex[:6]
        job = {
            "id": job_id,
            "kind": request.kind,
            "note": request.note,
            "status": "queued",
            "created_at": now(),
            "started_at": None,
            "finished_at": None,
            "error": None,
        }
        write_job(job)
        log_path(job_id).write_text("", encoding="utf-8")
        _current_job["id"] = job_id
    thread = threading.Thread(target=run_job, args=(job_id, request.kind), daemon=True)
    thread.start()
    return job


@app.get("/api/jobs")
def list_jobs(limit: int = 20):
    jobs = []
    for path in sorted(JOBS.glob("*.json"), reverse=True)[: max(1, min(limit, 100))]:
        jobs.append(json.loads(path.read_text(encoding="utf-8")))
    return {"jobs": jobs}


@app.get("/api/jobs/{job_id}")
def get_job(job_id: str):
    job = read_job(job_id)
    log = log_path(job_id)
    if log.exists():
        lines = log.read_text(encoding="utf-8", errors="replace").splitlines()
        job["log_tail"] = "\n".join(lines[-200:])
    else:
        job["log_tail"] = ""
    return job


@app.post("/api/restart")
def restart(x_api_token: str | None = Header(default=None)):
    require_token(x_api_token)
    if os.environ.get("STUDY_ALLOW_RESTART") != "1":
        raise HTTPException(
            status_code=403,
            detail="restart disabled; set STUDY_ALLOW_RESTART=1 and use systemd/docker restart policy",
        )
    threading.Timer(0.8, lambda: os._exit(0)).start()
    return {"ok": True, "message": "restarting; supervisor should start it again"}
