import pandas as pd
import matplotlib.pyplot as plt

# -----------------------------
# Load and validate raw data
# -----------------------------
df = pd.read_csv("results.csv")

required_columns = [
    "n",
    "nn_cost", "nn_time_us",
    "nn2opt_cost", "nn2opt_time_us",
    "bruteforce_cost", "bruteforce_time_us"
]

missing = [col for col in required_columns if col not in df.columns]
if missing:
    raise ValueError(f"Missing required columns in results.csv: {missing}")

# Keep only valid rows
df = df[
    (df["nn_cost"] > 0) &
    (df["nn2opt_cost"] > 0) &
    (df["bruteforce_cost"] > 0) &
    (df["nn_time_us"] > 0) &
    (df["nn2opt_time_us"] > 0) &
    (df["bruteforce_time_us"] > 0)
].copy()

if df.empty:
    raise ValueError("No valid benchmark rows found after filtering.")

# -----------------------------
# Aggregate
# -----------------------------
summary = df.groupby("n").agg(
    nn_cost_mean=("nn_cost", "mean"),
    nn_cost_std=("nn_cost", "std"),
    nn_time_mean=("nn_time_us", "mean"),
    nn_time_std=("nn_time_us", "std"),
    nn2opt_cost_mean=("nn2opt_cost", "mean"),
    nn2opt_cost_std=("nn2opt_cost", "std"),
    nn2opt_time_mean=("nn2opt_time_us", "mean"),
    nn2opt_time_std=("nn2opt_time_us", "std"),
    bruteforce_cost_mean=("bruteforce_cost", "mean"),
    bruteforce_cost_std=("bruteforce_cost", "std"),
    bruteforce_time_mean=("bruteforce_time_us", "mean"),
    bruteforce_time_std=("bruteforce_time_us", "std"),
    samples=("n", "count")
).reset_index()

summary = summary.fillna(0)

# -----------------------------
# Derived metrics
# -----------------------------
summary["nn_quality_ratio"] = summary["nn_cost_mean"] / summary["bruteforce_cost_mean"]
summary["nn2opt_quality_ratio"] = summary["nn2opt_cost_mean"] / summary["bruteforce_cost_mean"]
summary["two_opt_improvement_pct"] = (
    (summary["nn_cost_mean"] - summary["nn2opt_cost_mean"]) / summary["nn_cost_mean"] * 100.0
)

# Rounded summary for easier reading
summary_export = summary.copy()
for col in summary_export.columns:
    if col != "n" and col != "samples":
        summary_export[col] = summary_export[col].round(3)

summary_export.to_csv("benchmark_summary.csv", index=False)

# A lightweight table for README / HR-friendly viewing
readme_table = summary[[
    "n",
    "nn_time_mean",
    "nn2opt_time_mean",
    "bruteforce_time_mean",
    "nn_quality_ratio",
    "nn2opt_quality_ratio",
    "two_opt_improvement_pct"
]].copy()

readme_table.columns = [
    "n",
    "NN runtime (us)",
    "NN+2opt runtime (us)",
    "Brute Force runtime (us)",
    "NN / Optimal",
    "NN+2opt / Optimal",
    "2-opt improvement (%)"
]

readme_table = readme_table.round(3)
readme_table.to_csv("benchmark_readme_table.csv", index=False)

# -----------------------------
# 1. Runtime scalability
# Use log scale so NN is visible
# -----------------------------
plt.figure(figsize=(8, 5))
plt.plot(summary["n"], summary["nn_time_mean"], marker="o", label="Nearest Neighbor")
plt.plot(summary["n"], summary["nn2opt_time_mean"], marker="o", label="Nearest Neighbor + 2-opt")
plt.plot(summary["n"], summary["bruteforce_time_mean"], marker="o", label="Brute Force")
plt.yscale("log")
plt.xlabel("Number of vertices")
plt.ylabel("Average runtime (microseconds, log scale)")
plt.title("Runtime Scalability")
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig("01_runtime_scalability.png", dpi=300)
plt.close()

# -----------------------------
# 2. Solution quality comparison
# -----------------------------
plt.figure(figsize=(8, 5))
plt.plot(summary["n"], summary["nn_cost_mean"], marker="o", label="Nearest Neighbor")
plt.plot(summary["n"], summary["nn2opt_cost_mean"], marker="o", label="Nearest Neighbor + 2-opt")
plt.plot(summary["n"], summary["bruteforce_cost_mean"], marker="o", label="Brute Force")
plt.xlabel("Number of vertices")
plt.ylabel("Average tour cost")
plt.title("Solution Quality Comparison")
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig("02_solution_quality.png", dpi=300)
plt.close()

# -----------------------------
# 3. Relative solution quality
# -----------------------------
plt.figure(figsize=(8, 5))
plt.plot(summary["n"], summary["nn_quality_ratio"], marker="o", label="NN / Optimal")
plt.plot(summary["n"], summary["nn2opt_quality_ratio"], marker="o", label="NN + 2-opt / Optimal")
plt.axhline(1.0, linestyle="--", label="Optimal")
plt.xlabel("Number of vertices")
plt.ylabel("Cost ratio")
plt.title("Relative Solution Quality")
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig("03_relative_quality.png", dpi=300)
plt.close()

# -----------------------------
# 4. Impact of 2-opt
# -----------------------------
plt.figure(figsize=(8, 5))
plt.plot(summary["n"], summary["two_opt_improvement_pct"], marker="o")
plt.xlabel("Number of vertices")
plt.ylabel("Improvement over NN (%)")
plt.title("Impact of 2-opt Optimization")
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig("04_two_opt_impact.png", dpi=300)
plt.close()

# -----------------------------
# 5. Runtime vs solution quality trade-off
# -----------------------------
tradeoff = pd.DataFrame({
    "n": pd.concat([df["n"], df["n"]], ignore_index=True),
    "runtime_us": pd.concat([df["nn_time_us"], df["nn2opt_time_us"]], ignore_index=True),
    "cost": pd.concat([df["nn_cost"], df["nn2opt_cost"]], ignore_index=True),
    "algorithm": ["Nearest Neighbor"] * len(df) + ["Nearest Neighbor + 2-opt"] * len(df)
})

plt.figure(figsize=(8, 5))
for algo in tradeoff["algorithm"].unique():
    subset = tradeoff[tradeoff["algorithm"] == algo]
    plt.scatter(subset["runtime_us"], subset["cost"], alpha=0.7, label=algo)
plt.xlabel("Runtime (microseconds)")
plt.ylabel("Tour cost")
plt.title("Speed vs Solution Quality Trade-off")
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig("05_tradeoff_runtime_vs_quality.png", dpi=300)
plt.close()

# -----------------------------
# 6. Error bars for stability
# -----------------------------
plt.figure(figsize=(8, 5))
plt.errorbar(
    summary["n"], summary["nn2opt_cost_mean"],
    yerr=summary["nn2opt_cost_std"],
    marker="o", capsize=4, label="NN + 2-opt"
)
plt.errorbar(
    summary["n"], summary["nn_cost_mean"],
    yerr=summary["nn_cost_std"],
    marker="o", capsize=4, label="Nearest Neighbor"
)
plt.xlabel("Number of vertices")
plt.ylabel("Average tour cost ± std")
plt.title("Solution Stability Across Random Graphs")
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig("06_solution_stability.png", dpi=300)
plt.close()

print("Generated files:")
print("- benchmark_summary.csv")
print("- benchmark_readme_table.csv")
print("- 01_runtime_scalability.png")
print("- 02_solution_quality.png")
print("- 03_relative_quality.png")
print("- 04_two_opt_impact.png")
print("- 05_tradeoff_runtime_vs_quality.png")
print("- 06_solution_stability.png")