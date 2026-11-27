import pandas as pd
import numpy as np

np.random.seed(7)

bikes = pd.read_csv("bike_listings_s6.csv")

print(bikes.shape)
print(bikes.head())

# Multiply 10 random prices by 6
price_idx = bikes.sample(10, random_state=7).index

bikes.loc[price_idx, "price_inr"] *= 6

# Set 6 random km_driven values to 400000
km_idx = bikes.sample(6, random_state=10).index

bikes.loc[km_idx, "km_driven"] = 400000

bikes[["price_inr", "km_driven"]].boxplot(
    figsize=(8, 5)
) 


def iqr_outliers(series):
    q1 = series.quantile(0.25)
    q3 = series.quantile(0.75)

    iqr = q3 - q1

    lower = q1 - 1.5 * iqr
    upper = q3 + 1.5 * iqr

    outliers = series[(series < lower) | (series > upper)]

    return outliers, lower, upper


price_outliers, price_lower, price_upper = iqr_outliers(
    bikes["price_inr"]
)

km_outliers, km_lower, km_upper = iqr_outliers(
    bikes["km_driven"]
)

print("Price IQR outliers:", len(price_outliers))
print("KM IQR outliers:", len(km_outliers))

def zscore_outliers(series):
    z = (series - series.mean()) / series.std()

    return series[z.abs() > 3]


price_z = zscore_outliers(bikes["price_inr"])
km_z = zscore_outliers(bikes["km_driven"])

print("Price Z-score outliers:", len(price_z))
print("KM Z-score outliers:", len(km_z))


bikes["price_capped"] = bikes["price_inr"].clip(
    lower=price_lower,
    upper=price_upper
)


q05 = bikes["price_inr"].quantile(0.05)
q95 = bikes["price_inr"].quantile(0.95)

bikes["price_wins"] = bikes["price_inr"].clip(
    lower=q05,
    upper=q95
)

bikes["km_log"] = np.log1p(bikes["km_driven"])


comparison = pd.DataFrame({
    "max": [
        bikes["price_inr"].max(),
        bikes["price_capped"].max(),
        bikes["price_wins"].max(),
        bikes["km_driven"].max(),
        bikes["km_log"].max()
    ],
    "mean": [
        bikes["price_inr"].mean(),
        bikes["price_capped"].mean(),
        bikes["price_wins"].mean(),
        bikes["km_driven"].mean(),
        bikes["km_log"].mean()
    ]
}, index=[
    "price_inr",
    "price_capped",
    "price_wins",
    "km_driven",
    "km_log"
])

print(comparison)

bikes_typed = bikes.copy()

memory_before = bikes_typed.memory_usage(deep=True).sum()

print("Memory before:", memory_before, "bytes")
print(bikes_typed.dtypes)

bikes_typed["price_inr"] = bikes_typed["price_inr"].apply(
    lambda x: f"Rs {x:,.0f}"
)

print(bikes_typed["price_inr"].head())

bikes_typed["price_inr"] = pd.to_numeric(
    bikes_typed["price_inr"]
    .str.replace("Rs ", "", regex=False)
    .str.replace(",", "", regex=False),
    errors="coerce"
)

memory_after = bikes_typed.memory_usage(deep=True).sum()

print("\nData types after conversion:")
print(bikes_typed.dtypes)

print("\nMemory before:", memory_before, "bytes")
print("Memory after:", memory_after, "bytes")
print("Memory saved:", memory_before - memory_after, "bytes")