"""SplitAudit soil case study (Scottish soil ARG survey, Knapp et al. 2019, OGL-UK-3.0).
Design fixed BEFORE running (no label picked on results):
 - drop rows with implausible coordinates (lat outside 54-61, lon outside -8..-1)
 - features: detection indicators (abundance not missing) of all genes
 - labels: the 5 gene stems whose detection prevalence is closest to 0.5 (one gene per stem);
   for each label, drop every column with the same stem (e.g. acrA_01..05) from features
 - groups: (a) LOCATION name (replicate sites), (b) spatial blocks KMeans k=10, (c) k=20 on lon/lat (equirectangular)
 - models logreg/rf/gb, AUC, 5-fold, 5 repeats
"""
import re, sys, numpy as np, pandas as pd
from sklearn.cluster import KMeans
from splitaudit.audit import run_audit, optimism
src, outdir = sys.argv[1], sys.argv[2]
d = pd.read_csv(src, encoding="latin1"); d.columns = [c.replace("ï»¿", "") for c in d.columns]
n0 = len(d)
d = d[d.Latitude.between(54, 61) & d.Longitude.between(-8, -1)].reset_index(drop=True)
print("dropped rows:", n0 - len(d))
genes = [c for c in d.columns if c not in ("Longitude", "Latitude", "LOCATION", "@16S_rRNA")]
X = d[genes].notna().astype(int)
stem = lambda c: re.sub(r"_\d+$", "", c)
prev = X.mean()
cand = pd.DataFrame({"gene": prev.index, "prev": prev.values}); cand["stem"] = cand.gene.map(stem)
cand["dist"] = (cand.prev - 0.5).abs()
labels = cand.sort_values("dist").drop_duplicates("stem").head(5)
print(labels.to_string())
xy = np.c_[d.Longitude * np.cos(np.radians(d.Latitude)), d.Latitude]
grp = {"location": d.LOCATION.values}
for k in (10, 20):
    grp[f"block{k}"] = KMeans(k, n_init=10, random_state=0).fit_predict(xy)
rows = []
for _, r in labels.iterrows():
    feat = [c for c in genes if stem(c) != r.stem]
    for gname, g in grp.items():
        df = X[feat].copy(); df["y"] = X[r.gene].values; df["g"] = g
        res = run_audit(df, feat, "y", "g", models=("logreg", "rf", "gb"), repeats=5, metric="auc")
        o = optimism(res); o["label"] = r.gene; o["label_prev"] = round(r.prev, 3)
        o["grouping"] = gname; o["n_groups"] = len(set(g)); o["n"] = len(df); rows.append(o)
        print(r.gene, gname, flush=True)
out = pd.concat(rows); out.to_csv(f"{outdir}/real_soil_audit.csv", index=False)
print(out.round(3).to_string())
