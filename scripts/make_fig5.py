import sys, matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
fig, ax = plt.subplots(figsize=(11, 6.2)); ax.set_xlim(0, 11); ax.set_ylim(0, 6.2); ax.axis("off")
ink="#1f2933"; mute="#52606d"
def box(x,y,w,h,t,fc="#ffffff",ec="#3e4c59",bold=False):
    ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle="round,pad=0.02,rounding_size=0.08",fc=fc,ec=ec,lw=1.2))
    ax.text(x+w/2,y+h/2,t,ha="center",va="center",fontsize=9.5,color=ink,fontweight="bold" if bold else "normal",wrap=True)
def arr(x1,y1,x2,y2):
    ax.add_patch(FancyArrowPatch((x1,y1),(x2,y2),arrowstyle="-|>",mutation_scale=12,lw=1.2,color=mute))
ax.text(5.5,5.9,"SplitAudit: how to audit a grouped dataset",ha="center",fontsize=13,fontweight="bold",color=ink)
box(0.3,4.4,2.4,0.9,"1. Data table\nfeatures, label,\ngroup column")
box(3.3,4.4,2.4,0.9,"2. Declare groups\n(lineage, site, space,\nreplicates)")
box(6.3,4.4,2.4,0.9,"3. Same data, same model,\nthree splits: random,\nstratified, group-held-out")
box(9.0,4.4,1.7,0.9,"4. Optimism =\nrandom - group\n(+ interval)")
for a,b in [(2.7,3.3),(5.7,6.3),(8.7,9.0)]: arr(a,4.85,b,4.85)
box(0.3,2.5,3.3,1.2,"Hygiene checks (before splitting)\nlabel-duplicate features,\npreprocessing inside folds,\nnested tuning",fc="#e8f1fa")
box(3.9,2.5,3.3,1.2,"Diagnostic A\nSame-group nearest-neighbour\nrate vs chance:\nare groups identifiable?",fc="#e8f1fa")
box(7.5,2.5,3.2,1.2,"Diagnostic B\nWithin-group label permutation:\ngroup-split AUC should be ~0.5",fc="#e8f1fa")
arr(1.5,4.4,1.5,3.7); arr(7.5,4.4,5.55,3.7); arr(7.5,4.4,8.6,3.7)
box(2.2,1.85,6.6,0.5,"Read optimism (step 4) together with the checks above",fc="#f5f7fa")
for x in (1.95,5.55,9.1): arr(x,2.5,min(max(x,3.0),8.0),2.35)
box(0.3,0.3,4.9,1.05,"Small optimism: random split gives a similar\nanswer on this dataset. Still report both scores\n(a high NN rate signals risk, not certainty).",fc="#eef6ee")
box(5.8,0.3,4.9,1.05,"Large optimism: report the group-split score\nas the headline and state what the\ninterval covers.",fc="#fdf1e3")
arr(4.0,1.85,2.75,1.35); arr(7.0,1.85,8.25,1.35)
ax.text(5.5,-0.1,"Blue = diagnostics; optimism measures sensitivity to the split, not model correctness.",ha="center",fontsize=8.5,color=mute)
fig.savefig((sys.argv[1] if len(sys.argv)>1 else "docs")+"/fig5_audit_flow.png",dpi=200,bbox_inches="tight",facecolor="white")
