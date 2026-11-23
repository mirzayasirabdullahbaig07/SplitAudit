# Roadmap — SplitAudit (8 weeks, ~2–3 h/day)
Definition of done: preprint with (a) the audit tool, (b) real-data optimism estimates, (c) a leakage reporting checklist.

## Week 1 — Literature + data hunt
- **D1** Run tests + `simulate`. Explain the ρ-sweep table in your own words.
- **D2** Read the 2024 Briefings in Bioinformatics AMR benchmarking paper (phylogeny-aware evaluation) and the 2025 homology-aware clustering preprint. Note how each defines the split.
- **D3** Search specifically for soil / environmental AMR ML papers. Build a spreadsheet: paper | data type | split used | n groups | metric | score.
- **D4** Ask your review collaborators which datasets from the review are public and have a site/sample/taxon column. Write down the **grouping variable** for each.
- **D5** Gap statement (≤150 words). Be explicit about what is NOT new (leakage is known).
- **D6–7** Fill `docs/review_coding_sheet.csv` for the first 10 papers.

## Week 2 — Real data
- **D8–9** Download 1–3 public datasets (check licences). Clean to `label, group, numeric features` CSV.
- **D10** First `splitaudit audit` run. Inspect: groups with few rows? class imbalance? Fix.
- **D11–14** Add: stratified-by-group option, class-balanced metric (bacc), cluster-based groups (e.g. cluster samples by feature similarity or sequence identity as a proxy for relatedness).

## Weeks 3–4 — Experiments
RQ1–RQ3 on real data (10+ repeats), plus a **sensitivity grid** on synthetic data (n_groups × group_size × ρ). Add a gradient-boosting model. Keep a clean `EXPERIMENT_LOG.md`.

## Week 5 — Review integration
Finish coding all review papers; test whether leakage-risk rating correlates with reported score (Spearman, with CI). This links directly to your joint review.

## Week 6 — Recommendations
Write the reporting checklist (≤10 items) and a decision flowchart "which split should I use?".

## Week 7 — Writing · Week 8 — Release
Same as other projects: Zenodo DOI, arXiv, supervisor feedback.

## Go / no-go gates
- End Week 2: no public dataset with a usable group column? Then run the audit on 2–3 *non-soil* public grouped datasets (any domain) and frame the paper as a general tool + checklist; keep AMR as a case study in the review.
- End Week 4: optimism ≈ 0 on all real data? Report it: "random splits were adequate here" is a legitimate finding.

## Paper outline
1 Introduction · 2 Background (leakage in grouped data; AMR-ML context) · 3 Audit method (schemes, diagnostic, null) · 4 Synthetic validation · 5 Real-data case studies · 6 Review meta-analysis · 7 Checklist & recommendations · 8 Limitations.
