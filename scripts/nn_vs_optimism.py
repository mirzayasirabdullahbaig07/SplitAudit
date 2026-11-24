"""Does same-group NN rate (excess over chance) track optimism? Pools simulation (rho=1), E. coli (3 groupings x 2 labels x models, AUC) and soil (45 cells).
Usage: python nn_vs_optimism.py <docs_dir> <soil_csv> <out_csv>"""
import sys, numpy as np, pandas as pd
from scipy import stats
from sklearn.cluster import KMeans
D, soil_csv, out = sys.argv[1:4]
rows=[]
# simulation: rho=1; chance = 1/40 (40 groups of equal size)
sim=pd.read_csv(f"{D}/synthetic_multiseed_summary.csv"); nn=pd.read_csv(f"{D}/synthetic_nn_diagnostic.csv")
nnm=nn[nn.scheme=="random"].groupby("fp_sd").nn_same_group.mean()
for _,r in sim[sim.rho==1.0].iterrows():
    rows.append(dict(dataset="simulation",cell=f"fp{r.fp_sd}|{r.model}",nn=nnm[r.fp_sd],chance=1/40,optimism=r.optimism_mean,model=r.model))
# E. coli (AUC rows)
e=pd.read_csv(f"{D}/real_ecoli_robustness.csv"); e=e[e.metric=="auc"]
ch={"st":0.025,"phylogroup":0.201,"country":0.113}
for _,r in e.iterrows():
    rows.append(dict(dataset="E. coli",cell=f"{r.label}|{r.group}|{r.model}",nn=r.nn_same_group_random,chance=ch[r.group],optimism=r.optimism,model=r.model))
# soil: chance = sum p_g^2 from group sizes
s=pd.read_csv(f"{D}/real_soil_audit.csv")
d=pd.read_csv(soil_csv,encoding="latin1"); d.columns=[c.replace("ï»¿","") for c in d.columns]
d=d[d.Latitude.between(54,61)&d.Longitude.between(-8,-1)].reset_index(drop=True)
xy=np.c_[d.Longitude*np.cos(np.radians(d.Latitude)),d.Latitude]
grp={"location":d.LOCATION.values,"block10":KMeans(10,n_init=10,random_state=0).fit_predict(xy),"block20":KMeans(20,n_init=10,random_state=0).fit_predict(xy)}
chs={k:float(((pd.Series(v).value_counts(normalize=True))**2).sum()) for k,v in grp.items()}
print("soil chance levels:",{k:round(v,3) for k,v in chs.items()})
for _,r in s.iterrows():
    rows.append(dict(dataset="soil",cell=f"{r.label}|{r.grouping}|{r.model}",nn=r.nn_same_group_random,chance=chs[r.grouping],optimism=r.optimism,model=r.model))
t=pd.DataFrame(rows); t["excess_nn"]=t.nn-t.chance; t.to_csv(out,index=False)
for name,g in t.groupby("dataset"):
    rho,p=stats.spearmanr(g.excess_nn,g.optimism); print(name,len(g),"spearman",round(rho,2),"p",round(p,4),"excess range",round(g.excess_nn.min(),3),round(g.excess_nn.max(),3))
real=t[t.dataset!="simulation"]; rho,p=stats.spearmanr(real.excess_nn,real.optimism); print("real pooled",len(real),round(rho,2),round(p,4))
allp=t; rho,p=stats.spearmanr(allp.excess_nn,allp.optimism); print("all pooled",len(allp),round(rho,2),round(p,4))
print(t.groupby('dataset')[['excess_nn','optimism']].agg(['min','median','max']).round(3))
