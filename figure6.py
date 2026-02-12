import pandas as pd
import matplotlib.pyplot as plt

cost_rows = [
    ("e2-standard", 2, "standard", 0.08),
    ("e2-standard", 2, "spot",     0.03),

    ("e2-highcpu",  2, "standard", 0.06),
    ("e2-highcpu",  2, "spot",     0.02),

    ("e2-highmem",  2, "standard", 0.10),
    ("e2-highmem",  2, "spot",     0.04),
]

cost_df = pd.DataFrame(cost_rows, columns=["Machine Type", "vCPUs", "Model", "hourly_cost_usd"])

# Fixed comparison at vCPUs=2
cost_df = cost_df[cost_df["vCPUs"] == 2].copy()

# Ensure numeric
cost_df["hourly_cost_usd"] = pd.to_numeric(cost_df["hourly_cost_usd"], errors="coerce")
cost_df = cost_df.dropna(subset=["hourly_cost_usd"])

# Pivot for grouped bars (standard vs spot for each instance type)
pivot = cost_df.pivot(index="Machine Type", columns="Model", values="hourly_cost_usd")
pivot = pivot.reindex(["e2-standard", "e2-highcpu", "e2-highmem"])

plt.figure(figsize=(8, 4.8))
pivot.plot(kind="bar", ax=plt.gca())

plt.xlabel("Instance Type (vCPUs=2)")
plt.ylabel("Hourly Cost (USD)")
plt.title("Figure 6: Absolute hourly cost by instance type (standard vs spot)")

plt.gca().set_axisbelow(True)
plt.grid(axis="y", alpha=0.5)
plt.tight_layout()
plt.savefig("fig6.png", dpi=300)
plt.show()
