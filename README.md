# SplitAudit

**How much do random train/test splits overstate model performance on grouped data? A tool, a simulation study and four real antimicrobial-resistance (AMR) case studies.**

Status (2026-11-25): working code with tests, validated simulations, four real-data audits, and a complete first draft of the paper (`paper/MANUSCRIPT_DRAFT.md`). **Not peer reviewed, not submitted, not yet checked by a domain expert.** Every number in this file comes from a file in `docs/`, and every run is logged in `EXPERIMENT_LOG.md`.

Contents: [1 Problem](#1-the-problem) · [2 Idea](#2-what-splitaudit-does) · [3 Method](#3-method-in-detail) · [4 Results](#4-results) · [5 Install and use](#5-install-and-use) · [6 Reproduce](#6-reproducing-the-papers-numbers) · [7 Repository map](#7-repository-map) · [8 Data and licences](#8-data-and-licences) · [9 Progress](#9-progress) · [10 Limits](#10-limitations-and-what-we-do-not-claim) · [11 Open items](#11-open-items) · [12 Honesty notes](#12-lessons-and-honesty-notes) · [13 Citing](#13-citing-and-ai-assistance)

---

## 1. The problem
Machine-learning papers on AMR often report one cross-validated score. Their samples, however, come in **groups**: bacterial genomes from the same lineage (sequence type, population cluster) or soil samples from the same site. With a **random split**, close relatives land on both sides of the train/test line, so the model can score well by recognising the group instead of learning something that carries over to **new** groups (a new lineage, a new site). A **group split** keeps whole groups on one side and measures what most users actually care about.

The size of the gap is not known in advance. It depends on how identifiable the groups are from the features. SplitAudit measures it for your data before you report a number.

## 2. What SplitAudit does
For the same data and models, it runs three five-fold schemes (random, stratified, group-held-out) and reports:

| Output | Meaning |
|---|---|
| **Optimism** | score(random) − score(group), with a bootstrap interval over repeated splits. |
| **Same-group nearest-neighbour (NN) rate** | Model-free. How often a test row's nearest training row (in feature space) is from its own group. It is exactly 0 under a group split. It is reported with its **chance level** Σ p_g² (the sum of squared group proportions) and the **excess** = NN rate − chance. |
| **Within-group label-permutation null** | Shuffling labels inside groups should push group-split AUC to about 0.5. It is a sanity check on the pipeline. |

A reporting checklist is in `paper/reporting_checklist.md`.

## 3. Method in detail
- **Splits:** `KFold` (random), `StratifiedKFold`, and `GroupKFold` (5 folds each), repeated with different seeds.
- **Models:** logistic regression, random forest, gradient boosting, all default and untuned. Tuning is not the point of an audit, and untuned models keep the comparison transparent.
- **Metrics:** AUC (main) and balanced accuracy.
- **Uncertainty:** bootstrap interval over split repeats. This reflects splitting noise on **one** dataset only. It does not reflect variation across datasets.
- **Simulations** (`src/splitaudit/synthetic.py`) separate two kinds of leakage with known ground truth: label leakage (`rho`, labels correlated within groups) and covariate leakage (`fingerprint_sd`, groups identifiable from features). Optimism requires the second.
- **Real-data protocol:** groups and labels are declared **before** looking at results. Features are filtered by an unsupervised rule that does not use labels. Where several groupings are plausible, all are run.

## 4. Results
Full tables, caveats and figures are in the manuscript. Optimism is in AUC units.

### 4.1 Simulation (8 datasets per cell)
- With groups **not** identifiable from features (`fingerprint_sd = 0`): optimism ≈ 0.
- With strong fingerprints (`fingerprint_sd = 1.5`, `rho = 1`): 0.135 (logistic regression), 0.240 (random forest), 0.219 (gradient boosting).
- Simulated optimism is a designed effect. It is not an estimate for real data.

### 4.2 Four real-data case studies
| # | Dataset | Design | Result |
|---|---|---|---|
| 1 | **E. coli resistome**, 738 genomes (Mendeley, CC BY 4.0) | CTX-M and tet(A) labels; 3 models; AUC and balanced accuracy; groups = sequence type, phylogroup, country; 36 cells | Optimism positive in **36/36** cells, 0.013 to 0.084; every interval excludes 0 |
| 2 | **Scottish soil survey**, 199 samples (Knapp et al. 2019) | 5 gene-detection labels; groups = site name or spatial blocks; 45 cells | **Small and inconsistent**: median 0.002 to 0.012; interval excludes 0 in 13 of 45 cells. Chance levels 0.007 / 0.113 / 0.054 |
| 3 | **E. coli, Yu et al. 2025**, 5,836 genomes, 2,775 gene presence/absence features | 5 antibiotics (chosen by a fixed rule); groups = ST and fastbaps; 3 models; 5 repeats; 30 cells | **30/30** positive, interval above 0. Median **0.096** (0.043 to 0.297). Median AUC 0.855 random vs 0.771 (ST) and 0.760 (fastbaps) |
| 4 | **Salmonella enterica, Yu et al. 2025**, 3,619 genomes, 2,237 features | same rule and design; 30 cells | **30/30** positive, interval above 0. Median **0.171** (0.066 to 0.444). Median AUC 0.943 random vs 0.805 (ST) and 0.643 (fastbaps) |

Further detail:
- **Dataset 3:** by grouping, ST 0.078 and fastbaps 0.111. By model, gb 0.059, logreg 0.102, rf 0.123. The NN rate was 0.75 to 0.88 for ST (chance 0.03 to 0.07) and 0.98 to 0.99 for fastbaps (chance 0.06 to 0.08).
- **Dataset 4:** by grouping, ST 0.126 and fastbaps 0.276. By model, gb 0.144, rf 0.151, logreg 0.260. The NN rate was 0.93 to 0.96 for ST and 0.97 to 0.99 for fastbaps.
- **NN rate vs optimism:** in the cells we ran, the NN rate was high almost everywhere, and its rank correlation with optimism was weak (Spearman 0.28, p = 0.13 for E. coli; 0.22, p = 0.23 for Salmonella). Treat it as a **risk signal** that groups are identifiable, not as a predictor of how large the optimism will be.
- **Salmonella gap:** the authors' own published S. enterica pairs have a median optimism of 0.063, well below our 0.171. The two designs differ (their clade splits vs our GroupKFold on ST or fastbaps groups), but we have **not** explained the gap. It is flagged in the paper and `HANDOVER.md`.

### 4.3 Secondary analysis of the authors' published results
Re-analysing 218 published random-vs-group pairs from Yu, Wheeler & Barquist (2025): 210 positive; median 0.090 (mean 0.122; range −0.024 to 0.436). By species: E. coli 0.134, K. pneumoniae 0.123, S. enterica 0.063, S. pneumoniae 0.030, S. aureus 0.014. This comes from their published tables and is not our own audit. The numbers still need checking against their Fig 2B.

### 4.4 What the evidence says
The size of the problem **depends on the data and on how identifiable the groups are**: near zero in the soil data, modest in the small E. coli resistome table, and large in whole-genome gene content. It can be checked before reporting.

## 5. Install and use
```bash
pip install -e . pytest && python -m pytest -q          # 7 tests, ~90 s
splitaudit simulate --repeats 3                          # synthetic sweep
splitaudit simulate --fingerprint-sd 0 1.5 --models logreg rf gb
splitaudit audit --csv data.csv --label y --group site --repeats 10   # your data
```
`audit` uses all numeric columns except the label and group as features unless `--features` is given, and `--metric auc|bacc`. Declare the groups before looking at results. Labels must be binary.

## 6. Reproducing the paper's numbers
Run from the repository root. Raw data are **not** in the repository (see section 8).

| What | Command |
|---|---|
| Multi-dataset simulation | `python scripts/multiseed.py` |
| Sensitivity (groups, rows per group) | `python scripts/sensitivity.py` |
| NN diagnostic | `python scripts/nn_diagnostic.py` |
| Permutation null | `python scripts/permutation_null.py <outdir>` (outdir must exist) |
| E. coli resistome: prepare and audit | `python scripts/prepare_ecoli.py`, then `splitaudit audit --csv data/ecoli_resistome/ecoli_ctxm_prepared.csv --label y --group st --repeats 10` (also `phylogroup`, `country`); robustness: `python scripts/real_ecoli_robustness.py` |
| Soil audit | `python scripts/real_soil_audit.py data/scottish_soil/N019776_Scotland_soil_survey_antibiotic_resistance_genes.csv docs` |
| Yu E. coli: prepare | `python scripts/prepare_yu_ecoli.py <gene_presence_absence.Rtab.gz> <metadata> <out_dir> 0.20` (keeps genes at 20 to 80% prevalence) |
| Yu audits (E. coli and Salmonella) | `python scripts/real_yu_audit.py <genes.npz> <metadata.tsv> <out_csv> <repeats> [min_n=1000]` (long: hours on 2 CPU cores) |
| Yu published-results analysis | `python scripts/yu_published_optimism.py` |
| NN vs optimism | `python scripts/nn_vs_optimism.py` |
| Figures 1 to 6 | `make_fig1.py` to `make_fig6.py` in `scripts/` (some take an output folder) |

Exact commands, seeds and run times are in `EXPERIMENT_LOG.md`. The numbers in the manuscript are cross-checked against saved files in `paper/NUMBER_CHECK.md`.

## 7. Repository map
```
SplitAudit/
├── README.md                this file
├── HANDOVER.md              state of the work, open points, for the supervisor
├── EXPERIMENT_LOG.md        every run, with dates and corrections
├── PAPER_ROADMAP.md, ROADMAP.md   plans
├── CITATION.cff, pyproject.toml
├── src/splitaudit/          audit.py (core), synthetic.py, cli.py
├── tests/                   test_splitaudit.py
├── scripts/                 experiments, data preparation, figures
├── docs/                    result CSVs, figures (fig1..fig6), DATASETS.md,
│                            LITERATURE_NOTES.md, review_coding_sheet.csv
├── paper/                   MANUSCRIPT_DRAFT.md (central), section drafts,
│                            NUMBER_CHECK.md, references.md,
│                            reporting_checklist.md
├── literature/              PDFs (git-ignored)
├── results/                 CLI output
└── data/                    raw data (git-ignored); see data/README.md
```

## 8. Data and licences
- **E. coli resistome:** Mendeley Data, doi 10.17632/r5ccbmsnhw.1, CC BY 4.0.
- **Scottish soil ARG survey:** Knapp et al. 2019, NERC EIDC, doi 10.5285/d3498e93-4ac5-4eab-bc1a-eb2328771d24, OGL-UK-3.0 (attribution: "Contains data supplied by UK Centre for Ecology & Hydrology").
- **Yu, Wheeler & Barquist 2025** (five species; gene presence/absence, MLST/ST, fastbaps clusters): Mendeley Data, doi 10.17632/zs2mbjv7dn.3, CC BY 4.0; code BarquistLab/AMR_prediction (MIT); Zenodo doi 10.5281/zenodo.17398581.
- **Code licence: not yet chosen.** A `LICENSE` file must be added before release.

Large files (gene matrices, archives, PDFs) are git-ignored (`*.gz`, `*.tar.gz`, `*.pdf`, `data/`). `data/README.md` documents file names and layout.

## 9. Progress
About **78%** toward a postable preprint. This estimates the work that can be done without outside input. It is not a measure of quality.

| Area | Done | Status |
|---|---|---|
| Method, code, tests | ~95% | 7 tests pass on a clean install |
| Simulation study | ~95% | 8-dataset intervals, sensitivity, permutation null |
| Real-data audits | ~90% | 4 datasets and the secondary analysis; K. pneumoniae optional and not done |
| Figures | 100% | 6 of 6 (captions of Fig 2 and 3 still to be checked) |
| Manuscript draft | ~85% | all sections written; not edited or reviewed by anyone else |
| Number and claim checking | ~80% | `NUMBER_CHECK.md`; Section 5.5 still to compare with the authors' figure |
| Literature review | ~60% | 6 papers coded; L04 and L05 unread; no second coder; risk ratings blank |
| Release | ~20% | no licence, authors, venue, tag or DOI |

## 10. Limitations and what we do not claim
- **Binary labels only.** Groups must be known and are treated as given. Nested or overlapping groups (for example ST inside phylogroup) need care.
- **Optimism measures sensitivity to the split.** It does not measure model correctness. A group split is not automatically "right"; it answers a different question.
- **Intervals cover split repeats of one dataset.** They understate uncertainty across datasets.
- **Default, untuned models.** The feature filter on the Yu data was tightened after one pilot cell (E. coli), and this is disclosed.
- **Soil study:** 199 samples, no environmental covariates; spatial blocks were k-means clusters of arbitrary size.
- **No temporal blocking.**
- **Literature:** the review is a small case sample, not a survey. Some statements about other papers rest on abstracts or fetch summaries and need checking against the PDFs. We make no claim about how common the issue is in the literature, and we do not claim that environmental studies are generally leaky.

## 11. Open items
1. Explain or confirm the Salmonella gap against the authors' published 0.063.
2. Domain-expert read of the manuscript; compare Section 5.5 with the authors' Fig 2B.
3. Read L04 and L05, add a second coder, fill the risk ratings.
4. Decide authors, affiliations and venue; choose a code licence.
5. Optional: audit K. pneumoniae; run all long scripts from a clean checkout.
6. Tag a release (v0.2.0) and mint a Zenodo DOI; then post a preprint.

Details: `HANDOVER.md`, `PAPER_ROADMAP.md`.

## 12. Lessons and honesty notes
- A first E. coli run was invalid: genes appeared under two naming schemes, so the label leaked into the features (AUC ≈ 0.99). Check the most predictive feature before trusting any real-data audit.
- A claim that the soil NN rate was "far above chance" was wrong (chance was 0.113 for 10 blocks). It was corrected everywhere and logged.
- Single-dataset intervals understate uncertainty; use several datasets where possible.
- Group-split AUC can fall below 0.5 on individual simulated datasets (not on average at the settings we ran).
- The NN rate is a risk signal. It does not predict the size of the optimism.

## 13. Citing and AI assistance
Citation metadata are in `CITATION.cff` (authors and DOI to be completed). This project was developed with the help of an AI assistant (Claude, Anthropic), which drafted code, analyses and text. The human author is responsible for the content and must verify results and references before any submission, and disclose the assistance as the venue requires.
