import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("Cloud Systems Benchmarking AE1 - Sheet1.csv")

# Fix config to make a fair spot vs standard comparison
fixed_type = "e2-standard"
fixed_vcpu = 2

df = df[df["Machine Type"] == fixed_type]
df["vCPUs"] = pd.to_numeric(df["vCPUs"], errors="coerce")
df = df[df["vCPUs"] == fixed_vcpu]

y_col = "CPU Speed (events/sec)"
df[y_col] = pd.to_numeric(df[y_col], errors="coerce")
df = df.dropna(subset=["Model", y_col])

models_order = ["standard", "spot"]
present = [m for m in models_order if m in df["Model"].str.strip().str.lower().unique()]

grouped = []
labels = []
for m in present:
    vals = df[df["Model"].str.strip().str.lower() == m][y_col].dropna().values
    grouped.append(vals)
    labels.append(m)

plt.figure(figsize=(7.5, 4.8))
bp = plt.boxplot(grouped, labels=labels, showmeans=True, patch_artist=True)

for box in bp["boxes"]:
    box.set_alpha(0.6)
for median in bp["medians"]:
    median.set_linewidth(2)

plt.xlabel("Pricing Model")
plt.ylabel("Events Per Second")
plt.title(f"Figure 5: Spot vs standard variability ({fixed_type}, {fixed_vcpu} vCPU)")

plt.gca().set_axisbelow(True)
plt.grid(axis="y", alpha=0.5)
plt.tight_layout()
plt.savefig("fig5.png", dpi=300)
plt.show()
