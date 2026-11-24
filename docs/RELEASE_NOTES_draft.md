# Release notes (DRAFT) — v0.2.0

Do not tag until: tests pass on a clean install, LICENSE chosen, scripts' output paths checked, manuscript claims verified (see paper/NUMBER_CHECK.md).

## Added since v0.1.0
- Gradient boosting model (`--models gb`); covariate leakage control (`--fingerprint-sd`); balanced accuracy metric.
- Scripts: multi-dataset simulation, sensitivity grid, NN diagnostic, permutation null, E. coli preparation and audits, soil audit, five figure scripts.
- Docs: dataset register, literature notes, coding sheet, reporting checklist and pilot, references, manuscript draft, number check.
- Results CSVs under `docs/`; experiment log.

## Known issues
- Some scripts use hard-coded output paths (`/tmp/...`) — parameterise before release.
- Real-data intervals cover split repeats only.
- Tests: 7 (5 original + 2 fingerprint tests); not run on a clean machine since the latest changes.

## Release checklist
- [ ] Choose and add LICENSE (code); keep data out of the repo
- [ ] Bump version in pyproject.toml to 0.2.0
- [ ] `pip install -e . && pytest -q` on a clean environment
- [ ] Tag `v0.2.0`, create GitHub release, connect to Zenodo for a DOI
- [ ] Add DOI and citation (CITATION.cff) to README
