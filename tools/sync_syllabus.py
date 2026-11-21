import json
from pathlib import Path

root = Path(__file__).resolve().parent.parent
latest = json.loads((root / ".local" / "source" / "syllabus-latest.json").read_text(encoding="utf-8"))

# Keep the locally added Lee Robinson guest lecture video.
w3 = latest[2]["sessions"][1]
if not any(link.get("label") == "Video" for link in w3.get("links", [])):
    w3.setdefault("links", []).append(
        {"label": "Video", "href": "https://www.youtube.com/watch?v=L1OBRtfPS34"}
    )

(root / "data" / "syllabus2026.json").write_text(
    json.dumps(latest, ensure_ascii=False, indent=2), encoding="utf-8"
)
print("synced", len(latest), "weeks")
