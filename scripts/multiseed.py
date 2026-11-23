import sys, numpy as np, pandas as pd
from splitaudit.synthetic import make_grouped
from splitaudit.audit import run_audit
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
    pd.DataFrame(rows).to_csv("/tmp/multiseed_raw.csv",index=False); print("seed",seed,"done",flush=True)
