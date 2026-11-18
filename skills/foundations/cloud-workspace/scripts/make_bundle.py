#!/usr/bin/env python3
"""Render a whole document bundle (e.g. a Career Hub) for the Files or Manual adapter.

  python3 make_bundle.py --bundle bundle.yaml --templates TEMPLATES_DIR --lang en \
      --mode lead --format files|manual --context context.json --out OUT_DIR \
      [--include evidence,onboarding] [--ladder LADDER.yaml] [--paste-guide GUIDE.md] [--with-sheet]

--format files   -> one .docx per document + the .xlsx spreadsheet (needs python-docx, openpyxl)
--format manual  -> one filled-in .md per document + HOW-TO-PASTE.md (needs only pyyaml;
                    add --with-sheet to also build the .xlsx when openpyxl is available)

TEMPLATES_DIR contains <lang>/ folders and the sheet specs (the layout of templates/<category>/).
Links between documents use relative file names; the hub is rendered last.
Prints the list of created files as JSON on the last line.
"""

import argparse
import json
import sys
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import render_doc  # noqa: E402


def selected(bundle, mode, include):
    out = []
    for d in bundle["documents"]:
        if mode not in d["modes"]:
            continue
        if d.get("optional") and d["key"] not in include:
            continue
        out.append(d)
    return out


def file_name(doc, lang, fmt):
    title = doc["title"][lang]
    if doc["kind"] == "sheet":
        return f"{doc['id']} - {title}.xlsx" if fmt == "files" else f"{doc['id']} - {title}.md"
    return f"{doc['id']} - {title}.{'docx' if fmt == 'files' else 'md'}"


def doc_list(docs, names, lang):
    labels = {
        "en": ("start here", "spreadsheet — text version; the .xlsx is in the Manual Kit"),
        "pt-BR": ("comece aqui", "planilha — versão em texto; o .xlsx está no Kit Manual"),
    }[lang]
    lines = []
    for i, d in enumerate(docs, 1):
        note = (
            f" — **{labels[0]}**"
            if d.get("hub")
            else (f" — {labels[1]}" if d["kind"] == "sheet" and names[d["key"]].endswith(".md") else "")
        )
        lines.append(f"{i}. `{names[d['key']]}`{note}")
    return "\n".join(lines)


def make(bundle_path, templates, lang, mode, fmt, context, out, include=(), ladder=None, paste_guide=None, with_sheet=False):
    bundle = yaml.safe_load(Path(bundle_path).read_text(encoding="utf-8"))
    templates = Path(templates)
    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    docs = selected(bundle, mode, set(include))
    names = {}
    for d in docs:
        names[d["key"]] = file_name(d, lang, fmt)
        if d["kind"] == "sheet" and fmt == "manual" and with_sheet:
            names[d["key"]] = f"{d['id']} - {d['title'][lang]}.xlsx"
    ctx = dict(context)
    for d in bundle["documents"]:
        name = names.get(d["key"], "")
        # Markdown links can't contain bare spaces: <...> keeps "01 - 🎶 1:1 Notes.md" a valid link
        ctx[f"doc_link_{d['key']}"] = f"<{name}>" if (name and fmt == "manual") else name
    created = []
    hub = None
    for d in docs:
        target = out / names[d["key"]]
        if d.get("hub"):
            hub = (d, target)
            continue
        if d["kind"] == "sheet":
            if target.suffix == ".xlsx":
                import build_sheet

                spec = build_sheet.load(str(templates / d["spec"]))
                strings = build_sheet.load(str(templates / lang / d["strings"]))
                lad = build_sheet.load(str(ladder)) if ladder else None
                sctx = dict(ctx)
                if lad and "ladder_source_label" not in sctx:
                    sctx["ladder_source_label"] = (
                        strings["src_generic"] if lad.get("source") == "generic" else strings["src_company"]
                    )
                build_sheet.Builder(spec, strings, sctx, lad).build().save(target)
            else:
                text = render_doc.fill((templates / lang / d["text_fallback"]).read_text(encoding="utf-8"), ctx, False)
                target.write_text(text, encoding="utf-8")
        else:
            render_one(templates / lang / d["template"], target, ctx)
        created.append(target)
    if hub:
        render_one(templates / lang / hub[0]["template"], hub[1], ctx)
        created.insert(0, hub[1])
    if fmt == "manual" and paste_guide:
        gctx = dict(
            ctx, folder_name=render_doc.fill(bundle["folder_title"][lang], ctx, False), doc_list=doc_list(docs, names, lang)
        )
        guide = out / "HOW-TO-PASTE.md"
        guide.write_text(render_doc.fill(Path(paste_guide).read_text(encoding="utf-8"), gctx, False), encoding="utf-8")
        created.insert(0, guide)
    return created


def render_one(src, target, ctx):
    text = render_doc.fill(Path(src).read_text(encoding="utf-8"), ctx, False)
    if target.suffix == ".md":
        target.write_text(text, encoding="utf-8")
        return
    blocks = list(render_doc.parse_blocks(text.splitlines()))
    title = next((v[1] for k, v in blocks if k == "h"), "")
    render_doc.to_docx(blocks, str(target), title.replace("*", ""))


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--bundle", required=True)
    ap.add_argument("--templates", required=True)
    ap.add_argument("--lang", required=True, choices=["en", "pt-BR"])
    ap.add_argument("--mode", required=True, choices=["self", "lead"])
    ap.add_argument("--format", required=True, choices=["files", "manual"])
    ap.add_argument("--context", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--include", default="", help="optional document keys, comma-separated")
    ap.add_argument("--ladder")
    ap.add_argument("--paste-guide")
    ap.add_argument("--with-sheet", action="store_true")
    args = ap.parse_args(argv)
    context = json.loads(Path(args.context).read_text(encoding="utf-8"))
    include = [x for x in args.include.split(",") if x]
    created = make(
        args.bundle,
        args.templates,
        args.lang,
        args.mode,
        args.format,
        context,
        args.out,
        include,
        args.ladder,
        args.paste_guide,
        args.with_sheet,
    )
    print(json.dumps([str(p) for p in created], ensure_ascii=False))


if __name__ == "__main__":
    main()
