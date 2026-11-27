import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

from ydata_profiling import ProfileReport

taxi = sns.load_dataset("taxis")

print(taxi.head())
print("Original shape:", taxi.shape)

taxi_sample = taxi.sample(n=3000, random_state=42)

print("Sample shape:", taxi_sample.shape)
print(taxi_sample.head())

profile = ProfileReport(
    taxi_sample,
    title="Taxi Trips Profile",
    explorative=True
)

profile.to_file("taxi_profile.html")


import sweetviz as sv

report = sv.compare_intra(
    taxi_sample,
    taxi_sample["payment"] == "cash",
    ["Cash", "Other"],
    target_feat="fare"
)

report.show_html(
    filepath="taxi_sweetviz_cash_vs_other.html",
    open_browser=False
)



import dtale

d = dtale.show(taxi_sample)

print("D-Tale link:", d.main_url())

d.open_browser()

d = dtale.show(taxi_sample)

d.open_browser()


corr = taxi_sample.corr(numeric_only=True)

corr_filtered = corr.drop(index="total", columns="total")

upper_triangle = corr_filtered.abs().where(
    np.triu(np.ones(corr_filtered.shape), k=1).astype(bool)
)

strongest_pair = upper_triangle.stack().idxmax()
strongest_value = corr_filtered.loc[strongest_pair[0], strongest_pair[1]]

print("Strongest relationship:")
print("Column 1:", strongest_pair[0])
print("Column 2:", strongest_pair[1])
print("Correlation:", strongest_value)
print("Absolute correlation:", abs(strongest_value))


plt.figure(figsize=(12, 8))

sns.heatmap(
    corr,
    annot=True,
    cmap="coolwarm",
    fmt=".2f",
    vmin=-1,
    vmax=1,
    linewidths=0.5
)

plt.title("Taxi Dataset Correlation Heatmap")
plt.tight_layout()

plt.savefig("taxi_corr_check.png", dpi=150)
plt.show()

taxi_sample.to_csv("taxi_sample.csv", index=False)