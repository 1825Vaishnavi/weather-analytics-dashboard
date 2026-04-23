# 🌤️ NOAA Weather Analytics Dashboard

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://1825vaishnavi-weather-analytics-dashboard-app-kzfyrk.streamlit.app/)
![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Processing-green?logo=pandas)
![Plotly](https://img.shields.io/badge/Plotly-Interactive%20Viz-purple?logo=plotly)
![NOAA](https://img.shields.io/badge/Data-NOAA%20Climate-orange)

## 🎯 Why This Project Matters for Accelerate Wind

This dashboard was built using **real NOAA weather data** across **164 Massachusetts 
weather stations** - the same type of environmental datasets used in wind energy 
site selection and turbine performance monitoring.

It directly mirrors two tools Accelerate Wind is building:
-  **GIS Software Tool** → Interactive station map with wind speed scoring
-  **Customer Dashboard** → Turbine operations reporting with live KPIs

---

## 🚀 Live Demo

🔗 **[View Live Dashboard →](https://1825vaishnavi-weather-analytics-dashboard-app-kzfyrk.streamlit.app/)**

---

## 🏗️ High Level Design (HLD)

!<img width="1440" height="1440" alt="image" src="https://github.com/user-attachments/assets/1556524a-db37-414e-b3ae-a0a5da667939" />

---

## 📊 What This Dashboard Does

| Feature | Description | Resume Bullet |
|---|---|---|
| 🗺️ GIS Station Map | 164 stations plotted with wind speed coloring | Spatial data intuition |
| 🎯 Site Suitability Score | 0-10 wind turbine viability per station | Geospatial analysis |
| 💨 12-Month Wind Trends | Avg/Max/Min wind across full year | Time-series visualization |
| 📈 ML Wind Forecast | Scikit-learn linear regression, 30-day prediction | ML pipeline |
| ⚠️ Anomaly Detection | 95th percentile wind spike flagging | Outlier detection |
| 🌡️ Temperature Analysis | Seasonal TMAX/TMIN box plots | Multi-dimension analysis |
| 🌧️ Precipitation Trends | Monthly seasonal breakdown | Environmental datasets |
| 📋 Turbine Ops Report | Site-level KPI table for field engineers | Operating statistics |

---

## 🔧 Tech Stack

| Layer | Tools |
|---|---|
| Data Ingestion | Python, Pandas, NOAA NCEI API |
| Processing | NumPy, feature engineering, median imputation |
| ML | Scikit-learn (Linear Regression) |
| Visualization | Plotly (5+ interactive charts) |
| Dashboard | Streamlit |
| GIS | Plotly Mapbox, lat/long geospatial processing |
| Version Control | Git, GitHub |

---

## 📁 Project Structure

```
weather-analytics-dashboard/
│
├── pipeline.py              # Data ingestion, cleaning, feature engineering
├── app.py                   # Streamlit dashboard (8 sections)
├── requirements.txt         # Reproducible environment
├── README.md
│
└── data/
    ├── raw/                 # NOAA NCEI CSV (local only, gitignored)
    └── processed/           # Cleaned dataset (21 columns, 46,700 rows)
```

---

## 🚀 How to Run

```bash
# 1. Clone
git clone https://github.com/1825Vaishnavi/weather-analytics-dashboard
cd weather-analytics-dashboard

# 2. Virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux

# 3. Install
pip install -r requirements.txt

# 4. Run pipeline (generates cleaned data)
python pipeline.py

# 5. Launch dashboard
streamlit run app.py
```

---

## 📈 Pipeline Architecture

```
NOAA CSV (raw)
↓
pipeline.py
↓ load_and_clean()
├── Median imputation (nulls)
├── Feature engineering (MONTH, WEEK, SEASON)
├── Anomaly detection (95th percentile)
├── Site suitability scoring (0-10)
└── cleaned_weather.csv (21 cols, 46,700 rows)
↓
app.py (Streamlit)
↓
├── GIS Map
├── Site Score
├── Wind Trends
├── ML Forecast
├── Anomaly Detection
├── Temperature
├── Precipitation
└── Turbine Ops Report
```

---

## 📊 Dataset

| Attribute | Value |
|---|---|
| Source | NOAA NCEI Climate Data Online |
| Region | Massachusetts, USA |
| Stations | 164 weather stations |
| Records | 46,700 daily observations |
| Date Range | Jan 2024 – Dec 2024 |
| Raw Columns | 13 (STATION, DATE, AWND, PRCP, SNOW, TMAX, TMIN...) |
| Engineered | 8 (MONTH, WEEK, SEASON, anomaly flags, SITE_SCORE) |
| Total Dimensions | 21 |

---

## 🧠 Key Technical Decisions

**Why 95th percentile for anomaly detection?**  
Standard in turbine monitoring - flags only the most extreme wind events 
that pose real safety/performance risk, avoiding false positives from 
normal wind variation.

**Why Linear Regression for forecasting?**  
Interpretable, fast, and directly explainable to non-technical 
stakeholders (building managers, field engineers). Appropriate for 
trend-based wind forecasting over 30-day horizons.

**Why site suitability scoring?**  
Directly mirrors the wind site selection process - combining avg wind 
speed (60% weight) and consistency (40% weight) to rank stations by 
turbine deployment viability.

---

**Vaishnavi Mallikarjun Gajarla**  
MS Data Analytics Engineering - Northeastern University  
gajarla.v@northeastern.edu
