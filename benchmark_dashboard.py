import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# -----------------------------
# Load data
# -----------------------------
df = pd.read_csv("results.csv")

required_columns = [
    "n",
    "nn_cost", "nn_time_us",
    "nn2opt_cost", "nn2opt_time_us",
    "bruteforce_cost", "bruteforce_time_us"
]

missing = [c for c in required_columns if c not in df.columns]
if missing:
    raise ValueError(f"Missing columns in results.csv: {missing}")

df = df[
    (df["nn_cost"] > 0) &
    (df["nn2opt_cost"] > 0) &
    (df["bruteforce_cost"] > 0) &
    (df["nn_time_us"] > 0) &
    (df["nn2opt_time_us"] > 0) &
    (df["bruteforce_time_us"] > 0)
].copy()

summary = df.groupby("n").agg(
    nn_cost_mean=("nn_cost", "mean"),
    nn_time_mean=("nn_time_us", "mean"),
    nn2opt_cost_mean=("nn2opt_cost", "mean"),
    nn2opt_time_mean=("nn2opt_time_us", "mean"),
    bruteforce_cost_mean=("bruteforce_cost", "mean"),
    bruteforce_time_mean=("bruteforce_time_us", "mean")
).reset_index()

summary["nn_quality_ratio"] = summary["nn_cost_mean"] / summary["bruteforce_cost_mean"]
summary["nn2opt_quality_ratio"] = summary["nn2opt_cost_mean"] / summary["bruteforce_cost_mean"]
summary["two_opt_improvement_pct"] = (
    (summary["nn_cost_mean"] - summary["nn2opt_cost_mean"]) / summary["nn_cost_mean"] * 100.0
)

# -----------------------------
# Build dashboard
# -----------------------------
fig = make_subplots(
    rows=2, cols=2,
    subplot_titles=(
        "Runtime Scalability",
        "Solution Quality",
        "Relative Solution Quality",
        "2-opt Improvement"
    )
)

# Runtime
fig.add_trace(
    go.Scatter(x=summary["n"], y=summary["nn_time_mean"], mode="lines+markers", name="Nearest Neighbor"),
    row=1, col=1
)
fig.add_trace(
    go.Scatter(x=summary["n"], y=summary["nn2opt_time_mean"], mode="lines+markers", name="NN + 2-opt"),
    row=1, col=1
)
fig.add_trace(
    go.Scatter(x=summary["n"], y=summary["bruteforce_time_mean"], mode="lines+markers", name="Brute Force"),
    row=1, col=1
)

# Solution quality
fig.add_trace(
    go.Scatter(x=summary["n"], y=summary["nn_cost_mean"], mode="lines+markers", name="NN Cost"),
    row=1, col=2
)
fig.add_trace(
    go.Scatter(x=summary["n"], y=summary["nn2opt_cost_mean"], mode="lines+markers", name="NN+2opt Cost"),
    row=1, col=2
)
fig.add_trace(
    go.Scatter(x=summary["n"], y=summary["bruteforce_cost_mean"], mode="lines+markers", name="Brute Force Cost"),
    row=1, col=2
)

# Relative quality
fig.add_trace(
    go.Scatter(x=summary["n"], y=summary["nn_quality_ratio"], mode="lines+markers", name="NN / Optimal"),
    row=2, col=1
)
fig.add_trace(
    go.Scatter(x=summary["n"], y=summary["nn2opt_quality_ratio"], mode="lines+markers", name="NN+2opt / Optimal"),
    row=2, col=1
)

# 2-opt improvement
fig.add_trace(
    go.Scatter(x=summary["n"], y=summary["two_opt_improvement_pct"], mode="lines+markers", name="2-opt Improvement (%)"),
    row=2, col=2
)

fig.update_layout(
    title="Traveling Salesman Problem Benchmark Dashboard",
    height=850,
    width=1200,
    template="plotly_white"
)

fig.update_xaxes(title_text="Number of vertices")
fig.update_yaxes(title_text="Runtime (microseconds)", type="log", row=1, col=1)
fig.update_yaxes(title_text="Average tour cost", row=1, col=2)
fig.update_yaxes(title_text="Cost ratio", row=2, col=1)
fig.update_yaxes(title_text="Improvement (%)", row=2, col=2)

fig.write_html("benchmark_dashboard.html", include_plotlyjs="cdn")
print("Generated: benchmark_dashboard.html")