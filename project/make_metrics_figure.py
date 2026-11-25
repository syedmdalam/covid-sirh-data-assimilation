"""Summary figure of PF vs EnKF scores (values from the metrics cell of epi.ipynb)."""
import matplotlib.pyplot as plt
import numpy as np

metrics = {  # copied from epi.ipynb, cell "metrics" output
    "EnKF": {"MAE": 6.04, "RMSE": 17.41, "CRPS": 7.94, "CVG50": 0.974, "CVG90": 1.000},
    "PF":   {"MAE": 1018.02, "RMSE": 1638.54, "CRPS": 1016.30, "CVG50": 0.013, "CVG90": 0.038},
}
colors = {"EnKF": "#2a78d6", "PF": "#eb6834"}
ink, muted = "#0b0b0b", "#52514e"

plt.rcParams.update({"font.size": 11, "axes.edgecolor": muted, "axes.labelcolor": ink,
                     "xtick.color": muted, "ytick.color": muted})
fig, (a1, a2) = plt.subplots(1, 2, figsize=(11, 4.2), facecolor="#fcfcfb")
w = 0.36

def panel(ax, keys, labels, fmt, log=False):
    x = np.arange(len(keys))
    for i, m in enumerate(metrics):
        vals = [metrics[m][k] for k in keys]
        bars = ax.bar(x + (i - 0.5) * w, vals, w - 0.03, color=colors[m], label=m)
        for b, v in zip(bars, vals):
            ax.annotate(fmt(v), (b.get_x() + b.get_width() / 2, v), ha="center", va="bottom",
                        xytext=(0, 3), textcoords="offset points", fontsize=9, color=ink)
    ax.set_xticks(x, labels)
    ax.set_facecolor("#fcfcfb")
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(axis="y", color="#e6e5e0", lw=0.8)
    ax.set_axisbelow(True)
    if log:
        ax.set_yscale("log")

panel(a1, ["MAE", "RMSE", "CRPS"], ["MAE", "RMSE", "CRPS"], lambda v: f"{v:,.0f}" if v >= 100 else f"{v:.1f}", log=True)
a1.set_ylim(1, 2e4)
a1.set_ylabel("Hospitalizations (log scale)")
a1.set_title("Error: lower is better", loc="left", color=ink)

panel(a2, ["CVG50", "CVG90"], ["50% interval", "90% interval"], lambda v: f"{v:.0%}")
for xpos, nominal in [(0, 0.5), (1, 0.9)]:
    a2.hlines(nominal, xpos - 0.42, xpos + 0.42, colors=ink, linestyles="--", lw=1.2)
    a2.annotate(f"nominal {nominal:.0%}", (xpos + 0.42, nominal), xytext=(2, 3),
                textcoords="offset points", fontsize=8, color=muted, ha="right", va="bottom")
a2.set_ylim(0, 1.12)
a2.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v:.0%}"))
a2.set_ylabel("Share of observations inside interval")
a2.set_title("Interval coverage: closer to nominal is better", loc="left", color=ink)

a1.legend(frameon=False, loc="upper left")
fig.tight_layout()
fig.savefig("metrics_summary.png", dpi=150, facecolor=fig.get_facecolor())
