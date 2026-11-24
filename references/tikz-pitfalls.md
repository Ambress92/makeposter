# LaTeX and TikZ pitfalls on a poster-sized page

Each entry: what you see, why, and the fix. `posterstyle.sty` and the templates already
contain these fixes; the list is here so that they are not removed and so that new code
follows them.

## Text in nodes

**Words run together in large text.** A TikZ node with `text width` sets `\spaceskip` from the
10 pt document font, so 33 pt text gets 3 pt word spaces. Fix: every font change goes through
`\fsz{size}{leading}`, which resets `\spaceskip` and `\xspaceskip`. Never write a bare
`\fontsize...\selectfont` in a node.

**The last paragraph of a node has the wrong line spacing.** Leading is applied when the
paragraph ends, and a group that closes before `\par` restores the old leading. Fix: end every
paragraph inside the group that sets its font, `{\fCaption text\par}`.

**`align=` on a node with `text width`** brings the spacing problem back. Use `\raggedright` or
`\centering` inside the node text instead.

**A line after a displayed formula starts slightly indented.** The paragraph continues after
`\]`, and a line break in the source becomes a space. Fix: `\]\par` and then `\vspace{...}`
before the next block.

**Hyphenated words.** The style sets `\hyphenpenalty=10000`. Keep it: hyphens look wrong at
this size.

**An inline formula breaks in an odd place.** TeX may break after any relation or binary
operator at the outer level. Display the formula, or wrap the part that must stay together in
braces.

## Math

**Tiny sum signs, braces and fraction bars.** `lmodern` declares the math extension font at a
fixed 10 pt. The style redeclares it scalable:
`\DeclareFontShape{OMX}{lmex}{m}{n}{<->lmex10}{}`.

**Text inside a displayed formula** (`\text{swaps, at distance}`) uses the surrounding text
font and size, which is what you want; put spaces around it with `\ \ `.

## Pictures inside boxes

**Nodes of a nested `tikzpicture` sit in the wrong place**: dots hang below their axis, labels
touch the band above them. Nested nodes inherit `anchor=north` and `inner sep=0pt` from the
box node that contains them. Fix: every node of a nested picture states its own anchor
(`anchor=center`, `anchor=base`, `anchor=south`, ...). To find such an error, draw two thin red
guide lines at known coordinates and look where the nodes land.

**Labels that should share a baseline do not.** `anchor=north` aligns the tops of the text
boxes, and letters with ascenders or descenders differ in height. Use `anchor=base` (or
`base east`, `base west`) with one y coordinate.

**A placeholder or frame that is exactly `\linewidth` wide gives an overfull box.** The line
width of its border adds to its size. Fix the bounding box first (`\useasboundingbox`) and
draw the border inside it.

**Minipages side by side do not align at the top** when one starts with a picture. Start both
with `\vspace{0pt}` and use `[t]`.

## Tables and rules

`booktabs` rule widths are tied to the 10 pt font. The style sets `\heavyrulewidth` to 3 pt,
`\lightrulewidth` to 1.5 pt and the separations in centimetres. A table that spans the box:
`\begin{tabular*}{\linewidth}{@{}l@{\extracolsep{\fill}}ll@{}}`.

## Plots (matplotlib)

- `bbox_inches="tight"` changes the size of each figure a little. Include plots by height.
- A legend needs headroom: multiply the upper axis limit until the legend clears the data.
- On a log axis with many decades, `LogLocator(base=100)` and no minor ticks keep the labels
  readable.
- With `mathtext.fontset = "custom"` and a sans font, exponents sit a little apart from the
  base. It is acceptable; do not switch to a serif math font to avoid it.
- Fonts are embedded as Type 3 outlines by default, which prints fine. If a print shop's
  preflight objects, set `pdf.fonttype: 42` and regenerate.

## Building and inspecting

- `poster.py build` compiles, lists errors and box warnings, prints the page size and removes
  `.aux`, `.log` and `.out`. Zero overfull boxes is the target.
- To look at a region, give its corners in poster centimetres:
  `poster.py view --region X0 Y0 X1 Y1 --dpi 60`. The whole sheet at 22 to 24 dpi, a box at
  about 60 dpi, a detail at 100 dpi or more.
- When a change is a plain text substitution, apply it with a small script that asserts the old
  text occurs exactly once; a silent no-op is worse than an error.
- In shell heredocs that contain `$` or backslashes, quote the delimiter (`<<'EOF'`).
- OpenCV (for decoding QR codes) may conflict with packages of the user's Python. Install it
  aside, `python3 -m pip install --target DIR opencv-python-headless`, and run the check with
  `PYTHONPATH=DIR`. Files in a temporary folder can vanish after a few days; reinstall if an
  import fails oddly.
