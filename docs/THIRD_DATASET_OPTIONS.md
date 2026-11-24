# Third real dataset: options (2026-11-25)

Why: the paper has two real datasets and the soil one has no environmental covariates. A third dataset with a natural group column (lineage, site, study) and a real prediction label would strengthen it most.

Selection criteria (fix before looking at results): (1) public and downloadable without registration; (2) licence allows reuse; (3) a group column that exists in the data (lineage/cluster, site, study, patient); (4) a binary label that is not trivially encoded in the features; (5) at least ~300 samples and ~10 groups.

## Candidate found (not yet downloaded or checked)
- **Yu, Wheeler & Barquist data (Mendeley Data, doi 10.17632/zs2mbjv7dn.3, published 27 Oct 2025).** The record's description lists gene presence/absence tables, SNP files and a metadata file (`meta_checkm.csv`) for the AMR-prediction study of 24,000+ genomes from five pathogens, plus train/test split files; the analysis scripts are in the GitHub repository BarquistLab/AMR_prediction. The licence field was cut off in the search result: check it. The record describes the data as large, so take one species and one antibiotic. Lineage groups would need to be derived or taken from the provided split files. This is the same group's work cited in the paper as evidence that sampling bias confounds AMR prediction, so a result on their data should be framed carefully: we would be auditing how much random splits inflate scores there, not re-testing their claim.
- Where to get it: https://data.mendeley.com/datasets/zs2mbjv7dn (download in your browser; my workspace cannot reach Mendeley).

## Other ideas (unchecked; need a search by someone with open web access)
- A public soil or environmental ARG dataset that includes sample-level covariates (pH, land use, climate), e.g. from a supplementary table of a metagenomics paper; check the licence and that sample IDs map to sites.
- Hu et al. 2024 (Briefings in Bioinformatics) benchmark data, if the repository or Zenodo record is openly downloadable.
- Any clinical isolate collection with patient or hospital IDs.

## If none can be found
Say so in the Limitations (already stated), and keep the claims scoped to two datasets. Do not stretch the soil result into a statement about soil studies in general.

## Protocol once a dataset is chosen
1. Write the label and grouping rule in `EXPERIMENT_LOG.md` before running.
2. Check for label-duplicate features (top predictive feature; both naming schemes).
3. Run `splitaudit audit` with 10 repeats for 3 models, AUC and balanced accuracy.
4. Add a row to the log and a subsection to Section 5; update Fig 4.
