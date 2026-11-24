# Dataset register — SplitAudit

Status key: **TODO** = not yet downloaded/inspected · **OK** = inspected, usable · **NO** = rejected (note why).
Nothing below has been downloaded or checked yet. Fill the "Verified" columns as you go.

## Candidate datasets

| ID | Dataset | Domain | Size (as reported) | Where | Candidate group variable | Status |
|---|---|---|---|---|---|---|
| D1 | Delgado-Baquerizo et al. 2022, *The global distribution and environmental drivers of the soil antibiotic resistome*, Microbiome | Soil ARG | 285 ARGs, 1012 sites, all continents | Figshare link in the paper's Data availability section (DOI 10.1186/s40168-022-01405-w) | biome / continent / country (site is too fine — one row per site) | TODO — **start here** |
| D2 | Zheng et al. 2022, *Global biogeography and projection of soil antibiotic resistance genes*, Science Advances | Soil ARG | 1088 soil metagenomes, 558 ARGs, 169 spatial covariates | Paper: doi 10.1126/sciadv.abq8015 — data location not yet found | habitat type / region / source study | TODO — locate data |
| D3 | Curated resource of 214K metagenomes (PLOS Biology 2022) | Global resistome | read counts aligned to ARGs, country + collection-date metadata | Paper: doi 10.1371/journal.pbio.3001792 | country / BioProject / sample type | TODO — large; later option |
| D4 | Hu et al. 2024, *Assessing computational predictions of AMR phenotypes from microbial genomes*, Briefings in Bioinformatics | Clinical AMR | 78 species-antibiotic datasets with random, phylogeny-aware and homology-aware folds | Mendeley Data doi 10.17632/6vc2msmsxj; code github.com/hzi-bifo/AMR_benchmarking | phylogeny / homology cluster (folds provided) | TODO — lists genome IDs only; features must be built from genomes (heavy for a laptop) |

## Related prior work (cite; do not treat as datasets to audit)
- Yu, Wheeler & Barquist 2025 — biased sampling confounds ML prediction of AMR (24,000+ genomes, 5 pathogens). Mendeley Data doi 10.17632/zs2mbjv7dn.
- Lüftinger et al. 2021 — genome-distance-aware cross-validation for AMR prediction. Front. Cell. Infect. Microbiol., doi 10.3389/fcimb.2021.610348.

## Per-dataset checklist (complete before using a dataset in the paper)
- [ ] Licence / terms recorded
- [ ] Download date and file hash recorded in `EXPERIMENT_LOG.md`
- [ ] Label defined (binary): ______________________
- [ ] Group variable defined and justified: ______________________
- [ ] n rows / n groups / smallest group size / positive rate recorded
- [ ] Groups with very few rows handled (merge or drop, and say so)
- [ ] Cleaned to `label, group, numeric features` CSV
- [ ] First `splitaudit audit --csv ... --label ... --group ... --repeats 10` run logged

## Design note
In D1–D3 each row is a site or sample, so the group must be a coarser unit (biome, region, country, study). Report optimism under **at least two** grouping choices; the estimate depends on that choice.

## Gap statement caution
Leakage in AMR prediction from genomes is already documented (Lüftinger 2021; Hu 2024; Yu 2025). The contribution here is the soil/environmental application, the reusable audit, and the reporting checklist — not the discovery that leakage exists.

## Update 2026-11-24 — datasets actually obtained
| ID | Dataset | Status |
|---|---|---|
| D5 | E. coli resistome matrix, Mendeley doi 10.17632/r5ccbmsnhw.1 (743 genomes) | **OK — used.** Prepared as CTX-M carriage task; groups = sequence type (218), phylogroup (10), country (56). First audit in `docs/real_ecoli_ctxm_audit.csv`. Licence still to record. |
| D6 | Scottish soil ARG survey, EIDC doi 10.5285/d3498e93-4ac5-4eab-bc1a-eb2328771d24 (183 locations, ~300 ARGs, OGL v3) | **Partial** — only the supporting package downloaded; the data CSV is still missing (see `data/README.md`). |
| D1 | Delgado-Baquerizo 2022 | Not available (private link not downloadable; authors not expected to share). Supplementary PDF and paper PDF are in the folder but contain no data table. |
