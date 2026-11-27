import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
np.random.seed(42)

n = 1500

data = {
    "age": np.random.randint(21, 61, n),

    "monthly_income_inr": np.random.randint(15000, 150001, n),

    "loan_amount_inr": np.random.randint(50000, 800001, n),

    "tenure_months": np.random.choice(
        [12, 24, 36, 48, 60], n
    ),

    "employment": np.random.choice(
        ["Salaried", "Self-employed", "Business"], n
    ),

    "city_tier": np.random.randint(1, 4, n),

    "credit_score": np.random.randint(550, 851, n)
}

df = pd.DataFrame(data)

default_probability = (
    0.05
    + np.where(df["credit_score"] < 650, 0.15, 0)
    + np.where(
        df["loan_amount_inr"] > 10 * df["monthly_income_inr"],
        0.10,
        0
    )
)

df["defaulted"] = np.random.binomial(
    1,
    default_probability
)

print(df.head())

print("\nDataset shape:", df.shape)



df = pd.read_csv("loan_applications.csv")

numeric_cols = [
    "age",
    "monthly_income_inr",
    "loan_amount_inr",
    "tenure_months",
    "credit_score",
    "defaulted"
]

categorical_cols = [
    "employment",
    "city_tier",
    "defaulted"
]

print("NUMERIC DESCRIPTIVE STATISTICS")
print(df[numeric_cols].describe())

for col in categorical_cols:
    print(f"\n{col.upper()} DISTRIBUTION")
    print(df[col].value_counts(normalize=True))

fig, axes = plt.subplots(2, 3, figsize=(15, 9))

for ax, col in zip(axes.flatten(), numeric_cols):
    sns.histplot(
        data=df,
        x=col,
        bins=25,
        kde=True if col != "defaulted" else False,
        ax=ax
    )

    ax.set_title(f"Distribution of {col}")
    ax.set_xlabel(col)
    ax.set_ylabel("Frequency")

plt.suptitle("Loan Applications: Numeric Distributions", fontsize=16)
plt.tight_layout()

plt.savefig("loan_numeric.png", dpi=150)
plt.show()

fig, axes = plt.subplots(1, 3, figsize=(15, 4))

for ax, col in zip(axes, categorical_cols):
    sns.countplot(
        data=df,
        x=col,
        ax=ax
    )

    ax.set_title(f"Count of {col}")
    ax.set_xlabel(col)
    ax.set_ylabel("Number of Applications")

plt.suptitle("Loan Applications: Categorical Distributions", fontsize=16)
plt.tight_layout()

plt.savefig("loan_categorical.png", dpi=150)
plt.show()





df = pd.read_csv("loan_applications.csv")

plt.figure(figsize=(9, 6))

sns.scatterplot(
    data=df,
    x="monthly_income_inr",
    y="loan_amount_inr",
    hue="defaulted",
    palette={0: "teal", 1: "red"},
    alpha=0.65
)

plt.title("Monthly Income vs Loan Amount by Default Status")
plt.xlabel("Monthly Income (INR)")
plt.ylabel("Loan Amount (INR)")
plt.legend(title="Defaulted")
plt.tight_layout()

plt.savefig("loan_scatter.png", dpi=150)
plt.show()



df = pd.read_csv("loan_applications.csv")

sample = df.sample(n=500, random_state=42)

print("Original dataset:", df.shape)
print("Sample dataset:", sample.shape)

g = sns.pairplot(
    data=sample,
    vars=[
        "age",
        "monthly_income_inr",
        "loan_amount_inr",
        "credit_score"
    ],
    hue="defaulted",
    corner=True,
    diag_kind="hist",
    plot_kws={"alpha": 0.6}
)

g.fig.suptitle(
    "Multivariate Analysis: Loan Applications",
    y=1.02
)

g.savefig("loan_pairplot.png", dpi=150)
plt.show()


corr = df.corr(numeric_only=True)

mask = np.triu(
    np.ones_like(corr, dtype=bool)
)

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

plt.title("Loan Application Correlation Heatmap")
plt.tight_layout()

plt.savefig("loan_heatmap.png", dpi=150)
plt.show()


overall_default = df["defaulted"].mean() * 100

credit_by_default = df.groupby("defaulted")["credit_score"].mean()

df["credit_group"] = np.where(
    df["credit_score"] < 650,
    "Below 650",
    "650 or above"
)

credit_default_rate = (
    df.groupby("credit_group")["defaulted"].mean() * 100
)

df["high_loan_burden"] = (
    df["loan_amount_inr"] > 10 * df["monthly_income_inr"]
)

burden_default_rate = (
    df.groupby("high_loan_burden")["defaulted"].mean() * 100
)

employment_rates = df.groupby("employment")["defaulted"].mean() * 100

highest_employment = employment_rates.idxmax()
highest_employment_rate = employment_rates.max()

eda_findings = pd.DataFrame([
    {
        "finding": "Overall default rate",
        "evidence": f"{overall_default:.2f}% of applications defaulted"
    },
    {
        "finding": "Average credit score by default status",
        "evidence": (
            f"Non-default: {credit_by_default.loc[0]:.2f}; "
            f"Default: {credit_by_default.loc[1]:.2f}"
        )
    },
    {
        "finding": "Default rate by credit score",
        "evidence": (
            f"Below 650: {credit_default_rate.loc['Below 650']:.2f}%; "
            f"650 or above: {credit_default_rate.loc['650 or above']:.2f}%"
        )
    },
    {
        "finding": "Default rate by loan burden",
        "evidence": (
            f"Loan above 10x income: {burden_default_rate.loc[True]:.2f}%; "
            f"Other loans: {burden_default_rate.loc[False]:.2f}%"
        )
    },
    {
        "finding": "Employment category with highest default rate",
        "evidence": (
            f"{highest_employment}: {highest_employment_rate:.2f}%"
        )
    }
])

print(eda_findings)

overall_default = df["defaulted"].mean() * 100

credit_by_default = df.groupby("defaulted")["credit_score"].mean()

df["credit_group"] = np.where(
    df["credit_score"] < 650,
    "Below 650",
    "650 or above"
)

credit_default_rate = (
    df.groupby("credit_group")["defaulted"].mean() * 100
)

df["high_loan_burden"] = (
    df["loan_amount_inr"] > 10 * df["monthly_income_inr"]
)

burden_default_rate = (
    df.groupby("high_loan_burden")["defaulted"].mean() * 100
)

employment_rates = df.groupby("employment")["defaulted"].mean() * 100

highest_employment = employment_rates.idxmax()
highest_employment_rate = employment_rates.max()

eda_findings = pd.DataFrame([
    {
        "finding": "Overall default rate",
        "evidence": f"{overall_default:.2f}% of applications defaulted"
    },
    {
        "finding": "Average credit score by default status",
        "evidence": (
            f"Non-default: {credit_by_default.loc[0]:.2f}; "
            f"Default: {credit_by_default.loc[1]:.2f}"
        )
    },
    {
        "finding": "Default rate by credit score",
        "evidence": (
            f"Below 650: {credit_default_rate.loc['Below 650']:.2f}%; "
            f"650 or above: {credit_default_rate.loc['650 or above']:.2f}%"
        )
    },
    {
        "finding": "Default rate by loan burden",
        "evidence": (
            f"Loan above 10x income: {burden_default_rate.loc[True]:.2f}%; "
            f"Other loans: {burden_default_rate.loc[False]:.2f}%"
        )
    },
    {
        "finding": "Employment category with highest default rate",
        "evidence": (
            f"{highest_employment}: {highest_employment_rate:.2f}%"
        )
    }
])

print(eda_findings)