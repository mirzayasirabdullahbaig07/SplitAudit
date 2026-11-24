# SplitAudit reporting checklist (DRAFT v0)

Purpose: a short list a paper can answer in a sentence each, so readers can judge whether the reported score reflects performance on new groups. Each item says where it comes from in this project. Items marked (observed) were gaps seen in the small coded sample (docs/review_coding_sheet.csv); that sample is five papers and does not show how common the gaps are.

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
11. **Identifiability.** Report the same-group nearest-neighbour rate under a random split together with its chance level (the sum of squared group proportions), and the excess over chance. A large excess means groups are recognisable from the features. *(E. coli ST: 0.27 vs 0.025; soil 10 spatial blocks: 0.18-0.21 vs 0.113, a small excess, with small optimism.)* The rate describes identifiability; it does not by itself predict the size of the optimism, which also depends on how much the label varies by group.
12. **Permutation null.** Within-group label permutation under group splits should give AUC near 0.5.
13. **External set.** If an external or held-out-group set exists, report it next to the internal score. *(L03: external scores lower for some regions.)*

## E. Reporting uncertainty
14. **Intervals.** Say what the interval covers. Repeats of one dataset's splits understate uncertainty; across-dataset variation is wider. *(synthetic: 8-seed intervals wider than single-dataset ones.)*
15. **Metric.** Report a threshold-free metric and one threshold-based metric; optimism can differ between them. *(E. coli: AUC median 0.030, balanced accuracy 0.038.)*

## How to use / limits
- Optimism measures sensitivity to the split, not whether the model is right for the right reasons; linked genes (plasmids, operons) can make prediction partly genuine.
- No threshold of optimism is "acceptable"; report the number and context.
- Not yet tested: whether authors find the checklist usable. Pilot it on 3-5 papers before claiming it helps.
