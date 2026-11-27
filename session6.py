import pandas as pd
import numpy as np

np.random.seed(42)

n = 400

bikes = pd.DataFrame({
    "listing_id": range(1, n + 1),
    "brand": np.random.choice(
        ["Veloce", "Rajhans", "Sundar", "Tarang"], n
    ),
    "city": np.random.choice(
        ["Ahmedabad", "Surat", "Vadodara", "Rajkot"], n
    ),
    "model_year": np.random.randint(2008, 2024, n),
    "km_driven": np.random.randint(2000, 90001, n),
    "owner_count": np.random.randint(1, 4, n),
    "price_inr": np.random.randint(25000, 140001, n)
})

print(bikes.head())
print(bikes.shape)

km_idx = bikes.sample(frac=0.08, random_state=42).index

bikes.loc[km_idx, "km_driven"] = np.nan

old_bikes = bikes[bikes["model_year"] < 2013]

owner_idx = old_bikes.sample(
    frac=0.5,
    random_state=42
).index

bikes.loc[owner_idx, "owner_count"] = np.nan

price_limit = bikes["price_inr"].quantile(0.95)

price_idx = bikes[bikes["price_inr"] >= price_limit].index

bikes.loc[price_idx, "price_inr"] = np.nan

bikes.to_csv("bike_listings_raw.csv", index=False)

print(bikes.isna().sum())

missing_report = pd.DataFrame({
    "missing_count": bikes.isna().sum(),
    "missing_percentage": bikes.isna().mean() * 100
})

missing_report["mechanism"] = [
    "None",
    "None",
    "None",
    "None",
    "MCAR",
    "MAR",
    "MNAR"
]

print(missing_report)
complete_rows = bikes.notnull().all(axis=1).sum()

print("Fully complete rows:", complete_rows)

old_mask = bikes["model_year"] < 2013
new_mask = bikes["model_year"] >= 2013

old_missing_rate = bikes.loc[
    old_mask, "owner_count"
].isna().mean() * 100

new_missing_rate = bikes.loc[
    new_mask, "owner_count"
].isna().mean() * 100

print("Before 2013 missing rate:", old_missing_rate, "%")
print("2013 and later missing rate:", new_missing_rate, "%")

drop_any = bikes.dropna(how="any")

print("drop_any:", drop_any.shape)

drop_thresh = bikes.dropna(thresh=6)

print("drop_thresh:", drop_thresh.shape)

comparison = pd.DataFrame({
    "rows": [
        len(bikes),
        len(drop_any),
        len(drop_thresh)
    ],
    "columns": [
        bikes.shape[1],
        drop_any.shape[1],
        drop_thresh.shape[1]
    ],
    "mean_price": [
        bikes["price_inr"].mean(),
        drop_any["price_inr"].mean(),
        drop_thresh["price_inr"].mean()
    ]
}, index=[
    "Raw Data",
    "Drop Any",
    "Drop Threshold"
])

print(comparison)

bikes_filled = bikes.copy() 

bikes_filled["km_driven"] = bikes_filled["km_driven"].fillna(
    bikes_filled["km_driven"].median()
)
bikes_filled["owner_count"] = bikes_filled["owner_count"].fillna(
    bikes_filled["owner_count"].mode()[0]
)

bikes_filled = bikes_filled.sort_values("model_year")

bikes_filled["price_inr"] = (
    bikes_filled["price_inr"]
    .ffill()
    .bfill()
)


mean_comparison = pd.DataFrame({
    "mean_price": [
        bikes["price_inr"].mean(),
        drop_any["price_inr"].mean(),
        bikes_filled["price_inr"].mean()
    ]
}, index=[
    "Raw Non-Missing",
    "Drop Any",
    "Filled Data"
])

print(mean_comparison)