import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("Cloud Systems Benchmarking AE1 - Sheet1.csv")

df = df[df["Model"].str.strip().str.lower() == "standard"]

df["vCPUs"] = pd.to_numeric(df["vCPUs"], errors="coerce")
df["Threads"] = pd.to_numeric(df["Threads"], errors="coerce")
df["CPU Speed (events/sec)"] = pd.to_numeric(df["CPU Speed (events/sec)"], errors="coerce")
df = df.dropna(subset=["Machine Type", "vCPUs", "Threads", "CPU Speed (events/sec)"])

df = df[df["Threads"] == df["vCPUs"]]
df["eps_per_vcpu"] = df["CPU Speed (events/sec)"] / df["vCPUs"]

order = ["e2-standard", "e2-highcpu", "e2-highmem"]
present = [t for t in order if t in df["Machine Type"].unique()]
if not present:
    present = sorted(df["Machine Type"].unique())

vals = df.groupby("Machine Type")["eps_per_vcpu"].median().reindex(present)

plt.figure(figsize=(8, 4.8))
plt.bar(vals.index, vals.values)

plt.xlabel("Instance Type")
plt.ylabel("Events Per Second per vCPU")
plt.title("Figure 3: Normalized CPU performance per vCPU (median, standard only, Threads=vCPUs)")

plt.gca().set_axisbelow(True)
plt.grid(axis="y", alpha=0.5)
plt.tight_layout()
plt.savefig("fig3.png", dpi=300)
plt.show()
