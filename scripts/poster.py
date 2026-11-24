#!/usr/bin/env python3
"""Helper for posters built with the makeposter skill.

  poster.py build  [poster.tex]                      compile, report errors and box warnings, remove build files
  poster.py view   [poster.tex] [--box NAME | --region X0 Y0 X1 Y1] [--dpi N] [--out DIR]
                                                     render the poster, one box or one region to a PNG
  poster.py boxes  [poster.tex]                      free space inside every box, and the page margins
  poster.py text   [poster.tex] [--box NAME]         text layer of the PDF, box by box, for proofreading
  poster.py fit    [poster.tex] --width CM [--font caption] "text" ["text" ...]
                                                     how many lines each candidate text takes
  poster.py check  [poster.tex] [--size WxH]         final technical check of the PDF
  poster.py png    [poster.tex] [--width PX] [--out FILE]   image for a virtual poster upload

All coordinates are those of the .tex file: centimetres, origin at the bottom left of the sheet.
Boxes are read from the \\pbox{x0}{y0}{x1}{y1}{Title} and \\pframe{x0}{y0}{x1}{y1} lines of the
.tex file, so their coordinates must be plain numbers.
"""
import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile

PT_PER_CM = 72 / 2.54
FONTS = {  # name: (size, leading) of the type scale in posterstyle.sty
    "title": (110, 120), "subtitle": (54, 64), "authors": (40, 48), "boxtitle": (46, 54),
    "paneltitle": (36, 44), "body": (33, 43), "caption": (28, 36), "qr": (30, 36),
}


def run(cmd, cwd=None, check=False):
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, check=check)


def need(tool):
    if shutil.which(tool) is None:
        sys.exit(f"{tool} not found. Run scripts/setup.sh to see what is missing.")


def paths(tex):
    tex = os.path.abspath(tex)
    if not os.path.isfile(tex):
        sys.exit(f"no such file: {tex}")
    return tex, os.path.splitext(tex)[0] + ".pdf", os.path.dirname(tex)


def page_cm(pdf):
    need("pdfinfo")
    out = run(["pdfinfo", pdf]).stdout
    m = re.search(r"Page size:\s+([\d.]+) x ([\d.]+) pts", out)
    if not m:
        sys.exit(f"cannot read the page size of {pdf}")
    return float(m.group(1)) / PT_PER_CM, float(m.group(2)) / PT_PER_CM


BOX_RE = re.compile(
    r"\\p(box|frame)\{([^{}]*)\}\{([^{}]*)\}\{([^{}]*)\}\{([^{}]*)\}(?:\s*\{((?:[^{}]|\{[^{}]*\})*)\})?")


def read_boxes(tex):
    """[(name, x0, y0, x1, y1)] from the \\pbox and \\pframe lines that carry plain numbers."""
    boxes, nframe = [], 0
    for line in open(tex, encoding="utf-8"):
        if line.lstrip().startswith("%"):
            continue
        for m in BOX_RE.finditer(line):
            try:
                x0, y0, x1, y1 = (float(m.group(k)) for k in (2, 3, 4, 5))
            except ValueError:
                continue                       # macro arguments such as #1: a definition, not a box
            if m.group(1) == "frame":
                nframe += 1
                name = f"frame {nframe}"
            else:
                name = re.sub(r"\\[a-zA-Z]+\s*|[{}$]", "", m.group(6) or "").strip() or "untitled"
            boxes.append((name, x0, y0, x1, y1))
    return boxes


def pick_box(boxes, key):
    hits = [b for b in boxes if key.lower() in b[0].lower()]
    if len(hits) != 1:
        names = ", ".join(repr(b[0]) for b in boxes)
        sys.exit(f"--box {key!r} matches {len(hits)} boxes. Boxes: {names}")
    return hits[0]


def render(pdf, out_png, dpi, region=None, gray=False):
    """Render the page or a region (x0, y0, x1, y1 in cm, origin bottom left) to out_png."""
    need("pdftoppm")
    w, h = page_cm(pdf)
    cmd = ["pdftoppm", "-r", str(dpi), "-png", "-singlefile"]
    if gray:
        cmd.append("-gray")
    if region:
        x0, y0, x1, y1 = region
        x0, x1 = max(0.0, min(x0, x1)), min(w, max(x0, x1))
        y0, y1 = max(0.0, min(y0, y1)), min(h, max(y0, y1))
        px = lambda cm: int(round(cm / 2.54 * dpi))
        cmd += ["-x", str(px(x0)), "-y", str(px(h - y1)), "-W", str(px(x1 - x0)), "-H", str(px(y1 - y0))]
    cmd += [pdf, os.path.splitext(out_png)[0]]
    r = run(cmd)
    if r.returncode != 0 or not os.path.isfile(out_png):
        sys.exit(f"pdftoppm failed: {r.stderr.strip()}")
    return out_png


# ---------------------------------------------------------------------------------------------
def cmd_build(a):
    tex, pdf, d = paths(a.tex)
    need("pdflatex")
    r = run(["pdflatex", "-interaction=nonstopmode", "-halt-on-error", os.path.basename(tex)], cwd=d)
    logf = os.path.splitext(tex)[0] + ".log"
    log = open(logf, encoding="latin-1").read() if os.path.isfile(logf) else r.stdout
    errors = [m.group(0) for m in re.finditer(r"^!.*(?:\n.*){0,4}", log, flags=re.M)]
    over, under = log.count("Overfull"), log.count("Underfull")
    for e in errors[:5]:
        print(e, "\n")
    for m in re.finditer(r"^(?:Overfull|Underfull).*$", log, flags=re.M):
        print(" ", m.group(0))
    for m in re.finditer(r"^.*(?:Missing character|Font shape .* undefined|LaTeX Warning: Reference).*$", log, flags=re.M):
        print(" ", m.group(0))
    for ext in (".aux", ".log", ".out"):
        f = os.path.splitext(tex)[0] + ext
        if os.path.isfile(f):
            os.remove(f)
    if errors or r.returncode != 0:
        print(f"BUILD FAILED: {len(errors)} error(s)")
        return 1
    w, h = page_cm(pdf)
    print(f"built {os.path.basename(pdf)}: {w:.1f} x {h:.1f} cm, errors 0, overfull {over}, underfull {under}")
    return 1 if over else 0


def cmd_view(a):
    tex, pdf, d = paths(a.tex)
    out_dir = a.out or os.path.join(d, "preview")
    os.makedirs(out_dir, exist_ok=True)
    if a.box:
        name, x0, y0, x1, y1 = pick_box(read_boxes(tex), a.box)
        pad = 0.8
        region, dpi = (x0 - pad, y0 - pad, x1 + pad, y1 + pad), a.dpi or 60
        stem = "box_" + re.sub(r"[^a-z0-9]+", "_", name.lower()).strip("_")
    elif a.region:
        region, dpi, stem = tuple(a.region), a.dpi or 60, "region_" + "_".join(f"{v:g}" for v in a.region)
    else:
        region, dpi, stem = None, a.dpi or 24, "full"
    print(render(pdf, os.path.join(out_dir, stem + ".png"), dpi, region))
    return 0


def ink_array(pdf, dpi=72):
    try:
        import numpy as np
        from PIL import Image
    except ImportError:
        sys.exit("this command needs numpy and Pillow (python3 -m pip install numpy pillow)")
    Image.MAX_IMAGE_PIXELS = None
    with tempfile.TemporaryDirectory() as t:
        png = render(pdf, os.path.join(t, "gray.png"), dpi, gray=True)
        return np.array(Image.open(png).convert("L")) < 200


def cmd_boxes(a):
    tex, pdf, d = paths(a.tex)
    import numpy as np
    ink = ink_array(pdf)
    H, W = ink.shape
    pw, ph = page_cm(pdf)
    ppc = W / pw
    X = lambda x: int(round(x * ppc))
    Y = lambda y: int(round((ph - y) * ppc))
    print(f"page {pw:.1f} x {ph:.1f} cm")
    print(f"{'box':38s} {'x0':>6s} {'y0':>6s} {'x1':>6s} {'y1':>6s} {'above':>6s} {'below':>6s}   free space in cm")
    edge, clear = 0.15 + 0.08, 3.2            # inner edge of the 0.3 cm border; stay clear of the round corners
    for name, x0, y0, x1, y1 in read_boxes(tex):
        sub = ink[Y(y1 - edge):Y(y0 + edge), X(x0 + clear):X(x1 - clear)]
        rows = np.where(sub.any(axis=1))[0]
        if len(rows) == 0:
            print(f"{name[:38]:38s} {x0:6.1f} {y0:6.1f} {x1:6.1f} {y1:6.1f}   (empty)")
            continue
        above = rows[0] / ppc + 0.08
        below = (sub.shape[0] - 1 - rows[-1]) / ppc + 0.08
        note = "  <- tight" if below < 1.0 else ("  <- room to give away" if below > 3.5 else "")
        print(f"{name[:38]:38s} {x0:6.1f} {y0:6.1f} {x1:6.1f} {y1:6.1f} {above:6.2f} {below:6.2f}{note}")
    rows, cols = np.where(ink.any(axis=1))[0], np.where(ink.any(axis=0))[0]
    print(f"page margins: top {rows[0]/ppc:.2f}  bottom {(H-1-rows[-1])/ppc:.2f}  "
          f"left {cols[0]/ppc:.2f}  right {(W-1-cols[-1])/ppc:.2f} cm")
    return 0


def box_text(pdf, ph, x0, y0, x1, y1):
    need("pdftotext")
    pt = lambda cm: str(int(round(cm * PT_PER_CM)))
    out = run(["pdftotext", "-x", pt(x0), "-y", pt(ph - y1), "-W", pt(x1 - x0), "-H", pt(y1 - y0), pdf, "-"]).stdout
    return re.sub(r"\n\s*\n+", "\n", out).strip()


def cmd_text(a):
    tex, pdf, d = paths(a.tex)
    pw, ph = page_cm(pdf)
    boxes = read_boxes(tex)
    if a.box:
        boxes = [pick_box(boxes, a.box)]
    else:
        boxes = [("whole page", 0, 0, pw, ph)] if not boxes else boxes
    everything = ""
    for name, x0, y0, x1, y1 in boxes:
        txt = box_text(pdf, ph, x0, y0, x1, y1)
        everything += " " + txt
        print(f"===== {name}\n{txt}\n")
    if not a.box:
        full = box_text(pdf, ph, 0, 0, pw, ph)
        doubled = sorted(set(m.group(1) for m in re.finditer(r"\b([A-Za-z]{2,})\s+\1\b", full)))
        print("===== checks on the whole page")
        print("doubled words:", ", ".join(doubled) if doubled else "none")
        print("words in the text layer:", len(full.split()))
    return 0


def cmd_fit(a):
    tex, pdf, d = paths(a.tex)
    need("pdflatex")
    size, lead = FONTS[a.font] if a.font else (a.size, a.leading)
    if not size or not lead:
        sys.exit("give --font NAME or both --size PT and --leading PT")
    sty = os.path.join(d, "posterstyle.sty")
    if not os.path.isfile(sty):
        sty = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "posterstyle.sty")
    scale = "1"
    m = re.search(r"\\renewcommand\{\\posterfontscale\}\{([^}]*)\}", open(tex, encoding="utf-8").read())
    if m:
        scale = m.group(1)
    with tempfile.TemporaryDirectory() as t:
        shutil.copy(sty, os.path.join(t, "posterstyle.sty"))
        body = "".join(
            "\\setbox0=\\vbox{\\hsize=%scm \\parindent=0pt \\raggedright\\fsz{%s}{%s}\\strut %s\\par\\xdef\\nl{\\the\\prevgraf}}"
            "\\setbox2=\\hbox{\\fsz{%s}{%s}%s}\\typeout{FIT %d: lines=\\nl\\space width=\\the\\wd2}\n"
            % (a.width, size, lead, txt, size, lead, txt, i) for i, txt in enumerate(a.texts))
        src = ("\\documentclass{article}\n\\usepackage{posterstyle}\n\\renewcommand{\\posterfontscale}{%s}\n"
               "\\begin{document}\n\\hyphenpenalty=10000\\exhyphenpenalty=10000\n%s\\end{document}\n" % (scale, body))
        open(os.path.join(t, "fit.tex"), "w", encoding="utf-8").write(src)
        r = run(["pdflatex", "-interaction=nonstopmode", "fit.tex"], cwd=t)
        found = dict((int(m.group(1)), (int(m.group(2)), float(m.group(3))))
                     for m in re.finditer(r"FIT (\d+): lines=(\d+) width=([\d.]+)pt", r.stdout))
        if len(found) != len(a.texts):
            print(r.stdout[-1500:])
            sys.exit("the measurement failed; check the LaTeX in the candidate texts")
    print(f"width {a.width} cm, font {size}/{lead} pt (scale {scale})")
    for i, txt in enumerate(a.texts):
        lines, wd = found[i]
        wcm = wd / PT_PER_CM * 72 / 72.27
        print(f"  {lines} line(s), natural width {wcm:6.1f} cm = {wcm/float(a.width):.2f} lines of text:  {txt[:90]}")
    return 0


def cmd_check(a):
    tex, pdf, d = paths(a.tex)
    problems = []
    print("== build")
    if cmd_build(a) != 0:
        problems.append("the build has errors or overfull boxes")
    w, h = page_cm(pdf)
    print("== page size")
    if a.size:
        m = re.fullmatch(r"\s*([\d.]+)\s*[xX]\s*([\d.]+)\s*", a.size)
        if not m:
            sys.exit("--size wants WIDTHxHEIGHT in cm, for example 140x90")
        ew, eh = float(m.group(1)), float(m.group(2))
        ok = abs(w - ew) < 0.05 and abs(h - eh) < 0.05
        print(f"  {w:.2f} x {h:.2f} cm, expected {ew:g} x {eh:g}: {'ok' if ok else 'MISMATCH'}")
        if not ok:
            problems.append("page size differs from the size the venue asks for")
    else:
        print(f"  {w:.2f} x {h:.2f} cm (pass --size WxH to compare with the venue's size)")
    print("== fonts")
    need("pdffonts")
    rows = run(["pdffonts", pdf]).stdout.splitlines()[2:]
    not_emb = [r for r in rows if re.search(r"\s(no)\s+(yes|no)\s+(yes|no)\s+\d+\s+\d+\s*$", r)]
    print(f"  {len(rows)} fonts, {len(not_emb)} not embedded")
    for r in not_emb:
        print("   ", r)
        problems.append("a font is not embedded")
    print("== raster images")
    need("pdfimages")
    imgs = run(["pdfimages", "-list", pdf]).stdout.splitlines()[2:]
    if not imgs:
        print("  none: the poster is all vector")
    for r in imgs:
        f = r.split()
        if len(f) > 13:
            ppi = min(float(f[12]), float(f[13]))
            flag = "" if ppi >= 150 else "  <- below 150 ppi at print size"
            print(f"  {f[3]}x{f[4]} px, {ppi:.0f} ppi{flag}")
            if ppi < 150:
                problems.append("a raster image is below 150 ppi at print size")
    print("== placeholders left in the source")
    src = open(tex, encoding="utf-8").read()
    visible = "\n".join(l for l in src.splitlines() if not l.lstrip().startswith("%"))
    left = [p for p in ("0000.00000", "user/repository", "TODO", "FIXME") if p in visible]
    missing = [m.group(1) for m in re.finditer(r"\\posterimg\{[^{}]*\}\{[^{}]*\}\{([^{}]*)\}", visible)
               if not os.path.isfile(os.path.join(d, m.group(1)))]
    print("  " + (", ".join(left) if left else "none"))
    for f in missing:
        print(f"  missing file (a placeholder is printed instead): {f}")
    if left or missing:
        problems.append("placeholders are left in the poster")
    print("== QR codes")
    urls = re.findall(r"\\(?:posterqr\{[^{}]*\}\{[^{}]*\}\{[^{}]*\}|qrcode(?:\[[^\]]*\])?)\{([^{}]*)\}", visible)
    try:
        import cv2
        with tempfile.TemporaryDirectory() as t:
            dpi = 100 if w * h < 15000 else 72
            img = cv2.imread(render(pdf, os.path.join(t, "qr.png"), dpi))
            ok, decoded, _, _ = cv2.QRCodeDetector().detectAndDecodeMulti(img)
            decoded = sorted(x for x in (decoded if ok else []) if x)
        for u in decoded:
            print("  decoded:", u)
        lost = sorted(set(urls) - set(decoded))
        for u in lost:
            print("  IN THE SOURCE BUT NOT DECODED:", u)
            problems.append("a QR code did not decode")
        if not urls and not decoded:
            print("  no QR code in the poster")
    except ImportError:
        print("  not checked: OpenCV is missing (python3 -m pip install opencv-python-headless)")
        for u in urls:
            print("  in the source:", u)
    print("== result")
    if problems:
        for p in sorted(set(problems)):
            print("  PROBLEM:", p)
        return 1
    print("  no technical problem found. Still to do by eye: proofread (poster.py text), look at every box")
    print("  (poster.py view --box), recompute the numbers of every example, re-read the venue's instructions.")
    return 0


def cmd_png(a):
    tex, pdf, d = paths(a.tex)
    need("pdftoppm")
    out = os.path.abspath(a.out or os.path.splitext(pdf)[0] + ".png")
    r = run(["pdftoppm", "-png", "-singlefile", "-scale-to-x", str(a.width), "-scale-to-y", "-1", pdf, os.path.splitext(out)[0]])
    if r.returncode != 0:
        sys.exit(r.stderr)
    print(out)
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    def add(name, fn):
        p = sub.add_parser(name)
        p.add_argument("tex", nargs="?", default="poster.tex")
        p.set_defaults(fn=fn)
        return p
    add("build", cmd_build)
    p = add("view", cmd_view)
    p.add_argument("--box"); p.add_argument("--region", nargs=4, type=float, metavar=("X0", "Y0", "X1", "Y1"))
    p.add_argument("--dpi", type=int); p.add_argument("--out", help="folder for the PNG (default: preview/ next to the .tex)")
    add("boxes", cmd_boxes)
    p = add("text", cmd_text); p.add_argument("--box")
    p = sub.add_parser("fit"); p.set_defaults(fn=cmd_fit, tex="poster.tex")
    p.add_argument("--tex", default="poster.tex"); p.add_argument("--width", required=True, help="text width in cm")
    p.add_argument("--font", choices=sorted(FONTS)); p.add_argument("--size", type=float); p.add_argument("--leading", type=float)
    p.add_argument("texts", nargs="+")
    p = add("check", cmd_check); p.add_argument("--size", help="expected page size in cm, for example 140x90")
    p = add("png", cmd_png); p.add_argument("--width", type=int, default=5000); p.add_argument("--out")
    a = ap.parse_args()
    if a.cmd == "fit" and not a.font and not a.size:
        a.font = "caption"
    sys.exit(a.fn(a))


if __name__ == "__main__":
    main()
