<<<<<<< HEAD
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# task 1:

data = sns.load_dataset('penguins')

data = data.dropna(how='any')
# print(data.info())

# sns.histplot(
#     data=data,
#     x="body_mass_g",
#     hue='species',
#     bins=25,
#     kde=True
# )
# plt.show()
# plt.savefig('penguin_hist.png')

# task 2:

fig, ax = plt.subplots(figsize=(9, 5))

result1 = sns.kdeplot(
    data=data,
    x="flipper_length_mm",
    hue="species",
    fill=True,
    ax=ax
)

ax.set_title("Flipper Length Distribution by Species")
ax.set_xlabel("Flipper Length (mm)")
ax.set_ylabel("Density")

plt.tight_layout()
fig.savefig("flipper_axes_level.png", dpi=150)
plt.show()

print("kdeplot return type:", type(result1))


result2 = sns.displot(
    data=data,
    x="flipper_length_mm",
    kind="kde",
    hue="species",
    fill=True,
    col="island",
    height=4,
    aspect=1
)

result2.set_axis_labels("Flipper Length (mm)", "Density")
result2.fig.suptitle("Flipper Length Distribution by Species and Island")

result2.savefig("flipper_figure_level.png", dpi=150)
plt.show()

print("displot return type:", type(result2))

# task 3:
penguins = sns.load_dataset("penguins")
penguins = penguins.dropna()

fig, axes = plt.subplots(1, 3, figsize=(15, 4))

# 1. Countplot: Island by species
sns.countplot(
    data=penguins,
    x="island",
    hue="species",
    ax=axes[0]
)
axes[0].set_title("Penguin Count by Island")
axes[0].set_xlabel("Island")
axes[0].set_ylabel("Count")

# 2. Boxplot: Body mass by species
sns.boxplot(
    data=penguins,
    x="species",
    y="body_mass_g",
    ax=axes[1]
)
axes[1].set_title("Body Mass by Species")
axes[1].set_xlabel("Species")
axes[1].set_ylabel("Body Mass (g)")

# 3. Violinplot: Bill length by sex
sns.violinplot(
    data=penguins,
    x="sex",
    y="bill_length_mm",
    ax=axes[2]
)
axes[2].set_title("Bill Length by Sex")
axes[2].set_xlabel("Sex")
axes[2].set_ylabel("Bill Length (mm)")

plt.tight_layout()

plt.savefig("penguin_categorical.png", dpi=150)
plt.show()


# task 4:


penguins = sns.load_dataset("penguins")
penguins = penguins.dropna()

def make_panel(style, filename):
    sns.set_theme(style=style)

    fig, axes = plt.subplots(1, 3, figsize=(15, 4))

    # 1. Countplot: island by species
    sns.countplot(
        data=penguins,
        x="island",
        hue="species",
        ax=axes[0]
    )
    axes[0].set_title("Penguin Count by Island")
    axes[0].set_xlabel("Island")
    axes[0].set_ylabel("Count")

    # 2. Boxplot: body mass by species
    sns.boxplot(
        data=penguins,
        x="species",
        y="body_mass_g",
        ax=axes[1]
    )
    axes[1].set_title("Body Mass by Species")
    axes[1].set_xlabel("Species")
    axes[1].set_ylabel("Body Mass (g)")

    # 3. Violinplot: bill length by sex
    sns.violinplot(
        data=penguins,
        x="sex",
        y="bill_length_mm",
        ax=axes[2]
    )
    axes[2].set_title("Bill Length by Sex")
    axes[2].set_xlabel("Sex")
    axes[2].set_ylabel("Bill Length (mm)")

    plt.tight_layout()
    fig.savefig(filename, dpi=150, bbox_inches="tight")
    plt.show()
    plt.close(fig)
=======
import pandas as pd
>>>>>>> e5cb423bdb340c361f1b4fbc5045eb090a0107f0
