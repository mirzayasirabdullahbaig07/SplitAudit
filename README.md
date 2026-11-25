# SplitAudit
**How much does an ordinary random train/test split overstate performance when samples come in groups (sites, lineages, patients, studies)? An open-source audit, with simulation and two real-data case studies in antimicrobial-resistance (AMR) machine learning.**

Status (2026-11-25): code and tests; synthetic validation; two real-data case studies; manuscript draft in `paper/MANUSCRIPT_DRAFT.md` (not peer reviewed, not yet submitted). Numbers below come from files in `docs/`; every run is logged in `EXPERIMENT_LOG.md`.

## Progress (updated 2026-11-25): about 78% toward a preprint

This is an estimate of the work needed to reach a postable preprint, not a measure of quality. Most analysis and drafting exist; checking, outside input and release remain.

| Area | Status |
|---|---|
| Code and tests | Done (7 tests pass on a clean install) |
| Simulation study | Done (8-dataset intervals, sensitivity, permutation null; numbers checked against saved files) |
| Real-data case studies | Done for two datasets: E. coli (consistent effect) and Scottish soil (near-null) |
| Third and fourth datasets | Done: E. coli (5,836 genomes) and Salmonella enterica (3,619 genomes with gene presence/absence), 30 cells each, 5 repeats; optimism positive with interval above zero in all 60 (medians 0.096 and 0.171 AUC; manuscript Sections 5.3-5.4). Yu et al. published results re-analysed in Section 5.5 |
| Manuscript | First draft of every section (`paper/MANUSCRIPT_DRAFT.md`), abstract and discussion updated for four settings; not yet edited or reviewed |
| Figures | 6 of 6 made (Fig 6 now covers all four settings); Fig 2 and 3 captions to be checked |
| Reporting checklist | Drafted; piloted on 2 fully read papers only |
| Literature review | Weakest part: about 40% of the coded papers unread (6 coded; L06 Delgado-Baquerizo 2022 added); statements about other papers need checking against the PDFs |
| Release | Not started: no code licence, tag or DOI yet |

**Remaining:** verify literature claims against the papers; get collaborators' paper list and a second coder; decide authors, venue and licence; edit the manuscript; tag a release and mint a Zenodo DOI; post a preprint.
**Known weaknesses:** two real datasets only (the soil table has no environmental covariates); real-data intervals cover split repeats only; the prevalence of unstated splits in the literature is not yet established.

Detailed plan and status: `PAPER_ROADMAP.md`.

## 1. What it does
For the same data and models, SplitAudit compares three five-fold schemes (random, stratified, group-held-out) and reports:
- **Optimism** = score(random) − score(group), with a bootstrap interval over split repeats.
- **Same-group nearest-neighbour rate** (model-free): how often a test row's nearest training row is from its own group. Exactly 0 under a group split; under a random split it shows how identifiable the groups are.
- **Within-group label-permutation null**: the group-split AUC should be near 0.5.

## 2. Results so far (see the manuscript for caveats)
| Setting | Finding |
|---|---|
| Simulation (8 datasets per cell) | Optimism ≈ 0 when groups cannot be identified from features (`fingerprint_sd=0`); with strong fingerprints (`fingerprint_sd=1.5`, `rho=1`) 0.135 (logreg), 0.240 (random forest), 0.219 (gradient boosting) AUC |
| E. coli resistome (738 genomes; CTX-M and tet(A) labels; 3 models, AUC and balanced accuracy, groups = sequence type / phylogroup / country) | Optimism positive in 36/36 cells, 0.013 to 0.084; every split-repeat interval excludes 0 |
| Scottish soil survey (199 samples; 5 gene-detection labels; groups = site name or spatial blocks) | Small and inconsistent: median 0.002 to 0.012; interval excludes 0 in 13 of 45 cells |

Intervals on real data reflect repeated splits of one dataset only and understate uncertainty across datasets. Simulated optimism is a designed effect, not an estimate for real data.

## 3. Quick start
```bash
pip install -e . pytest && python -m pytest -q          # ~90 s
splitaudit simulate --repeats 3                          # synthetic sweep
splitaudit simulate --fingerprint-sd 0 1.5 --models logreg rf gb
splitaudit audit --csv data.csv --label y --group site --repeats 10   # your data
```
`audit` uses all numeric columns except the label and group as features unless `--features` is given, and `--metric auc|bacc`. Declare the groups before looking at results.

## 4. Reproducing the paper's numbers
| What | Command |
|---|---|
| Multi-dataset simulation | `python scripts/multiseed.py` |
| Sensitivity (groups, rows per group) | `python scripts/sensitivity.py` |
| NN diagnostic | `python scripts/nn_diagnostic.py` |
| Permutation null and group-split AUC | `python scripts/permutation_null.py <outdir>` (outdir must exist) |
| E. coli data preparation | `python scripts/prepare_ecoli.py` (needs the raw file in `data/ecoli_resistome/`) |
| E. coli audits | `splitaudit audit --csv data/ecoli_resistome/ecoli_ctxm_prepared.csv --label y --group st --repeats 10` (also `phylogroup`, `country`); robustness: `python scripts/real_ecoli_robustness.py` |
| Soil audit | `python scripts/real_soil_audit.py data/scottish_soil/N019776_Scotland_soil_survey_antibiotic_resistance_genes.csv docs` |
| Figures | `python scripts/make_fig2.py`, `make_fig3.py`; `make_fig1.py [outdir]`, `make_fig5.py [outdir]`, `make_fig4.py [folder with the CSVs]` |

Scripts take optional output paths (defaults point into `docs/` or `data/`; run from the repository root). `multiseed.py` writes both the raw and the summary CSV (t-intervals across datasets). Raw data are not in the repository (`data/` is git-ignored); see `data/README.md` for sources, licences and download notes.

## 5. Data and licences
- E. coli resistome: Mendeley Data, doi 10.17632/r5ccbmsnhw.1, CC BY 4.0.
- Scottish soil ARG survey: Knapp et al. 2019, NERC EIDC, doi 10.5285/d3498e93-4ac5-4eab-bc1a-eb2328771d24, OGL-UK-3.0 (attribution: "Contains data supplied by UK Centre for Ecology & Hydrology").
- Code licence: **not yet chosen** — add a `LICENSE` file before release.

## 6. Lessons recorded in the log
- A first E. coli run was invalid: genes appeared under two naming schemes, so the label leaked into the features (AUC ≈ 0.99). Check the most predictive feature before trusting any real-data audit.
- Single-dataset intervals understate uncertainty; use several datasets where possible.
- Group-split AUC can fall below 0.5 on individual simulated datasets (not on average at the settings we ran).

## 7. Limitations
Binary labels only; groups must be known and are treated as given (nested or overlapping groups, e.g. sequence type within phylogroup, need care); optimism measures sensitivity to the split, not model correctness; default untuned models; two real datasets; no temporal blocking; spatial blocks in the soil study were k-means clusters of arbitrary size. Literature statements in the manuscript are partly based on abstracts and fetch summaries and need verification against the papers.

See `PAPER_ROADMAP.md` (paper plan and status), `ROADMAP.md` (project plan), `docs/DATASETS.md`, `docs/LITERATURE_NOTES.md`, `paper/reporting_checklist.md`.
