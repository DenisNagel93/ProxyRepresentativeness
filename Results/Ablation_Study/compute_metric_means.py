import pandas as pd
import glob
import re

"""
Scan all CSV files in the directory, finds the Proxy-Score section, extract all numeric key–value metrics that follow and load them into a pandas DataFrame. Compute the mean of each metric across all files and writes those averages to stats_means.csv.

"""

files = glob.glob("*.csv")
stats_list = []

for f in files:
    with open(f, "r", encoding="utf-8") as file:
        lines = file.readlines()

    start_index = None
    for i, line in enumerate(lines):
        if line.startswith("Proxy-Score"):
            start_index = i
            break
    if start_index is None:
        continue

    stats = {}
    for line in lines[start_index:]:
        if ":" in line:
            key, value = line.split(":", 1)
            key = key.strip()
            match = re.search(r"[-+]?\d*\.?\d+(?:[eE][-+]?\d+)?", value)
            if match:
                stats[key] = float(match.group())

    stats_list.append(stats)

df_stats = pd.DataFrame(stats_list)
df_mean = df_stats.mean()

# Write one metric per line: MetricName,MeanValue
df_mean.to_csv("stats_means.csv", header=False)

print("Done.")

