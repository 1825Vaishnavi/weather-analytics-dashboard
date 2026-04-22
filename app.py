import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression

st.set_page_config(
    page_title="Weather Analytics Dashboard",
    page_icon="🌤️",
    layout="wide"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&display=swap');
html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
section[data-testid="stSidebar"] {
    background: #f8fafc;
    border-right: 1px solid #e2e8f0;
}
[data-testid="stMetricValue"] {
    font-size: 1.8rem !important;
    font-weight: 700 !important;
    color: #0f172a !important;
}
[data-testid="stMetricLabel"] {
    font-size: 0.72rem !important;
    color: #64748b !important;
    text-transform: uppercase !important;
    letter-spacing: 0.8px !important;
}
[data-testid="metric-container"] {
    background: #ffffff !important;
    border: 1px solid #e2e8f0 !important;
    border-radius: 12px !important;
    padding: 1rem 1.2rem !important;
    box-shadow: 0 1px 3px rgba(0,0,0,0.06) !important;
}
.section-header {
    font-size: 1.1rem;
    font-weight: 600;
    color: #0f172a;
    padding: 1.5rem 0 0.5rem 0;
    border-bottom: 2px solid #0ea5e9;
    margin-bottom: 1rem;
    display: block;
}
.hero-box {
    background: linear-gradient(135deg, #0f172a 0%, #1e3a5f 100%);
    padding: 2.5rem;
    border-radius: 16px;
    margin-bottom: 2rem;
}
.insight-box {
    background: #f0f9ff;
    border-left: 4px solid #0ea5e9;
    padding: 1rem 1.2rem;
    border-radius: 0 8px 8px 0;
    margin: 0.5rem 0 1rem 0;
    color: #0f172a;
    font-size: 0.92rem;
}
.score-high { color: #16a34a; font-weight: 700; }
.score-mid  { color: #d97706; font-weight: 700; }
.score-low  { color: #dc2626; font-weight: 700; }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    df = pd.read_csv("data/processed/cleaned_weather.csv", parse_dates=["DATE"])
    return df

df = load_data()

# ── Sidebar ─────────────────────────────────────
with st.sidebar:
    st.markdown("### 🌤️ Dashboard")
    st.markdown("""
    <div style='background:#f1f5f9;border-radius:10px;padding:0.8rem;margin-bottom:1rem;font-size:0.88rem;'>
        <a href='#kpis' style='display:block;padding:0.4rem 0.6rem;border-radius:6px;color:#334155;text-decoration:none;margin:0.15rem 0;'>📊 Key Statistics</a>
        <a href='#map' style='display:block;padding:0.4rem 0.6rem;border-radius:6px;color:#334155;text-decoration:none;margin:0.15rem 0;'>🗺️ Station Map</a>
        <a href='#score' style='display:block;padding:0.4rem 0.6rem;border-radius:6px;color:#334155;text-decoration:none;margin:0.15rem 0;'>🎯 Site Suitability Score</a>
        <a href='#wind' style='display:block;padding:0.4rem 0.6rem;border-radius:6px;color:#334155;text-decoration:none;margin:0.15rem 0;'>💨 Wind Trends</a>
        <a href='#forecast' style='display:block;padding:0.4rem 0.6rem;border-radius:6px;color:#334155;text-decoration:none;margin:0.15rem 0;'>📈 Wind Forecast</a>
        <a href='#temp' style='display:block;padding:0.4rem 0.6rem;border-radius:6px;color:#334155;text-decoration:none;margin:0.15rem 0;'>🌡️ Temperature</a>
        <a href='#anomaly' style='display:block;padding:0.4rem 0.6rem;border-radius:6px;color:#334155;text-decoration:none;margin:0.15rem 0;'>⚠️ Anomaly Detection</a>
        <a href='#precip' style='display:block;padding:0.4rem 0.6rem;border-radius:6px;color:#334155;text-decoration:none;margin:0.15rem 0;'>🌧️ Precipitation</a>
        <a href='#report' style='display:block;padding:0.4rem 0.6rem;border-radius:6px;color:#334155;text-decoration:none;margin:0.15rem 0;'>📋 Turbine Ops Report</a>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 🔍 Filters")
    seasons = st.multiselect("Season",
        options=df["SEASON"].unique(),
        default=df["SEASON"].unique())
    months = st.multiselect("Month",
        options=sorted(df["MONTH"].unique()),
        default=sorted(df["MONTH"].unique()))
    st.markdown("---")
    st.caption("NOAA NCEI Climate Data\nNortheastern University\nVaishnavi M. Gajarla")

filtered = df[df["SEASON"].isin(seasons) & df["MONTH"].isin(months)]

# ── Hero ─────────────────────────────────────────
st.markdown("""
<div class='hero-box'>
    <h1 style='color:#ffffff;margin:0;font-size:2rem;font-weight:700;'>
        🌤️ NOAA Weather Analytics Dashboard
    </h1>
    <p style='color:#94a3b8;margin:0.5rem 0 0 0;font-size:1rem;'>
        164 Weather Stations &nbsp;·&nbsp; 46,700+ Daily Records &nbsp;·&nbsp;
        Massachusetts &nbsp;·&nbsp; Jan–Dec 2024
    </p>
    <p style='color:#38bdf8;margin:0.4rem 0 0 0;font-size:0.85rem;'>
        ⚡ GIS-ready · Wind anomaly detection · Site suitability scoring · Turbine ops reporting · ML forecasting
    </p>
</div>
""", unsafe_allow_html=True)

# ── KPIs ─────────────────────────────────────────
st.markdown("<div id='kpis'></div>", unsafe_allow_html=True)
st.markdown("<span class='section-header'>📊 Key Statistics</span>", unsafe_allow_html=True)
c1,c2,c3,c4,c5,c6 = st.columns(6)
c1.metric("Total Records", f"{len(filtered):,}")
c2.metric("Avg Wind (m/s)", f"{filtered['AWND'].mean():.2f}")
c3.metric("Avg Max Temp", f"{filtered['TMAX'].mean():.1f}°C")
c4.metric("Total Snow", f"{filtered['SNOW'].sum():.0f}mm")
c5.metric("Wind Anomalies", f"{filtered['WIND_ANOMALY'].sum():,}")
c6.metric("Stations", f"{filtered['STATION'].nunique()}")
st.markdown("---")

# ── CHART 1: GIS Map ──────────────────────────────
st.markdown("<div id='map'></div>", unsafe_allow_html=True)
st.markdown("<span class='section-header'>🗺️ Chart 1 — Geospatial Station Map</span>", unsafe_allow_html=True)
st.caption("Stations colored by avg wind speed · Sized by precipitation · GIS-ready for wind site analysis")

station_stats = filtered.groupby(["STATION","NAME","LATITUDE","LONGITUDE"]).agg(
    Avg_Wind=("AWND","mean"),
    Total_Precip=("PRCP","sum"),
    Avg_TMAX=("TMAX","mean"),
    Site_Score=("SITE_SCORE","mean")
).reset_index()

fig1 = px.scatter_mapbox(
    station_stats, lat="LATITUDE", lon="LONGITUDE",
    color="Avg_Wind", size="Total_Precip",
    hover_name="NAME",
    hover_data={"Avg_Wind":":.2f","Site_Score":":.2f",
                "Total_Precip":":.1f","LATITUDE":False,"LONGITUDE":False},
    color_continuous_scale="RdYlGn",
    size_max=22, zoom=7,
    mapbox_style="open-street-map"
)
fig1.update_layout(height=460, margin=dict(l=0,r=0,t=0,b=0),
    coloraxis_colorbar=dict(title="Wind (m/s)"))
st.plotly_chart(fig1, use_container_width=True)
st.markdown("---")

# ── FEATURE 1: Site Suitability Score ─────────────
st.markdown("<div id='score'></div>", unsafe_allow_html=True)
st.markdown("<span class='section-header'>🎯 Wind Site Suitability Score</span>", unsafe_allow_html=True)
st.caption("Each station scored 0–10 for wind turbine viability based on avg wind speed, consistency, and anomaly frequency")

top_stations = station_stats.sort_values("Avg_Wind", ascending=False).head(15).copy()

fig_score = go.Figure()
colors = ["#16a34a" if s >= 4 else "#d97706" if s >= 2 else "#dc2626"
          for s in top_stations["Site_Score"]]
fig_score.add_trace(go.Bar(
    x=top_stations["NAME"].str[:20],
    y=top_stations["Site_Score"],
    marker_color=colors,
    text=top_stations["Site_Score"].round(2),
    textposition="outside"
))
fig_score.add_hline(y=4, line_dash="dash", line_color="#16a34a",
    annotation_text="High Viability Threshold")
fig_score.add_hline(y=2, line_dash="dash", line_color="#d97706",
    annotation_text="Moderate Viability")
fig_score.update_layout(
    height=380, margin=dict(l=0,r=0,t=30,b=80),
    plot_bgcolor="#f8fafc", paper_bgcolor="#ffffff",
    xaxis=dict(tickangle=-35, gridcolor="#e2e8f0"),
    yaxis=dict(gridcolor="#e2e8f0", title="Site Score (0-10)", range=[0,11]),
    font=dict(color="#334155")
)
st.plotly_chart(fig_score, use_container_width=True)

best = top_stations.loc[top_stations["Site_Score"].idxmax()]
worst = top_stations.loc[top_stations["Site_Score"].idxmin()]
st.markdown(f"""
<div class='insight-box'>
🧠 <b>Smart Insight:</b> <b>{best['NAME'][:30]}</b> scores highest at 
<span class='score-high'>{best['Site_Score']:.2f}/10</span> — 
optimal wind consistency for turbine deployment. 
<b>{worst['NAME'][:30]}</b> scores lowest at 
<span class='score-low'>{worst['Site_Score']:.2f}/10</span> — 
high wind variability reduces turbine efficiency.
</div>
""", unsafe_allow_html=True)

# ── CHART 2: Wind 12-Month ────────────────────────
st.markdown("<div id='wind'></div>", unsafe_allow_html=True)
st.markdown("<span class='section-header'>💨 Chart 2 — Wind Speed Trends (12-Month)</span>", unsafe_allow_html=True)

month_names = {1:"Jan",2:"Feb",3:"Mar",4:"Apr",5:"May",6:"Jun",
               7:"Jul",8:"Aug",9:"Sep",10:"Oct",11:"Nov",12:"Dec"}
mw = filtered.groupby("MONTH")["AWND"].agg(["mean","max","min"]).reset_index()
mw["Month"] = mw["MONTH"].map(month_names)

fig2 = go.Figure()
fig2.add_trace(go.Scatter(x=mw["Month"], y=mw["mean"],
    mode="lines+markers", name="Avg Wind",
    line=dict(color="#0ea5e9",width=3), marker=dict(size=8)))
fig2.add_trace(go.Scatter(x=mw["Month"], y=mw["max"],
    mode="lines", name="Max Wind",
    line=dict(color="#f97316",dash="dash",width=2)))
fig2.add_trace(go.Scatter(x=mw["Month"], y=mw["min"],
    mode="lines", name="Min Wind",
    line=dict(color="#22c55e",dash="dot",width=2)))
fig2.update_layout(
    height=360, margin=dict(l=0,r=0,t=20,b=0),
    plot_bgcolor="#f8fafc", paper_bgcolor="#ffffff",
    xaxis=dict(gridcolor="#e2e8f0"),
    yaxis=dict(gridcolor="#e2e8f0",title="Wind Speed (m/s)"),
    legend=dict(orientation="h",y=1.1),
    font=dict(color="#334155")
)
st.plotly_chart(fig2, use_container_width=True)

peak_month = mw.loc[mw["mean"].idxmax()]
st.markdown(f"""
<div class='insight-box'>
🧠 <b>Smart Insight:</b> Peak avg wind speed occurs in 
<b>{peak_month['Month']}</b> at <b>{peak_month['mean']:.2f} m/s</b>. 
This represents the highest energy generation potential period for 
edge-of-roof turbine deployments in this region.
</div>
""", unsafe_allow_html=True)
st.markdown("---")

# ── FEATURE 2: ML Wind Forecast ───────────────────
st.markdown("<div id='forecast'></div>", unsafe_allow_html=True)
st.markdown("<span class='section-header'>📈 Wind Speed Forecast — ML Linear Regression</span>", unsafe_allow_html=True)
st.caption("Scikit-learn linear regression trained on historical wind data to forecast next 30 days")

daily_wind = filtered.groupby("DATE")["AWND"].mean().reset_index()
daily_wind["DAY_NUM"] = (daily_wind["DATE"] - daily_wind["DATE"].min()).dt.days

X = daily_wind[["DAY_NUM"]].values
y = daily_wind["AWND"].values

model = LinearRegression()
model.fit(X, y)

last_day = daily_wind["DAY_NUM"].max()
future_days = np.array([[last_day + i] for i in range(1, 31)])
future_dates = pd.date_range(
    start=daily_wind["DATE"].max() + pd.Timedelta(days=1), periods=30)
predictions = model.predict(future_days)

fig_forecast = go.Figure()
fig_forecast.add_trace(go.Scatter(
    x=daily_wind["DATE"], y=daily_wind["AWND"],
    mode="lines", name="Historical",
    line=dict(color="#94a3b8", width=1), opacity=0.7))
fig_forecast.add_trace(go.Scatter(
    x=future_dates, y=predictions,
    mode="lines+markers", name="30-Day Forecast",
    line=dict(color="#f97316", width=3, dash="dash"),
    marker=dict(size=6)))
fig_forecast.add_vrect(
    x0=future_dates[0], x1=future_dates[-1],
    fillcolor="#fff7ed", opacity=0.5, line_width=0)
fig_forecast.update_layout(
    height=380, margin=dict(l=0,r=0,t=20,b=0),
    plot_bgcolor="#f8fafc", paper_bgcolor="#ffffff",
    xaxis=dict(gridcolor="#e2e8f0"),
    yaxis=dict(gridcolor="#e2e8f0", title="Wind Speed (m/s)"),
    legend=dict(orientation="h", y=1.1),
    font=dict(color="#334155")
)
st.plotly_chart(fig_forecast, use_container_width=True)

avg_forecast = predictions.mean()
st.markdown(f"""
<div class='insight-box'>
🧠 <b>ML Insight:</b> Linear regression model predicts avg wind speed of 
<b>{avg_forecast:.2f} m/s</b> over the next 30 days 
(R² = {model.score(X,y):.3f}). 
Forecast applicable to turbine output planning and anemometer threshold calibration.
</div>
""", unsafe_allow_html=True)
st.markdown("---")

# ── CHART 3: Temperature ──────────────────────────
st.markdown("<div id='temp'></div>", unsafe_allow_html=True)
st.markdown("<span class='section-header'>🌡️ Chart 3 — Temperature Range by Season</span>", unsafe_allow_html=True)

colors_map = {"Winter":"#818cf8","Spring":"#34d399","Summer":"#f87171","Fall":"#fb923c"}
fig3 = go.Figure()
for season, color in colors_map.items():
    s = filtered[filtered["SEASON"]==season]
    if len(s) > 0:
        fig3.add_trace(go.Box(y=s["TMAX"], name=f"{season} Max",
            marker_color=color, line_color=color, boxmean=True))
        fig3.add_trace(go.Box(y=s["TMIN"], name=f"{season} Min",
            marker_color=color, opacity=0.6, line_color=color, boxmean=True))
fig3.update_layout(
    height=360, margin=dict(l=0,r=0,t=20,b=0),
    plot_bgcolor="#f8fafc", paper_bgcolor="#ffffff",
    yaxis=dict(gridcolor="#e2e8f0", title="Temperature (°C)"),
    font=dict(color="#334155")
)
st.plotly_chart(fig3, use_container_width=True)
st.markdown("---")

# ── CHART 4: Anomaly Detection ────────────────────
st.markdown("<div id='anomaly'></div>", unsafe_allow_html=True)
st.markdown("<span class='section-header'>⚠️ Chart 4 — Wind Speed Anomaly Detection (95th Percentile)</span>", unsafe_allow_html=True)

threshold_w = filtered["AWND"].quantile(0.95)
anomalies = filtered[filtered["WIND_ANOMALY"]==1]
normal = filtered[filtered["WIND_ANOMALY"]==0]
pct = round(len(anomalies)/len(filtered)*100, 2)

ca,cb,cc = st.columns(3)
ca.error(f"⚠️ {len(anomalies):,} Wind Anomalies")
cb.info(f"📊 Top 5% Threshold: {threshold_w:.2f} m/s")
cc.warning(f"🎯 {pct}% Records Flagged")

fig4 = go.Figure()
fig4.add_trace(go.Scatter(x=normal["DATE"], y=normal["AWND"],
    mode="markers", name="Normal",
    marker=dict(color="#94a3b8", size=3, opacity=0.4)))
fig4.add_trace(go.Scatter(x=anomalies["DATE"], y=anomalies["AWND"],
    mode="markers", name="⚠️ Anomaly",
    marker=dict(color="#ef4444", size=8, symbol="x")))
fig4.add_hline(y=threshold_w, line_dash="dash", line_color="#f97316",
    annotation_text=f"95th Percentile Threshold: {threshold_w:.2f} m/s",
    annotation_font_color="#f97316")
fig4.update_layout(
    height=380, margin=dict(l=0,r=0,t=20,b=0),
    plot_bgcolor="#f8fafc", paper_bgcolor="#ffffff",
    xaxis=dict(gridcolor="#e2e8f0"),
    yaxis=dict(gridcolor="#e2e8f0", title="Wind Speed (m/s)"),
    legend=dict(orientation="h", y=1.1),
    font=dict(color="#334155")
)
st.plotly_chart(fig4, use_container_width=True)

peak_anomaly_month = anomalies.groupby("MONTH").size().idxmax()
st.markdown(f"""
<div class='insight-box'>
🧠 <b>Smart Insight:</b> {len(anomalies):,} extreme wind events detected 
above the 95th percentile threshold ({threshold_w:.2f} m/s). 
Peak anomaly month: <b>{month_names[peak_anomaly_month]}</b>. 
These events represent critical monitoring periods for turbine safety 
and anemometer calibration.
</div>
""", unsafe_allow_html=True)
st.markdown("---")

# ── CHART 5: Precipitation ────────────────────────
st.markdown("<div id='precip'></div>", unsafe_allow_html=True)
st.markdown("<span class='section-header'>🌧️ Chart 5 — Monthly Precipitation by Season</span>", unsafe_allow_html=True)

mp = filtered.groupby(["MONTH","SEASON"])["PRCP"].mean().reset_index()
mp["Month"] = mp["MONTH"].map(month_names)
fig5 = px.bar(mp, x="Month", y="PRCP", color="SEASON",
    labels={"PRCP":"Avg Precipitation (mm)"},
    color_discrete_map=colors_map)
fig5.update_layout(
    height=360, margin=dict(l=0,r=0,t=20,b=0),
    plot_bgcolor="#f8fafc", paper_bgcolor="#ffffff",
    xaxis=dict(gridcolor="#e2e8f0"),
    yaxis=dict(gridcolor="#e2e8f0"),
    legend=dict(orientation="h", y=1.1),
    font=dict(color="#334155")
)
st.plotly_chart(fig5, use_container_width=True)
st.markdown("---")

# ── FEATURE 3: Turbine Ops Report ─────────────────
st.markdown("<div id='report'></div>", unsafe_allow_html=True)
st.markdown("<span class='section-header'>📋 Turbine Operations Report — Site Level</span>", unsafe_allow_html=True)
st.caption("Mirrors Accelerate Wind customer dashboard format — aggregated KPIs per season for field engineers & building managers")

report = filtered.groupby("SEASON").agg(
    Avg_Wind_ms=("AWND","mean"),
    Max_Wind_ms=("AWND","max"),
    Wind_Anomalies=("WIND_ANOMALY","sum"),
    Avg_MaxTemp_C=("TMAX","mean"),
    Avg_MinTemp_C=("TMIN","mean"),
    Total_Precip_mm=("PRCP","sum"),
    Total_Snow_mm=("SNOW","sum"),
    Avg_Site_Score=("SITE_SCORE","mean"),
    Records=("AWND","count")
).round(2).reset_index()

report["Energy_Potential"] = report["Avg_Wind_ms"].apply(
    lambda x: "🟢 High" if x >= 3.5 else "🟡 Moderate" if x >= 2.5 else "🔴 Low"
)
report["Risk_Level"] = report["Wind_Anomalies"].apply(
    lambda x: "🔴 High" if x >= 300 else "🟡 Moderate" if x >= 200 else "🟢 Low"
)

st.dataframe(report, use_container_width=True, height=220)

st.markdown(f"""
<div class='insight-box'>
🧠 <b>Operations Insight:</b> Spring shows highest anomaly count 
({report.loc[report['SEASON']=='Spring','Wind_Anomalies'].values[0] if 'Spring' in report['SEASON'].values else 'N/A'}) 
— recommend increased anemometer monitoring frequency during March–May. 
Winter records highest max wind speeds — critical period for turbine safety thresholds.
</div>
""", unsafe_allow_html=True)

# ── Pipeline Summary ──────────────────────────────
st.markdown("---")
st.markdown("<span class='section-header'>🔬 Pipeline Summary</span>", unsafe_allow_html=True)
p1,p2,p3 = st.columns(3)
p1.info("**Dimensions**\n\nRaw Columns: 13\nEngineered: 8\nTotal: 21")
p2.info(f"**Coverage**\n\nStations: {filtered['STATION'].nunique()}\nDates: {filtered['DATE'].min().date()} → {filtered['DATE'].max().date()}")
p3.info("**Methods**\n\nAnomalies: 95th Percentile\nForecast: Linear Regression\nScoring: Multi-factor Wind Index")

st.markdown("---")
st.caption("Vaishnavi Mallikarjun Gajarla · MS Data Analytics Engineering · Northeastern University · NOAA NCEI")