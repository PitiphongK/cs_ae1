import pandas as pd
import matplotlib.pyplot as plt

# --- Load benchmark data ---
bench = pd.read_csv("Cloud Systems Benchmarking AE1 - Sheet1.csv")

bench["vCPUs"] = pd.to_numeric(bench["vCPUs"], errors="coerce")
bench["Threads"] = pd.to_numeric(bench["Threads"], errors="coerce")
bench["CPU Speed (events/sec)"] = pd.to_numeric(bench["CPU Speed (events/sec)"], errors="coerce")
bench["Model"] = bench["Model"].str.strip().str.lower()

bench = bench.dropna(subset=["Machine Type", "vCPUs", "Threads", "Model", "CPU Speed (events/sec)"])
bench = bench[bench["Threads"] == bench["vCPUs"]]  # matched utilization

# Median events/sec per deployment option
perf = (bench
        .groupby(["Machine Type", "vCPUs", "Model"])["CPU Speed (events/sec)"]
        .median()
        .reset_index()
        .rename(columns={"CPU Speed (events/sec)": "median_events_per_sec"}))

# --- Cost table (EDIT THESE VALUES) ---
cost_rows = [
    ("e2-standard", 2, "standard", 0.08),
    ("e2-standard", 2, "spot",     0.03),

    ("e2-highcpu",  2, "standard", 0.06),
    ("e2-highcpu",  2, "spot",     0.02),

    ("e2-highmem",  2, "standard", 0.10),
    ("e2-highmem",  2, "spot",     0.04),
]

cost = pd.DataFrame(cost_rows, columns=["Machine Type", "vCPUs", "Model", "hourly_cost_usd"])

# Merge cost + performance
merged = perf.merge(cost, on=["Machine Type", "vCPUs", "Model"], how="inner")
merged = merged.dropna(subset=["hourly_cost_usd", "median_events_per_sec"])

merged["cost_per_event"] = merged["hourly_cost_usd"] / merged["median_events_per_sec"]
merged["option"] = merged["Machine Type"] + " (" + merged["Model"] + ")"

# Sort best (lowest cost per event) first
merged = merged.sort_values("cost_per_event")

plt.figure(figsize=(9, 4.8))
plt.bar(merged["option"], merged["cost_per_event"])

plt.xlabel("Deployment Option")
plt.ylabel("Cost per Event (USD per event/sec unit)")
plt.title("Figure 7: Cost–performance ratio (hourly_cost / median_events_per_sec)")
plt.xticks(rotation=30, ha="right")

plt.gca().set_axisbelow(True)
plt.grid(axis="y", alpha=0.5)
plt.tight_layout()
plt.savefig("fig7.png", dpi=300)
plt.show()
