# SplitAudit — handover note for the supervising researcher

Prepared 2026-11-25. Read this first (10 minutes), then `paper/MANUSCRIPT_DRAFT.md`.

## 1. One-paragraph summary
SplitAudit asks how much an ordinary random train/test split overstates performance when samples come in groups (lineage, site, space), and provides an open-source audit: optimism (random minus group-held-out score), a model-free same-group nearest-neighbour diagnostic, and a within-group permutation null. Evidence so far: a simulation with known ground truth (optimism ≈ 0 when groups cannot be identified from features; 0.135–0.240 AUC when they can), a clinical AMR case study (738 E. coli genomes: optimism positive in 36/36 model/metric/grouping/label combinations, 0.013–0.084), and an environmental case study (Scottish soil survey: small and inconsistent, interval excludes zero in 13 of 45 combinations). A first draft of the whole paper exists. It is not peer reviewed and nothing has been submitted.

## 2. Where things are
| What | Where |
|---|---|
| Manuscript draft (all sections, figure captions, checklist appendix, references) | `paper/MANUSCRIPT_DRAFT.md` (built from the other `paper/draft_*.md` files) |
| Paper plan and status | `PAPER_ROADMAP.md` (section 10 = status) |
| Every run: command, seed, data version, result | `EXPERIMENT_LOG.md` |
| Result tables (CSV) and figures | `docs/` |
| Number check of the manuscript against saved files | `paper/NUMBER_CHECK.md` |
| Literature notes, coding sheet, references | `docs/LITERATURE_NOTES.md`, `docs/review_coding_sheet.csv`, `paper/references.md` |
| Reporting checklist and pilot | `paper/reporting_checklist.md`, `paper/checklist_pilot.*` |
| Data sources, licences, caveats (data not in git) | `data/README.md`, `docs/DATASETS.md` |
| Data layout (all under `data/`, not in git): `ecoli_resistome/`, `scottish_soil/`, `yu_amr_bias/{metadata,authors_results}/`, `_zips/`; PDFs in `literature/` | `data/README.md` |
| Yu et al. audits (E. coli, Salmonella) | `scripts/prepare_yu_ecoli.py`, `scripts/real_yu_ecoli_audit.py`, `scripts/real_yu_audit.py`, `docs/real_yu_ecoli_audit.csv`, `docs/real_yu_salmonella_audit.csv`, manuscript Sections 5.3-5.4 |
| Secondary analysis of Yu et al. published results | `scripts/yu_published_optimism.py`, `docs/yu_published_optimism_*.csv`, manuscript Section 5.3 |
| Code | `src/splitaudit/`, `scripts/`, `tests/` (7 tests pass on a clean install) |
| Release plan | `docs/RELEASE_NOTES_draft.md` |

## 3. Decisions needed from you
1. **Authors, affiliations, venue, preprint server.** Not decided.
2. **Code licence.** None chosen; without one the code cannot be legally reused. MIT or Apache-2.0 are typical.
3. **Framing.** The draft states plainly that the soil result is near-null and that the effect depends on how identifiable the groups are. Confirm this is the paper you want (a methods/measurement paper with mixed real-data results), not a "leakage is everywhere" paper, which the evidence does not support.
4. **Scope.** Is two real datasets enough? The soil table has no environmental covariates, so it is not a realistic prediction task. A third dataset with covariates would strengthen the paper most.
5. **Literature/review component.** The planned correlation between leakage-risk rating and reported score was dropped (only 2 papers fully coded). Decide whether the collaborators' review can supply about 10+ coded papers, and who the second coder is.

## 4. What is solid and what is not
Solid (recomputed from saved files; see `paper/NUMBER_CHECK.md`): simulation tables and p-values, E. coli and soil results, tests.
Needs verification before submission:
- **All statements about other people's papers** (Sections 1, 2, 5, 6 and the checklist pilot). Two papers were read through full-text fetch summaries, one from its abstract only, two not at all. Read the PDFs and fix the cells in `docs/review_coding_sheet.csv`; leakage-risk ratings are deliberately blank.
- **References.** Four checked against Crossref/arXiv; the rest are marked unverified in `paper/references.md`. Two points to resolve: the Yu/Wheeler/Barquist paper is now in PLOS Biology (cite that version), and the Meyer et al. 2019 paper is about spatial predictor selection, so check it supports the claim it is cited for.
- **Section 6.2** (why soil differs from E. coli) is a hypothesis, untested.
- **Figure captions** (Fig 2, Fig 3) were written from memory of the plots.

## 5. Known weaknesses a reviewer will raise
- **Novelty / prior tools (found 2026-11-25).** Existing tools overlap: DataSAIL (leakage-reduced splitting), blockCV (spatial and leave-group-out folds), and especially the R package BORG, which includes a random-versus-blocked CV comparison. An earlier draft said no reusable tool existed; that was wrong and has been corrected. Before submission someone should install BORG and compare it with SplitAudit on the simulated data, then state the differences precisely.
- Two real datasets; one has no covariates.
- Real-data intervals cover repeated splits of one dataset only and understate uncertainty across datasets.
- Prevalence of unstated or leaky splits in the literature is not established (five papers coded, two read fully).
- Optimism measures sensitivity to the split, not whether a model is right; linked genes and nested groupings complicate interpretation.
- Models are untuned defaults (logistic regression, random forest, gradient boosting).
- Spatial blocks in the soil study were arbitrary k-means clusters; the block count changed the result.

## 6. Things that went wrong, so you can trust the record
- First E. coli run was invalid: genes appeared under two naming schemes, so the label leaked into the features (AUC ≈ 0.99). Found by inspecting the top feature, fixed, logged as invalid.
- Several early simulation claims rested on one dataset or 4 seeds; replaced with 8-dataset results. Two manuscript claims (permutation null "always 0.45–0.55"; "about 0.4 AUC below chance") were too strong and were corrected after re-running.
- Files in the working folder were reverted by an unknown process three times (the experiment log twice, README once). Check `git status` and `git diff` before trusting a pull.

## 7. Suggested next steps (about in order)
1. Read the manuscript; mark disagreements.
2. Verify literature claims against PDFs; complete the coding sheet and references.
3. Decide authors, licence, venue; add `LICENSE`, `CITATION.cff`.
4. Two datasets from Yu, Wheeler & Barquist 2025 (CC BY 4.0) are now audited: E. coli (Section 5.3; median 0.096 AUC) and Salmonella enterica (Section 5.4; median 0.171), 30 cells each, 5 repeats, all positive. Open points: the Salmonella effect is larger than the authors' own published S. enterica pairs (0.063) and we have not explained the gap; feature filter tightened after one pilot cell (E. coli only); K. pneumoniae gene matrix is on hand but not audited (its metadata may lack fastbaps); default models. A second coder for the literature sheet is still needed.
5. Edit the manuscript (expect one or two rounds), regenerate figures if anything changes.
6. Re-run long scripts from a clean checkout, tag `v0.2.0`, mint a Zenodo DOI, post a preprint.

## 8. Reproduce
```bash
pip install -e . pytest && python -m pytest -q
```
Raw data go in `data/` as described in `data/README.md` (not in git). Commands for each result are in the README table "Reproducing the paper's numbers".
