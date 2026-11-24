# Checklist pilot (DRAFT) — what this can and cannot show

Codes: Y = reported/done; N = not done or evidently violated; NS = not stated in the text we saw; NA = not applicable; NR = not read/not assessable.
Source: `docs/review_coding_sheet.csv`, which for L02 and L03 rests on full-text fetch summaries (to be re-verified against the PDFs by you), for L05 on the abstract only, and not at all for L01 and L04.

## What the two assessed papers show
- L02 (200 sequences): item 7 N (features filtered on the full dataset before splitting); item 10 N (negatives chosen on feature differences); items 4 and 2 NS; no group-held-out score (5 N), no diagnostics (11, 12 N); Y only for reporting AUC and accuracy.
- L03: item 4 N (single 60/40, assignment not stated); item 13 Y (external mystery set, scored lower in some regions); item 14 Y (95% CI on accuracy); preprocessing and tuning isolation NS. Items 1/3 are NA-ish because city is the prediction target.

## Limits (do not overstate)
- n = 2 fully assessed papers. This is a worked demonstration of the checklist, not evidence about the field.
- "NS" means we did not find it in a summary; the paper itself may say it. Re-read before using any cell.
- Several items cannot be judged from text alone (e.g. 9 label-leak check), and were marked NS even when leaks might exist.
- The coder is one person-plus-model; no second coder, so no agreement estimate.

## To make this publishable
1. Re-verify L02/L03 cells against the PDFs; read L01, L04 and L05 full text.
2. Add your collaborators' ~10 papers.
3. Have a second person code a subset and report agreement.
