"""SplitAudit audit of one Yu, Wheeler & Barquist 2025 species (Mendeley doi 10.17632/zs2mbjv7dn.3, CC BY 4.0).
Same design as the E. coli run, with the labels chosen by a mechanical rule instead of a hand-written list:
 - samples: genomes with a resistant/susceptible call for the antibiotic and a gene-matrix row; intermediate dropped;
   genomes with conflicting calls for that antibiotic dropped
 - features: genes present in 20%-80% of all genomes in the gene matrix (unsupervised, applied before any split)
 - labels: among antibiotics with >= MIN_N labelled genomes, the 5 whose resistant fraction is closest to 0.5
 - groups: ST and fastbaps (genomes with a missing group dropped)
 - models logreg/rf/gb, AUC, 5-fold, random/stratified/group, REPEATS repeats
usage: python real_yu_audit.py <genes.npz> <metadata.tsv> <out_csv> <repeats> [min_n=1000] [list_labels_only]"""
import sys, numpy as np, pandas as pd
from splitaudit.audit import run_audit, optimism
npz, meta, out_csv, reps = sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4])
min_n = int(sys.argv[5]) if len(sys.argv) > 5 else 1000; list_only = len(sys.argv) > 6
Z = np.load(npz, allow_pickle=True); X = Z["X"]; pos = {str(g): i for i, g in enumerate(Z["ids"])}
m = pd.read_csv(meta, sep="\t", low_memory=False); m["genome_id"] = m.genome_id.astype(str)
def clean(ab):
    g = m[(m.antibiotic == ab) & m.resistant_phenotype.isin(["resistant", "susceptible"])].copy()
    g["y"] = (g.resistant_phenotype == "resistant").astype(int)
    c = g.groupby("genome_id").y.nunique(); g = g[~g.genome_id.isin(c[c > 1].index)].drop_duplicates("genome_id")
    return g[g.genome_id.isin(pos)]
cand = []
for ab in m.antibiotic.dropna().unique():
    g = clean(ab)
    if len(g) >= min_n: cand.append((abs(g.y.mean() - 0.5), ab, len(g), g.y.mean()))
cand.sort(); labels = [c[1] for c in cand[:5]]
print("labels:", [(c[1], c[2], round(c[3], 3)) for c in cand[:5]], flush=True)
if list_only: sys.exit()
rows = []
for ab in labels:
    g = clean(ab); idx = [pos[x] for x in g.genome_id]; feat = [f"f{i}" for i in range(X.shape[1])]
    base = pd.DataFrame(X[idx], columns=feat); base["y"] = g.y.values
    for gname, col in (("st", "ST"), ("fastbaps", "fastbaps")):
        gv = g[col].values; ok = ~pd.isna(gv)
        df = base[ok].reset_index(drop=True); df["g"] = gv[ok].astype(int)
        res = run_audit(df, feat, "y", "g", models=("logreg", "rf", "gb"), repeats=reps, metric="auc")
        o = optimism(res); o["label"] = ab; o["label_prev"] = round(df.y.mean(), 3); o["grouping"] = gname
        o["n_groups"] = df.g.nunique(); o["n"] = len(df)
        p = pd.Series(df.g).value_counts(normalize=True); o["chance"] = round(float((p ** 2).sum()), 4)
        o["excess_nn"] = o["nn_same_group_random"] - o["chance"]; rows.append(o); print(ab, gname, len(df), flush=True)
        pd.concat(rows).to_csv(out_csv, index=False)
