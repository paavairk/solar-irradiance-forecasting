import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Solar Irradiance Forecast Panel", page_icon="☀️", layout="wide")

st.title("☀️ Solar Irradiance Forecasting Dashboard")
st.markdown("### Location: Erlangen, Bavaria (49.5910°N, 11.0078°E)")

# --- LOAD AND TRAIN MODEL ---
@st.cache_data
def load_and_train():
    df = pd.read_csv('data/processed/erlangen_features.csv')
    df['date'] = pd.to_datetime(df['date'])
    df.set_index('date', inplace=True)
    
    feature_cols = [
        'T2M', 'CLOUD_AMT', 'WS10M', 'solar_elevation', 'solar_zenith',
        'month', 'day_of_year', 'ghi_lag_1', 'ghi_lag_7', 'ghi_lag_30',
        'ghi_rolling_mean_7', 'ghi_rolling_std_7'
    ]
    
    # Train set
    train_df = df.loc['2010':'2022']
    X_train = train_df[feature_cols]
    y_train = train_df['GHI']
    
    model = RandomForestRegressor(n_estimators=50, random_state=42, n_jobs=-1)
    model.fit(X_train, y_train)
    
    # Test set
    test_df = df.loc['2023':'2024']
    return model, test_df, feature_cols

model, test_df, feature_cols = load_and_train()

# --- SIDEBAR INTERACTION ---
st.sidebar.header("📅 Step 1: Select a Target Date")
available_dates = test_df.index.strftime('%Y-%m-%d').tolist()
selected_date_str = st.sidebar.selectbox("Choose a day to forecast:", available_dates, index=len(available_dates)-1)
selected_date = pd.to_datetime(selected_date_str)

# Extract original row data for that day
original_row = test_df.loc[selected_date].copy()

st.sidebar.header("🛠️ Step 2: Weather Overrides")
st.sidebar.write("Modify the day's weather conditions to see how the model reacts:")

# Sliders initialize at exactly what the real weather was on that specific day
input_cloud = st.sidebar.slider("Cloud Amount Fraction", 0.0, 1.0, float(original_row['CLOUD_AMT']), step=0.05)
input_temp = st.sidebar.slider("Air Temperature (2m, °C)", -15.0, 40.0, float(original_row['T2M']), step=1.0)
input_wind = st.sidebar.slider("Wind Speed (10m, m/s)", 0.0, 20.0, float(original_row['WS10M']), step=0.5)

# --- INFERENCE CALCULATION ---
# Build a customized row combining historical lags with the user's slider overrides
custom_row = original_row.copy()
custom_row['CLOUD_AMT'] = input_cloud
custom_row['T2M'] = input_temp
custom_row['WS10M'] = input_wind

# Convert to DataFrame matching feature column exact orders
input_vector = pd.DataFrame([custom_row[feature_cols]])
predicted_ghi = model.predict(input_vector)[0]
actual_ghi = original_row['GHI']

# --- DISPLAY METRICS ---
st.subheader(f"📊 Forecast vs. Reality Analysis for {selected_date_str}")

m1, m2, m3 = st.columns(3)
with m1:
    st.metric(label="Predicted GHI (With Sliders)", value=f"{predicted_ghi:.2f} W/m²")
with m2:
    st.metric(label="Actual Observed GHI (NASA)", value=f"{actual_ghi:.2f} W/m²")
with m3:
    status = "Clear Sky Profile" if input_cloud < 0.2 else "Heavy Overcast Attenuation" if input_cloud > 0.7 else "Partial Clouds"
    st.metric(label="Atmospheric Condition Mode", value=status)

# --- HISTORICAL CONTEXT WINDOW GRAPH ---
st.markdown("---")
st.subheader("📉 Operational Timeline View (Surrounding 30 Days)")

# Slice 15 days before and 15 days after the chosen date for context
idx = test_df.index.get_loc(selected_date)
start_idx = max(0, idx - 15)
end_idx = min(len(test_df), idx + 15)
window_df = test_df.iloc[start_idx:end_idx]

fig, ax = plt.subplots(figsize=(12, 4))
ax.plot(window_df.index, window_df['GHI'], label='Actual Observed GHI', color='darkorange', marker='o', alpha=0.6)
ax.axvline(selected_date, color='teal', linestyle='--', linewidth=2, label='Your Selected Date')
ax.scatter(selected_date, predicted_ghi, color='cyan', s=150, zorder=5, edgecolor='black', label='Your Slider Prediction')

ax.set_ylabel("Irradiance (W/m²)")
ax.grid(True, linestyle='--', alpha=0.4)
ax.legend()
plt.xticks(rotation=25)

st.pyplot(fig)