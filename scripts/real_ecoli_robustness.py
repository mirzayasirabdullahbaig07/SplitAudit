"""Usage: python scripts/real_ecoli_robustness.py [prepared_csv] [out_csv]"""
import sys, pandas as pd, numpy as np
from splitaudit.audit import run_audit, optimism, same_group_nn_rate
src=sys.argv[1] if len(sys.argv)>1 else 'data/ecoli_resistome/ecoli_ctxm_prepared.csv'
out_csv=sys.argv[2] if len(sys.argv)>2 else 'docs/real_ecoli_robustness.csv'
df0=pd.read_csv(src)
gcols=[c for c in df0.columns if c.startswith('g_')]
labels={'ctxm':(df0['y'],gcols),
        'teta':((df0[[c for c in gcols if 'tet(a)' in c.lower()]].sum(axis=1)>0).astype(int),
                [c for c in gcols if 'tet(a)' not in c.lower()])}
rows=[]
for ln,(y,feat) in labels.items():
    for grp in ['st','phylogroup','country']:
        d=df0[feat+[grp]].copy(); d['y']=y.values
        for metric in ['auc','bacc']:
            res=run_audit(d,feat,'y',grp,models=('logreg','rf','gb'),repeats=5,metric=metric)
            op=optimism(res)
            op['label']=ln; op['group']=grp; op['metric']=metric
            rows.append(op); print(ln,grp,metric,flush=True)
out=pd.concat(rows); out.to_csv(out_csv,index=False); print(out.to_string())
