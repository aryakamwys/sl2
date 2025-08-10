import json
import datetime as dt
import urllib.request
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Params
LAT, LON = -6.914744, 107.609810  # Bandung
YEAR = 2025
START = f"{YEAR}0101"
today = dt.date.today()
END = f"{YEAR}1231" if today.year > YEAR else today.strftime("%Y%m%d")

# Fetch NASA POWER (daily point)
url = (
    "https://power.larc.nasa.gov/api/temporal/daily/point"
    f"?parameters=T2M,T2M_MAX,T2M_MIN&community=RE"
    f"&longitude={LON}&latitude={LAT}"
    f"&start={START}&end={END}&format=JSON&time-standard=UTC"
)
with urllib.request.urlopen(url) as resp:
    data = json.load(resp)

# Parse
recs = []
T2M = data["properties"]["parameter"]["T2M"]
T2M_MAX = data["properties"]["parameter"]["T2M_MAX"]
T2M_MIN = data["properties"]["parameter"]["T2M_MIN"]
for d, v in T2M.items():
    recs.append({
        "date": pd.to_datetime(d),
        "T2M": v,
        "T2M_MAX": T2M_MAX[d],
        "T2M_MIN": T2M_MIN[d],
    })
df = pd.DataFrame(recs).sort_values("date").reset_index(drop=True)
df["month"] = df["date"].dt.month
df["dow"] = df["date"].dt.dayofweek

# Clean
df = df.replace(-999, np.nan)
for col in ["T2M", "T2M_MAX", "T2M_MIN"]:
    df[col] = pd.to_numeric(df[col], errors="coerce")
    df.loc[(df[col] < -10) | (df[col] > 60), col] = np.nan
df = df.dropna(subset=["T2M"]).copy()

# Holidays & cuti 2025
libur = [
    "2025-01-01", "2025-01-27", "2025-01-29",
    "2025-03-29", "2025-03-31", "2025-04-01",
    "2025-04-18", "2025-04-20",
    "2025-05-01", "2025-05-12", "2025-05-29",
    "2025-06-01", "2025-06-06", "2025-06-27",
    "2025-08-17", "2025-09-05", "2025-12-25",
]
cuti = [
    "2025-01-28",
    "2025-03-28",
    "2025-04-02", "2025-04-03", "2025-04-04", "2025-04-07",
    "2025-05-13",
    "2025-05-30",
    "2025-06-09",
    "2025-12-26",
    "2025-08-18",
]
holidays_all = pd.to_datetime(libur + cuti)

# Limit to data range
start_date, end_date = df["date"].min(), df["date"].max()
holidays = set(holidays_all[(holidays_all >= start_date) & (holidays_all <= end_date)])

df["is_holiday"] = df["date"].isin(holidays)

# Holiday window (±1 day, within range)
window = set()
for h in holidays:
    for delta in (-1, 0, 1):
        day = h + pd.Timedelta(days=delta)
        if start_date <= day <= end_date:
            window.add(day)
df["is_holiday_window"] = df["date"].isin(window)

# Summaries
def summarize(mask, label):
    sub = df[mask]
    return pd.Series({
        "n_hari": len(sub),
        "mean_T2M": sub["T2M"].mean(),
        "median_T2M": sub["T2M"].median(),
        "mean_T2M_MAX": sub["T2M_MAX"].mean(),
        "mean_T2M_MIN": sub["T2M_MIN"].mean(),
        "label": label,
    })

summary = pd.concat([
    summarize(df["is_holiday"], "Libur/Cuti"),
    summarize(~df["is_holiday"], "Non-libur"),
    summarize(df["is_holiday_window"], "Jendela libur (±1)"),
    summarize(~df["is_holiday_window"], "Di luar jendela"),
], axis=1).T

# Seasonality control (median by month; months with >=3 days each category)
counts = df.groupby(["month", "is_holiday"]).size().unstack(fill_value=0)
valid_months = counts[(counts[True] >= 3) & (counts[False] >= 3)].index

per_bulan = (
    df[df["month"].isin(valid_months)]
    .groupby(["month", "is_holiday"])["T2M"].median()
    .reset_index()
    .pivot(index="month", columns="is_holiday", values="T2M")
    .rename(columns={False: "non_libur", True: "libur"})
)
per_bulan["Δ_libur_minus_non"] = per_bulan["libur"] - per_bulan["non_libur"]

# Weekend vs weekday (median)
df["is_weekend"] = df["dow"] >= 5
weekend_vs_weekday = df.groupby("is_weekend")["T2M"].median()

# Print
print("Ringkasan umum (°C):")
print(summary.round(2))
print("\nKontrol musiman — selisih per bulan (median, °C) [bulan valid]:")
print(per_bulan.round(2))
print("\nMedian T2M weekend vs weekday:", weekend_vs_weekday.round(2).to_dict())

# Plots
plt.figure(figsize=(12, 4), dpi=120)
plt.plot(df["date"], df["T2M"], label="T2M harian")
plt.scatter(df.loc[df["is_holiday"], "date"],
            df.loc[df["is_holiday"], "T2M"],
            label="Hari libur/cuti", s=28)
plt.title(f"Bandung {YEAR} — Suhu harian (T2M) & penanda libur/cuti")
plt.xlabel("Tanggal"); plt.ylabel("°C"); plt.legend(); plt.tight_layout()
plt.savefig("grafik.png"); plt.show()

plt.figure(figsize=(6, 4), dpi=120)
grp_mean = df.groupby("is_holiday")["T2M"].mean()
plt.bar(["Non-libur", "Libur/Cuti"],
        [grp_mean.get(False, np.nan), grp_mean.get(True, np.nan)])
plt.title(f"Rata-rata T2M {YEAR}: Libur/Cuti vs Non-libur (Bandung)")
plt.ylabel("°C"); plt.tight_layout()
plt.savefig("bar.png"); plt.show()

# Export
out = df.copy()
out["date"] = out["date"].dt.date
out.to_csv(f"bandung_{YEAR}_t2m_with_holidays_clean.csv", index=False)
print(f"CSV disimpan: bandung_{YEAR}_t2m_with_holidays_clean.csv")
