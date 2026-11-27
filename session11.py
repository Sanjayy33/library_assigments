import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# task 1:
try:
    df = pd.read_csv("auto_trips.csv", parse_dates=["trip_date"])
except FileNotFoundError:
    np.random.seed(42)
    n = 600
    areas = ["Navrangpura", "Maninagar", "Satellite", "Vastrapur", "Paldi"]
    distance = np.random.uniform(1, 15, size=n)
    noise = np.random.uniform(-15, 25, size=n)

    df = pd.DataFrame({
        "trip_id": range(1, n + 1),
        "trip_date": pd.Timestamp("2025-04-01") + pd.to_timedelta(
            np.random.randint(0, 30, size=n), unit="D"
        ),
        "area": np.random.choice(areas, size=n),
        "distance_km": np.round(distance, 2)
    })
    df["fare_inr"] = np.round(30 + 14 * df["distance_km"] + noise).astype(int)
    df.to_csv("auto_trips.csv", index=False, date_format="%Y-%m-%d")

df["trip_date"] = pd.to_datetime(df["trip_date"])
daily_fare = df.set_index("trip_date")["fare_inr"].resample("D").sum()
area_counts = df["area"].value_counts().sort_values(ascending=False)

fig, axes = plt.subplots(2, 2, figsize=(12, 8))

axes[0, 0].plot(daily_fare.index, daily_fare.values, marker="o")
axes[0, 0].set_title("Daily Total Fare")
axes[0, 0].set_xlabel("Trip Date")
axes[0, 0].set_ylabel("Total Fare (INR)")
axes[0, 0].tick_params(axis="x", rotation=45)
axes[0, 0].grid(True, alpha=0.3)

short_trips = df[df["distance_km"] <= 5]
long_trips = df[df["distance_km"] > 5]
axes[0, 1].scatter(short_trips["distance_km"], short_trips["fare_inr"],
                   color="orange", alpha=0.6, label="Up to 5 km")
axes[0, 1].scatter(long_trips["distance_km"], long_trips["fare_inr"],
                   color="teal", alpha=0.6, label="Over 5 km")
axes[0, 1].set_title("Distance vs Fare")
axes[0, 1].set_xlabel("Distance (km)")
axes[0, 1].set_ylabel("Fare (INR)")
axes[0, 1].legend()

axes[1, 0].bar(area_counts.index, area_counts.values,
               color=["orange", "teal", "skyblue", "coral", "purple"])
axes[1, 0].set_title("Trips per Area")
axes[1, 0].set_xlabel("Area")
axes[1, 0].set_ylabel("Number of Trips")
axes[1, 0].tick_params(axis="x", rotation=25)

axes[1, 1].hist(df["fare_inr"], bins=15, color="teal",
                edgecolor="black", alpha=0.75)
mean_fare = df["fare_inr"].mean()
axes[1, 1].axvline(mean_fare, color="red", linestyle="--",
                   label=f"Mean = ₹{mean_fare:.2f}")
axes[1, 1].set_title("Fare Distribution")
axes[1, 1].set_xlabel("Fare (INR)")
axes[1, 1].set_ylabel("Frequency")
axes[1, 1].legend()

plt.tight_layout()
plt.savefig("trip_grid.png", dpi=150)
plt.show()


# task 2:
df = pd.read_csv("auto_trips.csv", parse_dates=["trip_date"])

daily_fare = (
    df.set_index("trip_date")["fare_inr"]
      .resample("D")
      .sum()
)

daily_trips = (
    df.set_index("trip_date")["trip_id"]
      .resample("D")
      .count()
)

fig, ax1 = plt.subplots(figsize=(11, 5))

line1 = ax1.plot(
    daily_fare.index,
    daily_fare.values,
    color="teal",
    linewidth=2,
    marker="o",
    label="Daily Total Fare"
)

ax1.set_xlabel("Trip Date")
ax1.set_ylabel("Total Fare (INR)", color="teal")
ax1.tick_params(axis="y", labelcolor="teal")

ax2 = ax1.twinx()

line2 = ax2.plot(
    daily_trips.index,
    daily_trips.values,
    color="orange",
    linestyle="--",
    marker="s",
    label="Daily Trip Count"
)

ax2.set_ylabel("Number of Trips", color="orange")
ax2.tick_params(axis="y", labelcolor="orange")

lines = line1 + line2
labels = [line.get_label() for line in lines]

ax1.legend(lines, labels, loc="upper left")

plt.title("Daily Fare vs Daily Trip Count")
fig.autofmt_xdate()
plt.tight_layout()

plt.savefig("fare_vs_trips_dual.png", dpi=150)
plt.show()


# task 3:
df = pd.read_csv("auto_trips.csv")

areas = [
    "Navrangpura",
    "Maninagar",
    "Satellite",
    "Vastrapur",
    "Paldi"
]

fare_data = [
    df.loc[df["area"] == area, "fare_inr"].tolist()
    for area in areas
]

fig, ax = plt.subplots(figsize=(9, 5))

ax.boxplot(fare_data)

ax.set_xticklabels(areas)
ax.set_title("Fare Distribution by Area")
ax.set_xlabel("Area")
ax.set_ylabel("Fare (INR)")

plt.tight_layout()

plt.savefig("fare_by_area_box.png", dpi=150)

plt.show()


# task 4:
df = pd.read_csv("auto_trips.csv", parse_dates=["trip_date"])

daily_fare = (
    df.set_index("trip_date")["fare_inr"]
      .resample("D")
      .sum()
)

peak_date = daily_fare.idxmax()
peak_fare = daily_fare.loc[peak_date]
average_fare = daily_fare.mean()

annotated_date = peak_date
assert annotated_date == daily_fare.idxmax()

fig, ax = plt.subplots(figsize=(11, 5))

ax.plot(
    daily_fare.index,
    daily_fare.values,
    color="teal",
    linewidth=2,
    marker="o",
    label="Daily total fare"
)

ax.axhline(
    average_fare,
    color="orange",
    linestyle="--",
    linewidth=1.8,
    label=f"Average daily fare: ₹{average_fare:.2f}"
)

ax.annotate(
    f"Peak: ₹{peak_fare:.0f}",
    xy=(peak_date, peak_fare),
    xytext=(20, 25),
    textcoords="offset points",
    arrowprops={"arrowstyle": "->", "color": "red"},
    color="red",
    fontweight="bold"
)

ax.text(
    peak_date,
    peak_fare,
    f"  ₹{peak_fare:.0f}",
    va="bottom",
    ha="left"
)

ax.set_title("Daily Total Fare with Peak Day and Average")
ax.set_xlabel("Trip Date")
ax.set_ylabel("Total Fare (INR)")
ax.legend()
ax.grid(True, alpha=0.3)
fig.autofmt_xdate()
plt.tight_layout()

plt.savefig("fare_peak_annotated.png", dpi=150)
plt.show()

print("Peak date:", peak_date.date())
print("Peak fare:", peak_fare)
print("Average daily fare:", round(average_fare, 2))
print("Assertion passed:", annotated_date == daily_fare.idxmax())
