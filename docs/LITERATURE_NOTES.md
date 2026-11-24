# Literature notes — SplitAudit (Week 1)

Status (updated 2026-11-24): L02 and L03 read via full-text fetch (summaries to re-verify against the PDFs); L05 primary paper located (abstract only); L01 and L04 still unread (L01 full text blocked by bot check). Earlier notes were built from abstracts/snippets. Every `NOT CHECKED` in `docs/review_coding_sheet.csv` must be filled from the full paper before any claim is made about it. Leakage-risk ratings are deliberately blank.

## A. Soil / environmental ARG machine-learning papers (rows L01–L05 in the coding sheet)
Zheng 2022 (global soil ARG map); KeshikNevisRazavi 2026 (ARG identification, 98% RF accuracy on 200 samples); Danko 2021 (geographic origin prediction); phyllosphere resistome prediction; a soil-ARG-under-climate-scenarios study (primary paper still to find).

## B. Leakage and validation evidence in genomic AMR (cite; already established)
- Lüftinger et al. 2021 — genome-distance-aware cross-validation (Front Cell Infect Microbiol, doi 10.3389/fcimb.2021.610348)
- Hu et al. 2024 — random vs phylogeny-aware vs homology-aware folds (Brief Bioinform, doi 10.1093/bib/bbae206)
- Yu, Wheeler & Barquist 2025 — biased sampling confounds ML prediction of AMR
- Tutorial: genomic data + ML for AMR with several cross-validation techniques (PLOS Comput Biol 2024, doi 10.1371/journal.pcbi.1012579)

## C. Leakage magnitude in spatial/ecological ML (benchmark for our effect sizes)
- Koldasbayeva & Zaytsev 2025 (arXiv 2502.03480) — species distribution models: random CV overestimated AUC by up to 0.16.
- Meyer et al. (arXiv 1908.07805) — spatial CV essential to avoid over-optimistic performance with random forests.
- Roberts-style spatial CV assessment (arXiv 2303.07334).
Use: our synthetic optimism (up to ~0.24 AUC) is larger than 0.16, which is expected in a simulation built to leak; do not present it as a real-data estimate.

## D. Soil microbiome ML (context; split design not yet checked)
Wilhelm et al. 2022 (soil health from microbiome, Soil Biol Biochem 164:108472); Aghdam & Solís-Lemus (potato yield/disease from soil microbiome, BMC Bioinformatics 2024).

## Draft gap statement (≤150 words) — DRAFT, edit with your collaborators
Random cross-validation is known to overstate performance when samples are grouped by phylogeny, site or space, in genomic AMR prediction and in spatial ecology. Yet machine-learning studies of antimicrobial resistance in soil and other environmental samples often do not state which validation split they used. Tools for leakage-aware splitting or leakage detection exist (e.g. DataSAIL, blockCV, BORG, bioLeak; see below); in a limited search we did not find one that pairs a random-versus-group optimism estimate with a chance-referenced identifiability measure and a permutation check, validated on simulations and AMR data. We present SplitAudit, an open-source audit that compares random, stratified and group-held-out splits on identical data and models, with a model-free leakage diagnostic and a permutation null; we validate it on simulations with known ground truth, apply it to public soil data, and propose a short reporting checklist.

## Still to do
1. Find the primary paper for L05; complete the citation for L04.
2. Read full text of L01–L05 and fill every `NOT CHECKED` field.
3. Rate leakage risk (low/med/high) from the full text, with a one-line justification in `notes`.
4. Add the papers your review collaborators are already reading (first 10 papers target).

## Update 2026-11-24 (findings from full-text reads)
- L02 (KeshikNevisRazavi 2026): feature filter applied before the split; split type and homology between train/test not stated; RF accuracy 0.988 on 200 sequences. Strong audit candidate.
- L03 (Danko 2021): single 60/40 split, city is the target; external mystery set scored lower for some regions (0.49 South America vs ~0.80 East Asia).
- L05 primary paper: Kenzi et al., Sci Total Environ (PubMed 42224874): 10-fold CV, LightGBM fold SD of AUC 0.008; split type unstated.
- Remaining: L01 manual PDF read; L04 full citation.

## Tool search 2026-11-25 (snippets only; verify before citing)
CORRECTION: the earlier claim 'no reusable tool' was wrong. Existing: DataSAIL (Nat Commun 2025), blockCV (R; leave-group-out in recent versions), BORG (R; includes a random vs blocked CV comparison, the closest overlap), bioLeak (R), mlleak (Python), leakaudit/leakr (R). Action: install BORG and compare outputs on our simulated data before finalising the novelty paragraph; state differences precisely.
