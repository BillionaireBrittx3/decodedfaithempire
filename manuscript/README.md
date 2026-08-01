# God, Strengthen the Man I'm Becoming — Manuscript Rebuild

Rebuild of the 365-day devotional to remove the verbatim-repeated teaching
paragraph and prayer template, giving each devotion a distinct voice, opening,
teaching angle, and prayer posture — while preserving all other content exactly.

## Status: CHECKPOINT — 42 of 365 devotions rebuilt (paused at request)

- **Rewritten:** teaching section + prayer for devotions **1–42** (Part One
  complete; Part Two through devotion 42).
- **Untouched so far:** devotions 43–365 still carry the original text (will be
  rebuilt in subsequent batches).
- **Preserved verbatim everywhere:** devotion titles, the one-line "Today's
  Real-Life Struggle" statement, Scripture paraphrases + references, "What God
  Is Building in You," "Your Faith Step Today," all front matter and back
  matter, the two-page structure, and the exact 753-page layout.

## Deliverables

- `God_Strengthen_the_Man_Im_Becoming_REBUILT.docx` — editable master.
- `God_Strengthen_the_Man_Im_Becoming_REBUILT.pdf` — KDP-ready render:
  6×9 trim, original margins (T 0.48" / B 0.5" / L·R 0.62"), Noto Serif
  (the source's embedded typeface), centered page-number footers, exact
  original pagination (753 pages, verified against the source, zero overflow).

## Titles flagged for author decision

Two devotions were the only ones in the book without a real title — both the
Part One and Part Two closers carried the placeholder **"The Next Faithful
Step 31"** (verified on source PDF pages 71/72 and 134/135; "31" = each one's
position within its 31-devotion Part). They have been set to
**"The Next Faithful Step"** (artifact "31" removed, no invented content). Say
the word to differentiate them instead.

A second, likely-intentional duplicate remains untouched: **"Correcting Without
Crushing"** appears as devotion #111 (leadership) and #158 (fatherhood).

## Reproducing / resuming (`pipeline/`)

1. Write the next batch's `{teaching:[5], prayer:[6]}` into `rewrites.json`.
2. `python3 apply.py Man_rebuilt.docx` — injects text into the DOCX,
   preserving all formatting, adding typographic quotes, applying title fixes.
3. `python3 render_pdf.py Man_rebuilt.docx Man_rebuilt_render.pdf` — renders the
   KDP PDF using `fonts/` and the original page breaks in `pagemap.json`.

`progress.json` tracks the next devotion; `context.json` holds every devotion's
preserved material; `variety_ledger.json` records the opening/voice/angle/prayer
posture used per devotion to keep the whole book varied.
