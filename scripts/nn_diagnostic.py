"""Same-group nearest-neighbour rate across the multi-seed synthetic design (model-free).
Usage: python scripts/nn_diagnostic.py [out_csv]"""
import sys, numpy as np, pandas as pd
from sklearn.preprocessing import StandardScaler
from splitaudit.synthetic import make_grouped
from splitaudit.audit import _splits, same_group_nn_rate
out = sys.argv[1] if len(sys.argv) > 1 else "docs/synthetic_nn_diagnostic.csv"
rows = []
for seed in range(1, 9):
    for fp in (0.0, 0.5, 1.5):
        for rho in (0.0, 0.5, 1.0):
            df = make_grouped(rho=rho, seed=seed, fingerprint_sd=fp)
            f = [c for c in df if c.startswith("f")]
            X = df[f].to_numpy(float); y = df.y.to_numpy(int); g = df.group.to_numpy(str)
            Xs = StandardScaler().fit_transform(X)
            for scheme in ("random", "group"):
                rates = [same_group_nn_rate(Xs[tr], g[tr], Xs[te], g[te])
                         for rep in range(2) for tr, te in _splits(scheme, X, y, g, 5, rep)]
                rows.append(dict(seed=seed, fp_sd=fp, rho=rho, scheme=scheme, nn_same_group=float(np.mean(rates))))
t = pd.DataFrame(rows); t.to_csv(out, index=False)
s = t.groupby(["scheme", "fp_sd"]).nn_same_group.agg(["mean", "std", "min", "max"]).round(3)
print(s)
