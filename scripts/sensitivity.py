"""Sensitivity grid: optimism vs number of groups and rows per group (synthetic).
Usage: python scripts/sensitivity.py [out_raw.csv] [seed_lo] [seed_hi]   (set PYTHONPATH=src if not pip-installed)"""
import sys, pandas as pd
from splitaudit.synthetic import make_grouped
from splitaudit.audit import run_audit
out = sys.argv[1] if len(sys.argv) > 1 else "docs/synthetic_sensitivity_raw.csv"
seed_lo = int(sys.argv[2]) if len(sys.argv) > 2 else 1     # first data seed
seed_hi = int(sys.argv[3]) if len(sys.argv) > 3 else 4     # last data seed (inclusive)
rows = []
for seed in range(seed_lo, seed_hi + 1):
    for ng in (10, 20, 40, 80):
        for pg in (10, 25, 50):
            df = make_grouped(n_groups=ng, per_group=pg, rho=1.0, fingerprint_sd=1.5, seed=seed)
            f = [c for c in df if c.startswith("f")]
            r = run_audit(df, f, models=("logreg", "rf"), repeats=2)
            per = r.groupby(["model", "scheme", "repeat"]).score.mean().unstack("scheme")
            opt = (per["random"] - per["group"]).groupby("model").mean()
            for m, v in opt.items():
                rows.append(dict(seed=seed, n_groups=ng, per_group=pg, model=m, optimism=v))
    pd.DataFrame(rows).to_csv(out, index=False); print("seed", seed, "done", flush=True)
