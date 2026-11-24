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

## 5.3 Environmental AMR: Scottish soil survey

**Data.** Knapp et al. (2019), NERC EIDC, doi 10.5285/d3498e93-4ac5-4eab-bc1a-eb2328771d24, licence OGL-UK-3.0: relative abundance of ~300 resistance genes in soil from the National Soils Inventory of Scotland. The table has 200 rows (177 distinct site names), coordinates and gene abundances only; there are no soil-property or land-use columns. One row with latitude -2.00 (impossible for Scotland) was dropped, leaving 199.

**Task and design (fixed before running).** Predict detection of a gene from detection of all other genes (298 binary features). The five labels are the genes whose detection prevalence is closest to 0.5 (mexA, cmlA1_01, oprJ, vgb_01, tnpA_01), one per gene stem; same-stem columns were removed from features. Groupings: site name (176 groups after cleaning), and spatial k-means blocks on longitude/latitude with k=10 and k=20. Logreg, rf, gb; AUC; 5 repeats.

**Result (45 cells).** Optimism was positive in 31 cells but its interval excluded zero in only 13. Median optimism was 0.002 (site name), 0.002 (10 blocks) and 0.012 (20 blocks); by model 0.002 (gb), 0.004 (logreg), 0.010 (rf). The largest was 0.056 (tnpA_01, random forest, 10 blocks). Random-split AUCs ranged 0.57-0.94. Same-group nearest-neighbour rates under random splits were about 0.01 for site name (chance 0.007), 0.06-0.08 for 20 blocks (chance 0.054) and 0.18-0.21 for 10 blocks (chance 0.113): groups were only weakly to modestly identifiable, with an excess over chance of at most about 0.10 (Fig 6).

**Reading.** In contrast to the E. coli data and the simulation, random splits overstated performance only slightly and inconsistently here. Spatial blocking gave small positive optimism for some labels/models and none for others, and replicate site names gave essentially none. A plausible reason is that these gene-detection features carry little spatial fingerprint, which our simulation predicts yields little optimism, but this explanation is untested here. We report this as a null-leaning result, not as evidence that soil ARG studies are safe: the 20 km-grid design and the choice of features and labels are specific to this dataset.

**Limitations.** Labels are gene detections, not a real prediction task from environmental covariates (none are in the table); k-means blocks are arbitrary and block count changes the result; same-operon genes (e.g. mexA/mexE) were not removed; intervals are over split repeats only.
