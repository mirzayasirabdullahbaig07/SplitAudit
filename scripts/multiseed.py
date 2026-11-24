"""Multi-dataset simulation: 8 data seeds x fingerprint SD x rho x model, 2 repeats.
Usage: python scripts/multiseed.py [raw_out.csv] [summary_out.csv]   (defaults: docs/synthetic_multiseed_raw.csv, docs/synthetic_multiseed_summary.csv)"""
import sys, numpy as np, pandas as pd
from scipy import stats
from splitaudit.synthetic import make_grouped
from splitaudit.audit import run_audit
raw_out = sys.argv[1] if len(sys.argv) > 1 else "docs/synthetic_multiseed_raw.csv"
sum_out = sys.argv[2] if len(sys.argv) > 2 else "docs/synthetic_multiseed_summary.csv"
rows=[]
for seed in range(1,9):
    for fp in (0.0,0.5,1.5):
        for rho in (0.0,0.5,1.0):
            df=make_grouped(rho=rho,seed=seed,fingerprint_sd=fp)
            f=[c for c in df if c.startswith('f')]
            r=run_audit(df,f,models=("logreg","rf","gb"),repeats=2)
            per=r.groupby(["model","scheme","repeat"]).score.mean().unstack("scheme")
            opt=(per["random"]-per["group"]).groupby("model").mean()
            for m,v in opt.items(): rows.append(dict(seed=seed,fp_sd=fp,rho=rho,model=m,optimism=v))
    pd.DataFrame(rows).to_csv(raw_out,index=False); print("seed",seed,"done",flush=True)

def summarise(raw):
    g = []
    for (fp, rho, m), d in raw.groupby(["fp_sd", "rho", "model"]):
        x = d.optimism.to_numpy(); n = len(x); mu = x.mean(); sd = x.std(ddof=1)
        h = stats.t.ppf(0.975, n - 1) * sd / np.sqrt(n)
        g.append(dict(fp_sd=fp, rho=rho, model=m, n_datasets=n, optimism_mean=round(mu, 3), ci_lo=round(mu - h, 3), ci_hi=round(mu + h, 3), sd_across_datasets=round(sd, 3)))
    return pd.DataFrame(g)
summarise(pd.read_csv(raw_out)).to_csv(sum_out, index=False)
