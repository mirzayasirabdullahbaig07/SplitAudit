# Abstract, Introduction and Related Work (DRAFT v0)

Status: draft for you and your collaborators to edit. All SplitAudit numbers come from saved CSVs in `docs/`. Related-work claims rest on abstracts/snippets or partial reads, flagged below; verify each against the paper before submission. `[CITE]` = citation still to add.

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

## Writing cautions
- Do not write "studies in the field are leaky" until the review sample supports it.
- Simulated optimism (up to 0.24) is a designed effect, not an estimate for real data (real: ≤0.084).
- The soil result is near-null; keep it in the abstract.
