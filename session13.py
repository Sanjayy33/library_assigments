import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from pathlib import Path

# Load dataset
mpg = sns.load_dataset("mpg")

# Remove missing values
mpg = mpg.dropna()

# Display dataset shape
print("Dataset shape:", mpg.shape)


g = sns.pairplot(
    data=mpg,
    vars=["mpg", "horsepower", "weight", "acceleration"],
    hue="origin",
    corner=True
)

g.savefig("mpg_pairplot.png", dpi=150)

plt.show()

corr = mpg.corr(numeric_only=True)

print(corr)

# Create upper triangle mask
mask = np.triu(np.ones_like(corr, dtype=bool))

# Draw heatmap
plt.figure(figsize=(10, 7))

sns.heatmap(
    corr,
    annot=True,
    fmt=".2f",
    cmap="coolwarm",
    vmin=-1,
    vmax=1,
    mask=mask
)

plt.title("MPG Dataset Correlation Heatmap")
plt.tight_layout()

plt.savefig("mpg_corr.png", dpi=150)
plt.show()

mpg_corr = corr["mpg"].drop("mpg")

most_negative = mpg_corr.idxmin()
lowest_correlation = mpg_corr.min()

print("Most negatively correlated column:", most_negative)
print("Correlation value:", round(lowest_correlation, 3))




g = sns.relplot(
    data=mpg,
    x="model_year",
    y="mpg",
    hue="origin",
    kind="line",
    errorbar=None,
    marker="o"
)

g.fig.suptitle("MPG by Model Year and Origin")
g.savefig("mpg_relplot.png", dpi=150)

plt.show()
print("Relplot return type:", type(g))


g = sns.jointplot(
    data=mpg,
    x="weight",
    y="mpg",
    kind="reg",
    marginal_kws={"bins": 25, "fill": True}
)

g.fig.suptitle("Vehicle Weight vs MPG")
g.fig.tight_layout()

g.savefig("mpg_joint.png", dpi=150)
plt.show()


files = sorted(Path(".").glob("mpg_*.png"))

for file in files:
    print(file)

print("Total PNG files:", len(files))

assert len(files) == 6, f"Expected 6 files, found {len(files)}"
print("All six image files are present.")