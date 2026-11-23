# Experiment log

| date | command | seed | data version | result | next step |
|---|---|---|---|---|---|
| 2026-11-23 | `python -m pytest -q` | n/a | none | 5 passed in 67 s | run `simulate` |
| 2026-11-23 | `splitaudit simulate --repeats 3` | default | synthetic | RF optimism 0.034 (rho=0) -> 0.216 (rho=1); logreg 0.008 -> 0.160; group-split AUC < 0.5 at rho>=0.75 for logreg and rho=1 for RF | investigate non-zero RF optimism at rho=0; run on real data |
| 2026-11-23 | `splitaudit simulate --repeats 2 --fingerprint-sd 0 1.5` | default | synthetic | RF optimism at fp_sd=0: ~ -0.01 to -0.02 for all rho (no group identifiability -> no gain); at fp_sd=1.5: 0.032 (rho=0) -> 0.229 (rho=1). Explains RF optimism at rho=0: covariate leakage via group fingerprints, not a bug | add logreg/GB to grid; real data |
| 2026-11-24 | `splitaudit simulate --repeats 5 --models logreg rf gb --fingerprint-sd 0 0.5 1.5` | default (data seed 1) | synthetic | Optimism at rho=1: fp_sd=0 -> -0.006 to -0.011 (all models); fp_sd=0.5 -> logreg 0.064, rf 0.042, gb 0.016; fp_sd=1.5 -> logreg 0.153, rf 0.222, gb 0.187. Saved as docs/synthetic_grid.csv | repeat over several data seeds; real data |
| 2026-11-24 | `python scripts/multiseed.py` (8 data seeds x fp_sd {0,0.5,1.5} x rho {0,0.5,1} x 3 models, 2 split repeats) | data seeds 1-8 | synthetic | Mean optimism (95% t-CI across datasets). fp_sd=0: ~0 for all models/rho. fp_sd=1.5, rho=1: gb 0.219 [0.188,0.251], rf 0.240 [0.206,0.274], logreg 0.135 [0.103,0.168]. fp_sd=1.5, rho=0: rf 0.015 [0.006,0.024], gb 0.016 [0.001,0.030], logreg 0.002 [-0.004,0.009]. Single-seed (seed 1) values were larger at rho=0 (~0.03) -> use multi-seed numbers in the paper | real data; plots for Fig 2/3 |
