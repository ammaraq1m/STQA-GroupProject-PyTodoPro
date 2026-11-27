"""Generate static figures from recorded Locust CSV rows."""
import csv
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
with (ROOT / "results" / "performance.csv").open() as stream:
    rows = list(csv.DictReader(stream))
users = sorted({int(row["users"]) for row in rows})
endpoints = ["/", "/dashboard", "/api/tasks", "/api/dashboard"]
palette = ["#17689a", "#67428d", "#a75019", "#147871"]


def plot_metric(ax, key, label, series, colors):
    for endpoint, color in zip(series, colors):
        records = sorted((row for row in rows if row["endpoint"] == endpoint),
                         key=lambda row: int(row["users"]))
        ax.plot([int(row["users"]) for row in records], [float(row[key]) for row in records],
                marker="o", color=color, label=endpoint)
    ax.set(xlabel="Concurrent simulated users", ylabel=label, xticks=users)
    ax.grid(alpha=.22)


fig, axes = plt.subplots(1,3, figsize=(13,4.2), layout="constrained")
for ax, key, label in zip(axes, ("mean_ms","median_ms","p95_ms"), ("Mean (ms)","Median (ms)","95th percentile (ms)")):
    plot_metric(ax,key,label,endpoints,palette)
axes[0].legend(loc="upper left",fontsize=8)
fig.suptitle("PyTodo Pro · Response time by endpoint and workload")
fig.savefig(ROOT/"charts"/"latency.png",dpi=155)
plt.close(fig)

fig, axes = plt.subplots(1,2, figsize=(9,4.2), layout="constrained")
plot_metric(axes[0],"requests_per_s","Requests per second",["Aggregated"],["#17689a"])
plot_metric(axes[1],"error_pct","Failed requests (%)",["Aggregated"],["#a75019"])
axes[1].set_ylim(-.2, max(1, max(float(row["error_pct"]) for row in rows)+.2))
fig.suptitle("PyTodo Pro · Aggregate throughput and failure rate")
fig.savefig(ROOT/"charts"/"throughput-errors.png",dpi=155)
plt.close(fig)
