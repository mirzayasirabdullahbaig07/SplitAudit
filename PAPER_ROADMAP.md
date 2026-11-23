# Paper Roadmap — SplitAudit

Working title: **SplitAudit: Quantifying how much random validation splits overstate performance on grouped data, with a case study in antimicrobial-resistance ML**

Companion to `ROADMAP.md` (project/experiment plan). This file tracks the *paper*: claims, evidence needed, sections, figures, and submission.

## 1. Core claim (one sentence)
Random train/test splits on grouped data (site, taxon, patient, study) overstate performance by a measurable, predictable amount; a model-free diagnostic plus a group-held-out comparison lets authors quantify it, and a short checklist helps them report it.

## 2. Contributions (what we can honestly claim)
1. **Tool** — open-source audit (random vs stratified vs group splits, same-group nearest-neighbour rate, within-group label-permutation null, bootstrap CIs).
2. **Synthetic validation** — ground-truth study: optimism ≈ 0 at ρ=0 and grows monotonically with group-effect share ρ.
3. **Real-data case studies** — optimism estimates on 1–3 public grouped datasets (AMR/soil if available, otherwise other domains).
4. **Review meta-analysis** — leakage-risk rating vs reported score across papers from the joint AMR-in-soil review.
5. **Checklist** — ≤10-item leakage reporting checklist + "which split?" flowchart.

*Not new:* that leakage exists. Frame novelty as quantification, a reusable audit, and the soil/AMR application.

## 3. Evidence needed per section

| Section | Must contain | Source / status |
|---|---|---|
| 1 Introduction | Problem, gap statement (≤150 words), contributions list | Draft after Week 2 |
| 2 Background | Leakage in grouped data; phylogeny-/homology-aware evaluation (2024 Briefings in Bioinformatics; 2025 bioRxiv); AMR-ML context | Literature sheet (Week 1) |
| 3 Method | Split schemes, same-group NN diagnostic, permutation null, optimism definition, bootstrap CI | Code exists (`src/splitaudit/audit.py`) |
| 4 Synthetic validation | ρ sweep; n_groups × group_size × ρ grid; model capacity (logreg / RF / GB); below-0.5 AUC artefact explained | Partly done; needs full grid |
| 5 Real-data case studies | 1–3 datasets, 10+ repeats, balanced accuracy + AUC, cluster-based groups | **Blocked on dataset** |
| 6 Review meta-analysis | Coding sheet for all papers; Spearman (rating vs score) with CI | `docs/review_coding_sheet.csv` |
| 7 Checklist | ≤10 items + flowchart | Week 6 |
| 8 Limitations | Binary labels only; groups must be known; synthetic ≠ real; no spatial/temporal blocking | Already in README |

## 4. Figures and tables (target list)
- **Fig 1** Schematic: random vs group split and where leakage enters.
- **Fig 2** Optimism vs ρ (synthetic), per model, with CI bands.
- **Fig 3** Sensitivity heatmap: optimism over n_groups × group_size.
- **Fig 4** Real-data optimism: random vs group score per dataset (paired dots).
- **Fig 5** Review meta-analysis: leakage-risk rating vs reported score.
- **Fig 6** "Which split should I use?" flowchart.
- **Tab 1** Literature summary (paper | data | split | n groups | metric | score).
- **Tab 2** Datasets used (source, licence, n rows, n groups, label balance).
- **Tab 3** Reporting checklist.

## 5. Timeline (8 weeks; shift the start date to fit your other deadlines)

| Week | Paper milestone | Exit check |
|---|---|---|
| 1 | Literature sheet, gap statement, review coding for first 10 papers | Gap statement ≤150 words approved by collaborators |
| 2 | Datasets chosen and cleaned; first real `splitaudit audit` run | Go/no-go: usable group column exists? |
| 3 | Real-data experiments, 10+ repeats; start Method section | Fig 4 draft |
| 4 | Synthetic sensitivity grid + gradient boosting; write Sections 3–4 | Fig 2, Fig 3 final; go/no-go on optimism ≈ 0 |
| 5 | Finish review coding; Spearman analysis; write Section 6 | Fig 5 + Tab 1 final |
| 6 | Checklist + flowchart; write Sections 2, 5, 7 | Tab 3, Fig 6 |
| 7 | Full draft: Intro, Abstract, Limitations; internal read-through | Complete draft to supervisor |
| 8 | Revise, release code + Zenodo DOI, post arXiv preprint | Tagged `v1.0.0` release |

## 6. Go / no-go gates
- **End Week 2:** no public dataset with a usable group column → run on 2–3 non-soil grouped datasets and position the paper as a general tool + checklist; keep AMR as the review case study.
- **End Week 4:** optimism ≈ 0 on all real data → report it ("random splits were adequate here"); that is a legitimate finding.

## 7. Reproducibility checklist (needed before submission)
- [ ] Fixed seeds logged in `EXPERIMENT_LOG.md` for every reported number
- [ ] Every figure regenerates from one script/command
- [ ] Dataset versions and licences recorded
- [ ] `pytest` passes on a clean install
- [ ] Release tagged, Zenodo DOI minted, DOI cited in the paper

## 8. Target venues (verify scope and deadlines before choosing)
- Preprint first: arXiv (stat.ML / q-bio.QM) or bioRxiv.
- Journal/workshop options: bioinformatics-methods journals, ML-for-health or reproducibility workshops.

## 9. Immediate next actions
1. Push the repo to GitHub (see commands in chat).
2. Run `python -m pytest -q` and `splitaudit simulate --repeats 3`; save output to `EXPERIMENT_LOG.md`.
3. Start the Week 1 literature spreadsheet.
4. Ask review collaborators which datasets are public and have a site/sample/taxon column.
