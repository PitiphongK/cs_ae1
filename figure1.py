import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("Cloud Systems Benchmarking AE1 - Sheet1.csv")

# Standard only
df = df[df["Model"].str.strip().str.lower() == "standard"]

x_col = "Machine Type"
y_col = "CPU Speed (events/sec)"

order = ["e2-standard", "e2-highcpu", "e2-highmem"]
present = [t for t in order if t in df[x_col].unique()]
grouped = [df.loc[df[x_col] == t, y_col].dropna().values for t in present]

plt.figure(figsize=(8, 4.8))
bp = plt.boxplot(grouped, labels=present, showmeans=True, patch_artist=True)

# Color boxes by machine type
color_map = {"e2-standard": "tab:blue", "e2-highcpu": "tab:orange", "e2-highmem": "tab:green"}
for box, inst in zip(bp["boxes"], present):
    box.set_facecolor(color_map.get(inst, "lightgray"))
    box.set_alpha(0.6)

for median in bp["medians"]:
    median.set_linewidth(2)

plt.xlabel("Instance Type")
plt.ylabel("Events Per Second")
plt.title("Figure 1: CPU throughput by instance type (standard only)")

plt.gca().set_axisbelow(True)
plt.grid(axis="y", alpha=0.5)  # horizontal lines for each y tick
plt.tight_layout()
plt.savefig("fig1.png", dpi=300)
plt.show()
