import pandas as pd, numpy as np, matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
e=pd.read_csv("real_ecoli_robustness.csv"); e=e[e.metric=="auc"]
s=pd.read_csv("real_soil_audit.csv")
col={"logreg":"#0072B2","rf":"#D55E00","gb":"#009E73"}; mk={"logreg":"o","rf":"s","gb":"D"}
off={"logreg":-0.22,"rf":0,"gb":0.22}
ink="#1f2933"; mute="#52606d"; grid="#e4e7eb"
elab={"ctxm":"CTX-M","teta":"tet(A)"}; egr={"st":"sequence type","phylogroup":"phylogroup","country":"country"}
erows=[(l,g) for l in ("ctxm","teta") for g in ("st","phylogroup","country")]
slab=list(dict.fromkeys(s.label)); sgr={"location":"site name","block10":"10 blocks","block20":"20 blocks"}
srows=[(l,g) for l in slab for g in ("location","block10","block20")]
fig,axs=plt.subplots(2,1,figsize=(8.2,10.2),gridspec_kw={"height_ratios":[len(erows),len(srows)]},sharex=True)
def panel(ax,df,rows,labkey,namefn,title):
    for i,(l,g) in enumerate(rows):
        y=len(rows)-1-i
        for m in ("logreg","rf","gb"):
            r=df[(df[labkey]==l)&(df.grouping==g if "grouping" in df else df.group==g)&(df.model==m)].iloc[0]
            yy=y+off[m]
            ax.plot([r.ci_lo,r.ci_hi],[yy,yy],color=col[m],lw=1.6,solid_capstyle="round",zorder=2)
            ax.plot(r.optimism,yy,mk[m],color=col[m],ms=5.5,mec="white",mew=0.8,zorder=3)
    ax.axvline(0,color=ink,lw=1,zorder=1)
    ax.set_yticks(range(len(rows))); ax.set_yticklabels([namefn(l,g) for l,g in rows][::-1],fontsize=8.5,color=ink)
    ax.set_ylim(-0.6,len(rows)-0.4); ax.grid(axis="x",color=grid,lw=0.8); ax.set_axisbelow(True)
    for sp in ("top","right","left"): ax.spines[sp].set_visible(False)
    ax.tick_params(axis="y",length=0)
    for k in range(3,len(rows),3): ax.axhline(len(rows)-k-0.5,color=grid,lw=0.8)
    ax.set_title(title,loc="left",fontsize=11,fontweight="bold",color=ink)
panel(axs[0],e,erows,"label",lambda l,g:f"{elab[l]} | {egr[g]}","A. E. coli genomes (738): 18 AUC cells, 5 repeats")
panel(axs[1],s,srows,"label",lambda l,g:f"{l} | {sgr[g]}","B. Scottish soil survey (199 samples): 45 AUC cells, 5 repeats")
axs[1].set_xlabel("Optimism = random-split AUC minus group-split AUC  (dot = mean, line = split-repeat interval)",fontsize=9,color=mute)
axs[0].legend(handles=[Line2D([0],[0],marker=mk[m],color=col[m],lw=1.6,ms=6,label={"logreg":"logistic regression","rf":"random forest","gb":"gradient boosting"}[m]) for m in col],
              loc="lower right",frameon=False,fontsize=8.5)
fig.suptitle("Random splits overstated AUC clearly in E. coli, but only slightly and inconsistently in soil",x=0.02,ha="left",fontsize=12,fontweight="bold",color=ink,y=0.995)
fig.text(0.02,0.012,"Intervals reflect repeated splits of one dataset only and understate uncertainty across datasets.",fontsize=8,color=mute)
fig.tight_layout(rect=(0,0.02,1,0.975))
fig.savefig("fig4_real_data_optimism.png",dpi=200,facecolor="white")
