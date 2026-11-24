import numpy as np, matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, FancyArrowPatch
rng=np.random.default_rng(3)
centers=np.array([[1.3,4.1],[3.75,4.1],[6.2,4.1],[1.3,1.4],[3.75,1.4],[6.2,1.4]]); names="ABCDEF"
pts=[];grp=[]
for i,c in enumerate(centers):
    p=[]
    while len(p)<10:
        q=rng.normal(0,0.36,2)
        if (q[0]/0.95)**2+(q[1]/0.72)**2<1: p.append(c+q)
    pts.append(np.array(p)); grp+=[i]*10
pts=np.vstack(pts); grp=np.array(grp)
ink="#1f2933"; mute="#52606d"; train="#7b8794"; test="#D55E00"; blue="#0072B2"
fig,axs=plt.subplots(1,2,figsize=(11,5.2))
def base(ax,title,sub):
    ax.set_xlim(0,7.5); ax.set_ylim(0,5.4); ax.set_aspect("equal"); ax.axis("off")
    ax.set_title(title,loc="left",fontsize=12,fontweight="bold",color=ink,pad=26)
    ax.text(0,5.55,sub,fontsize=9.5,color=mute,va="bottom")
    for i,c in enumerate(centers):
        ax.add_patch(Ellipse(c,2.1,1.62,fc="none",ec="#cbd2d9",lw=1.2,ls="--"))
        ax.text(c[0],c[1]+0.92,"group "+names[i],ha="center",fontsize=8.5,color=mute)
# A random
ax=axs[0]; base(ax,"A. Random split","Rows from the same group land in both train and test")
is_test=np.zeros(len(pts),bool); is_test[rng.choice(len(pts),12,replace=False)]=True
for idx in np.where(is_test)[0]:
    d=np.linalg.norm(pts[~is_test]-pts[idx],axis=1); j=np.where(~is_test)[0][d.argmin()]
    ax.add_patch(FancyArrowPatch(pts[idx],pts[j],arrowstyle="-",lw=1.0,color=blue,alpha=0.8,shrinkA=3,shrinkB=3))
ax.scatter(*pts[~is_test].T,s=34,c=train,zorder=3,ec="white",lw=0.6)
ax.scatter(*pts[is_test].T,s=60,c=test,marker="s",zorder=4,ec="white",lw=0.8)
ax.text(3.75,0.12,"Blue lines: each test row's nearest training row is usually a groupmate",ha="center",fontsize=8.5,color=blue)
# B group
ax=axs[1]; base(ax,"B. Group split","Whole groups are held out: no group appears on both sides")
test_g=[2,5]; is_test=np.isin(grp,test_g)
ax.scatter(*pts[~is_test].T,s=34,c=train,zorder=3,ec="white",lw=0.6)
ax.scatter(*pts[is_test].T,s=60,c=test,marker="s",zorder=4,ec="white",lw=0.8)
ax.text(3.75,0.12,"Same-group nearest-neighbour rate is exactly 0 by construction",ha="center",fontsize=8.5,color=blue)
from matplotlib.lines import Line2D
fig.legend(handles=[Line2D([0],[0],marker="o",color="w",mfc=train,ms=7,label="training row"),Line2D([0],[0],marker="s",color="w",mfc=test,ms=8,label="test row")],loc="lower center",ncol=2,frameon=False,fontsize=9.5)
fig.suptitle("Where leakage enters: group identity is recognisable only when groups share a split",x=0.02,y=0.985,ha="left",fontsize=12.5,fontweight="bold",color=ink)
fig.text(0.02,0.075,"Toy illustration with simulated points (not data from this study). Optimism = random-split score minus group-split score.",fontsize=8,color=mute)
fig.tight_layout(rect=(0,0.09,1,0.92))
fig.savefig("fig1_split_schematic.png",dpi=200,facecolor="white")
