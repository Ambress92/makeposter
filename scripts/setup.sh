#!/usr/bin/env bash
# Check (and with --install, install) everything makeposter needs.
# Usage: scripts/setup.sh [--install]
# Exit 0 when all required pieces are present, 1 otherwise. Optional pieces never fail the check.
set -u
INSTALL=0; [ "${1:-}" = "--install" ] && INSTALL=1
missing=0
os="$(uname -s)"

say()  { printf '  %-30s %s\n' "$1" "$2"; }
have() { command -v "$1" >/dev/null 2>&1; }
tex_has() { kpsewhich "$1" >/dev/null 2>&1; }

echo "makeposter requirements:"

# 1. TeX engine
for b in pdflatex kpsewhich; do
  if have "$b"; then say "$b" "ok"; else say "$b" "MISSING"; missing=1; NEED_TEX=1; fi
done

# 2. LaTeX packages and fonts (file:tlmgr package)
if have kpsewhich; then
  TL_PKGS=""
  for pair in standalone.cls:standalone tikz.sty:pgf qrcode.sty:qrcode booktabs.sty:booktabs \
              helvet.sty:psnfss uhvr8a.pfb:helvetic lmodern.sty:lm amsmath.sty:amsmath \
              amssymb.sty:amsfonts xkeyval.sty:xkeyval xcolor.sty:xcolor; do
    f="${pair%%:*}"; p="${pair##*:}"
    if tex_has "$f"; then say "$f" "ok"; else
      say "$f" "MISSING (tlmgr: $p)"; missing=1
      case " $TL_PKGS " in *" $p "*) ;; *) TL_PKGS="$TL_PKGS $p";; esac
    fi
  done
fi

# 3. poppler: rendering, text layer, fonts and images of the PDF
for b in pdftoppm pdfinfo pdftotext pdffonts pdfimages; do
  if have "$b"; then say "$b" "ok"; else say "$b" "MISSING (poppler)"; missing=1; NEED_POPPLER=1; fi
done

# 4. python
PY_PKGS=""
for pair in numpy:numpy PIL:pillow matplotlib:matplotlib; do
  m="${pair%%:*}"; p="${pair##*:}"
  if python3 -c "import $m" 2>/dev/null; then say "python3 $m" "ok"; else say "python3 $m" "MISSING"; missing=1; PY_PKGS="$PY_PKGS $p"; fi
done

# 5. optional
if python3 -c "import cv2" 2>/dev/null; then say "python3 cv2 (optional)" "ok"; else
  say "python3 cv2 (optional)" "missing: QR codes cannot be decoded (pip: opencv-python-headless)"; OPT_CV=1; fi
if have rsvg-convert; then say "rsvg-convert (optional)" "ok"; else
  say "rsvg-convert (optional)" "missing: needed only to turn SVG logos into PDF (librsvg)"; OPT_RSVG=1; fi

[ $missing -eq 0 ] && { echo "all required pieces present"; exit 0; }

echo
if [ $INSTALL -eq 0 ]; then
  echo "Missing pieces. Re-run with --install, or run by hand:"
else
  echo "Installing missing pieces:"
fi

run() { echo "  $*"; [ $INSTALL -eq 1 ] && eval "$*"; }

if [ "${NEED_TEX:-0}" = 1 ]; then
  case "$os" in
    Darwin) have brew && run "brew install --cask basictex && eval \"\$(/usr/libexec/path_helper)\"" || echo "  install BasicTeX from https://www.tug.org/mactex/morepackages.html";;
    Linux)  run "sudo apt-get install -y texlive-latex-base texlive-latex-extra texlive-pictures texlive-fonts-recommended lmodern";;
  esac
fi
if [ -n "${TL_PKGS:-}" ] && have tlmgr; then
  run "sudo tlmgr update --self"
  run "sudo tlmgr install$TL_PKGS"
fi
if [ "${NEED_POPPLER:-0}" = 1 ]; then
  case "$os" in
    Darwin) run "brew install poppler";;
    Linux)  run "sudo apt-get install -y poppler-utils";;
  esac
fi
if [ -n "${PY_PKGS:-}" ]; then
  run "python3 -m pip install --user$PY_PKGS"
fi

if [ $INSTALL -eq 1 ]; then
  echo; echo "re-checking:"; exec "$0"
fi
exit 1
