import html
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "content" / "study_src"

MAPPING = {
    "9-24": {
        "file": "w1-lecture-9-24-transcript.md",
        "slides": {
            1: ("text", "Welcome back. We have a quick one-two"),
            2: ("text", "I want to start with some logistics"),
            3: ("text", "Tuesday was a proof of concept"),
            4: ("text", "We'll be able to see everything except the intelligence layer"),
            5: ("text", "Two days ago, we went through the core execution loop"),
            6: ("text", "A lot goes into the harness around the intelligence"),
            7: ("text", "A lot goes into the harness around the intelligence"),
            8: ("text", "We said we'd start with tools, so let's dive into the tool lists"),
            9: ("text", "For anyone who isn't familiar, a system prompt"),
            10: ("text", "CLAUDE.md is a user-controlled counterpart"),
            11: ("text", "Plan mode is a mode you can use"),
            12: ("text", "At their core, skills describe a written procedure"),
            13: ("text", "Subagents let you delegate parts of a task"),
            14: ("text", "There are also hooks"),
            15: ("text", "When your context gets increasingly long"),
            16: ("text", "There are a lot of bells and whistles"),
            17: ("end", "## 学习者视角"),
        },
    },
    "9-29": {
        "file": "w2-lecture-9-29-transcript.md",
        "slides": {
            1: ("heading", "### 课程安排与 OSS 合作项目"),
            2: ("text", "Today we're also officially announcing the OSS Partners program"),
            3: ("text", "Today's focus is advanced prompting and context engineering"),
            4: ("text", "One of the biggest things you have to learn"),
            5: ("text", "Does anyone remember when"),
            6: ("text", "Does anyone remember when"),
            7: ("text", "Here's a thought exercise: how would you build a Mint clone?"),
            8: ("text", "To do that at production scale"),
            9: ("text", "First, you have to understand an unfamiliar codebase"),
            10: ("text", "We'll focus on REPIT: research, propose, plan, implement, and test"),
            11: ("text", "We'll focus on REPIT: research, propose, plan, implement, and test"),
            12: ("text", "The first step is research"),
            13: ("text", "When do you clear context?"),
            14: ("text", "There's an open question: when should you use vanilla prompting"),
            15: ("text", "Something like a copy change or a small fix"),
            16: ("text", "For very large projects in my day-to-day work"),
            17: ("text", "Superpowers is effectively the framework I described on steroids"),
            18: ("text", "At its core, the repository is just a set of skills"),
        },
    },
    "10-1": {
        "file": "w2-lecture-10-1-transcript.md",
        "slides": {
            1: ("heading", "### 课程要求：AI Slop 直接 0 分"),
            2: ("text", "One hard requirement for grading"),
            3: ("heading", "### MCP 是什么"),
            4: ("text", "LLMs today are pretrained systems"),
            5: ("text", "MCP stands for Model Context Protocol"),
            6: ("text", "Traditionally, when we wanted to connect"),
            7: ("text", "MCP provides a more efficient way"),
            8: ("text", "As long as the LLM side knows how to speak MCP"),
            9: ("text", "The host is what we mean when we say Cursor"),
            10: ("text", "At a high level, when you're interacting with an MCP server"),
            11: ("text", "You shouldn't think of an MCP server as just a REST API wrapper"),
            12: ("text", "The basic approach is to create a meta MCP server"),
            13: ("text", "Suppose the request is"),
            14: ("text", "MCP gateways are a separate topic"),
            15: ("end", "## 学习者视角"),
            16: ("end", "## 学习者视角"),
            17: ("end", "## 学习者视角"),
        },
    },
}


def block(deck, number):
    return (
        f'<div class="slide-block"><p class="slide-block-title">对应 PPT · Slide {number}</p>'
        f'<div class="slide-strip"><figure class="slide">'
        f'<a class="slide-link" href="assets/slides/{deck}/{number:02d}.png" target="_blank" rel="noopener noreferrer">'
        f'<img src="assets/slides/{deck}/{number:02d}.png" alt="{deck} slide {number}" loading="lazy"></a>'
        f'<figcaption>Slide {number}</figcaption></figure></div></div>\n\n'
    )


def pair_spans(text):
    spans = []
    for match in re.finditer(r'<div class="bilingual-pair">\s*<p class="src">(.*?)</p>', text, re.S):
        source = html.unescape(re.sub(r"<[^>]+>", "", match.group(1)))
        spans.append((match.start(), source))
    return spans


def locate(text, kind, anchor):
    if kind == "heading":
        position = text.find(anchor)
    elif kind == "end":
        position = text.find(anchor)
    else:
        position = -1
        for start, source in pair_spans(text):
            if anchor in source:
                position = start
                break
    return position


def process(deck, config):
    path = SRC / config["file"]
    text = path.read_text(encoding="utf-8")
    text = re.sub(r'<div class="slide-block">.*?</div></div>\n*', "", text, flags=re.S)
    text = re.sub(r"<!-- slides:.*?-->.*?<!-- /slides -->\n*", "", text, flags=re.S)

    placed = []
    for number, (kind, anchor) in sorted(config["slides"].items()):
        position = locate(text, kind, anchor)
        if position < 0:
            print(f"  WARN {deck} slide {number}: anchor not found: {anchor}")
            continue
        placed.append((position, number))

    grouped = {}
    for position, number in placed:
        grouped.setdefault(position, []).append(number)
    for position in sorted(grouped, reverse=True):
        numbers = sorted(grouped[position])
        injected = "".join(block(deck, number) for number in numbers)
        text = text[:position] + injected + text[position:]

    path.write_text(text, encoding="utf-8")
    print(f"  {deck}: placed {len(placed)} slides")


def main():
    for deck, config in MAPPING.items():
        process(deck, config)


if __name__ == "__main__":
    main()
