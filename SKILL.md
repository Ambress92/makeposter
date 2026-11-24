---
name: makeposter
description: Build a conference poster in LaTeX/TikZ from a paper's sources and figures, in the blue house style (gradient title band, white boxes with rounded blue borders, Helvetica, vector QR codes), drawn at the exact print size taken from the venue's poster instructions, then review it box by box with the user and run a print-ready final check. Use whenever the user asks for a poster, a conference poster, a poster for NeurIPS, ICML, ICLR, KDD, ECML, VLDB or any other venue, "make the poster for my paper", a poster session printout or a virtual poster image, and also when they want to revise, shorten, proofread, check or export a poster that was made with this skill, even if they never say LaTeX.
---

# makeposter

Turn a paper (LaTeX sources, figures, result files, optionally slides) into a poster that is
printed at the size the venue asks for. The poster is one `tikzpicture` in a `standalone`
document whose unit is one centimetre on the printed sheet, so every size in the source is a
size on paper.

The work has three stages that need different behaviour:

1. **First draft.** Find the inputs, ask once for what cannot be found, and build the complete
   poster right away. Do not ask the user to approve a plan first.
2. **Review, box by box.** The user leads. Change one box at a time, in moderate steps, and
   show the exact new text every time.
3. **Final check.** Verify the PDF, the text, the numbers and the venue's rules before it goes
   to print.

`<skill>` below is this skill's folder. The helper is `python3 <skill>/scripts/poster.py`,
run from the poster folder.

## 0. Requirements (first thing, every run)

Run `bash <skill>/scripts/setup.sh` (report only). If everything required is present, continue
silently. If something is missing, show the list and the commands, then ask with
AskUserQuestion: "Install for me" (run `setup.sh --install`, then re-check), "I will install it
myself" (stop and resume when told), or "Continue without" (build the sources and say clearly
which steps were skipped). Never run `--install` without the first answer.

## 1. Collect the inputs

Look for each item yourself. Ask only for what you cannot find, in one round of questions.

- **Paper.** The main `.tex` and its inputs: abstract, contributions, definitions, the main
  theorem with its proof idea, the algorithm, the experiments. Also the plotting code and the
  result files behind the figures, because the plots are redrawn at print size.
- **Slides or an older poster** of the same paper, if any. Reuse their wording and figures so
  that talk and poster say the same thing in the same terms.
- **Venue and size.** Fetch the venue's official poster instructions and quote the size and
  orientation from the page (for example NeurIPS 2026 main conference: 140 cm wide, 90 cm
  high, landscape, "do not print larger"). Sizes change between years and between main
  conference and workshops, so never reuse the size of an older poster. Note the hanging
  method and any upload of a virtual poster. If the page cannot be found, ask. This is the only
  web request the skill needs, and it carries nothing about the user or the paper.
- **Authors** in the paper's order. Affiliations are carried by the logos.
- **Links for the QR codes**, usually the paper (arXiv) and the code. Search the paper, the
  README, project notes and memory. Never invent a link; ask when one is missing.
- **Logos.** Look in `<skill>/logos-private/` first, then in the project (slides, older
  posters). Vector files only; convert SVG with `rsvg-convert -f pdf -o logo.pdf logo.svg`.
  Ask for the ones still missing, and copy every new logo into `<skill>/logos-private/` for
  the next poster (create the folder if needed, and add a line to its `INDEX.md`). That folder
  is ignored by git: logos never go into the skill's repository.
- **Output folder.** `poster/` next to the paper, unless the project already has a place for it.

Treat the paper as read-only. The poster never requires a change to the paper.

## 2. Build the first draft

1. **Start from the template.** Copy `assets/posterstyle.sty` and one of
   `assets/poster_landscape.tex` (140 x 90 cm, three columns over a row of plots) or
   `assets/poster_portrait.tex` (A0, two columns, footer with logos and QR codes) to the poster
   folder as `poster.tex`. Copy the logos to `logos/`. For any other size, read
   `references/layout.md` and recompute the grid; the page size goes into `\PW` and `\PH`.
2. **Fill the boxes.** Read `references/content.md` before writing a word. The default plan is

   | Box | Holds | Form |
   |---|---|---|
   | Problem | why current methods fall short | two sentences, a small drawing, one sentence |
   | Formal setting | the measure and the problem | `Definition (Name).` blocks and a `Problem.` block with displayed formulas |
   | Method (largest box) | the idea, the algorithm, one worked example | two sentences, a 4 to 5 line algorithm with a short note beside it, the example figure, a two-line caption |
   | Main result | the theorem | `Definition`, `Theorem.` as one displayed sentence, `Proof idea.` in two sentences |
   | Guarantees and cost | everything else that is proved | a small table, then at most two sentences |
   | Row of plots | the experiments | two or three plots, each with a claim as title and a two-line caption |

   Adapt the plan to the paper (an empirical paper trades the theorem box for a second result),
   but keep one job per box.
3. **Make the figures.** Read `references/figures.md`. Redraw the plots at print size with
   `figures/make_poster_figs.py` (copy it from `assets/`), reading the paper's own result
   files. Draw the worked example in TikZ, or rebuild the paper's overview figure with poster
   fonts.
4. **Build and look.** `poster.py build`, then `poster.py view` for the whole sheet and
   `poster.py view --box NAME` for every box. Read every image. The source compiling says
   nothing about overlaps, clipped labels or a label sitting on a line. When something looks
   wrong, check `references/tikz-pitfalls.md` before guessing: most surprises are listed there.
5. **Fit.** `poster.py boxes` prints the free space under the content of every box. Aim for at
   least 1.1 cm, and for similar values in boxes that sit on top of each other; move their
   shared border to balance them. No overfull boxes.
6. **Check your own draft** against the list in section 6 before the user sees it.
7. **Hand over.** Give the link to the PDF, one line per box on what it holds, and anything
   you could not verify. Then wait: the review belongs to the user.

## 3. Review box by box

The first draft is a proposal. The author knows the paper and the audience better than the
draft does, and a poster is rewritten several times before it is right. What worked:

- **One box at a time**, in the order the user picks. Do not touch other boxes, except for a
  layout side effect such as moving a shared border, which you report.
- **Moderate steps.** "A bit less text" means a quarter less, not half. A large rewrite that
  nobody asked for gets reverted and costs trust. When the user says the poster has too much
  text in general, propose the cuts box by box and wait.
- **Show the exact new text** after every change, quoted in full, then what changed, what was
  dropped, and what the build said. The user approves text, not descriptions of text.
- **Fix false or misleading statements at once** and say what you changed. This is the one
  kind of change that needs no request.
- **"Is it fine now?" asks for a recommendation.** Answer yes or no, give at most one concrete
  improvement with its exact wording, and name what you would leave out and why.
- **Words the user uses and what they ask for.** "Almost good": two or three small changes.
  "Unclear": split the sentence into plain ones, setting first and reason second. "Pointless":
  remove it, do not defend it. "Think": weigh the alternatives yourself and come back with one
  recommendation, built, plus the runner-up in a sentence.
- **Measure instead of guessing.** `poster.py fit` tells how many lines a candidate text
  takes; use it before promising "two lines". `poster.py boxes` tells whether a box has room.
- **Keep a way back.** Copy `poster.tex` (and any figure you regenerate) to the scratchpad
  before each change, and say in the report that the old version is one step away.
- **Keep the folder clean.** `poster.py build` removes the build files; previews go to the
  scratchpad (`--out`) or to `preview/`, which you delete at the end.
- **Keep notes.** After each box, record in memory which boxes are approved and what the user
  rejected, so that a later session does not reopen settled questions.

## 4. Final check

When the user asks for it, or before any print or upload, follow `references/final-check.md`.
In short: `poster.py check --size WxH`, proofread from `poster.py text`, recompute every
number that the poster shows, re-read the venue's instructions, and measure the free space.
Report what you checked, what you changed (layout only, unless something is wrong), and a
short list of suggestions for the user to accept or decline.

## 5. Deliver

The PDF at print size; on request `poster.py png` for a virtual poster upload; the print notes
from `references/final-check.md` (colours, margins, how the venue hangs posters). Delete
`preview/`. Leave the sources, the figure script and the logos in the poster folder. If the
paper's slides share a figure or a sentence that changed during the review, say so and offer to
align them.

## 6. What a good poster in this style gets right

Check the draft against these before the user sees it, and again in the final check.

1. **Every sentence is true as written, titles included.** A title is a claim. "Worst case",
   "dominates", "optimal", "scales to millions" must hold exactly as stated; when the paper
   proves less, say less. Verify empirical claims against the result files, not the paper's prose.
2. **One name per concept, everywhere.** The terms that the formal-setting box introduces are
   the only ones used in the other boxes, in axis labels, in legends and in captions. Plot
   code often carries older names; replace them.
3. **Defined before use, in reading order** (left to right, then the plots). Each symbol and
   term appears first where it is explained.
4. **Formal blocks carry the mathematics.** `Definition (Name).`, `Problem.`, `Theorem.`,
   `Proof idea.` as bold run-in heads, formulas displayed, the theorem stated as one sentence.
   State formulas exactly as the paper does, corner cases included: the poster's own example
   may sit in the corner case.
5. **A table beats a paragraph** when several settings share the same attributes (guarantee,
   running time).
6. **Captions are two plain sentences on at most two lines**: what is plotted, then how to
   read it or why it matters. A single sentence with a trailing "which" clause is harder to
   read than two short ones.
7. **Pictures earn their place.** One worked example, reused across boxes with the same items
   and colours. Put the example's numbers into the picture's own labels. Do not add a second
   picture that repeats what the first one shows.
8. **Numbers are recomputed and rounded once.** The same constant is written the same way in
   every box and plot. Recompute the worked example with a script.
9. **Conjectures, limits and special cases keep the paper's wording and scope.**
10. **Nothing decorative, nothing cramped.** No one-word last lines, no text closer than about
    a centimetre to a border, plots in a row aligned on one baseline.

The user's own writing rules (from their CLAUDE.md, if any) apply to every line on the poster
and to every report you write.

## 7. Files in this skill

- `assets/posterstyle.sty`: palette, type scale, `\pbox`, `\pframe`, `\posterband`,
  `\posterimg`, `\posterqr`, `\ppanel`, `posteralg`.
- `assets/poster_landscape.tex`, `assets/poster_portrait.tex`: templates that compile as they
  are; missing logos and figures show as labelled placeholders.
- `assets/make_poster_figs.py`: three demo plots at print size, to be replaced by the paper's.
- `scripts/setup.sh`: requirements check; `--install` installs what is missing.
- `scripts/poster.py`: `build`, `view`, `boxes`, `text`, `fit`, `check`, `png`.
- `references/layout.md`: sheet sizes, grids, type scale, box capacity, header, plot row.
- `references/content.md`: what goes in each box, with examples, and the writing rules.
- `references/figures.md`: plots at print size, the worked example, logos, QR codes.
- `references/tikz-pitfalls.md`: symptoms, causes and fixes for the LaTeX and TikZ surprises.
- `references/final-check.md`: the checklist before printing, and the print notes.
- `logos-private/`: the user's logo library, kept out of git.
