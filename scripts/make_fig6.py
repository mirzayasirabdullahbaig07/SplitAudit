import sys, pandas as pd, matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
src=sys.argv[1] if len(sys.argv)>1 else "docs/nn_vs_optimism.csv"; out=sys.argv[2] if len(sys.argv)>2 else "docs/fig6_identifiability_vs_optimism.png"
t=pd.read_csv(src)
col={"simulation":"#009E73","E. coli":"#D55E00","E. coli (Yu)":"#CC79A7","Salmonella (Yu)":"#E69F00","soil":"#0072B2"}; mk={"logreg":"o","rf":"s","gb":"D"}
ink="#1f2933"; mute="#52606d"
fig,ax=plt.subplots(figsize=(8,5.4))
for ds,g in t.groupby("dataset"):
    for m,h in g.groupby("model"):
        ax.scatter(h.excess_nn,h.optimism,s=46,marker=mk[m],c=col[ds],alpha=0.8,ec="white",lw=0.7,zorder=3)
ax.axhline(0,color=ink,lw=1,zorder=1); ax.grid(color="#e4e7eb",lw=0.8); ax.set_axisbelow(True)
for sp in ("top","right"): ax.spines[sp].set_visible(False)
ax.set_xlabel("Group identifiability: same-group nearest-neighbour rate minus chance (random split)",fontsize=9.5,color=mute)
ax.set_ylabel("Optimism (random minus group AUC)",fontsize=9.5,color=mute)
h1=[Line2D([0],[0],marker="o",color="w",mfc=col[k],ms=8,label=k) for k in col]
h2=[Line2D([0],[0],marker=mk[m],color="w",mfc="#9aa5b1",ms=8,label=l) for m,l in (("logreg","logistic regression"),("rf","random forest"),("gb","gradient boosting"))]
ax.legend(handles=h1+h2,loc="upper left",frameon=False,fontsize=9)
ax.set_title("Group identifiability and optimism across the five settings",loc="left",fontsize=11,fontweight="bold",color=ink)
fig.text(0.01,0.012,"Simulation: rho = 1, 3 fingerprint levels x 3 models. E. coli: 18 AUC cells (3 groupings). E. coli (Yu) and Salmonella (Yu): 30 cells each (2 groupings).\nSoil: 45 cells (3 groupings). Few distinct x values per dataset and cells are not independent: descriptive only, no p-values.",fontsize=7.5,color=mute)
fig.tight_layout(rect=(0,0.08,1,1)); fig.savefig(out,dpi=200,facecolor="white")
