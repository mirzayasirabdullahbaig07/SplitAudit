# Section 5 (DRAFT): Real-data case study 1 — E. coli resistome

Status: draft. Numbers come from `docs/real_ecoli_ctxm_audit.csv` (10 repeats; logreg, rf) and `docs/real_ecoli_robustness.csv` (5 repeats; logreg, rf, gb; AUC and balanced accuracy; two labels). Soil case study (5.2) is pending data. [CITE] = citation still needed.

## 5.1 Clinical AMR: E. coli genomes

**Data.** 738 E. coli genomes with presence/absence of acquired resistance genes, metadata for sequence type (ST, 218 groups), phylogroup (10) and country (56). Source and licence: see `data/README.md` [licence to be recorded; CITE].

**Task.** Predict carriage of a CTX-M gene (ESBL marker; positive rate 0.378) from the other resistance genes (326 features). All columns naming CTX-M were removed under both naming schemes in the table; a first attempt that removed only one scheme leaked the label (AUC ~0.99) and is logged as invalid.

**Protocol.** Random, stratified and group 5-fold CV, grouped by ST, phylogroup or country; optimism = random AUC − group AUC; bootstrap interval over split repeats.

**Main result (logreg / rf, 10 repeats).**

| Group | Optimism logreg | Optimism rf | Group-split AUC (logreg / rf) | Same-group NN rate (chance) |
|---|---|---|---|---|
| ST | 0.050 | 0.025 | 0.782 / 0.873 | 0.270 (0.025) |
| Phylogroup | 0.050 | 0.044 | 0.781 / 0.854 | 0.514 (0.201) |
| Country | 0.064 | 0.069 | 0.767 / 0.829 | 0.316 (0.113) |

**Robustness (5 repeats; 3 models × 2 metrics × 3 groupings × 2 labels = 36 cells).** Optimism was positive in all 36 cells and every split-repeat interval excluded zero. Median optimism was 0.050 for CTX-M and 0.026 for a second label, tet(A) carriage (range 0.013–0.084 overall). By grouping the medians were 0.029 (ST), 0.042 (phylogroup), 0.048 (country); by metric 0.030 (AUC) and 0.038 (balanced accuracy); by model 0.049 (logreg), 0.034 (rf), 0.031 (gb).

**Reading.** Random splits overstated performance by roughly 0.01–0.08 AUC/bacc on this dataset, with the largest gaps for country grouping and for CTX-M. The effect is modest, not dramatic: group-split performance remains good (AUC 0.77–0.94). Same-group NN rates far above chance confirm that genomes are identifiable by group, the condition under which our simulation predicts optimism.

## 5.2 Limitations to state in the paper
- Intervals reflect split repeats on one dataset only; they do not capture sampling variability across datasets.
- Groups are nested/overlapping (ST within phylogroup), and country is partly confounded with sampling effort; results are per grouping, not additive.
- Genes may be physically linked (plasmids), so some predictability is biological, not leakage; the audit measures optimism from random splitting, not whether the model is "right for the right reason".
- No tuning of hyperparameters; default settings only.
- Only two labels; the tet(A) label removed both naming schemes by substring match.

## 5.3 Soil case study (PENDING)
Scottish soil AMR gene dataset (183 locations). The data table has not been obtained: the downloaded package contains only documentation. To do once the CSV is placed in `data/scottish_soil/`. Note: it has no obvious binary label; a defensible label and grouping (e.g. land-use or region) must be fixed before any audit is run.
