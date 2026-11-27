import pandas as pd
import numpy as np
from difflib import get_close_matches

np.random.seed(42)

bikes = pd.read_csv("bike_listings_s7.csv")

print(bikes.shape)
print(bikes.head())

duplicate_rows = bikes.sample(25, random_state=42)

# Create 10 relisted rows
relisted = bikes.sample(10, random_state=42).copy()

relisted["price_inr"] = (relisted["price_inr"] * 0.95).round(0)

# Combine all data
bikes = pd.concat(
    [bikes, duplicate_rows, relisted],
    ignore_index=True
)

print("Total rows:", len(bikes))

# Count exact duplicate rows
print("Exact duplicates:", bikes.duplicated().sum())

# Show all rows sharing listing_id
duplicate_ids = bikes[
    bikes.duplicated(subset="listing_id", keep=False)
]

print(duplicate_ids.sort_values("listing_id"))

bikes_nodup = bikes.drop_duplicates()

print("After removing exact duplicates:", len(bikes_nodup))

bikes_unique = bikes_nodup.drop_duplicates(
    subset="listing_id",
    keep="last"
)

print("After removing relisted rows:", len(bikes_unique))

assert len(bikes_unique) == 400
assert bikes_unique["listing_id"].is_unique


brands = bikes_unique["brand"].str.strip().str.title().unique().tolist()
cities = bikes_unique["city"].str.strip().str.title().unique().tolist()

print("Original brands:", brands)
print("Original cities:", cities)

bikes_dirty = bikes_unique.copy()

# Random 30 rows: lowercase brand and city
idx_lower = bikes_dirty.sample(30, random_state=10).index

bikes_dirty.loc[idx_lower, "brand"] = (
    bikes_dirty.loc[idx_lower, "brand"].str.lower()
)

bikes_dirty.loc[idx_lower, "city"] = (
    bikes_dirty.loc[idx_lower, "city"].str.lower()
)

# Add trailing spaces to 20 random rows
idx_space = bikes_dirty.sample(20, random_state=20).index

bikes_dirty.loc[idx_space, "brand"] = (
    bikes_dirty.loc[idx_space, "brand"] + "   "
)

bikes_dirty.loc[idx_space, "city"] = (
    bikes_dirty.loc[idx_space, "city"] + "   "
)   

# Misspell Veloce in 12 rows
idx_veloce = bikes_dirty[
    bikes_dirty["brand"].str.strip().str.title() == "Veloce"
].sample(12, random_state=30).index

bikes_dirty.loc[idx_veloce, "brand"] = "Velose"

# Misspell Ahmedabad in 12 rows
idx_ahmedabad = bikes_dirty[
    bikes_dirty["city"].str.strip().str.title() == "Ahmedabad"
].sample(12, random_state=40).index

bikes_dirty.loc[idx_ahmedabad, "city"] = "Ahmdabad"

print(bikes_dirty["brand"].value_counts())
print(bikes_dirty["city"].value_counts())


bikes_dirty["brand"] = (
    bikes_dirty["brand"].str.strip().str.title()
)

bikes_dirty["city"] = (
    bikes_dirty["city"].str.strip().str.title()
)

bikes_dirty["brand"] = bikes_dirty["brand"].replace({
    "Velose": "Veloce"
})

bikes_dirty["city"] = bikes_dirty["city"].replace({
    "Ahmdabad": "Ahmedabad"
})


def fix_spelling(value, correct_values):
    matches = get_close_matches(
        value,
        correct_values,
        n=1,
        cutoff=0.8
    )

    return matches[0] if matches else value


bikes_dirty["brand"] = bikes_dirty["brand"].apply(
    lambda x: fix_spelling(x, brands)
)

bikes_dirty["city"] = bikes_dirty["city"].apply(
    lambda x: fix_spelling(x, cities)
)

print(bikes_dirty["brand"].value_counts())
print(bikes_dirty["city"].value_counts())