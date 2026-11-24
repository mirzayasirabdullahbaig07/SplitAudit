"""Saves (a) the within-group label-permutation null and (b) group-split AUC at rho=1, fp_sd=1.5.
Synthetic data seeds 1-8; rho in {0,1}; fp_sd in {0,1.5}; 10 permutations per dataset/model."""
import sys, numpy as np, pandas as pd
from splitaudit.synthetic import make_grouped
from splitaudit.audit import label_permutation_null, run_audit
out=sys.argv[1]; rows=[]; aucs=[]
for seed in range(1,9):
    for rho in (0.0,1.0):
        for fp in (0.0,1.5):
            df=make_grouped(rho=rho,seed=seed,fingerprint_sd=fp)
            feats=[c for c in df.columns if c not in("y","group")]
            for m in ("logreg","rf","gb"):
                sc=label_permutation_null(df,feats,"y","group",model=m,n_perm=10,seed=seed)
                rows.append(dict(seed=seed,rho=rho,fp_sd=fp,model=m,perm_mean=sc.mean(),perm_min=sc.min(),perm_max=sc.max()))
            if rho==1.0 and fp==1.5:
                r=run_audit(df,feats,"y","group",models=("logreg","rf","gb"),schemes=("random","group"),k=5,repeats=2)
                g=r.groupby(["model","scheme"]).score.mean().unstack(); g["seed"]=seed; aucs.append(g.reset_index())
        print("seed",seed,flush=True)
pd.DataFrame(rows).to_csv(f"{out}/synthetic_permutation_null.csv",index=False)
pd.concat(aucs).to_csv(f"{out}/synthetic_group_auc_rho1_fp1.5.csv",index=False)
