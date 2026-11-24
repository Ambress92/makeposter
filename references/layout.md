# Layout: sheet, grid, type scale, capacity

Contents: 1. Sheet and coordinates. 2. The two template grids. 3. Another size. 4. Type scale.
5. What fits in a box. 6. Balancing free space. 7. Header, logos and QR codes. 8. The row of plots.

## 1. Sheet and coordinates

The poster is one `tikzpicture` with `x=1cm,y=1cm` in a `standalone` document, clipped to
`\useasboundingbox (0,0) rectangle (\PW,\PH)`. The origin is the bottom left corner of the
printed sheet. A box written as `\pbox{1.5}{30.5}{40.5}{57}{Title}{...}` spans 1.5 to 40.5 cm
from the left edge and 30.5 to 57 cm from the bottom edge. Because sizes are absolute, the PDF
needs no scaling at the print shop, and `poster.py` can crop, measure and proofread any box
from its coordinates. Keep those coordinates as plain numbers.

Take the size from the venue's instructions of the current year. Examples: NeurIPS 2026 main
conference 140 x 90 cm landscape, its workshops 61 x 85 cm portrait, A0 84.1 x 118.9 cm,
36 x 48 inch 91.4 x 121.9 cm. Many venues forbid a larger sheet; a smaller one is allowed.

## 2. The two template grids

Shared measures: outer margin 1.5 cm at the sides and 1.4 cm at top and bottom, 1.5 cm between
columns and between rows, 1.9 cm between two boxes stacked inside one column, box border
0.3 cm, corner radius 2.6 cm.

Landscape, 140 x 90 cm (`poster_landscape.tex`):

| Part | x (cm) | y (cm) |
|---|---|---|
| Logos (venue over institution) | centred at 13 | 85.5 and 80.2 |
| Title band | 25 to 117 | 78.4 to 88.6 |
| QR codes, 7.6 cm | centred at 123.3 and 133.4 | top at 88.6 |
| Left column, two boxes | 1.5 to 40.5 | 30.5 to 77.0, split near 57 |
| Middle column, one box | 42 to 98 | 30.5 to 77.0 |
| Right column, two boxes | 99.5 to 138.5 | 30.5 to 77.0, split near 52 |
| Row of plots | 1.5 to 138.5 | 1.4 to 29.0 |

The middle column is the widest because it holds the method and the worked example, which is
what a visitor looks at first. Reading order: left column, middle, right column, plots.

Portrait, A0 (`poster_portrait.tex`): the band spans the full width at the top, since a band
squeezed between logos and QR codes would be too narrow for the title. Logos and QR codes move
to a footer. Two columns of 39.8 cm (1.5 to 41.3 and 42.8 to 82.6). Rows from the top: band
106.3 to 117.4, problem and formal setting 83.8 to 104.8, method across both columns 56.3 to
82.3, main result and guarantees 35.3 to 54.8, plots 11.8 to 33.8, footer below 10.3.

These row heights are starting points. After the text is in, move the borders so that every
box is comfortably full (section 6).

## 3. Another size

1. Set `\PW` and `\PH`.
2. Pick the template with the same orientation. Scale its x coordinates by the ratio of the
   widths and its y coordinates by the ratio of the heights.
3. Put the gutters back to 1.5 cm and the stacked gap back to 1.9 cm (they must not scale).
4. Choose the type scale from the column width (section 4).
5. On a sheet under 70 cm wide, use one column for the text boxes: two columns would force
   body text under 24 pt.

## 4. Type scale

Sizes are in points on paper, set by `\fsz{size}{leading}` in `posterstyle.sty`.

| Role | Macro | Size / leading |
|---|---|---|
| Title | `\fTitle` | 110 / 120 |
| Subtitle | `\fSub` | 54 / 64 |
| Authors | `\fAuthors` | 40 / 48 |
| Box title | `\fBoxTitle` | 46 / 54, bold, navy |
| Plot title | `\fPanelTitle` | 36 / 44, bold, navy |
| Body | `\fBody` | 33 / 43 |
| Caption, table note | `\fCaption` | 28 / 36 |
| QR label | `\fQR` | 30 / 36 |
| Plot ticks, axis labels, small-multiple titles, legend | in `make_poster_figs.py` | 22, 26, 28, 22 |

The scale suits columns about 39 cm wide: roughly 60 characters of body text per line, which
reads well from one to two metres. For narrower columns write
`\renewcommand{\posterfontscale}{s}` after loading the style, with `s` about the column width
divided by 39, and set the same `SCALE` in the figure script. Keep body text at 28 pt or more
on a large sheet and never under 24 pt, captions and plot labels never under 20 pt. If the text
does not fit at those sizes, the poster has too much text; cut text, do not shrink type.

A long title: at 110 pt a title takes about 1.75 cm per character. Use the short
name of the method as the title and the rest of the paper title as the subtitle. If it still
does not fit, reduce `\fTitle` for this poster rather than breaking the title over two lines.

## 5. What fits in a box

- Text width is the box width minus 3.4 cm.
- Body text: about 1.7 characters per centimetre of text width, one line every 1.52 cm.
- Captions: about 2 characters per centimetre, one line every 1.27 cm.
- The title block uses the first 4.0 cm of a box.
- A displayed formula takes about 2.2 cm, or 3 cm with a fraction or a sum.
- A table row takes about 1.6 cm; the three rules of a small table add about 1.8 cm.

So a 39 x 24 cm box holds about twelve lines of body text, or six lines and two displayed
formulas. As a density target, a text box that is more than two thirds running text reads as a
wall: turn part of it into a formula, a table or a picture, or cut it.

## 6. Balancing free space

`poster.py boxes` prints, for every box, the free space above the title and below the last
ink. Targets: at least 1.1 cm below the content, similar values for boxes that sit on top of
each other, and not much more than 3 cm anywhere (a half-empty box looks unfinished).

Two stacked boxes share a border position. To move free space from one to the other, change
the bottom `y0` of the upper box and the top `y1` of the lower box by the same amount, and
keep the 1.9 cm between them. This is a layout change with no change of text; make it freely
and mention it in the report.

Inside a box, spacing between blocks is set with `\vspace`: about 0.3 cm between two formal
blocks, 0.6 cm around a picture, more in the large method box. Use it to let the content
breathe when a box has room, before considering more text.

## 7. Header, logos and QR codes

- The band has rounded top-left and bottom-right corners (radius 5.5 cm) and a vertical
  gradient. `\posterband` centres title, subtitle and authors in it.
- Logos: venue logo and institution logos, vector, placed with `\posterimg{w}{h}{file}`, which
  fits the file into the given size and prints a labelled placeholder while the file is
  missing. Check the build log for nothing worse than pdfTeX's harmless "multiple pdfs with
  page group" note.
- QR codes: `\posterqr{x}{ytop}{size}{url}{label}`, at least 6.4 cm wide, each with a one-word
  label ("Paper", "Code"). Short URLs give coarser codes that scan from farther away. Decode
  them from the built PDF in the final check.
- The header needs no affiliation line when the logos carry the affiliations. A contact email
  and the venue with its year as text are optional; offer them, do not add them unasked.

## 8. The row of plots

`\pframe` draws the frame. `\ppanelsetup{ytitle}{yfigure}{ycaption}` sets three heights for the
row, and `\ppanel{xcentre}{width}{title}{figure}{caption}` places one plot:

- titles hang from one line and stay on one line each;
- figures stand on one line (`anchor=south`), so plots of equal height have their x-axes at the
  same level, which is what makes a row look tidy;
- captions start on one line (each begins with `\strut`, because an exponent in the first line
  would otherwise push that caption down) and are at most as wide as their plot.

Give all plots of a row the same height: draw them with the same `figsize` height and include
them with the same height in `\posterimg`, since `bbox_inches="tight"` trims each plot a little
differently. Leave at least 2 cm between neighbouring plots. With every caption on two lines,
move titles, plots and captions together until the free space above the titles equals the free
space below the captions.
