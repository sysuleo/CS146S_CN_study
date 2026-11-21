$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot
if (-not $env:HOST) { $env:HOST = "0.0.0.0" }
if (-not $env:PORT) { $env:PORT = "8787" }
python -m uvicorn app.server:app --host $env:HOST --port $env:PORT
