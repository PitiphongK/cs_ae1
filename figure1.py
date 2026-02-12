import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv("Cloud Systems Benchmarking AE1 - Sheet1.csv")

# Standard only
df = df[df["Model"].str.strip().str.lower() == "standard"]

# Columns
group_col = "Machine Type"
vcpu_col = "vCPUs"
y_col = "CPU Speed (events/sec)"

# Ensure numeric where needed
df[vcpu_col] = pd.to_numeric(df[vcpu_col], errors="coerce")
df[y_col] = pd.to_numeric(df[y_col], errors="coerce")
df = df.dropna(subset=[group_col, vcpu_col, y_col])

# Only use vCPUs = 2,4,8 as requested
vcpu_levels = [2, 4, 8]
df = df[df[vcpu_col].isin(vcpu_levels)]

# Order of VM types on x-axis
order = ["e2-standard", "e2-highcpu", "e2-highmem"]
vm_types = [t for t in order if t in df[group_col].unique()]
if not vm_types:
    vm_types = sorted(df[group_col].unique())

# Median throughput per (VM type, vCPU)
summary = (
    df.groupby([group_col, vcpu_col])[y_col]
      .median()
      .unstack(vcpu_col)
      .reindex(vm_types)
)

# Plot grouped bars
x = np.arange(len(vm_types))
width = 0.25

plt.figure(figsize=(9, 4.8))

for i, v in enumerate(vcpu_levels):
    if v in summary.columns:
        plt.bar(x + (i - 1) * width, summary[v].values, width=width, label=f"{v} vCPUs")

plt.xticks(x, vm_types)
plt.xlabel("Instance Type")
plt.ylabel("Events Per Second (median)")
plt.title("Figure 1: CPU throughput by instance type and vCPU (standard only)")
plt.legend(title="VM size")

ax = plt.gca()
ax.set_axisbelow(True)          # grid behind bars
ax.grid(axis="y", alpha=0.5)

plt.tight_layout()
plt.savefig("fig1.png", dpi=300)
plt.show()
