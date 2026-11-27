import pandas as pd
import numpy as np

np.random.seed(42)

n = 3000

start_date = pd.Timestamp("2025-01-01")
end_date = pd.Timestamp("2025-06-30 23:59")

total_minutes = int((end_date - start_date).total_seconds() // 60)

random_minutes = np.random.randint(0, total_minutes + 1, n)

txn_time = start_date + pd.to_timedelta(random_minutes, unit="m")

categories = ["Grocery", "Fuel", "Recharge", "Food", "Bills"]

upi = pd.DataFrame({
    "txn_id": range(1, n + 1),
    "txn_time": txn_time.strftime("%d/%m/%Y %H:%M"),
    "amount_inr": np.random.randint(10, 5001, n),
    "category": np.random.choice(categories, n)
})

upi.to_csv("upi_raw.csv", index=False)

# Reload CSV
upi = pd.read_csv("upi_raw.csv")

upi["txn_time"] = pd.to_datetime(
    upi["txn_time"],
    format="%d/%m/%Y %H:%M"
)

print(upi.dtypes)
print(upi.head())