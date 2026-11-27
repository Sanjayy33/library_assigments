import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# task 1:
np.random.seed(42)

n = 600
areas = ["Navrangpura", "Maninagar", "Satellite", "Vastrapur", "Paldi"]

trip_dates = pd.Timestamp("2025-04-01") + pd.to_timedelta(
    np.random.randint(0, 30, size=n), unit="D"
)
distance = np.random.uniform(1, 15, size=n)
noise = np.random.uniform(-15, 25, size=n)

df = pd.DataFrame({
    "trip_id": range(1, n + 1),
    "trip_date": trip_dates,
    "area": np.random.choice(areas, size=n),
    "distance_km": np.round(distance, 2)
})

df["fare_inr"] = np.round(30 + 14 * df["distance_km"] + noise).astype(int)

df.to_csv("auto_trips.csv", index=False, date_format="%Y-%m-%d")

daily_fare = (
    df.set_index("trip_date")["fare_inr"]
      .resample("D")
      .sum()
)

plt.figure(figsize=(11, 5))
plt.plot(daily_fare.index, daily_fare.values, marker="o")
plt.title("Daily Total Auto-Rickshaw Fare")
plt.xlabel("Trip Date")
plt.ylabel("Total Fare (INR)")
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()
plt.savefig("daily_fare_line.png", dpi=150)
plt.close()



# task 2:
df = pd.read_csv("auto_trips.csv")

short_trips = df[df["distance_km"] <= 5]
long_trips = df[df["distance_km"] > 5]

plt.figure(figsize=(8, 5))

plt.scatter(
    short_trips["distance_km"],
    short_trips["fare_inr"],
    color="orange",
    alpha=0.6,
    label="Trips up to 5 km"
)

plt.scatter(
    long_trips["distance_km"],
    long_trips["fare_inr"],
    color="teal",
    alpha=0.6,
    label="Trips over 5 km"
)

plt.title("Fare vs Distance")
plt.xlabel("Distance (km)")
plt.ylabel("Fare (INR)")
plt.legend()
plt.tight_layout()

plt.savefig("fare_vs_distance.png", dpi=150)
plt.show()


# task 3:
df = pd.read_csv("auto_trips.csv")

area_counts = df["area"].value_counts().sort_values(ascending=False)

fig, ax = plt.subplots(figsize=(8, 5))

ax.bar(
    area_counts.index,
    area_counts.values,
    color=["orange", "teal", "skyblue", "coral", "purple"]
)

ax.set_title("Number of Auto-Rickshaw Trips per Area")
ax.set_xlabel("Area")
ax.set_ylabel("Number of Trips")

plt.tight_layout()
plt.savefig("trips_per_area.png", dpi=150)
plt.show()

# task 4:
df = pd.read_csv("auto_trips.csv")

daily_fare = df.assign(trip_date=pd.to_datetime(df["trip_date"])) \
               .set_index("trip_date")["fare_inr"].resample("D").sum()

plt.figure(figsize=(11, 5))
plt.plot(daily_fare.index, daily_fare.values, marker="o")
plt.title("Daily Total Auto-Rickshaw Fare")
plt.xlabel("Trip Date")
plt.ylabel("Total Fare (INR)")
plt.xticks(rotation=45)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig("daily_fare_line.png", dpi=150)
plt.close()

short_trips = df[df["distance_km"] <= 5]
long_trips = df[df["distance_km"] > 5]

plt.figure(figsize=(8, 5))
plt.scatter(short_trips["distance_km"], short_trips["fare_inr"],
            color="orange", alpha=0.6, label="Trips up to 5 km")
plt.scatter(long_trips["distance_km"], long_trips["fare_inr"],
            color="teal", alpha=0.6, label="Trips over 5 km")
plt.title("Fare vs Distance")
plt.xlabel("Distance (km)")
plt.ylabel("Fare (INR)")
plt.legend()
plt.tight_layout()
plt.savefig("fare_vs_distance.png", dpi=150)
plt.close()

area_counts = df["area"].value_counts().sort_values(ascending=False)

fig, ax = plt.subplots(figsize=(8, 5))
ax.bar(area_counts.index, area_counts.values,
       color=["orange", "teal", "skyblue", "coral", "purple"])
ax.set_title("Number of Auto-Rickshaw Trips per Area")
ax.set_xlabel("Area")
ax.set_ylabel("Number of Trips")
plt.tight_layout()
plt.savefig("trips_per_area.png", dpi=150)
plt.close()

mean_fare = df["fare_inr"].mean()

fig, ax = plt.subplots(figsize=(8, 5))
ax.hist(df["fare_inr"], bins=15, color="teal", edgecolor="black", alpha=0.75)
ax.axvline(mean_fare, color="red", linestyle="--",
           linewidth=2, label=f"Mean fare = ₹{mean_fare:.2f}")
ax.set_title("Distribution of Auto-Rickshaw Fares")
ax.set_xlabel("Fare (INR)")
ax.set_ylabel("Frequency")
ax.legend()
plt.tight_layout()
plt.savefig("fare_hist.png", dpi=150)
plt.close()

png_files = [
    Path("daily_fare_line.png"),
    Path("fare_vs_distance.png"),
    Path("trips_per_area.png"),
    Path("fare_hist.png")
]

for file in png_files:
    print(f"{file.name}: {file.exists()}")
