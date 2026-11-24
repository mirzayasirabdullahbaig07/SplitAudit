# SplitAudit
**How much does an ordinary random train/test split overstate performance when samples come in groups (sites, taxa, patients, studies)? A reusable audit — built to be applied to antimicrobial-resistance (AMR) ML.**

Status: framework + tests complete (5 pass). Synthetic sweep works. **No real-data results yet** — you need the real dataset.

## 1. Why this project
Many applied-ML papers (including most of those you are reviewing for the AMR-in-soil review) report high accuracy from random cross-validation on data where samples from the same site/organism/study are correlated. If a random split puts relatives in both train and test, the model memorises group fingerprints and the score is optimistic. This is a **data-science methodology** question: no GPU, fast results, and directly useful for your review. Related work shows the issue is recognised in clinical AMR genomics (e.g. phylogeny-aware evaluation in Briefings in Bioinformatics 2024; homology-aware clustering in a 2025 bioRxiv preprint), but I found **no soil-specific audit** in my searches (not proof none exists).

## 2. Research questions
- **RQ1** Optimism = score(random) − score(group-held-out), with CIs, across models and metrics.
- **RQ2** What predicts optimism: number of groups, group size, group-effect share, model capacity (logreg vs random forest)?
- **RQ3 (real data)** Apply to public soil/AMR datasets: how much do published-style random splits overstate?
- **RQ4 (review)** Code each paper in your review with `docs/review_coding_sheet.csv`; correlate leakage-risk rating with reported scores.

## 3. Design choices and why
| Choice | Reason |
|---|---|
| Compare random / stratified / group splits on identical data and models | Isolates the split as the only difference |
| Nearest-neighbour same-group rate | A direct, model-free leakage diagnostic: how often is a test row's closest training row from its own group? ≈0 under clean group splits |
| Label-permutation-within-group null | Sanity check: group-split score must sit at chance; above chance signals a bug |
| Synthetic data with controllable group-effect share ρ | Gives ground truth for validating the audit: optimism must be ≈0 at ρ=0 and grow with ρ (tests assert this) |
| Bootstrap CI over repeats | Reports uncertainty, not a single number |
| Logistic regression and random forest | Low-capacity vs memorisation-prone model |

## 4. Quick start
```bash
pip install -e . pytest && python -m pytest -q      # ~90 s
splitaudit simulate --repeats 3                      # synthetic rho sweep
splitaudit audit --csv data.csv --label resistant --group site --repeats 10   # YOUR data
```
Two leakage mechanisms are simulated separately: label leakage (`rho`) and covariate leakage (`fingerprint_sd`, group-specific feature offsets). Optimism needs the model to be able to identify groups from features: at `fingerprint_sd=0` it stays ≈0 even at `rho=1`; at `rho=0` a random forest still shows ≈0.03 AUC optimism from fingerprints alone. Grid: `splitaudit simulate --fingerprint-sd 0 1.5`.

Synthetic sweep (2 repeats, illustrative only): RF optimism rises from ≈0.03 AUC at ρ=0 to ≈0.23 at ρ=1.

## 5. What is verified / not
Verified: group splits never share groups and random ones do; optimism ≈ 0 when there is no group effect AND no group fingerprint (`rho=0, fingerprint_sd=0`) and large with both (CI excludes 0); monotone in ρ; same-group-NN diagnostic flags random splits; permutation null ≈ chance.
Not verified: behaviour on real AMR data. **Caveat:** at high ρ, group-split AUC can fall *below* 0.5 (group effects don't transfer, so the model anti-learns). Report this honestly; it is a known artefact, not a bug.

## 6. Limitations
Binary labels only (extend to multi-class/regression); group structure must be known (clonal/phylogenetic relatedness may need clustering — see roadmap); synthetic ≠ real; no time/space blocking beyond a naive `blocked` option.

See `ROADMAP.md`.
