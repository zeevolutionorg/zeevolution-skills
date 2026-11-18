#!/usr/bin/env python3
"""Render a zeevolution-skills Markdown template to .docx (or .html / .md), filling {{placeholders}}.

Usage:
  python3 render_doc.py --in TEMPLATE.md --out OUT.docx [--context CONTEXT.json] [--keep-missing]
  python3 render_doc.py --in TEMPLATE.md --out OUT.html  [--context CONTEXT.json]
  python3 render_doc.py --in TEMPLATE.md --out OUT.md    [--context CONTEXT.json]

Supports the Markdown subset used by the templates (see doc-templates/SKILL.md):
headings, paragraphs, **bold**, *italic*, `code`, [links](url), bullet / numbered /
checkbox lists (2-space nesting), pipe tables, > callouts, and --- rules.
Callouts are styled by their first emoji: ℹ️ info, 💡 how-to, ✍️ example, 🗓️ rhythm, ⚠️ banner.
Requires python-docx for .docx output. The .docx opens in Word and converts to Google Docs on upload.
"""

import argparse
import html
import json
import re
import sys

CALLOUT_COLORS = {  # fill, left-bar color
    "🗓️": ("E8F1FF", "2563EB"),
    "ℹ️": ("F3F4F6", "6B7280"),
    "💡": ("FFF8DB", "D97706"),
    "✍️": ("ECFDF5", "059669"),
    "⚠️": ("FFEDD5", "EA580C"),
}
DEFAULT_CALLOUT = ("F3F4F6", "6B7280")
PLACEHOLDER = re.compile(r"\{\{([a-zA-Z0-9_]+)\}\}")


def fill(text, context, keep_missing):
    def sub(m):
        key = m.group(1)
        if key in context and context[key] not in (None, ""):
            return str(context[key])
        return m.group(0) if keep_missing else ""

    return PLACEHOLDER.sub(sub, text)


# --------------------------------------------------------------------------- parsing
def parse_blocks(lines):
    """Yield (kind, payload) blocks."""
    i = 0
    n = len(lines)
    while i < n:
        line = lines[i].rstrip("\n")
        if not line.strip():
            i += 1
            continue
        m = re.match(r"^(#{1,6})\s+(.*)$", line)
        if m:
            yield "h", (len(m.group(1)), m.group(2).strip())
            i += 1
            continue
        if re.match(r"^\s*---+\s*$", line):
            yield "hr", None
            i += 1
            continue
        if line.startswith(">"):
            buf = []
            while i < n and lines[i].startswith(">"):
                buf.append(lines[i][1:].lstrip(" ").rstrip("\n"))
                i += 1
            # one box per callout: a new callout emoji after a blank '>' line starts a new box
            group = []
            for k, ql in enumerate(buf):
                starts_new = any(ql.startswith(e) for e in CALLOUT_COLORS) and k > 0 and not buf[k - 1].strip()
                if starts_new and any(x.strip() for x in group):
                    yield "quote", group
                    group = []
                group.append(ql)
            if group:
                yield "quote", group
            continue
        if line.lstrip().startswith("|"):
            rows = []
            while i < n and lines[i].lstrip().startswith("|"):
                cells = [c.strip() for c in lines[i].strip().strip("|").split("|")]
                is_sep = any(cells) and all(re.fullmatch(r":?-{3,}:?", c) for c in cells if c)
                if not is_sep:
                    rows.append(cells)
                i += 1
            header = bool(rows) and any(rows[0])
            if rows and not any(rows[0]):
                rows = rows[1:]  # empty header row = key/value table without header
            yield "table", (header, rows)
            continue
        if re.match(r"^\s*([-*]|\d+\.)\s+", line):
            items = []
            while i < n and (
                re.match(r"^\s*([-*]|\d+\.)\s+", lines[i]) or (lines[i].startswith("  ") and lines[i].strip() and items)
            ):
                raw = lines[i].rstrip("\n")
                lm = re.match(r"^(\s*)([-*]|\d+\.)\s+(.*)$", raw)
                if lm:
                    level = len(lm.group(1)) // 2
                    ordered = lm.group(2)[0].isdigit()
                    items.append([level, ordered, lm.group(3)])
                else:  # continuation line of the previous item
                    items[-1][2] += "\n" + raw.strip()
                i += 1
            yield "list", items
            continue
        buf = []
        while i < n and lines[i].strip() and not re.match(r"^(#{1,6}\s|>|\s*\||\s*([-*]|\d+\.)\s|\s*---+\s*$)", lines[i]):
            buf.append(lines[i].strip())
            i += 1
        yield "p", " ".join(buf)


INLINE = re.compile(r"(\*\*[^*]+\*\*|\*[^*\s][^*]*\*|`[^`]+`|\[[^\]]*\]\([^)]*\))")


def inline_tokens(text):
    pos = 0
    for m in INLINE.finditer(text):
        if m.start() > pos:
            yield "t", text[pos : m.start()]
        tok = m.group(0)
        if tok.startswith("**"):
            yield "b", tok[2:-2]
        elif tok.startswith("`"):
            yield "c", tok[1:-1]
        elif tok.startswith("["):
            lm = re.match(r"\[([^\]]*)\]\(([^)]*)\)", tok)
            yield "a", (lm.group(1), lm.group(2).strip().strip("<>"))
        else:
            yield "i", tok[1:-1]
        pos = m.end()
    if pos < len(text):
        yield "t", text[pos:]


def checkbox(text):
    if text.startswith("[ ] "):
        return "☐ " + text[4:]
    if text.lower().startswith("[x] "):
        return "☑ " + text[4:]
    return text


# --------------------------------------------------------------------------- html / md
def to_html(blocks):
    def inl(text):
        out = []
        for kind, val in inline_tokens(text):
            if kind == "t":
                out.append(html.escape(val))
            elif kind == "b":
                out.append(f"<strong>{inl(val)}</strong>")
            elif kind == "i":
                out.append(f"<em>{html.escape(val)}</em>")
            elif kind == "c":
                out.append(f"<code>{html.escape(val)}</code>")
            else:
                label, url = val
                out.append(f'<a href="{html.escape(url)}">{inl(label)}</a>' if url else inl(label))
        return "".join(out).replace("\n", "<br>")

    parts = ['<html><head><meta charset="utf-8"></head><body style="font-family:Arial,sans-serif;font-size:11pt">']
    for kind, val in blocks:
        if kind == "h":
            parts.append(f"<h{val[0]}>{inl(val[1])}</h{val[0]}>")
        elif kind == "p":
            parts.append(f"<p>{inl(val)}</p>")
        elif kind == "hr":
            parts.append("<hr>")
        elif kind == "quote":
            bg, bar = CALLOUT_COLORS.get(next((e for e in CALLOUT_COLORS if val and val[0].startswith(e)), None), DEFAULT_CALLOUT)
            body = "".join(f"<p style='margin:4px 0'>{inl(checkbox(l))}</p>" for l in val if l.strip())
            parts.append(
                f"<table style='width:100%;border-collapse:collapse;margin:8px 0'><tr><td style='background:#{bg};border-left:4px solid #{bar};padding:8px'>{body}</td></tr></table>"
            )
        elif kind == "table":
            has_head, trs = val
            rows = "".join(
                "<tr>"
                + "".join(
                    f"<{'th' if (r == 0 and has_head) else 'td'} style='border:1px solid #D1D5DB;padding:4px 6px'>{inl(c)}</{'th' if (r == 0 and has_head) else 'td'}>"
                    for c in row
                )
                + "</tr>"
                for r, row in enumerate(trs)
            )
            parts.append(f"<table style='border-collapse:collapse;margin:8px 0'>{rows}</table>")
        elif kind == "list":
            tag = "ol" if val and val[0][1] else "ul"
            parts.append(
                f"<{tag}>"
                + "".join(f"<li style='margin-left:{lvl * 20}px'>{inl(checkbox(t))}</li>" for lvl, _, t in val)
                + f"</{tag}>"
            )
    parts.append("</body></html>")
    return "\n".join(parts)


# --------------------------------------------------------------------------- docx
def to_docx(blocks, out_path, title):
    try:
        from docx import Document
        from docx.enum.text import WD_ALIGN_PARAGRAPH  # noqa: F401
        from docx.oxml import OxmlElement
        from docx.oxml.ns import qn
        from docx.shared import Pt, RGBColor
    except ImportError:
        sys.exit("python-docx is required for .docx output: pip install python-docx")

    doc = Document()
    st = doc.styles["Normal"]
    st.font.name = "Arial"
    st.font.size = Pt(10.5)
    for lvl, size in ((1, 20), (2, 15), (3, 12.5), (4, 11.5)):
        hs = doc.styles[f"Heading {lvl}"]
        hs.font.name = "Arial"
        hs.font.size = Pt(size)
        hs.font.color.rgb = RGBColor(0x1F, 0x29, 0x37)

    def shade(cell, hex_fill):
        tcPr = cell._tc.get_or_add_tcPr()
        shd = OxmlElement("w:shd")
        shd.set(qn("w:val"), "clear")
        shd.set(qn("w:color"), "auto")
        shd.set(qn("w:fill"), hex_fill)
        tcPr.append(shd)

    def left_bar(cell, hex_color):
        tcPr = cell._tc.get_or_add_tcPr()
        borders = OxmlElement("w:tcBorders")
        for side in ("top", "left", "bottom", "right"):
            el = OxmlElement(f"w:{side}")
            if side == "left":
                el.set(qn("w:val"), "single")
                el.set(qn("w:sz"), "24")
                el.set(qn("w:color"), hex_color)
            else:
                el.set(qn("w:val"), "nil")
            borders.append(el)
        tcPr.append(borders)

    def add_hyperlink(par, url, text, bold=False):
        part = par.part
        r_id = part.relate_to(
            url, "http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink", is_external=True
        )
        link = OxmlElement("w:hyperlink")
        link.set(qn("r:id"), r_id)
        run = OxmlElement("w:r")
        rpr = OxmlElement("w:rPr")
        color = OxmlElement("w:color")
        color.set(qn("w:val"), "2563EB")
        u = OxmlElement("w:u")
        u.set(qn("w:val"), "single")
        rpr.append(color)
        rpr.append(u)
        if bold:
            rpr.append(OxmlElement("w:b"))
        run.append(rpr)
        t = OxmlElement("w:t")
        t.text = text
        t.set(qn("xml:space"), "preserve")
        run.append(t)
        link.append(run)
        par._p.append(link)

    def add_inline(par, text, bold=False, italic=False):
        lines = text.split("\n")
        for li, line in enumerate(lines):
            if li:
                par.add_run().add_break()
            for kind, val in inline_tokens(line):
                if kind == "t":
                    r = par.add_run(val)
                    r.bold, r.italic = bold or None, italic or None
                elif kind == "b":
                    add_inline(par, val, bold=True, italic=italic)
                elif kind == "i":
                    r = par.add_run(val)
                    r.italic = True
                    r.bold = bold or None
                elif kind == "c":
                    r = par.add_run(val)
                    r.font.name = "Courier New"
                else:
                    label, url = val
                    if url and not url.startswith("{{"):
                        add_hyperlink(par, url, re.sub(r"\*\*|\*", "", label), bold)
                    else:
                        r = par.add_run(re.sub(r"\*\*|\*", "", label))
                        r.bold = bold or None
                        r.underline = True

    for kind, val in blocks:
        if kind == "h":
            doc.add_heading(level=min(val[0], 4)).text = ""
            par = doc.paragraphs[-1]
            add_inline(par, val[1])
        elif kind == "p":
            add_inline(doc.add_paragraph(), val)
        elif kind == "hr":
            par = doc.add_paragraph()
            pPr = par._p.get_or_add_pPr()
            bdr = OxmlElement("w:pBdr")
            bottom = OxmlElement("w:bottom")
            for k, v in (("val", "single"), ("sz", "6"), ("space", "1"), ("color", "D1D5DB")):
                bottom.set(qn(f"w:{k}"), v)
            bdr.append(bottom)
            pPr.append(bdr)
        elif kind == "quote":
            emoji = next((e for e in CALLOUT_COLORS if val and val[0].startswith(e)), None)
            bg, bar = CALLOUT_COLORS.get(emoji, DEFAULT_CALLOUT)
            table = doc.add_table(rows=1, cols=1)
            cell = table.rows[0].cells[0]
            shade(cell, bg)
            left_bar(cell, bar)
            first = True
            for line in val:
                if not line.strip():
                    continue
                par = cell.paragraphs[0] if first else cell.add_paragraph()
                first = False
                lm = re.match(r"^(\d+\.|[-*])\s+(.*)$", line)
                if lm:
                    line = ("• " if not lm.group(1)[0].isdigit() else lm.group(1) + " ") + lm.group(2)
                add_inline(par, checkbox(line))
                par.paragraph_format.space_after = Pt(3)
            doc.add_paragraph().paragraph_format.space_after = Pt(2)
        elif kind == "table":
            has_head, trs = val
            if not trs:
                continue
            cols = max(len(r) for r in trs)
            table = doc.add_table(rows=len(trs), cols=cols)
            table.style = "Table Grid"
            for ri, row in enumerate(trs):
                for ci in range(cols):
                    cell = table.rows[ri].cells[ci]
                    text = row[ci] if ci < len(row) else ""
                    head = ri == 0 and has_head
                    add_inline(cell.paragraphs[0], text, bold=head)
                    if head:
                        shade(cell, "F3F4F6")
                    elif not has_head and ci == 0:
                        shade(cell, "F9FAFB")
            doc.add_paragraph()
        elif kind == "list":
            for lvl, ordered, text in val:
                style = "List Number" if ordered else "List Bullet"
                if lvl >= 1:
                    style += " 2"
                par = doc.add_paragraph(style=style)
                add_inline(par, checkbox(text))

    cp = doc.core_properties
    cp.author = cp.last_modified_by = "zeevolution-skills"
    cp.title = title
    cp.comments = ""
    cp.company = None if hasattr(cp, "company") else None
    doc.save(out_path)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--in", dest="src", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--context")
    ap.add_argument(
        "--keep-missing", action="store_true", help="keep {{placeholders}} that have no value (used for the manual kit)"
    )
    args = ap.parse_args(argv)
    context = {}
    if args.context:
        with open(args.context, encoding="utf-8") as fh:
            context = json.load(fh)
    with open(args.src, encoding="utf-8") as fh:
        text = fill(fh.read(), context, args.keep_missing)
    if args.out.endswith(".md"):
        with open(args.out, "w", encoding="utf-8") as fh:
            fh.write(text)
    else:
        blocks = list(parse_blocks(text.splitlines()))
        title = next((v[1] for k, v in blocks if k == "h"), "")
        title = re.sub(r"[*`]", "", title)
        if args.out.endswith(".html"):
            with open(args.out, "w", encoding="utf-8") as fh:
                fh.write(to_html(blocks))
        else:
            to_docx(blocks, args.out, title)
    print(f"wrote {args.out}")


if __name__ == "__main__":
    main()
