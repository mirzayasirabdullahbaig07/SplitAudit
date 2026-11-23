"""Fig 2: optimism (random - group AUC) vs rho, by fingerprint strength and model.
Input: docs/synthetic_multiseed_summary.csv  Output: docs/fig2_optimism_vs_rho.png"""
import sys, pandas as pd, matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
src = sys.argv[1] if len(sys.argv) > 1 else "docs/synthetic_multiseed_summary.csv"
out = sys.argv[2] if len(sys.argv) > 2 else "docs/fig2_optimism_vs_rho.png"
t = pd.read_csv(src)
SURF, INK, INK2, GRID = "#fcfcfb", "#0b0b0b", "#52514e", "#e6e5e1"
STY = {"logreg": ("Logistic regression", "#2a78d6", "o"),
       "rf": ("Random forest", "#eb6834", "s"),
       "gb": ("Gradient boosting", "#1baf7a", "^")}
fps = sorted(t.fp_sd.unique())
fig, axs = plt.subplots(1, len(fps), figsize=(11, 3.8), sharey=True, facecolor=SURF)
for ax, fp in zip(axs, fps):
    ax.set_facecolor(SURF)
    for m, (name, col, mk) in STY.items():
        d = t[(t.fp_sd == fp) & (t.model == m)].sort_values("rho")
        ax.fill_between(d.rho, d.ci_lo, d.ci_hi, color=col, alpha=0.15, linewidth=0)
        ax.plot(d.rho, d.optimism_mean, color=col, lw=2, marker=mk, ms=7,
                markeredgecolor=SURF, markeredgewidth=1.5, label=name)
    ax.axhline(0, color=INK2, lw=0.8, ls=(0, (3, 3)))
    ax.set_title(f"Fingerprint SD = {fp:g}", fontsize=11, color=INK, loc="left", pad=8)
    ax.set_xlabel("Group label effect ρ", color=INK2)
    ax.set_xlim(-0.12, 1.12); ax.set_xticks([0, 0.5, 1]); ax.grid(axis="y", color=GRID, lw=0.8)
    ax.tick_params(colors=INK2, length=0)
    for s in ("top", "right", "left"): ax.spines[s].set_visible(False)
    ax.spines["bottom"].set_color(GRID)
axs[0].set_ylabel("Optimism (random − group AUC)", color=INK2)
h, l = axs[0].get_legend_handles_labels()
fig.legend(h, l, loc="lower center", ncol=3, frameon=False, labelcolor=INK2, bbox_to_anchor=(0.5, -0.02))
fig.suptitle("Random splits overstate AUC only when groups are identifiable from the features",
             x=0.01, y=1.0, ha="left", fontsize=12.5, color=INK)
fig.text(0.01, 0.915, "Mean over 8 simulated datasets; bands = 95% t-interval across datasets; dashed line = no optimism",
         fontsize=9, color=INK2)
fig.tight_layout(rect=(0, 0.06, 1, 0.97))
fig.savefig(out, dpi=200, facecolor=SURF, bbox_inches="tight")
