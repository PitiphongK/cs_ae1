import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv("Cloud Systems Benchmarking AE1 - Sheet1.csv")

# --- Filter to standard only ---
df = df[df["Model"].astype(str).str.strip().str.lower() == "standard"]

# --- Columns ---
group_col = "Machine Type"
vcpu_col = "vCPUs"
y_col = "CPU Speed (events/sec)"

# --- Coerce numeric and clean ---
df[vcpu_col] = pd.to_numeric(df[vcpu_col], errors="coerce")
df[y_col] = pd.to_numeric(df[y_col], errors="coerce")
df = df.dropna(subset=[group_col, vcpu_col, y_col])

# --- Only vCPUs 2/4/8 ---
vcpu_levels = [2, 4, 8]
df = df[df[vcpu_col].isin(vcpu_levels)]

# --- Preferred VM order (includes new types) ---
preferred_order = [
    "e2-standard", "e2-highcpu", "e2-highmem",
    "n4-standard", "c2d-standard"
]

present_types = sorted(df[group_col].unique().tolist())

# Keep preferred order first, then append any extra machine types found in CSV
vm_types = [t for t in preferred_order if t in present_types] + \
           [t for t in present_types if t not in preferred_order]

# --- Median throughput per (VM type, vCPU) ---
summary = (
    df.groupby([group_col, vcpu_col])[y_col]
      .median()
      .unstack(vcpu_col)
      .reindex(vm_types)
      .reindex(columns=vcpu_levels)
)

# --- Grouped bar plot ---
x = np.arange(len(vm_types))
width = 0.24  # slightly narrower to fit more VM types nicely

plt.figure(figsize=(11, 4.8))

for i, v in enumerate(vcpu_levels):
    vals = summary[v].values
    plt.bar(x + (i - 1) * width, vals, width=width, label=f"{v} vCPUs")

plt.xticks(x, vm_types, rotation=15, ha="right")
plt.xlabel("Instance Type")
plt.ylabel("Events Per Second (median)")
plt.title("Figure 1: CPU throughput by instance type and vCPU (standard only)")
plt.legend(title="VM size")

ax = plt.gca()
ax.set_axisbelow(True)
ax.grid(axis="y", alpha=0.5)

plt.tight_layout()
plt.savefig("fig1.png", dpi=300)
plt.show()
