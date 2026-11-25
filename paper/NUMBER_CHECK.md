# Number check of MANUSCRIPT_DRAFT.md (2026-11-25)

Method: recomputed from saved CSVs in docs/ (and the two files created in this session).

## Verified (match the files)
- Sec 4.3-4.5 and abstract: multi-seed optimism table (fp_sd 0/0.5/1.5 x rho x model, 8 datasets) incl. -0.003..-0.002 at fp 0, rho 0; 0.063/0.056/0.043 and 0.135/0.240/0.219 at rho 1; 0.015/0.016/0.002 at fp 1.5, rho 0.
- Sec 4.6: same-group NN rate 0.022 / 0.100 / 0.845 (fp 0 / 0.5 / 1.5), 0 under group splits (synthetic_nn_diagnostic.csv, 8 seeds).
- Sec 4.7: group-count and rows-per-group means and paired t-test p-values recomputed: logreg 0.233 -> 0.100 (p=0.0032), rf 0.271 -> 0.223 (p=0.119); rows/group rf 0.209 -> 0.262 (p=0.0118), logreg 0.138 -> 0.166 (p=0.097); every cell between 0.09 and 0.296.
- Sec 5.1 main table (real_ecoli_ctxm_audit.csv): optimism, AUCs, NN rates and chance levels.
- Sec 5.1 robustness: 36/36 cells positive and CI > 0; range 0.013-0.084.
- Sec 5.2 soil: 31/45 positive, 13/45 CI > 0; medians 0.002 (site), 0.002 (10 blocks), 0.012 (20 blocks); by model 0.002/0.004/0.010; max 0.056; random AUC range 0.565-0.942.

## Resolved on 2026-11-25 (re-run, files saved)
- Repeats: `scripts/multiseed.py` uses repeats=2, matching Sec 4.2.
- Permutation null (`docs/synthetic_permutation_null.csv`, `scripts/permutation_null.py`): 96 cases, mean 0.501; per-case means 0.365-0.556; 5 of 96 outside 0.45-0.55, all at rho 1, fp 1.5. The earlier manuscript claim ("between 0.45 and 0.55") was too strong and has been rewritten in Sec 3.4.
- Sec 4.8: the "about 0.4" claim was only true for some datasets. Over 8 datasets the mean group-split AUC at rho 1, fp 1.5 is 0.497 (logreg), 0.507 (rf), 0.510 (gb), minimum 0.379 (`docs/synthetic_group_auc_rho1_fp1.5.csv`). Sentence rewritten. Note this weakens the "below chance" artefact: on average it is at chance, and the below-chance cases are dataset-specific.

## Still open
1. Sec 5.1 group-split AUC range "0.77-0.94" is from the robustness run (min 0.768); main table shows 0.767 for logreg/country (10 vs 5 repeats). Say which run each number comes from.
2. Intro/related work statements about other papers are unverified against PDFs (see paper/references.md and docs/review_coding_sheet.csv).

## Correction 2026-11-25 (identifiability)
Soil same-group NN rates were compared with a chance level of 1/groups in earlier text. Actual chance (sum of squared group proportions) is 0.007 (site), 0.113 (10 blocks), 0.054 (20 blocks). The earlier statements 'far above chance' (Sec 6.2) and 'a high rate signals risk, not certainty' (checklist item 11, Fig 5) were wrong and are rewritten. Source: docs/nn_vs_optimism.csv.

## Added 2026-11-25: Section 5.4 (Yu et al. published results)
All numbers from docs/yu_published_optimism_cells.csv and _summary.csv (computed from TS2.tsv). Pairing check: max training-size difference between paired random and clade cells 2e-13. Not yet compared against the authors' paper text.

## Added 2026-11-25: Section 5.3 (third dataset, own audit)
All numbers from docs/real_yu_ecoli_audit.csv (30 rows): positive cells 30/30, median 0.091, medians by grouping, model and label, NN rates and chance levels (chance = sum of squared group proportions on the labelled sample). Spearman(excess NN, optimism) = 0.34, p = 0.066. Two repeats only: no intervals reported.

## Updated 2026-11-25: Section 5.3 now uses the 5-repeat run
docs/real_yu_ecoli_audit.csv holds the 5-repeat results (30 rows): 30/30 positive and 30/30 intervals excluding zero; median 0.096, range 0.043 to 0.297; ST 0.078, fastbaps 0.111; gb 0.059, logreg 0.102, rf 0.123; labels cefotaxime 0.070, amoxicillin 0.079, trimethoprim 0.116, amoxicillin-clavulanic acid 0.123, ciprofloxacin 0.138; median AUC 0.855 random, 0.771 ST, 0.760 fastbaps; interval width median 0.016. Spearman(excess NN, optimism) 0.28, p = 0.135. The earlier 2-repeat figures (median 0.091 etc.) are superseded.

## Added 2026-11-25: Section 5.4 (Salmonella, own audit)
All numbers from docs/real_yu_salmonella_audit.csv (30 rows): 30/30 positive, 30/30 intervals above 0 (median width 0.014); median 0.171, range 0.066 to 0.444; ST 0.126, fastbaps 0.276; gb 0.144, rf 0.151, logreg 0.260; labels tetracycline 0.122, streptomycin 0.156, sulfisoxazole 0.175, ampicillin 0.235, chloramphenicol 0.287; median AUC 0.943 random, 0.805 ST, 0.643 fastbaps; NN rate ST 0.93-0.96 (chance 0.07-0.11), fastbaps 0.97-0.99 (chance 0.10-0.15); excess 0.83 to 0.88; Spearman 0.22, p = 0.23. Sections 5.4-5.5 were renumbered (secondary analysis is now 5.5, limitations 5.6).
