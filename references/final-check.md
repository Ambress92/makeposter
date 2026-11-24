# Final check before printing

Do every step, in this order, and report each with its evidence. Change only what is wrong
(and layout that needs no decision); collect everything else as suggestions for the user.

## 1. The file

```bash
python3 <skill>/scripts/poster.py check --size 140x90     # the venue's size in cm
```

It rebuilds the poster and reports: errors and overfull boxes (expect none), the page size
against the expected one, fonts that are not embedded (expect none), raster images and their
resolution at print size (expect none, or 150 ppi and more), placeholders left in the source
(template links, missing logos or figures), and the content of the QR codes decoded from the
PDF. If OpenCV is missing, install it aside as described in `tikz-pitfalls.md`, or ask the
user to scan both codes with a phone.

## 2. The venue's rules

Fetch the venue's poster instructions again and compare: size and orientation, "do not print
larger", how posters are hung, whether a virtual poster or a thumbnail must be uploaded and by
when. Quote the size line in the report.

## 3. The text

```bash
python3 <skill>/scripts/poster.py text
```

Read the text of every box as a visitor would. Look for typos, a term that changed name
between boxes, a symbol used before its definition, a number rounded differently in two
places, a claim stronger than the paper's. The command also lists doubled words. Search the
source for words that need proof ("worst", "best", "always", "optimal", "dominates") and
confirm each one.

## 4. The numbers

- Recompute the worked example with a script: each state, each cost, the final value, and by
  brute force any "optimal" or "maximal" on the poster.
- Check every number quoted in a caption against the result files ("in about a minute", "four
  datasets", parameter grids).
- Confirm each plot title against the data (see `figures.md`, section 4).

## 5. The look

```bash
python3 <skill>/scripts/poster.py boxes
python3 <skill>/scripts/poster.py view
python3 <skill>/scripts/poster.py view --box NAME      # once per box
```

Free space: at least 1.1 cm under the content of every box, similar in stacked boxes. Page
margins of about 1.3 cm on all sides. Then read every render: alignment of plots and captions,
labels touching lines, one-word last lines, anything clipped by a rounded corner.

## 6. The report

Lead with the verdict. Then what was checked, each with its evidence in one line. Then what
you changed. Then a numbered list of suggestions, each small enough to accept with one word.
Then the print notes below. Say plainly what you did not check (for example that the links
behind the QR codes were decoded but not opened).

## Print notes to pass on

- The PDF is at print size: print at 100 %, no scaling, no cropping. The outer margin is thin.
- Colours are RGB. Print shops convert to CMYK, and saturated blues can print slightly duller;
  ask for a proof when colour matters.
- Bring what the venue asks for to hang the poster (pins, adhesive strips or the venue's own).
- For a virtual poster: `poster.py png --width 5000` writes an image of the whole sheet.
