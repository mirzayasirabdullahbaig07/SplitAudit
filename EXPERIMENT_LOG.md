# Experiment log

| date | command | seed | data version | result | next step |
|---|---|---|---|---|---|
| 2026-11-23 | `python -m pytest -q` | n/a | none | 5 passed in 67 s | run `simulate` |
| 2026-11-23 | `splitaudit simulate --repeats 3` | default | synthetic | RF optimism 0.034 (rho=0) -> 0.216 (rho=1); logreg 0.008 -> 0.160; group-split AUC < 0.5 at rho>=0.75 for logreg and rho=1 for RF | investigate non-zero RF optimism at rho=0; run on real data |
