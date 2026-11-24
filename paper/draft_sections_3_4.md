# DRAFT — Sections 3 and 4 (SplitAudit)

Status: first draft written from the code in `src/splitaudit/` and the results in `docs/`. Every number below comes from `docs/synthetic_multiseed_summary.csv` or `docs/synthetic_sensitivity_summary.csv`. Items in [brackets] need a citation or a decision from you. Nothing here is about real data yet.

---

## 3. Audit method

**Setting.** We have rows with a binary label, numeric features and a known group identifier (site, taxon, patient, study, biome, ...). The question is how much the validation scheme changes the reported score of an otherwise identical model.

**3.1 Validation schemes.** SplitAudit evaluates the same data and the same models under three five-fold schemes:
- *random*: shuffled K-fold that ignores groups, the common default;
- *stratified*: stratified K-fold on the label, still ignoring groups;
- *group*: GroupKFold, in which no group appears in both the training and test folds. The order of groups is shuffled for each repeat so that repeats differ.
The only thing that differs between schemes is how rows are assigned to folds; features, labels, models and metric are identical.

**3.2 Optimism.** For each repeat we compute the mean test score under each scheme and define optimism as score(random) − score(group). A positive value means the random split overstates how well the model would do on unseen groups. We report the mean over repeats with a bootstrap confidence interval (2,000 resamples over repeats). The default metric is AUC; balanced accuracy is available.

**3.3 Leakage diagnostic (model-free).** For every test row we find its nearest training row in standardised feature space and record whether the two rows belong to the same group. The share of test rows whose nearest neighbour is from their own group is the *same-group nearest-neighbour rate*. It is 0 under a clean group split by construction. Under a random split it measures how identifiable groups are from the features, independently of any model.

**3.4 Permutation null (sanity check).** Labels are permuted within each group, which destroys the feature–label relationship while preserving group sizes and base rates. The group-split score must then be at chance (AUC ≈ 0.5); a score above chance indicates a bug. In our tests the mean over 10 permutations lies between 0.45 and 0.55.

**3.5 Models.** Logistic regression (standardised features), random forest (150 trees, fully grown), and histogram gradient boosting (150 iterations, learning rate 0.1), representing low-capacity and memorisation-prone learners. Hyperparameters are fixed and not tuned, so that differences come from the split and not from tuning.

---

## 4. Synthetic validation

**4.1 Simulator.** Data are generated with known ground truth. There are G groups with n rows each and 12 features. Each group g has a latent label propensity a_g ~ N(0,1) and a feature offset ("fingerprint") f_g ~ N(0, s²·I), where s is the fingerprint SD. A row's features are x = z + f_g with z ~ N(0, I). The label is Bernoulli with logit (1 − ρ)·(z·w) + ρ·2·a_g, where w is a fixed unit vector. Two parameters control leakage separately:
- ρ ∈ [0,1], **label leakage**: the share of the label that depends on the group rather than on the within-group signal z·w;
- s, **covariate leakage**: how strongly groups can be recognised from the features.
Defaults are G = 40 and n = 25 (1,000 rows). ρ = 0 and s = 0 is the true no-leakage control.

**4.2 Design.** For each combination of ρ ∈ {0, 0.5, 1}, s ∈ {0, 0.5, 1.5} and model, we generated 8 independent datasets (data seeds 1–8) and ran the audit with 2 repeats of five-fold validation. We report the mean optimism across datasets with a 95% t-interval across datasets, so the intervals reflect variation between datasets and not only between splits. (Fig 2.)

**4.3 No leakage, no optimism.** With s = 0, mean optimism is between −0.003 and −0.002 for every model at ρ = 0, and intervals include zero at ρ = 1 (for example, logistic regression −0.003, 95% CI −0.020 to 0.014). Label leakage alone does not inflate scores when groups cannot be identified from the features.

**4.4 Optimism needs identifiable groups.** At ρ = 1, optimism grows with s. With s = 0.5, logistic regression, random forest and gradient boosting show 0.063 (0.039–0.087), 0.056 (0.036–0.076) and 0.043 (0.022–0.063). With s = 1.5 the values are 0.135 (0.103–0.168), 0.240 (0.206–0.274) and 0.219 (0.188–0.251). At s = 1.5 the two flexible models are inflated more than logistic regression; at s = 0.5 the three models are statistically close, so we make no ranking claim there.

**4.5 Covariate leakage alone.** At ρ = 0 and s = 1.5, optimism is small but positive for the tree-based models: random forest 0.015 (0.006–0.024) and gradient boosting 0.016 (0.001–0.030); for logistic regression it is 0.002 (−0.004 to 0.009). A plausible mechanism is that a flexible model can memorise each group's offset under a random split and use it to recover the within-group signal; the offset is unknown for held-out groups. We tested this by removing the offsets (s = 0), which removes the effect. [This explanation is supported by the s = 0 control but not tested further, e.g. with an offset-removal preprocessing step.]

**4.6 Leakage diagnostic.** The same-group nearest-neighbour rate tracks identifiability: in a two-repeat run it was about 0.03 at s = 0 and 0.79 at s = 1.5 under random splits, and exactly 0 under group splits. [Report from the final multi-seed run; the values quoted here come from an earlier two-repeat run.]

**4.7 Sensitivity to group structure.** Holding ρ = 1 and s = 1.5, we varied the number of groups (10, 20, 40, 80) and rows per group (10, 25, 50), with 8 datasets per cell (Fig 3). Averaged over group sizes, logistic regression optimism falls from 0.233 at 10 groups to 0.100 at 80 (paired t-test p = 0.003), whereas random forest optimism stays between 0.22 and 0.27 (10 vs 80 groups, p = 0.12). For random forest, optimism rises with rows per group (0.209 at 10 rows, 0.262 at 50; p = 0.012); for logistic regression the trend is weaker (0.138 to 0.166; p = 0.097). These tests are exploratory and uncorrected for multiple comparisons. Optimism stayed between 0.09 and 0.30 in every cell, so the effect is not specific to one configuration.

**4.8 A known artefact.** At high ρ, the group-split AUC of some models falls below 0.5 (about 0.4 for logistic regression at ρ = 1, s = 1.5 in single-dataset runs). Group effects do not transfer to new groups, so a model that learned them performs worse than chance on held-out groups. This inflates the measured optimism relative to a model that merely guessed, and is reported here rather than hidden.

**4.9 Limitations of the synthetic study.** A single generative model; binary labels; AUC as the main metric; 12 features; untuned models; and interval estimates based on 8 datasets. The simulation shows that the audit behaves correctly when the truth is known. It does not show how large optimism is in real data, which is the subject of Section 5.

---

## Notes for you
1. Replace the 4.6 numbers with ones from the final multi-seed run (the diagnostic is computed but not yet saved in the multi-seed summary).
2. Add [CITE] for GroupKFold/scikit-learn and for the AMR leakage literature in `docs/LITERATURE_NOTES.md`.
3. The sentences about *why* optimism appears (4.5) are hypotheses supported by one control, not proven mechanisms.
