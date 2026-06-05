# ============================================================
# pdf_generator.py  —  Export summary as PDF or TXT
# Uses fpdf2 (pure Python, no system dependencies)
# ============================================================

import io
import re
from datetime import datetime
from fpdf import FPDF


def _strip_emoji(text: str) -> str:
    """Remove emoji characters that fpdf can't render."""
    emoji_pattern = re.compile(
        "["
        "\U0001F600-\U0001F64F"
        "\U0001F300-\U0001F5FF"
        "\U0001F680-\U0001F6FF"
        "\U0001F1E0-\U0001F1FF"
        "\U00002702-\U000027B0"
        "\U000024C2-\U0001F251"
        "⚠️📌📰🔍🔎⭐💼🎭🏥🔬⚽💻🌍🌦️💥📜🧠🤖📄🗓️📡"
        "]+",
        flags=re.UNICODE,
    )
    return emoji_pattern.sub("", text).strip()


class NewsPDF(FPDF):
    def __init__(self, title: str, lang: str):
        super().__init__()
        self.doc_title = title
        self.doc_lang  = lang
        self.set_auto_page_break(auto=True, margin=15)
        self.add_page()
        self._build_header()

    def _build_header(self):
        # ── Logo bar ────────────────────────────────────────
        self.set_fill_color(30, 58, 107)   # navy
        self.rect(0, 0, 210, 22, "F")
        self.set_text_color(255, 255, 255)
        self.set_font("Helvetica", "B", 14)
        self.set_xy(10, 5)
        self.cell(0, 12, "News Research Tool  |  AI Summary Report", ln=True)

        # ── Meta line ───────────────────────────────────────
        self.set_fill_color(46, 117, 182)  # accent blue
        self.rect(0, 22, 210, 10, "F")
        self.set_font("Helvetica", "", 9)
        self.set_xy(10, 23)
        self.cell(
            0, 8,
            f"Generated: {datetime.now().strftime('%d %b %Y  %H:%M')}  |  "
            f"Language: {self.doc_lang}  |  "
            f"Query: {_strip_emoji(self.doc_title)[:80]}",
            ln=True,
        )
        self.ln(6)
        self.set_text_color(0, 0, 0)

    def section_heading(self, text: str):
        clean = _strip_emoji(text)
        self.set_font("Helvetica", "B", 12)
        self.set_fill_color(234, 241, 251)
        self.set_text_color(30, 58, 107)
        self.cell(0, 8, clean, ln=True, fill=True)
        self.ln(2)
        self.set_text_color(0, 0, 0)

    def body_text(self, text: str):
        clean = _strip_emoji(text)
        self.set_font("Helvetica", "", 10)
        self.multi_cell(0, 6, clean)
        self.ln(3)

    def divider(self):
        self.set_draw_color(180, 200, 220)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(4)


def generate_pdf(
    query: str,
    summary: str,
    articles: list,
    language: str,
    source_counts: dict,
    model_name: str,
) -> bytes:
    """
    Build and return a PDF file as bytes.
    """
    pdf = NewsPDF(title=query, lang=language)

    # ── Stats section ──────────────────────────────────────────
    pdf.section_heading("Report Statistics")
    total = sum(source_counts.values())
    pdf.body_text(
        f"Total Articles Found: {total}\n"
        f"AI Model Used: {model_name}\n"
        f"News Sources: {', '.join(f'{s} ({c})' for s, c in source_counts.items() if c > 0)}"
    )
    pdf.divider()

    # ── Summary section ────────────────────────────────────────
    pdf.section_heading("AI-Generated Summary")
    # Split by markdown headings to format nicely
    lines = summary.split("\n")
    for line in lines:
        stripped = line.strip()
        if not stripped:
            pdf.ln(2)
            continue
        if stripped.startswith("## "):
            pdf.section_heading(stripped[3:])
        elif stripped.startswith("- ") or stripped.startswith("* "):
            pdf.set_font("Helvetica", "", 10)
            pdf.cell(6, 6, chr(149))   # bullet
            pdf.multi_cell(0, 6, _strip_emoji(stripped[2:]))
        else:
            pdf.body_text(stripped)

    pdf.divider()

    # ── Source articles ────────────────────────────────────────
    if articles:
        pdf.section_heading(f"Source Articles ({len(articles)})")
        for i, art in enumerate(articles, 1):
            pdf.set_font("Helvetica", "B", 10)
            pdf.set_text_color(30, 58, 107)
            pdf.multi_cell(0, 6, f"{i}. {_strip_emoji(art['title'])}")
            pdf.set_font("Helvetica", "", 9)
            pdf.set_text_color(80, 80, 80)
            pdf.cell(0, 5, f"{art['source']}  |  {art['published']}", ln=True)
            pdf.set_text_color(0, 0, 0)
            pdf.set_font("Helvetica", "", 9)
            pdf.multi_cell(0, 5, _strip_emoji(art["description"][:300]))
            pdf.set_font("Helvetica", "U", 9)
            pdf.set_text_color(0, 80, 160)
            pdf.cell(0, 5, art["url"][:100], ln=True)
            pdf.set_text_color(0, 0, 0)
            pdf.ln(3)

    return bytes(pdf.output())


def generate_txt(
    query: str,
    summary: str,
    articles: list,
    language: str,
    source_counts: dict,
    model_name: str,
) -> str:
    """Generate a plain-text export string."""
    lines = [
        "=" * 70,
        "  NEWS RESEARCH TOOL  |  AI Summary Report",
        "=" * 70,
        f"  Query:    {query}",
        f"  Language: {language}",
        f"  Model:    {model_name}",
        f"  Date:     {datetime.now().strftime('%d %b %Y  %H:%M')}",
        f"  Articles: {sum(source_counts.values())}  |  "
        + "  ".join(f"{s}:{c}" for s, c in source_counts.items() if c > 0),
        "=" * 70,
        "",
        "AI SUMMARY",
        "-" * 70,
        summary,
        "",
        "=" * 70,
        f"SOURCE ARTICLES ({len(articles)})",
        "-" * 70,
    ]
    for i, art in enumerate(articles, 1):
        lines += [
            f"\n[{i}] {art['title']}",
            f"    Source:    {art['source']}",
            f"    Published: {art['published']}",
            f"    Excerpt:   {art['description'][:300]}",
            f"    URL:       {art['url']}",
        ]
    lines += ["", "=" * 70, "  Generated by News Research Tool (Groq + LangChain)", "=" * 70]
    return "\n".join(lines)
