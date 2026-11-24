"""Prepare the E. coli resistome matrix for SplitAudit.
Input : data/ecoli_resistome/Tabla_completa_filtrada_con_MOB.csv  (Mendeley Data, doi 10.17632/r5ccbmsnhw.1)
Output: data/ecoli_resistome/ecoli_ctxm_prepared.csv
Task  : predict whether a genome carries a CTX-M gene (ESBL marker) from the OTHER resistance-gene presence columns.
Groups: st (Achtman sequence type), phylogroup, country  -> use with `splitaudit audit --group <col>`.
Usage : python scripts/prepare_ecoli.py [in_csv] [out_csv]
"""
import sys, numpy as np, pandas as pd
src = sys.argv[1] if len(sys.argv) > 1 else "data/ecoli_resistome/Tabla_completa_filtrada_con_MOB.csv"
out = sys.argv[2] if len(sys.argv) > 2 else "data/ecoli_resistome/ecoli_ctxm_prepared.csv"
df = pd.read_csv(src, low_memory=False)
gene_cols = [c for c in df.columns[8:] if not c.endswith("_Location")]      # presence/absence columns only
X = df[gene_cols].apply(pd.to_numeric, errors="coerce").fillna(0).clip(0, 1).astype(int)
ctxm = [c for c in gene_cols if "CTX-M" in c.upper()]   # the table lists genes under two naming schemes (e.g. blaCTX-M-15_1 and CTX-M-15): remove both
y = (X[ctxm].sum(axis=1) > 0).astype(int)
feat = [c for c in gene_cols if c not in ctxm]                              # label genes removed from features
X = X[feat]
X = X.loc[:, X.sum() > 0]                                                   # drop never-present columns
out_df = pd.DataFrame({"y": y})
out_df["st"] = "ST" + df["ST atchman"].round().astype("Int64").astype(str)
out_df["phylogroup"] = df["Grupo filogenetico"].astype(str).str.strip()
out_df["country"] = df["Pais"].astype(str).str.strip()
out_df = pd.concat([out_df, X.add_prefix("g_")], axis=1)
out_df = out_df.dropna(subset=["st"]).reset_index(drop=True)                 # rows without a sequence type are dropped
out_df.to_csv(out, index=False)
print(f"rows {len(out_df)}, features {X.shape[1]}, CTX-M columns removed {len(ctxm)}, positive rate {y.mean():.3f}")
for g in ("st", "phylogroup", "country"):
    s = out_df[g].value_counts()
    print(f"{g}: {len(s)} groups, largest {s.iloc[0]} rows ({s.index[0]}), groups with >=5 rows: {(s>=5).sum()}")
