"""SplitAudit third case study: E. coli from Yu, Wheeler & Barquist 2025 (Mendeley doi 10.17632/zs2mbjv7dn.3, CC BY 4.0).
Design fixed BEFORE running (nothing chosen on results):
 - samples: genomes with a resistant/susceptible phenotype for the antibiotic; intermediate/undefined dropped;
   genomes with conflicting labels for that antibiotic dropped
 - features: gene presence/absence (pan-genome Rtab) of genes present in 20%-80% of all 5,836 genomes (unsupervised
   filter applied before any split; 2,775 genes). CHANGED from 5%-95% (7,991 genes) for compute only: one pilot cell
   (trimethoprim x fastbaps, 1 repeat, 7,991 genes) took 8 minutes on 2 cores. That pilot cell's result was seen before the change.
 - labels: among antibiotics with >= 1,000 labelled genomes, the 5 whose resistant fraction is closest to 0.5:
   trimethoprim, amoxicillin, amoxicillin_clavulanic_acid, ciprofloxacin, cefotaxime
 - groups: (a) multilocus sequence type ST, (b) fastbaps population cluster (31 clusters; the study's clade proxy)
 - models logreg/rf/gb, AUC, 5-fold, REPEATS repeats (final run: 5), schemes random/stratified/group
usage: python real_yu_ecoli_audit.py <genes.npz> <metadata_checkm.csv> <out_dir> [repeats] [only_label] [only_group]"""
import sys, numpy as np, pandas as pd
from splitaudit.audit import run_audit, optimism
npz, meta, outdir = sys.argv[1:4]
reps = int(sys.argv[4]) if len(sys.argv) > 4 else 5
only_l = sys.argv[5] if len(sys.argv) > 5 else None
only_g = sys.argv[6] if len(sys.argv) > 6 else None
Z = np.load(npz, allow_pickle=True); X = Z["X"]; ids = list(map(str, Z["ids"])); pos = {g: i for i, g in enumerate(ids)}
m = pd.read_csv(meta, sep="\t", low_memory=False); m["genome_id"] = m.genome_id.astype(str)
LABELS = ["trimethoprim", "amoxicillin", "amoxicillin_clavulanic_acid", "ciprofloxacin", "cefotaxime"]
rows = []
for ab in LABELS:
    if only_l and ab != only_l: continue
    g = m[(m.antibiotic == ab) & m.resistant_phenotype.isin(["resistant", "susceptible"])].copy()
    g["y"] = (g.resistant_phenotype == "resistant").astype(int)
    conf = g.groupby("genome_id").y.nunique(); drop = set(conf[conf > 1].index)
    g = g[~g.genome_id.isin(drop)].drop_duplicates("genome_id")
    g = g[g.genome_id.isin(pos)]
    idx = [pos[x] for x in g.genome_id]
    feat = [f"f{i}" for i in range(X.shape[1])]
    base = pd.DataFrame(X[idx], columns=feat); base["y"] = g.y.values
    for gname, col in (("st", "ST"), ("fastbaps", "fastbaps")):
        if only_g and gname != only_g: continue
        gv = g[col].values; ok = ~pd.isna(gv)
        df = base[ok].reset_index(drop=True); df["g"] = gv[ok].astype(int)
        res = run_audit(df, feat, "y", "g", models=("logreg", "rf", "gb"), repeats=reps, metric="auc")
        o = optimism(res); o["label"] = ab; o["label_prev"] = round(df.y.mean(), 3); o["grouping"] = gname
        o["n_groups"] = df.g.nunique(); o["n"] = len(df); o["dropped_conflicting"] = len(drop); rows.append(o)
        print(ab, gname, len(df), flush=True)
out = pd.concat(rows); tag = f"_{only_l}_{only_g}" if (only_l or only_g) else ""
out.to_csv(f"{outdir}/real_yu_ecoli_audit{tag}.csv", index=False); print(out.round(3).to_string())
