import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("Cloud Systems Benchmarking AE1 - Sheet1.csv")

# Standard only
df = df[df["Model"].str.strip().str.lower() == "standard"]

# Ensure numeric
df["vCPUs"] = pd.to_numeric(df["vCPUs"], errors="coerce")
df["Threads"] = pd.to_numeric(df["Threads"], errors="coerce")
df["CPU Speed (events/sec)"] = pd.to_numeric(df["CPU Speed (events/sec)"], errors="coerce")
df = df.dropna(subset=["Machine Type", "vCPUs", "Threads", "CPU Speed (events/sec)"])

# Fair scaling comparison: match utilization
df = df[df["Threads"] == df["vCPUs"]]

order = ["e2-standard", "e2-highcpu", "e2-highmem"]
present = [t for t in order if t in df["Machine Type"].unique()]
if not present:
    present = sorted(df["Machine Type"].unique())

plt.figure(figsize=(8, 4.8))

for inst in present:
    sub = df[df["Machine Type"] == inst]
    summary = sub.groupby("vCPUs")["CPU Speed (events/sec)"].median().reset_index().sort_values("vCPUs")
    plt.plot(summary["vCPUs"], summary["CPU Speed (events/sec)"], marker="o", linewidth=2, label=inst)

plt.xlabel("vCPUs")
plt.ylabel("Events Per Second")
plt.title("Figure 2: CPU scalability with vCPUs (standard only, Threads=vCPUs)")
plt.legend(title="Instance Type")

plt.gca().set_axisbelow(True)
plt.grid(axis="y", alpha=0.5)
plt.tight_layout()
plt.savefig("fig2.png", dpi=300)
plt.show()
