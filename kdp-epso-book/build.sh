#!/usr/bin/env bash
# Rebuild every deliverable from source: content generators -> interior PDF -> covers -> Kindle EPUB.
set -euo pipefail
cd "$(dirname "$0")"
PY="${PYTHON:-python3}"
"$PY" -c "import reportlab, pypdf, PIL, fontTools" 2>/dev/null || "$PY" -m pip install -q reportlab rlPyCairo pypdf pillow fonttools
"$PY" src/gen_numerical.py
"$PY" src/gen_abstract.py
"$PY" src/gen_skills.py
"$PY" src/build_pdf.py
"$PY" src/cover.py "$@"
"$PY" src/build_epub.py
