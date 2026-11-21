import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
files = list((ROOT / "app" / "static" / "study").glob("*.html")) + [ROOT / "app" / "static" / "schedule.html"]

missing = []
total = 0
for path in files:
    text = path.read_text(encoding="utf-8")
    for href in re.findall(r'href="([^"]+)"', text):
        if href.startswith(("http", "#", "mailto:")):
            continue
        total += 1
        target = (path.parent / href.split("#")[0]).resolve()
        if not target.exists():
            missing.append((path.name, href))

index = (ROOT / "app" / "static" / "study/index.html").read_text(encoding="utf-8")
schedule = (ROOT / "app" / "static" / "schedule.html").read_text(encoding="utf-8")
pages = [p for p in (ROOT / "app" / "static" / "study").glob("*.html") if p.name != "index.html"]

print(f"local links: {total}, missing: {len(missing)}")
for item in missing[:30]:
    print("MISSING", item)
print(f"index cards: {index.count('class=\"card\"')}")
print(f"study pages: {len(pages)}")
print(f"schedule study links: {schedule.count('href=\"study/')}")
print(f"schedule 中译 chips: {schedule.count('class=\"mini\"')}")
