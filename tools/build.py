import html
import json
import re
from pathlib import Path

import markdown

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "content" / "study_src"
OUT = ROOT / "app" / "static" / "study"
ASSETS = OUT / "assets"

WEEK_TITLES = {
    1: "The Internals of Coding Agents",
    2: "Advanced Context Engineering",
    3: "Agent Skills and CLI",
    4: "Customizing Your Agent and Repository",
    5: "Agent-Ready Codebases",
    6: "Agentic Code Review",
    7: "Security",
    8: "Background Agents",
    9: "The Software Factory",
    10: "The AI-Native Team + The Future",
}

WEEK_ZH = {
    1: "Coding Agent 内部机制",
    2: "高级上下文工程",
    3: "Agent Skills 与 CLI",
    4: "定制 Agent 与代码仓库",
    5: "Agent-Ready 代码库",
    6: "Agent 代码审查",
    7: "安全",
    8: "后台 Agent",
    9: "软件工厂",
    10: "AI 原生团队与未来",
}

VIDEO_READINGS = {
    "https://youtube.com/watch?v=s7ZzkdvCMDY": "Building a Coding Agent",
    "https://www.youtube.com/watch?v=ShuJ_CN6zr4": "Making Codebases Agent Ready",
    "https://www.youtube.com/watch?v=L1OBRtfPS34": "Stanford CS146S: How always-on agents work",
}

READING_ORDER = {
    "w1-lessons-from-building-claude-code": 1,
    "w1-dive-into-claude-code": 2,
    "w1-lecture-9-24-transcript": 90,
    "w2-the-context-tax-when-to-compact": 1,
    "w2-openspec": 2,
    "w2-superpowers": 3,
    "w2-enterprise-mcp-cloudflare": 4,
    "w2-lecture-9-29-transcript": 90,
    "w2-lecture-10-1-transcript": 91,
    "w3-pstack": 1,
    "w3-matt-pocock-s-skills": 2,
    "w3-browse-sh": 3,
    "w4-i-still-prefer-mcp-over-skills": 1,
    "w4-agents-md-factory-docs": 2,
    "w4-steering-claude-code": 3,
    "w4-writing-a-good-claude-md": 4,
    "w5-making-ergonomic-repositories": 1,
    "w6-layered-code-review-and-risk-based-human-oversight": 1,
    "w6-coordinating-specialist-review-agents-at-scale": 2,
    "w6-beyond-the-diff-context-testing-and-model-selection": 3,
    "w8-spotify-background-coding-agent": 1,
    "w8-stripe-minions": 2,
    "w8-ramp-background-agent": 3,
    "w8-langchain-robin": 4,
    "w9-warp-factory-issue-to-pr": 1,
    "w9-software-factory": 2,
    "w9-openinspect-background-agents": 3,
    "w9-warpbench": 4,
}

TRANSCRIPT_PAGES = {
    "https://themodernsoftware.dev/materials/9-24-26-transcript.txt": "w1-lecture-9-24-transcript",
    "https://themodernsoftware.dev/materials/9-29-26-transcript.txt": "w2-lecture-9-29-transcript",
    "https://themodernsoftware.dev/materials/10-1-26-transcript.txt": "w2-lecture-10-1-transcript",
}


def parse_frontmatter(text):
    if not text.startswith("---"):
        return {}, text
    _, rest = text.split("---", 1)
    front, body = rest.split("---", 1)
    meta = {}
    for line in front.strip().splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            meta[key.strip()] = value.strip().strip('"').strip("'")
    return meta, body.lstrip()


def collect_pages():
    pages = []
    for path in sorted(SRC.glob("*.md")):
        meta, body = parse_frontmatter(path.read_text(encoding="utf-8"))
        meta["body"] = body
        meta["path"] = path
        meta.setdefault("slug", path.stem)
        meta["week"] = int(meta.get("week", 0))
        meta["minutes"] = int(meta.get("minutes", 10))
        pages.append(meta)
    pages.sort(key=lambda p: (p["week"], READING_ORDER.get(p["slug"], 99), p["slug"]))
    return pages


ARTICLE_TEMPLATE = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} · CS146S 学习站</title>
<meta name="description" content="{title} 的中文精译、学习者总结与延伸练习">
<link rel="stylesheet" href="assets/study.css">
</head>
<body>
<div class="progress" id="progress"></div>
<header class="topbar">
  <div class="topbar-inner">
    <a class="brand" href="index.html">CS146S <span>学习站</span></a>
    <nav>
      <a href="../schedule.html">返回课表</a>
      <a href="index.html">全部导读</a>
      <a class="original" href="{source_url}" target="_blank" rel="noopener noreferrer">阅读原文 ↗</a>
    </nav>
  </div>
</header>
<main class="article-shell">
  <div class="article-layout">
    <aside class="toc-side">
      <details open>
        <summary>本页目录</summary>
        <nav class="toc-nav">
{toc}
        </nav>
        <a class="toc-top" href="#top">回到顶部 ↑</a>
      </details>
    </aside>
    <article id="top">
      <div class="breadcrumb"><a href="index.html">学习站</a> / Week {week} · {week_zh}</div>
    <header class="article-head">
      <div class="kicker">Week {week} · {kind} · {coverage}</div>
      <h1>{title}</h1>
      <p class="original-title">原文：<a href="{source_url}" target="_blank" rel="noopener noreferrer">{original}</a></p>
      <div class="meta">
        <span>{author}</span>
        <span>{date}</span>
        <span>约 {minutes} 分钟</span>
      </div>
    </header>
    <div class="article-body">
{content}
    </div>
    <div class="article-foot">
      <div class="notice">
        <strong>阅读说明：</strong>{coverage_note}
      </div>
      <div class="pager">
        {prev_link}
        {next_link}
      </div>
      </div>
    </article>
  </div>
</main>
<footer class="site-foot">
  <p>CS146S: The Modern Software Developer · Fall 2026 · 中文学习站</p>
  <p><a href="../schedule.html">回到课程表</a></p>
</footer>
<script>
const bar = document.getElementById('progress');
addEventListener('scroll', () => {{
  const h = document.documentElement;
  const max = h.scrollHeight - h.clientHeight;
  bar.style.width = (max > 0 ? (h.scrollTop / max) * 100 : 0) + '%';
}}, {{ passive: true }});

const tocLinks = [...document.querySelectorAll('.toc-nav a')];
const tocDetails = document.querySelector('.toc-side details');
if (tocDetails && window.matchMedia('(max-width: 1080px)').matches) {{
  tocDetails.removeAttribute('open');
}}
const tocTargets = tocLinks
  .map((link) => document.getElementById(link.getAttribute('href').slice(1)))
  .filter(Boolean);
if ('IntersectionObserver' in window && tocTargets.length) {{
  const observer = new IntersectionObserver((entries) => {{
    entries.forEach((entry) => {{
      if (!entry.isIntersecting) return;
      tocLinks.forEach((link) => link.classList.remove('active'));
      const active = tocLinks.find((link) => link.getAttribute('href') === '#' + entry.target.id);
      if (active) active.classList.add('active');
    }});
  }}, {{ rootMargin: '-18% 0px -68% 0px', threshold: 0 }});
  tocTargets.forEach((target) => observer.observe(target));
}}
</script>
</body>
</html>"""


def coverage_note(meta):
    coverage = meta.get("coverage", "")
    if meta.get("slug") == "w1-dive-into-claude-code":
        return "正文逐段对照翻译；参考文献与附录未翻译，完整原文见页首链接。"
    if meta.get("slug") == "w3-browse-sh":
        return "产品说明、CLI 用法与示例逐段翻译；站点目录条目未逐条翻译。"
    if meta.get("kind") == "课堂实录":
        return (
            "本页按讲课顺序精译技术内容，删除寒暄、课程行政、口头填充和无法辨认片段；"
            "保留核心论证、例子、数字和结论。它不是逐字听写翻译，而是可复习的课堂精译。"
        )
    if "重点" in coverage or "论文" in coverage:
        return (
            "原文篇幅较长，本页采用“重点章节精译 + 全文结构导读”，"
            "保留核心论证、关键数据和作者结论；为避免低质量逐字机翻，未逐句复制全文。"
        )
    if "产品" in coverage or "文档" in coverage:
        return "原文为产品/文档页面，本页翻译核心说明与工作流，并补充学习者视角。"
    return "本页按原文顺序精译，合并了重复表述；所有关键论点、数据和结论均来自原文。"


def render_toc(tokens):
    items = []
    for token in tokens:
        if token.get("level", 2) > 4:
            continue
        children = render_toc(token.get("children", []))
        items.append(
            f'<li class="toc-l{token.get("level", 2)}">'
            f'<a href="#{token["id"]}">{html.escape(token["name"])}</a>'
            f'{children}</li>'
        )
    return "<ul>" + "".join(items) + "</ul>" if items else ""


def build_article(page, prev_page, next_page):
    md = markdown.Markdown(
        extensions=["extra", "sane_lists", "toc"],
        extension_configs={"toc": {"permalink": False}},
    )
    content = md.convert(page["body"])
    toc = render_toc(md.toc_tokens)
    prev_link = (
        f'<a class="prev" href="{prev_page["slug"]}.html">← {html.escape(prev_page["title"])}</a>'
        if prev_page
        else "<span></span>"
    )
    next_link = (
        f'<a class="next" href="{next_page["slug"]}.html">{html.escape(next_page["title"])} →</a>'
        if next_page
        else "<span></span>"
    )
    return ARTICLE_TEMPLATE.format(
        title=html.escape(page["title"]),
        original=html.escape(page.get("original", "")),
        week=page["week"],
        week_zh=WEEK_ZH.get(page["week"], ""),
        kind=html.escape(page.get("kind", "文章")),
        coverage=html.escape(page.get("coverage", "精译")),
        source_url=html.escape(page.get("source_url", "#")),
        author=html.escape(page.get("author", "—")),
        date=html.escape(page.get("date", "")),
        minutes=page["minutes"],
        content=content,
        toc=toc,
        coverage_note=coverage_note(page),
        prev_link=prev_link,
        next_link=next_link,
    )


def build_index(pages):
    groups = {}
    for page in pages:
        groups.setdefault(page["week"], []).append(page)

    cards = []
    for week in sorted(set(groups) | set(WEEK_TITLES)):
        items = []
        for page in groups.get(week, []):
            coverage = page.get("coverage", "")
            if "核心" in coverage:
                status_label, status_class = "部分精修", "status-partial"
            elif "直译" in coverage:
                status_label, status_class = "机翻待精修", "status-machine"
            else:
                status_label, status_class = "已精修", "status-polished"
            items.append(
                f"""<a class="card" href="{page['slug']}.html">
  <div class="card-top"><span><span class="tag">{html.escape(page.get('kind', '文章'))}</span> <span class="status {status_class}">{status_label}</span></span><span class="time">{page['minutes']} min</span></div>
  <h3>{html.escape(page['title'])}</h3>
  <p class="card-original">{html.escape(page.get('original', ''))}</p>
  <p class="card-desc">{html.escape(page.get('blurb', ''))}</p>
  <span class="card-link">阅读中译 →</span>
</a>"""
            )
        if items:
            body = f'<div class="card-grid">{"".join(items)}</div>'
        else:
            body = (
                '<p class="week-empty">本周课程没有指定阅读材料，内容以课堂讲授为主。'
                f'<a href="../schedule.html#w{week}">查看本周主题与 Slides →</a></p>'
            )
        cards.append(
            f"""<section class="week-block">
  <div class="week-head">
    <span class="week-no">W{week}</span>
    <div><h2>{WEEK_ZH.get(week, '')}</h2><p>{WEEK_TITLES.get(week, '')}</p></div>
    <a class="week-jump" href="../schedule.html#w{week}">课表 / Slides →</a>
  </div>
  {body}
</section>"""
        )

    videos = "".join(
        f"<li><a href=\"{html.escape(url)}\" target=\"_blank\" rel=\"noopener noreferrer\">{html.escape(title)}</a><span>视频 · 无中译</span></li>"
        for url, title in VIDEO_READINGS.items()
    )

    total_min = sum(p["minutes"] for p in pages)
    lecture_count = sum(1 for p in pages if p.get("kind") == "课堂实录")
    reading_count = len(pages) - lecture_count
    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>CS146S 中文学习站</title>
<meta name="description" content="CS146S Fall 2026 阅读材料中文精译、学习者总结与延伸练习">
<link rel="stylesheet" href="assets/study.css">
</head>
<body>
<header class="hero study-hero">
  <div class="hero-inner">
    <p class="eyebrow">STANFORD CS146S · FALL 2026</p>
    <h1>把课程阅读变成<br>一套可复习的中文学习资料</h1>
    <p class="hero-sub">{reading_count} 篇阅读材料 + {lecture_count} 篇课堂实录 · 中文精译 · 学习者视角总结 · 延伸练习</p>
    <div class="hero-actions">
      <a class="btn light" href="../schedule.html">返回课程表</a>
      <a class="btn ghost" href="#weeks">按周浏览</a>
    </div>
    <div class="hero-stats">
      <div><strong>{len(pages)}</strong><span>篇中译</span></div>
      <div><strong>{total_min}</strong><span>分钟阅读</span></div>
      <div><strong>{len(groups)}/{len(WEEK_TITLES)}</strong><span>周次有阅读</span></div>
    </div>
  </div>
</header>
<main class="index-shell">
  <section class="howto">
    <h2>怎么用这套资料</h2>
    <div class="howto-grid">
      <div><span>1</span><h3>先读原文</h3><p>打开每页顶部的“阅读原文”，先建立自己的理解。</p></div>
      <div><span>2</span><h3>再看精译</h3><p>对照关键段落，确认术语、数据和论证链条。</p></div>
      <div><span>3</span><h3>做延伸</h3><p>用每页末尾的问题和练习，把观点落到自己的项目。</p></div>
    </div>
  </section>
  <section id="weeks" class="weeks">{''.join(cards)}</section>
  <section class="video-note">
    <h2>视频材料</h2>
    <p>以下内容为视频，不做文字翻译；建议按课表时间观看，并记录演讲中的架构取舍。</p>
    <ul>{videos}</ul>
  </section>
</main>
<footer class="site-foot"><p>CS146S: The Modern Software Developer · Fall 2026 · 中文学习站</p></footer>
</body>
</html>"""


def inject_schedule_links(pages):
    schedule = ROOT / "app" / "static" / "schedule.html"
    text = schedule.read_text(encoding="utf-8")
    text = re.sub(r' <a class="mini" href="study/[^"]+">中译</a>', "", text)
    text = re.sub(r' <span class="mini mini-video">视频</span>', "", text)
    text = re.sub(r' <a class="mini mini-transcript" href="study/[^"]+">中译</a>', "", text)
    text = re.sub(
        r'\s*<a class="btn" href="(?:\.\./)?admin\.html">[^<]*</a>',
        "",
        text,
    )
    by_url = {p["source_url"]: p for p in pages}

    def repl(match):
        url = match.group(1)
        page = by_url.get(url)
        if page:
            return (
                f'{match.group(0)} '
                f'<a class="mini" href="study/{page["slug"]}.html">中译</a>'
            )
        if url in VIDEO_READINGS:
            return f'{match.group(0)} <span class="mini mini-video">视频</span>'
        return match.group(0)

    pattern = re.compile(
        r'<a class="reading" href="([^"]+)" target="_blank" rel="noopener noreferrer">[^<]+</a>'
    )
    text = pattern.sub(repl, text)
    for url, slug in TRANSCRIPT_PAGES.items():
        transcript_pattern = re.compile(
            r'(<a class="chip" href="' + re.escape(url) + r'"[^>]*>Transcript</a>)'
        )
        text = transcript_pattern.sub(
            r'\1 <a class="mini mini-transcript" href="study/' + slug + '.html">中译</a>',
            text,
        )
    if 'class="mini"' not in text:
        raise RuntimeError("No translation links injected into schedule")
    if 'href="study/index.html"' not in text:
        text = text.replace(
            '<a class="btn" href="https://themodernsoftware.dev/" target="_blank" rel="noopener noreferrer">课程官网 ↗</a>',
            '<a class="btn" href="study/index.html">中文学习站</a>\n      '
            '<a class="btn" href="https://themodernsoftware.dev/" target="_blank" rel="noopener noreferrer">课程官网 ↗</a>',
        )
    schedule.write_text(text, encoding="utf-8")


def main():
    pages = collect_pages()
    if not pages:
        raise SystemExit("No study markdown files found")
    OUT.mkdir(exist_ok=True)
    ASSETS.mkdir(exist_ok=True)

    for i, page in enumerate(pages):
        prev_page = pages[i - 1] if i > 0 else None
        next_page = pages[i + 1] if i + 1 < len(pages) else None
        (OUT / f"{page['slug']}.html").write_text(
            build_article(page, prev_page, next_page), encoding="utf-8"
        )

    (OUT / "index.html").write_text(build_index(pages), encoding="utf-8")
    inject_schedule_links(pages)
    print(f"Built {len(pages)} study pages + index")
    for page in pages:
        print(f"  W{page['week']} {page['minutes']:>2}min {page['slug']}")


if __name__ == "__main__":
    main()
