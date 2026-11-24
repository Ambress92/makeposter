# Figures: plots, the worked example, logos, QR codes

Contents: 1. Plots at print size. 2. Labels, legends, terms. 3. A row of plots. 4. Checking a
claim against the data. 5. The worked example. 6. Logos and QR codes.

## 1. Plots at print size

Never enlarge a figure from the paper. Its labels were set for a 14 cm column, and at poster
size they become oddly proportioned and the lines too thin. Redraw each plot with
`figures/make_poster_figs.py` (start from `assets/make_poster_figs.py`):

- `figsize` is the printed size in centimetres (`CM = 1/2.54`);
- tick labels 22 pt, axis labels 26 pt, titles of small multiples 28 pt, legends 22 pt, lines
  about 4 pt, markers about 10 pt; multiply by `SCALE` when `\posterfontscale` is not 1;
- Arial or Helvetica, to match the poster text;
- save a vector PDF, plus a small PNG to look at.

Read the same result files as the paper's plotting code, by importing the paper's loaders when
that is possible. Same data and same normalisation as in the paper; only size, fonts, labels
and legends change. Do not edit the paper's code or data. If the result files are not
available, say so and include the paper's vector figure as a fallback, with a warning to the
user that its labels will be small.

Choose plots that carry the poster's claims: usually the main comparison, one plot for the
theory (a bound or a convergence), and scalability. A plot that needs a paragraph to explain
is the wrong plot for a poster.

## 2. Labels, legends, terms

- **The poster's words.** Axis labels and legends use the terms defined on the poster. Plot
  code often keeps earlier names ("weighted", "unweighted") that the poster never defines.
- **One curve needs no legend.** The axis label names it. A reference line gets its label
  written on the line, in black.
- **Several curves keep a legend**, in a corner without data, with enough headroom that it
  does not touch a curve (extend the axis limit). Markers and dash patterns differ between
  curves, so identity never depends on colour alone.
- **Small multiples share one legend** above the row, and each panel has a short bold title.
- **Offsets** such as `1e-2` are printed as `×10⁻²` (`useMathText=True`).
- **Text is black or grey**, never the colour of a curve.
- Keep the paper's colours for the paper's methods, so that the poster, the paper and the
  slides match.

## 3. A row of plots

Give every plot in the row the same height and include each with that height
(`\posterimg{generous width}{same height}{file}`); `bbox_inches="tight"` trims plots
differently, so equal `figsize` heights are not enough. `\ppanel` stands the plots on one line,
which aligns their x-axes. Look at the row as a whole at about 36 dpi: axes level, captions
starting on one line, no legend near a curve.

## 4. Checking a claim against the data

A plot title is a claim and has to survive the data. Example: the title "FBS dominates
discretization baselines" was checked by running the method at exactly the fairness that each
baseline reached and comparing the two costs, because several baseline points sat close to the
curve and the plotted grid was too coarse to tell. The outcome (cheaper in 23 of 24 cases, tied
in one) is what allows the word "dominates". Write such a check as a small script in the
scratchpad, read-only with respect to the project, and report its result in one sentence.

Also check captions that describe the experiment (which baseline uses how many groups, which
parameter values were swept) against the paper's experimental section: these are easy to get
wrong from memory.

## 5. The worked example

One toy instance, shown step by step, is the centre of the poster.

- Draw it in TikZ, or recompile the paper's or the slides' overview figure with Helvetica,
  without its paper caption, header sentences and legend. The poster caption replaces them.
- Make it as large as the box allows. On paper, no label under 22 pt.
- Reuse the instance elsewhere (the same six items as dots in the problem box), with the same
  colours, so that the visitor meets it twice.
- Recompute it with a script: every intermediate state, every cost, the final value, and by
  brute force that the final value is what the poster says it is (optimal, maximal). Fifteen
  lines of Python prevent a wrong number on a printed sheet.
- If the example hits a corner case of the theory (an unreachable threshold, a parity
  constraint), the formulas on the poster must cover that case.

## 6. Logos and QR codes

- Logos are vector PDFs. Convert SVG with `rsvg-convert -f pdf -o logo.pdf logo.svg`. Keep the
  user's logos in `<skill>/logos-private/` and copy them into the poster's `logos/` folder.
- QR codes are drawn by the `qrcode` package as vector rules; nothing to download. After the
  build, decode them from the PDF (`poster.py check`) and compare with the intended links.
  Decoding is local. Do not open the links with a web request unless the user asks: they
  contain the user's account and project names.
