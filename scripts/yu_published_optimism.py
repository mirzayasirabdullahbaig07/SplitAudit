"""Optimism from the authors' published results (TS2.tsv): random-split AUC minus clade-split AUC.
This re-analyses PUBLISHED numbers (LightGBM only); it is not our own audit.
usage: python yu_published_optimism.py TS2.tsv out_cells.csv out_summary.csv"""
import sys, numpy as np, pandas as pd
d=pd.read_csv(sys.argv[1],sep='\t'); d['case']=d['case'].astype(str)
d['species']=d['species'].replace({'extend_E_coli':'Escherichia coli'})  # clade rows say 'Escherichia coli', random rows 'extend_E_coli' (same 11 antibiotics)
cmap={'A-a':'0','A-b':'1','A-c':'2','A-d':'3','B-a':'0','B-b':'1'}
g=d[d.split=='scheme'].copy(); g['k']=g['case'].map(cmap)
r=d[d.split=='random'].copy(); r['k']=r['case']
key=['species','antibiotic','scheme','k']
a=g.groupby(key).agg(auc_group=('AUC score','mean'),bacc_group=('Balanced accuracy score','mean'),n_group=('AUC score','size'),distance=('distance','mean'),R1=('R1','mean'),S1=('S1','mean'),Rn=('Rn','mean'),Sn=('Sn','mean'),MOA=('MOA','first'),drug_class=('drug_class','first')).reset_index()
b=r.groupby(key).agg(auc_random=('AUC score','mean'),bacc_random=('Balanced accuracy score','mean'),n_random=('AUC score','size'),R1r=('R1','mean'),S1r=('S1','mean'),Rnr=('Rn','mean'),Snr=('Sn','mean')).reset_index()
m=a.merge(b,on=key,how='inner')
m['train_size_diff']=(m.R1+m.S1-m.R1r-m.S1r).abs()
m['optimism_auc']=m.auc_random-m.auc_group; m['optimism_bacc']=m.bacc_random-m.bacc_group
m.to_csv(sys.argv[2],index=False)
print(len(a),len(b),len(m)); print('max train-size diff',m.train_size_diff.max(),'median',m.train_size_diff.median())
def s(x):
    return pd.Series({'cells':len(x),'positive':(x.optimism_auc>0).sum(),'median_auc_opt':x.optimism_auc.median(),'mean_auc_opt':x.optimism_auc.mean(),'min':x.optimism_auc.min(),'max':x.optimism_auc.max(),'median_bacc_opt':x.optimism_bacc.median()})
out=pd.concat([s(m).to_frame('ALL').T, m.groupby('species').apply(s), m.groupby('scheme').apply(s).rename(index=lambda i:'scheme '+i)])
out.to_csv(sys.argv[3]); print(out.round(3).to_string())
