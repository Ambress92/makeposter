# makeposter

A [Claude Code](https://claude.com/claude-code) skill that turns a paper
(LaTeX sources, figures, result files, optionally slides) into a conference
poster in LaTeX/TikZ. The house style is a gradient title band with two
rounded corners, white boxes with thick rounded blue borders, Helvetica text
with Latin Modern math, logos beside the band and vector QR codes. The poster
is drawn at its print size, in centimetres, in a single `tikzpicture`.

It was developed while building the NeurIPS 2026 poster for
*Fair Bubble Sort: Provably Optimal Fair Ranking with Continuous Sensitive
Attributes*, and encodes the lessons from that process: build the full draft
first, then rewrite it box by box with the author; state definitions and
theorems formally; keep every claim, term and number checkable; redraw plots
at print size; and run a real final check before anything goes to print.

## Install

```bash
git clone https://github.com/Ambress92/makeposter ~/.claude/skills/makeposter
```

Requirements: a TeX Live with `standalone`, `pgf`, `qrcode`, `booktabs`,
`helvetic`, `lm` (pdflatex); `poppler` (`pdftoppm`, `pdfinfo`, `pdftotext`,
`pdffonts`, `pdfimages`); Python 3 with numpy, Pillow and matplotlib.
Optional: OpenCV to decode the QR codes, `rsvg-convert` for SVG logos.
Check and install them with

```bash
bash ~/.claude/skills/makeposter/scripts/setup.sh            # report only
bash ~/.claude/skills/makeposter/scripts/setup.sh --install  # install what is missing
```

The skill runs the report-only check at the start of every session and
never installs anything unless you choose that option.

## Use

Open Claude Code in the folder that holds the paper and type

```
/makeposter
```

The skill then:

1. Checks the toolchain with `scripts/setup.sh`.
2. Finds the paper, its figures and result files, the authors, the links for
   the QR codes and the logos, and reads the venue's poster instructions for
   the exact size. It asks once, and only for what it could not find.
3. Builds the complete first draft from a template (`140 x 90 cm` landscape
   with three columns over a row of plots, or A0 portrait with two columns),
   redraws the plots at print size, compiles and inspects every box.
4. Reviews the poster with you box by box: one box at a time, moderate
   changes, the exact new text shown after each one.
5. Runs the final check (page size against the venue's rules, fonts, raster
   images, QR codes, proofreading, recomputed numbers, free space) and gives
   the print notes.

## What the style enforces

- Box titles name the answer, plot titles are full claims, and every claim
  holds exactly as written.
- Definitions, the problem and the theorem are formal blocks with displayed
  formulas (`Definition (Name).`, `Problem.`, `Theorem.`, `Proof idea.`).
- One name per concept across boxes, axis labels, legends and captions, and
  every symbol defined before its first use in reading order.
- A table instead of a paragraph when settings share attributes; captions of
  two plain sentences on at most two lines.
- One worked example, large, recomputed by script, reused across boxes.
- Plots redrawn at print size (22 pt tick labels and up), all vector, aligned
  on one baseline.
- Body text at 33 pt for columns about 39 cm wide; if the text does not fit,
  the text is cut, not the type.

## The helper

Run from the poster folder.

| Command | What it does |
|---|---|
| `poster.py build` | compile, list errors and box warnings, print the page size, remove build files |
| `poster.py view [--box NAME \| --region X0 Y0 X1 Y1]` | render the sheet, one box or one region (poster centimetres) to a PNG |
| `poster.py boxes` | free space above and below the content of every box, and the page margins |
| `poster.py text [--box NAME]` | the PDF's text layer box by box, for proofreading |
| `poster.py fit --width CM "text" ...` | how many lines each candidate text takes at that width |
| `poster.py check --size WxH` | final technical check: build, page size, fonts, raster images, placeholders, QR codes |
| `poster.py png` | an image of the whole sheet for a virtual poster upload |

## Layout

```
SKILL.md                      workflow and rules read by Claude Code
assets/posterstyle.sty        palette, type scale, boxes, band, QR codes, plot row, algorithm
assets/poster_landscape.tex   140 x 90 cm template, compiles as it is
assets/poster_portrait.tex    A0 portrait template, compiles as it is
assets/make_poster_figs.py    demo plots at print size, to be replaced by the paper's
scripts/setup.sh              dependency check, --install installs what is missing
scripts/poster.py             build, view, boxes, text, fit, check, png
references/layout.md          sheet sizes, grids, type scale, capacity of a box
references/content.md         what goes in each box, with examples, and the writing rules
references/figures.md         plots, the worked example, logos, QR codes
references/tikz-pitfalls.md   LaTeX and TikZ surprises at poster size, with fixes
references/final-check.md     checklist before printing, print notes
```

Logos are not part of the repository. The skill keeps yours in
`logos-private/`, which git ignores, and reuses them on later posters.

## License

MIT
