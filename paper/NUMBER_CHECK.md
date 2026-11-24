# Number check of MANUSCRIPT_DRAFT.md (2026-11-25)

Method: recomputed from saved CSVs in docs/ (and the two files created in this session).

## Verified (match the files)
- Sec 4.3-4.5 and abstract: multi-seed optimism table (fp_sd 0/0.5/1.5 x rho x model, 8 datasets) incl. -0.003..-0.002 at fp 0, rho 0; 0.063/0.056/0.043 and 0.135/0.240/0.219 at rho 1; 0.015/0.016/0.002 at fp 1.5, rho 0.
- Sec 4.6: same-group NN rate 0.022 / 0.100 / 0.845 (fp 0 / 0.5 / 1.5), 0 under group splits (synthetic_nn_diagnostic.csv, 8 seeds).
- Sec 4.7: group-count and rows-per-group means and paired t-test p-values recomputed: logreg 0.233 -> 0.100 (p=0.0032), rf 0.271 -> 0.223 (p=0.119); rows/group rf 0.209 -> 0.262 (p=0.0118), logreg 0.138 -> 0.166 (p=0.097); every cell between 0.09 and 0.296.
- Sec 5.1 main table (real_ecoli_ctxm_audit.csv): optimism, AUCs, NN rates and chance levels.
- Sec 5.1 robustness: 36/36 cells positive and CI > 0; range 0.013-0.084.
- Sec 5.2 soil: 31/45 positive, 13/45 CI > 0; medians 0.002 (site), 0.002 (10 blocks), 0.012 (20 blocks); by model 0.002/0.004/0.010; max 0.056; random AUC range 0.565-0.942.

## NOT verifiable from saved files (check or regenerate)
1. Sec 4.2 "2 repeats of five-fold" for the multi-seed run: no repeat count in the CSV.
2. Sec 3.4 "permutation null between 0.45 and 0.55 (mean over 10 permutations)": no saved permutation-null CSV found. Re-run and save, or remove the numbers.
3. Sec 4.8 "about 0.4 AUC for logistic regression at rho 1, fp 1.5 in single-dataset runs": no saved group-split AUC for that cell was checked.
4. Sec 5.1 group-split AUC range "0.77-0.94" is from the robustness CSV (min 0.768); the main table shows 0.767 for logreg/country: rounding across different repeat counts (10 vs 5). Say which in the text.
5. Intro/related work: statements about other papers are unverified against PDFs (see paper/references.md and docs/review_coding_sheet.csv).
