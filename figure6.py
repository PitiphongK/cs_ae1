import pandas as pd
import matplotlib.pyplot as plt

# Your provided hourly costs (monthly / 730.484)
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

# Build a DataFrame
cost_df = pd.DataFrame(cost_rows, columns=["Machine Type", "vCPUs", "Model", "hourly_cost"])

# Only vCPUs=2 (as your figure is defined)
cost_df = cost_df[cost_df["vCPUs"] == 2].copy()

# Order of families on x-axis
order = ["e2-standard", "e2-highcpu", "e2-highmem", "n4-standard", "c2d-standard"]
present = [t for t in order if t in cost_df["Machine Type"].unique()]
if not present:
    present = sorted(cost_df["Machine Type"].unique())

# Pivot for plotting (rows = machine type, columns = model)
pivot = (
    cost_df.pivot_table(index="Machine Type", columns="Model", values="hourly_cost", aggfunc="first")
          .reindex(present)
)

# Ensure numeric dtype (prevents "no numeric data to plot")
pivot = pivot.apply(pd.to_numeric, errors="coerce")

plt.figure(figsize=(10, 4.8))
pivot.plot(kind="bar", ax=plt.gca())

plt.xlabel("Instance Type (vCPUs=2)")
plt.ylabel("Hourly Cost")
plt.title("Figure 6: Absolute hourly cost by provisioning model (standard vs spot)")
plt.legend(title="Model")

ax = plt.gca()
ax.set_axisbelow(True)
ax.grid(axis="y", alpha=0.5)

plt.tight_layout()
plt.savefig("fig6.png", dpi=300)
plt.show()
