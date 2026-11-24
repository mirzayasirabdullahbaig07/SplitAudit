"""Fig 3: optimism heatmap over number of groups x rows per group (rho=1, fingerprint SD=1.5).
Input: docs/synthetic_sensitivity_raw.csv  Output: docs/fig3_sensitivity.png"""
import sys, numpy as np, pandas as pd, matplotlib; matplotlib.use("Agg")
from scipy import stats
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
src = sys.argv[1] if len(sys.argv) > 1 else "docs/synthetic_sensitivity_raw.csv"
out = sys.argv[2] if len(sys.argv) > 2 else "docs/fig3_sensitivity.png"
t = pd.read_csv(src)
g = t.groupby(["model", "n_groups", "per_group"]).optimism
m = g.mean().reset_index()
m["half"] = (g.std(ddof=1) / np.sqrt(g.count()) * stats.t.ppf(0.975, g.count() - 1)).values
N = int(t.seed.nunique())
SURF, INK, INK2 = "#fcfcfb", "#0b0b0b", "#52514e"
cmap = LinearSegmentedColormap.from_list("blue", ["#eaf2fc", "#2a78d6", "#123f78"])
vmax = m.optimism.max()
names = {"logreg": "Logistic regression", "rf": "Random forest"}
fig, axs = plt.subplots(1, 2, figsize=(9, 3.9), facecolor=SURF)
for ax, mod in zip(axs, ["logreg", "rf"]):
    p = m[m.model == mod].pivot(index="n_groups", columns="per_group", values="optimism").sort_index(ascending=False)
    hw = m[m.model == mod].pivot(index="n_groups", columns="per_group", values="half").sort_index(ascending=False)
    ax.imshow(p.values, cmap=cmap, vmin=0, vmax=vmax, aspect="auto")
    for i in range(p.shape[0]):
        for j in range(p.shape[1]):
            v = p.values[i, j]
            ax.text(j, i, f"{v:.2f}\n±{hw.values[i, j]:.2f}", ha="center", va="center", fontsize=10.5,
                    color="white" if v > 0.6 * vmax else INK)
    ax.set_xticks(range(p.shape[1])); ax.set_xticklabels(p.columns)
    ax.set_yticks(range(p.shape[0])); ax.set_yticklabels(p.index)
    ax.set_title(names[mod], loc="left", fontsize=11, color=INK)
    ax.set_xlabel("Rows per group", color=INK2); ax.tick_params(colors=INK2, length=0)
    for s in ax.spines.values(): s.set_visible(False)
axs[0].set_ylabel("Number of groups", color=INK2)
fig.suptitle("Optimism by number of groups and rows per group",
             x=0.01, y=1.0, ha="left", fontsize=12, color=INK)
fig.text(0.01, 0.9, f"Mean optimism (random − group AUC) ± 95% t-interval over {N} simulated datasets per cell; rho = 1, fingerprint SD = 1.5",
         fontsize=9, color=INK2)
fig.tight_layout(rect=(0, 0, 1, 0.88))
fig.savefig(out, dpi=200, facecolor=SURF, bbox_inches="tight")
