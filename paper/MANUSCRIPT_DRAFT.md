# SplitAudit: auditing how much random splits overstate performance on grouped data (MANUSCRIPT DRAFT v0)

Assembled 2026-11-25 from the section drafts in `paper/`. Not ready for submission: see "Open items" at the end. Authors, affiliations and acknowledgements to be added.

## Abstract (≈200 words)

Machine-learning studies of antimicrobial resistance (AMR) often evaluate models with random train/test splits, even when samples are grouped by lineage, site or space. When groups are identifiable from the features, random splits can overstate how well a model will perform on new groups. We present SplitAudit, an open-source tool that compares random, stratified and group-held-out splits on identical data and models, and reports an optimism score (random minus group performance), a model-free same-group nearest-neighbour leakage diagnostic, and a within-group permutation null. In simulations with known ground truth, optimism was near zero when groups could not be identified from features and rose to 0.13-0.24 AUC when they could, depending on the model. On 738 E. coli genomes, random splits overstated AUC by 0.013-0.084 across 36 model, metric, grouping and label combinations, and every interval excluded zero. On a Scottish soil resistance-gene survey the effect was small and inconsistent (median 0.002-0.012; interval excluded zero in 13 of 45 combinations). The size of the problem therefore depends on how identifiable groups are, and can be checked before reporting. We propose a short reporting checklist and release code, data preparation scripts and logs.

## 1. Introduction (outline with draft text)

**Para 1 — the problem.** Predicting resistance from genomic or environmental data is now routine, and results are often summarised by a single cross-validated score. In grouped data (isolates from the same lineage, samples from the same site) a random split puts near-relatives on both sides, so the score may reflect group recognition instead of generalisation to new groups.

**Para 2 — what is known.** The issue is established in genomic AMR, where genome-distance-aware, phylogeny-aware and homology-aware validation lower scores [Lüftinger 2021; Hu 2024; Yu, Wheeler & Barquist 2025 — CITE after verification], and in spatial ecology, where random cross-validation overestimated AUC by up to 0.16 in species distribution models [Koldasbayeva & Zaytsev 2025; Meyer et al. — CITE].

**Para 3 — the gap (edit with collaborators).** In the environmental-AMR papers we examined (small sample, see 2.2), the split type and the handling of near-identical samples were often not stated, and we found no reusable tool that quantifies the inflation on a given dataset. We do not claim that environmental studies are generally leaky; we provide a way to measure it.

**Para 4 — contributions.** (i) SplitAudit: the audit protocol and tool. (ii) Simulations separating label leakage from covariate leakage, showing optimism requires groups to be identifiable from features. (iii) Two real-data case studies with contrasting outcomes. (iv) A reporting checklist.

**Para 5 — what we do not claim.** Optimism measures sensitivity of the score to the split, not model correctness; intervals reflect split repeats on one dataset.

## 2. Related work (to expand)

### 2.1 Validation in genomic AMR
Lüftinger 2021; Hu 2024; Yu, Wheeler & Barquist 2025; PLOS Comput Biol 2024 tutorial. *Source: abstracts/snippets only in LITERATURE_NOTES.md.*

### 2.2 Environmental AMR machine learning (small coded sample)
Coded so far (`docs/review_coding_sheet.csv`):
- L02 KeshikNevisRazavi 2026: feature filter applied before the split; split type and train/test homology not stated; RF accuracy 0.988 on 200 sequences (full text via fetch summary; re-verify).
- L03 Danko 2021: single 60/40 split; city is the target; external mystery set scored lower in some regions (full text via fetch summary; re-verify).
- L05 Kenzi et al., Sci Total Environ: 10-fold CV, split type unstated (abstract only).
- L01 Zheng 2022 and L04: not yet read.
Five papers is a case sample, not a survey. A systematic review is needed before any statement about how common the issue is; your collaborators' review may supply it.

### 2.3 Spatial and ecological validation
Koldasbayeva & Zaytsev 2025; Meyer et al.; spatial CV assessments [CITE].


## 3. Audit method

**Setting.** We have rows with a binary label, numeric features and a known group identifier (site, taxon, patient, study, biome, ...). The question is how much the validation scheme changes the reported score of an otherwise identical model.

**3.1 Validation schemes.** SplitAudit evaluates the same data and the same models under three five-fold schemes:
- *random*: shuffled K-fold that ignores groups, the common default;
- *stratified*: stratified K-fold on the label, still ignoring groups;
- *group*: GroupKFold, in which no group appears in both the training and test folds. The order of groups is shuffled for each repeat so that repeats differ.
The only thing that differs between schemes is how rows are assigned to folds; features, labels, models and metric are identical.

**3.2 Optimism.** For each repeat we compute the mean test score under each scheme and define optimism as score(random) − score(group). A positive value means the random split overstates how well the model would do on unseen groups. We report the mean over repeats with a bootstrap confidence interval (2,000 resamples over repeats). The default metric is AUC; balanced accuracy is available.

**3.3 Leakage diagnostic (model-free).** For every test row we find its nearest training row in standardised feature space and record whether the two rows belong to the same group. The share of test rows whose nearest neighbour is from their own group is the *same-group nearest-neighbour rate*. It is 0 under a clean group split by construction. Under a random split it measures how identifiable groups are from the features, independently of any model.

**3.4 Permutation null (sanity check).** Labels are permuted within each group, which destroys the feature–label relationship while preserving group sizes and base rates. The group-split score should then be at chance (AUC ≈ 0.5), and a score clearly above chance would indicate a bug. We ran 10 permutations for each of 3 models on 32 simulated datasets (rho 0 or 1, fingerprint SD 0 or 1.5, 8 seeds; 96 cases). The mean over all cases was 0.501, and no case was consistently above chance. Per-case means ranged from 0.365 to 0.556; 91 of 96 lay within 0.45-0.55, and all 5 exceptions occurred at rho = 1 and fingerprint SD 1.5 (logistic regression 0.365, 0.434, 0.551; random forest 0.444, 0.556). This is the setting in which group-level label propensities are strongest and only 40 groups are available, so deviations in either direction are expected from sampling noise in group base rates (HYPOTHESIS: not separately tested); the check is therefore a bug detector for large positive departures, not a test that each dataset sits exactly at 0.5.

**3.5 Models.** Logistic regression (standardised features), random forest (150 trees, fully grown), and histogram gradient boosting (150 iterations, learning rate 0.1), representing low-capacity and memorisation-prone learners. Hyperparameters are fixed and not tuned, so that differences come from the split and not from tuning.


## 4. Synthetic validation

**4.1 Simulator.** Data are generated with known ground truth. There are G groups with n rows each and 12 features. Each group g has a latent label propensity a_g ~ N(0,1) and a feature offset ("fingerprint") f_g ~ N(0, s²·I), where s is the fingerprint SD. A row's features are x = z + f_g with z ~ N(0, I). The label is Bernoulli with logit (1 − ρ)·(z·w) + ρ·2·a_g, where w is a fixed unit vector. Two parameters control leakage separately:
- ρ ∈ [0,1], **label leakage**: the share of the label that depends on the group rather than on the within-group signal z·w;
- s, **covariate leakage**: how strongly groups can be recognised from the features.
Defaults are G = 40 and n = 25 (1,000 rows). ρ = 0 and s = 0 is the true no-leakage control.

**4.2 Design.** For each combination of ρ ∈ {0, 0.5, 1}, s ∈ {0, 0.5, 1.5} and model, we generated 8 independent datasets (data seeds 1–8) and ran the audit with 2 repeats of five-fold validation. We report the mean optimism across datasets with a 95% t-interval across datasets, so the intervals reflect variation between datasets and not only between splits. (Fig 2.)

**4.3 No leakage, no optimism.** With s = 0, mean optimism is between −0.003 and −0.002 for every model at ρ = 0, and intervals include zero at ρ = 1 (for example, logistic regression −0.003, 95% CI −0.020 to 0.014). Label leakage alone does not inflate scores when groups cannot be identified from the features.

**4.4 Optimism needs identifiable groups.** At ρ = 1, optimism grows with s. With s = 0.5, logistic regression, random forest and gradient boosting show 0.063 (0.039–0.087), 0.056 (0.036–0.076) and 0.043 (0.022–0.063). With s = 1.5 the values are 0.135 (0.103–0.168), 0.240 (0.206–0.274) and 0.219 (0.188–0.251). At s = 1.5 the two flexible models are inflated more than logistic regression; at s = 0.5 the three models are statistically close, so we make no ranking claim there.

**4.5 Covariate leakage alone.** At ρ = 0 and s = 1.5, optimism is small but positive for the tree-based models: random forest 0.015 (0.006–0.024) and gradient boosting 0.016 (0.001–0.030); for logistic regression it is 0.002 (−0.004 to 0.009). A plausible mechanism is that a flexible model can memorise each group's offset under a random split and use it to recover the within-group signal; the offset is unknown for held-out groups. We tested this by removing the offsets (s = 0), which removes the effect. [This explanation is supported by the s = 0 control but not tested further, e.g. with an offset-removal preprocessing step.]

**4.6 Leakage diagnostic.** The same-group nearest-neighbour rate tracks identifiability: across 8 datasets it was 0.022 at s = 0, 0.100 at s = 0.5 and 0.845 at s = 1.5 under random splits (chance 1/40 = 0.025), and exactly 0 under group splits.

**4.7 Sensitivity to group structure.** Holding ρ = 1 and s = 1.5, we varied the number of groups (10, 20, 40, 80) and rows per group (10, 25, 50), with 8 datasets per cell (Fig 3). Averaged over group sizes, logistic regression optimism falls from 0.233 at 10 groups to 0.100 at 80 (paired t-test p = 0.003), whereas random forest optimism stays between 0.22 and 0.27 (10 vs 80 groups, p = 0.12). For random forest, optimism rises with rows per group (0.209 at 10 rows, 0.262 at 50; p = 0.012); for logistic regression the trend is weaker (0.138 to 0.166; p = 0.097). These tests are exploratory and uncorrected for multiple comparisons. Optimism stayed between 0.09 and 0.30 in every cell, so the effect is not specific to one configuration.

**4.8 A known artefact.** At high ρ, the group-split AUC of some models falls below 0.5 on individual datasets, though not on average (at ρ = 1, s = 1.5 the mean group-split AUC over 8 datasets was 0.497 for logistic regression, 0.507 for random forest and 0.510 for gradient boosting, with individual datasets as low as 0.379 for logistic regression). Group effects do not transfer to new groups, so a model that learned them can perform worse than chance on held-out groups. When it does, measured optimism is larger than it would be against a model that merely guessed; because this occurs in some datasets and not others, we report it here rather than hide it.

**4.9 Limitations of the synthetic study.** A single generative model; binary labels; AUC as the main metric; 12 features; untuned models; and interval estimates based on 8 datasets. The simulation shows that the audit behaves correctly when the truth is known. It does not show how large optimism is in real data, which is the subject of Section 5.



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

## 5.2 Environmental AMR: Scottish soil survey

**Data.** Knapp et al. (2019), NERC EIDC, doi 10.5285/d3498e93-4ac5-4eab-bc1a-eb2328771d24, licence OGL-UK-3.0: relative abundance of ~300 resistance genes in soil from the National Soils Inventory of Scotland. The table has 200 rows (177 distinct site names), coordinates and gene abundances only; there are no soil-property or land-use columns. One row with latitude -2.00 (impossible for Scotland) was dropped, leaving 199.

**Task and design (fixed before running).** Predict detection of a gene from detection of all other genes (298 binary features). The five labels are the genes whose detection prevalence is closest to 0.5 (mexA, cmlA1_01, oprJ, vgb_01, tnpA_01), one per gene stem; same-stem columns were removed from features. Groupings: site name (176 groups after cleaning), and spatial k-means blocks on longitude/latitude with k=10 and k=20. Logreg, rf, gb; AUC; 5 repeats.

**Result (45 cells).** Optimism was positive in 31 cells but its interval excluded zero in only 13. Median optimism was 0.002 (site name), 0.002 (10 blocks) and 0.012 (20 blocks); by model 0.002 (gb), 0.004 (logreg), 0.010 (rf). The largest was 0.056 (tnpA_01, random forest, 10 blocks). Random-split AUCs ranged 0.57-0.94. Same-group nearest-neighbour rates were about 0.01 for site name, 0.06-0.08 for 20 blocks and 0.18-0.21 for 10 blocks.

**Reading.** In contrast to the E. coli data and the simulation, random splits overstated performance only slightly and inconsistently here. Spatial blocking gave small positive optimism for some labels/models and none for others, and replicate site names gave essentially none. A plausible reason is that these gene-detection features carry little spatial fingerprint, which our simulation predicts yields little optimism, but this explanation is untested here. We report this as a null-leaning result, not as evidence that soil ARG studies are safe: the 20 km-grid design and the choice of features and labels are specific to this dataset.

**Limitations.** Labels are gene detections, not a real prediction task from environmental covariates (none are in the table); k-means blocks are arbitrary and block count changes the result; same-operon genes (e.g. mexA/mexE) were not removed; intervals are over split repeats only.

## 5.3 Limitations specific to the case studies
- Intervals reflect split repeats on one dataset only; they do not capture sampling variability across datasets.
- Groups are nested/overlapping (ST within phylogroup), and country is partly confounded with sampling effort; results are per grouping, not additive.
- Genes may be physically linked (plasmids), so some predictability is biological, not leakage; the audit measures optimism from random splitting, not whether the model is "right for the right reason".
- No tuning of hyperparameters; default settings only.
- Only two labels; the tet(A) label removed both naming schemes by substring match.


## 6. Discussion

**6.1 What the evidence supports.** Across three settings the size of the random-split inflation tracked how identifiable the groups were from the features. In simulation, optimism was about zero when groups could not be recognised from features (fingerprint 0, optimism about -0.003 for all models, 8 datasets) and rose to 0.135 (logistic regression), 0.240 (random forest) and 0.219 (gradient boosting) with strong group fingerprints. In 738 E. coli genomes, random splits overstated AUC in all 36 model, metric, grouping and label combinations, by 0.013 to 0.084, and same-group nearest-neighbour rates sat far above chance (for example 0.27 against 0.025 for sequence type). In the Scottish soil survey the effect was small and inconsistent (median 0.002 to 0.012; the interval excluded zero in 13 of 45 combinations).

**6.2 Why the soil result differs (HYPOTHESIS).** One reading is that gene-detection patterns in this survey carry little group-specific signal relative to the label, so recognising the group helps little. We did not test this. Other readings are equally open: the labels (detection of one gene from the others) may be dominated by within-sample co-occurrence rather than site identity; the 20 km sampling grid may leave neighbouring sites too far apart for spatial autocorrelation to matter at these block sizes; and 199 samples give wide intervals. The nearest-neighbour rate alone does not separate these: with 10 blocks it was 0.18 to 0.21, far above chance, yet optimism stayed small. A high rate indicates risk, not a guaranteed inflation.

**6.3 What the audit is for.** The audit does not say whether a model is good. It says how much the reported score depends on the split. A paper reporting only a random-split score on grouped data leaves that dependence unknown; SplitAudit makes it a number the authors and readers can see, and the reporting checklist lists what to state.

**6.4 What we saw in the literature, and its limit.** In the small coded sample, split type and handling of near-duplicate samples were often not stated, and one paper filtered features on the full dataset before splitting. This is five papers, two read in full; it shows that such gaps occur, not how often. We make no claim about the field's prevalence of leakage.

**6.5 Practical guidance (modest).** (i) Declare the groups. (ii) Report random and group-held-out scores on the same data and model. (iii) Report an identifiability diagnostic with its chance level. (iv) Check for features that duplicate the label. Items (i), (ii) and (iv) are cheap; our own first E. coli run showed the last matters: duplicate gene naming schemes leaked the label (AUC about 0.99) until we removed both.

## 7. Limitations

1. **Two real datasets, one organism family and one survey.** Results may not transfer to other organisms, labels or sampling designs.
2. **Uncertainty is understated.** Real-data intervals reflect repeated splits of one dataset, not sampling variability across datasets. Multi-dataset intervals in simulation were wider.
3. **Optimism is not correctness.** Linked genes (plasmids, operons, clonal lineages) can make part of the predictability genuine, not leakage. Also, groupings here are nested or overlapping (sequence type within phylogroup; country partly confounded with sampling effort), so a held-out group may still resemble training groups, and results are per grouping, not additive.
4. **Soil analysis design.** Labels were gene detections chosen by a mechanical rule (prevalence nearest 0.5), not an applied prediction task; the table had no environmental covariates; spatial blocks came from k-means and the block count changed the result; same-operon genes were not removed; one row with an impossible latitude was dropped.
5. **Default models.** No hyperparameter tuning; three model families only.
6. **Literature evidence is thin.** Two papers read in full (from fetch summaries, to be re-verified against the PDFs), one abstract-only, two unread; one coder, no agreement estimate.
7. **Simulation is built to leak.** Simulated optimism (up to 0.24) is a designed effect and should not be read as an estimate for real data (real-data maximum 0.084).
8. **Checklist untested.** It has been applied to two fully assessed papers only, by the authors.

## 8. Conclusion (draft)

Random cross-validation can overstate performance on grouped data, but how much depends on whether the groups are identifiable from the features. SplitAudit measures this directly with an optimism score, a model-free identifiability diagnostic and a permutation null. In simulation the effect is large when groups leave a recognisable signature and absent when they do not; in E. coli genomes it was consistently positive and modest (0.013 to 0.084 AUC); in a Scottish soil survey it was small and inconsistent. We therefore recommend not a blanket rule but a routine check, reported with the groups declared and the interval's meaning stated. Next steps are validation on more datasets, a systematic review of how environmental AMR studies split their data, and testing the checklist with independent coders.


## Figures (captions are DRAFT; check each against the image in docs/)
- **Fig 1** (`docs/fig1_split_schematic.png`). Schematic with simulated toy points (not study data): under a random split, rows of the same group fall in both training and test sets, so a test row's nearest training row is often a groupmate; under a group split, whole groups are held out and that rate is zero by construction.
- **Fig 2** (`docs/fig2_optimism_vs_rho.png`). Simulated optimism (random minus group AUC) by label-leakage rho and model, for each fingerprint SD; points are means over 8 datasets with t-intervals across datasets.
- **Fig 3** (`docs/fig3_sensitivity.png`). Sensitivity of simulated optimism to the number of groups and rows per group (rho = 1, fingerprint SD = 1.5; 8 datasets per cell).
- **Fig 4** (`docs/fig4_real_data_optimism.png`). Optimism for each model in (A) 738 E. coli genomes, 18 AUC cells, and (B) the Scottish soil survey, 45 AUC cells; dot = mean, line = split-repeat interval (understates uncertainty across datasets).
- **Fig 5** (`docs/fig5_audit_flow.png`). The SplitAudit procedure: hygiene checks, three splits, optimism, two diagnostics, and how to read them together.

## Appendix A. Reporting checklist (draft)
## A. Data structure
1. **Groups.** What natural groups exist in the data (lineage/sequence type, site, study, country, spatial block, replicate)? List them and the number of groups. *(E. coli: optimism differed by grouping, 0.029 ST to 0.048 country median.)*
2. **Near-duplicates.** Were clonal, replicate or near-identical samples identified or removed? How? *(observed: not addressed in L02.)*
3. **Intended use.** Will the model be applied to new groups (new sites, new lineages)? The split should mirror that.

## B. Splitting
4. **Split scheme.** State exactly how train/test or folds were made: random, stratified, or grouped by which variable. *(observed: not stated in L02, L03, L05 abstract.)*
5. **Both numbers.** Report the score under a random split and under a group-held-out split on the same data and model, plus their difference (optimism).
6. **Spatial blocks.** If groups are spatial, state block size or method; results can change with block count. *(soil: median optimism 0.002 with 10 blocks vs 0.012 with 20.)*

## C. Leakage hygiene
7. **Preprocessing inside folds.** Feature selection, filtering, scaling and imputation were fitted on training data only. *(observed: L02 filtered features on the full dataset before splitting.)*
8. **Tuning.** Hyperparameters tuned without using the test fold (nested CV or a separate validation set). *(observed: L03 did not describe a separate tuning set.)*
9. **Label construction.** Confirm no feature encodes the label under another name. *(E. coli: duplicate gene naming schemes leaked the label, AUC ~0.99; found by inspecting the top feature.)*
10. **Sample selection tied to the label.** Were negatives or samples chosen using properties that differ by label? *(observed: L02 negatives selected on feature differences.)*

## D. Diagnostics
11. **Identifiability.** Report the same-group nearest-neighbour rate under a random split with its chance level. A rate far above chance means groups are recognisable. *(E. coli ST: 0.27 vs 0.025.)* Note: in soil, high-ish rates with 10 blocks (0.18-0.21) still gave small optimism, so a high rate signals risk, not certainty.
12. **Permutation null.** Within-group label permutation under group splits should give AUC near 0.5.
13. **External set.** If an external or held-out-group set exists, report it next to the internal score. *(L03: external scores lower for some regions.)*

## E. Reporting uncertainty
14. **Intervals.** Say what the interval covers. Repeats of one dataset's splits understate uncertainty; across-dataset variation is wider. *(synthetic: 8-seed intervals wider than single-dataset ones.)*
15. **Metric.** Report a threshold-free metric and one threshold-based metric; optimism can differ between them. *(E. coli: AUC median 0.030, balanced accuracy 0.038.)*

## How to use / limits
- Optimism measures sensitivity to the split, not whether the model is right for the right reasons; linked genes (plasmids, operons) can make prediction partly genuine.
- No threshold of optimism is "acceptable"; report the number and context.
- Not yet tested: whether authors find the checklist usable. Pilot it on 3-5 papers before claiming it helps.

## Open items before submission
1. Re-verify literature-derived statements (Sections 1, 2, 5, 6, checklist pilot) against the PDFs; read L01, L04, L05 in full.
2. Replace [CITE] markers with keys from `paper/references.md`; verify the unverified entries listed there; decide on the Meyer et al. 2019 citation.
3. Check figure captions against the images; confirm Fig 2/3 captions.
4. Record the E. coli dataset licence (`data/README.md`) and cite its source.
5. Decide on a third real dataset and a second coder for the literature/checklist pilot.
6. Data/code availability statement and Zenodo release.

## References
VERIFIED against Crossref / arXiv / PMC pages this session (title, authors, venue, year):
- [Lueftinger2021] Lüftinger L, Májek P, Beisken S, Rattei T, Posch AE. Learning from limited data: towards best practice techniques for antimicrobial resistance prediction from whole genome sequencing data. Front Cell Infect Microbiol 2021;11:610348. doi:10.3389/fcimb.2021.610348
- [Hu2024] Hu K, Meyer F, Deng ZL, Asgari E, Kuo TH, Münch PC, McHardy AC. Assessing computational predictions of antimicrobial resistance phenotypes from microbial genomes. Brief Bioinform 2024;25:bbae206. doi:10.1093/bib/bbae206 (author initials not checked)
- [Orcales2024] Orcales F, Moctezuma Tan, Johnson-Hagler, Suntay, Ali, Recto, Glenn, Pennings. Using genomic data and machine learning to predict antibiotic resistance: a tutorial paper. PLOS Comput Biol 2024;20(12):e1012579. doi:10.1371/journal.pcbi.1012579 (initials not checked)
- [Yu2025] Yu Y, Wheeler NE, Barquist L. Biased sampling driven by bacterial population structure confounds machine learning prediction of antimicrobial resistance. PLOS Biology 2025 (published 2025-12-16). doi:10.1371/journal.pbio.3003539. NOTE: earlier notes cited the bioRxiv preprint (10.1101/2025.01.07.631773); cite the PLOS Biology version.
- [Koldasbayeva2025] Koldasbayeva D, Zaytsev A. Foundation for unbiased cross-validation of spatio-temporal models for species distribution modeling. arXiv:2502.03480 (submitted Jan 2025, revised Dec 2025). Reports random CV inflating AUC by up to 0.16.
- [Meyer2019] Meyer H, Reudenbach C, Wöllauer S, Nauss T. Importance of spatial predictor variable selection in machine learning applications: moving from data reproduction to spatial prediction. Ecol Model 2019;411:108815. doi:10.1016/j.ecolmodel.2019.108815. NOTE: our notes described arXiv 1908.07805 only as "spatial CV essential"; its title is about spatial predictor selection, so check the exact claim before citing it for random-CV optimism.

FROM THE DATASET FILE (ro-crate-metadata.json), not re-checked online:
- [Knapp2019] Knapp CW, Graham DW, Freitag T, Pagaling E, Hough R, Avery L, Zhu Y-G, Su J, Zhou XY. Antibiotic resistance genes found in soils across the entire Scottish landscape (2007-10). NERC EIDC, 2019. doi:10.5285/d3498e93-4ac5-4eab-bc1a-eb2328771d24. Licence OGL-UK-3.0.

FROM EARLIER SEARCHES / ABSTRACTS, still to verify:
- [Zheng2022] Zheng D, et al. Sci Adv 2022;8(46):eabq8015.
- [Danko2021] Danko D, Mason C, Vassilev D. Front Genet 2021;12:642991.
- [KeshikNevisRazavi2026] Int J Soil Water Res 2026 (volume/pages missing).
- [Kenzi] Kenzi M, et al. Sci Total Environ (PubMed 42224874; volume/pages/year missing).

NOT YET LOOKED UP:
- scikit-learn (Pedregosa et al. 2011, JMLR 12:2825) for GroupKFold and models.
- Roberts-style spatial CV assessment (arXiv 2303.07334): authors/title unchecked.
- E. coli dataset citation and licence (Mendeley doi 10.17632/r5ccbmsnhw.1).
- Wilhelm 2022; Aghdam & Solís-Lemus 2024.
