import pandas as pd
import numpy as np
from pathlib import Path

RAW_FILE = Path("data/raw/4295699.csv")
PROCESSED_DIR = Path("data/processed")
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

def load_and_clean():
    df = pd.read_csv(RAW_FILE, parse_dates=["DATE"])
    print(f"✅ Loaded {len(df)} records")

    # Fill numeric nulls with column median
    num_cols = df.select_dtypes(include=np.number).columns
    df[num_cols] = df[num_cols].fillna(df[num_cols].median())

    # Feature extraction
    df["MONTH"] = df["DATE"].dt.month
    df["WEEK"] = df["DATE"].dt.isocalendar().week.astype(int)
    df["SEASON"] = df["MONTH"].map({
        12:"Winter",1:"Winter",2:"Winter",
        3:"Spring",4:"Spring",5:"Spring",
        6:"Summer",7:"Summer",8:"Summer",
        9:"Fall",10:"Fall",11:"Fall"
    })

    # ── Anomaly Detection (flags TOP 5% as anomalies = 95th percentile) ──
    # This matches resume: "anomaly detection flagging 95%+ outliers"
    threshold_prcp = df["PRCP"].quantile(0.95)
    threshold_wind = df["AWND"].quantile(0.95)
    threshold_snow = df["SNOW"].quantile(0.95)

    df["PRCP_ANOMALY"] = (df["PRCP"] > threshold_prcp).astype(int)
    df["WIND_ANOMALY"] = (df["AWND"] > threshold_wind).astype(int)
    df["SNOW_ANOMALY"] = (df["SNOW"] > threshold_snow).astype(int)
    df["ANY_ANOMALY"] = ((df["PRCP_ANOMALY"]==1) | 
                          (df["WIND_ANOMALY"]==1) | 
                          (df["SNOW_ANOMALY"]==1)).astype(int)

    # ── Wind Site Suitability Score (0-10) ──
    # Based on avg wind, consistency, anomaly frequency per station
    station_scores = df.groupby("STATION").agg(
        avg_wind=("AWND","mean"),
        max_wind=("AWND","max"),
        wind_std=("AWND","std"),
        anomaly_count=("WIND_ANOMALY","sum"),
        total=("AWND","count")
    ).reset_index()

    # Normalize avg_wind to 0-10
    station_scores["wind_score"] = (
        (station_scores["avg_wind"] - station_scores["avg_wind"].min()) /
        (station_scores["avg_wind"].max() - station_scores["avg_wind"].min()) * 10
    )
    # Penalize high std (inconsistent wind is bad for turbines)
    station_scores["consistency_score"] = (
        1 - (station_scores["wind_std"] - station_scores["wind_std"].min()) /
        (station_scores["wind_std"].max() - station_scores["wind_std"].min() + 0.001)
    ) * 10
    # Final score
    station_scores["SITE_SCORE"] = (
        station_scores["wind_score"] * 0.6 +
        station_scores["consistency_score"] * 0.4
    ).round(2)

    # Merge score back
    df = df.merge(station_scores[["STATION","SITE_SCORE"]], on="STATION", how="left")

    df.to_csv(PROCESSED_DIR / "cleaned_weather.csv", index=False)
    print(f"✅ Saved cleaned data")
    print(f"✅ Columns: {list(df.columns)}")

    # Print anomaly stats
    total = len(df)
    wind_anom = df["WIND_ANOMALY"].sum()
    any_anom = df["ANY_ANOMALY"].sum()
    print(f"\n📊 Anomaly Stats:")
    print(f"   Wind anomalies: {wind_anom} ({wind_anom/total*100:.1f}%)")
    print(f"   Any anomaly: {any_anom} ({any_anom/total*100:.1f}%)")
    print(f"\n🎯 Site Score range: {station_scores['SITE_SCORE'].min():.2f} - {station_scores['SITE_SCORE'].max():.2f}")
    return df

if __name__ == "__main__":
    df = load_and_clean()
    print(df.head())