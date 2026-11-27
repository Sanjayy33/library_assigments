import pandas as pd
import numpy as np

np.random.seed(42)

flats = [
    f"{block}-{number:02d}"
    for block in ["A", "B", "C", "D"]
    for number in range(1, 26)
]

months = pd.date_range(
    start="2025-01",
    periods=12,
    freq="MS"
).strftime("%Y-%m")

readings = pd.DataFrame({
    "flat_id": np.repeat(flats, 12),
    "month": np.tile(months, 100),
    "units_kwh": np.random.randint(60, 421, 1200)
})

readings["amount_inr"] = readings["units_kwh"] * 7.5

readings["paid"] = np.random.choice(
    ["Yes", "No"],
    size=1200,
    p=[0.9, 0.1]
)

print(readings.head())
print(readings.shape)

readings.to_csv("readings_comma.csv", index=False)

readings.to_csv(
    "readings_semicolon.csv",
    sep=";",
    index=False
)

readings.to_csv(
    "readings_tab.tsv",
    sep="\t",
    index=False
)
readings.to_excel(
    "readings.xlsx",
    index=False
)

readings.to_json(
    "readings.json",
    orient="records",
    indent=4
)


df_csv = pd.read_csv("readings_comma.csv")

df_semicolon = pd.read_csv(
    "readings_semicolon.csv",
    sep=";"
)

df_tab = pd.read_csv(
    "readings_tab.tsv",
    sep="\t"
)

df_excel = pd.read_excel("readings.xlsx")

df_json = pd.read_json("readings.json")


datasets = {
    "CSV": df_csv,
    "Semicolon CSV": df_semicolon,
    "TSV": df_tab,
    "Excel": df_excel,
    "JSON": df_json
}

comparison = pd.DataFrame({
    "file": list(datasets.keys()),
    "shape": [df.shape for df in datasets.values()],
    "units_sum": [
        df["units_kwh"].sum()
        for df in datasets.values()
    ]
})

print(comparison)

first = df_csv

all_match = all(
    df.equals(first)
    for df in datasets.values()
)

print("All five datasets match:", all_match)

messy = readings.copy()

missing_idx = messy.sample(
    frac=0.05,
    random_state=42
).index

messy.loc[missing_idx, "units_kwh"] = np.nan

messy["amount_inr"] = messy["amount_inr"].apply(
    lambda x: f"Rs {x:.2f}"
)

yes_mask = messy["paid"] == "Yes"

messy.loc[yes_mask, "paid"] = np.random.choice(
    ["yes", "YES"],
    size=yes_mask.sum()
)

no_mask = messy["paid"] == "No"

messy.loc[no_mask, "paid"] = "No"

messy.to_csv("readings_messy.csv", index=False)

df = pd.read_csv("readings_messy.csv")

df.info()

print(df.describe(include="all"))


issue_report = pd.DataFrame({
    "dtype": df.dtypes,
    "missing_count": df.isna().sum(),
    "unique_count": df.nunique()
})

print(issue_report)

issue_report.to_csv(
    "society_issue_report.csv",
    index=True
)


np.random.seed(42)

n = 60000

meter_big = pd.DataFrame({
    "flat_id": np.repeat(flats, 600),
    "hour_no": np.tile(np.arange(600), 100),
    "kwh": np.round(
        np.random.uniform(0.1, 2.5, n),
        2
    )
})

print(meter_big.head())
print(meter_big.shape)

meter_big.to_csv("meter_big.csv", index=False)


chunks = pd.read_csv(
    "meter_big.csv",
    chunksize=10000
)

total_rows = 0
total_kwh = 0
chunk_count = 0

for chunk in chunks:

    total_rows += len(chunk)

    total_kwh += chunk["kwh"].sum()

    chunk_count += 1

print("Total chunks:", chunk_count)
print("Total rows:", total_rows)
print("Total kwh:", total_kwh)