import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv("Cloud Systems Benchmarking AE1 - Sheet1.csv")

# --- Filter to standard only ---
df = df[df["Model"].astype(str).str.strip().str.lower() == "standard"]

# --- Columns ---
family_col = "Machine Type"
vcpu_col = "vCPUs"
thread_col = "Threads"
y_col = "Memory Read (mb/s)"

# --- Coerce numeric + clean ---
df[vcpu_col] = pd.to_numeric(df[vcpu_col], errors="coerce")
df[thread_col] = pd.to_numeric(df[thread_col], errors="coerce")
df[y_col] = pd.to_numeric(df[y_col], errors="coerce")
df = df.dropna(subset=[family_col, vcpu_col, thread_col, y_col])

# --- Only compare these VM families ---
families = ["e2-standard", "e2-highcpu", "e2-highmem"]
df = df[df[family_col].isin(families)]

# --- Match utilisation: Threads = vCPUs ---
df = df[df[thread_col] == df[vcpu_col]]

# --- Only vCPUs 2/4/8 ---
vcpu_levels = [2, 4, 8]
df = df[df[vcpu_col].isin(vcpu_levels)]

# --- Median throughput per (family, vCPU) ---
summary = (
    df.groupby([family_col, vcpu_col])[y_col]
      .median()
      .unstack(vcpu_col)
      .reindex(families)
      .reindex(columns=vcpu_levels)
)

# --- Plot grouped bars: x = VM family, bars = vCPU sizes ---
x = np.arange(len(families))
width = 0.25

plt.figure(figsize=(10, 4.8))

for i, v in enumerate(vcpu_levels):
    plt.bar(x + (i - 1) * width, summary[v].values, width=width, label=f"{v} vCPUs")

plt.xticks(x, families)
plt.xlabel("VM family")
plt.ylabel("Memory Read (MB/s, median)")
plt.title("Figure 3: Memory read speed comparison (standard only, Threads = vCPUs)")
plt.legend(title="VM size")

ax = plt.gca()
ax.set_axisbelow(True)
ax.grid(axis="y", alpha=0.5)

plt.tight_layout()
plt.savefig("fig3.png", dpi=300)
plt.show()
