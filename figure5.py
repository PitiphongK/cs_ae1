import pandas as pd
import matplotlib.pyplot as plt

# --- Load benchmark data ---
bench = pd.read_csv("Cloud Systems Benchmarking AE1 - Sheet1.csv")

bench["vCPUs"] = pd.to_numeric(bench["vCPUs"], errors="coerce")
bench["Threads"] = pd.to_numeric(bench["Threads"], errors="coerce")
bench["CPU Speed (events/sec)"] = pd.to_numeric(bench["CPU Speed (events/sec)"], errors="coerce")
bench["Model"] = bench["Model"].astype(str).str.strip().str.lower()

bench = bench.dropna(subset=["Machine Type", "vCPUs", "Threads", "Model", "CPU Speed (events/sec)"])

# matched utilization
bench = bench[bench["Threads"] == bench["vCPUs"]]

# limit to vCPUs=2 because cost table is for 2 vCPUs
bench = bench[bench["vCPUs"] == 2]

# keep only the models we care about (optional but tidy)
bench = bench[bench["Model"].isin(["standard", "spot"])]

# Median events/sec per deployment option
perf = (bench
        .groupby(["Machine Type", "vCPUs", "Model"])["CPU Speed (events/sec)"]
        .median()
        .reset_index()
        .rename(columns={"CPU Speed (events/sec)": "median_events_per_sec"}))

# --- Updated cost table ---
cost_rows = [
    ("e2-standard", 2, "standard", 54.21/730.484),
    ("e2-standard", 2, "spot",     21.92/730.484),

    ("e2-highcpu",  2, "standard", 40.13/730.484),
    ("e2-highcpu",  2, "spot",     16.29/730.484),

    ("e2-highmem",  2, "standard", 72.99/730.484),
    ("e2-highmem",  2, "spot",     29.42/730.484),

    ("n4-standard", 2, "standard", 74.80/730.484),
    ("n4-standard", 2, "spot",     15.25/730.484),

    ("c2d-standard", 2, "standard", 73.38/730.484),
    ("c2d-standard", 2, "spot",      8.54/730.484),
]

cost = pd.DataFrame(cost_rows, columns=["Machine Type", "vCPUs", "Model", "hourly_cost_usd"])
cost["Model"] = cost["Model"].astype(str).str.strip().str.lower()

# Merge cost + performance
merged = perf.merge(cost, on=["Machine Type", "vCPUs", "Model"], how="inner")
merged = merged.dropna(subset=["hourly_cost_usd", "median_events_per_sec"])

merged["cost_per_event"] = merged["hourly_cost_usd"] / merged["median_events_per_sec"]
merged["option"] = merged["Machine Type"] + " (" + merged["Model"] + ")"

# Sort best (lowest cost per event) first
merged = merged.sort_values("cost_per_event")

plt.figure(figsize=(10, 4.8))
plt.bar(merged["option"], merged["cost_per_event"])

plt.xlabel("Deployment Option (vCPUs=2, Threads=2)")
plt.ylabel("Cost per Event (USD per event/sec unit)")
plt.title("Figure 5: Cost-performance ratio (Hourly cost / Median events per sec)")
plt.xticks(rotation=30, ha="right")

ax = plt.gca()
ax.set_axisbelow(True)
ax.grid(axis="y", alpha=0.5)

plt.tight_layout()
plt.savefig("fig5.png", dpi=300)
plt.show()
