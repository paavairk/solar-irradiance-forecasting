# ☀️ Solar Irradiance Forecasting for Germany

> Predicting daily Global Horizontal Irradiance (GHI) using NASA satellite data and machine learning — built to support smarter solar energy grid planning.

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat-square&logo=python)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)
![Data](https://img.shields.io/badge/Data-NASA%20POWER-orange?style=flat-square)
![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=flat-square)

---

## What this project does

Solar power output is highly variable — clouds, seasons, and atmospheric conditions cause GHI to fluctuate day to day. Grid operators need accurate short-term forecasts to balance supply and demand. This project builds and benchmarks multiple forecasting models on 14 years of NASA satellite data for Bavaria, Germany, achieving **50.05% lower MAE than a naive baseline**.

The models are served through an interactive Streamlit dashboard where users can select a German city and forecast horizon and see predicted irradiance alongside historical trends.

---

## Results

| Model | MAE (W/m²) | RMSE (W/m²) | R² | vs. Baseline |
|---|---|---|---|---|
| Naive (lag-1) | 0.84 | 1.20 | 0.8443 | baseline |
| Random Forest | 0.42 | 0.60 | 0.9221 | 50.05% better |
| Prophet | — | — | — | —% better |
| LSTM | — | — | — | —% better |

*Test set: 2023–2024. Results are updated continuously as models are refined.*

---

## Data

Data is sourced from the [NASA POWER API](https://power.larc.nasa.gov/) — free, no login required.

| Parameter | Description |
|---|---|
| `ALLSKY_SFC_SW_DWN` | Global Horizontal Irradiance (target variable) |
| `T2M` | Air temperature at 2m |
| `CLOUD_AMT` | Cloud amount (fraction) |
| `WS10M` | Wind speed at 10m |

**Coverage:** 2010–2024 · Daily resolution · Location: Erlangen, Bavaria (49.5910°N, 11.0078°E)

---

## Project structure
solar-irradiance-forecasting/
├── data/
│   ├── raw/              # NASA POWER downloads (auto-generated, gitignored)
│   └── processed/        # Engineered datasets with physics/lag variables
├── notebooks/
│   ├── 02_feature_engineering.ipynb
│   └── 03_modelling.ipynb
├── src/
│   ├── fetch_data.py     # NASA POWER API client
│   ├── features.py       # Feature engineering pipeline
│   └── models.py         # Model training and evaluation
├── outputs/
│   └── figures/          # Saved plots (RF feature importance, etc.)
├── app.py                # Streamlit dashboard
├── requirements.txt
└── README.md


---

## Quickstart

```bash
# 1. Clone the repo
git clone [https://github.com/paavai-rk/solar-irradiance-forecasting.git](https://github.com/paavai-rk/solar-irradiance-forecasting.git)
cd solar-irradiance-forecasting

# 2. Install dependencies
pip install -r requirements.txt

# 3. Download the data (fetches from NASA POWER API automatically)
python src/fetch_data.py

# 4. Launch the dashboard (coming soon)
# streamlit run app.py
```
Methods
Feature engineering

    Astronomical features via pvlib: solar elevation angle, solar zenith angle

    Lag features: GHI at t−1, t−7, t−30 days

    Calendar features: day of year, month, season encoding

    Rolling statistics: 7-day rolling mean and standard deviation

Models

    Naive baseline — previous day's GHI (lag-1)

    Random Forest — ensemble of decision trees with 100 estimators; optimized to prevent data leakage from concurrent target derivations.

Evaluation

Chronological train/validation/test split to prevent data leakage:

    Training: 2010–2021

    Validation: 2022

    Test: 2023–2024

About

Built by Paavai Rajasekar Kavitha — M.Sc. Physics (FAU Erlangen), with a background in astrophysical data analysis, satellite data pipelines, and time-series modelling (blazar light curves, SED fitting).

This project bridges skills from high-energy astrophysics into the renewable energy domain — the same Python pipelines and signal variability methods used on FERMI and eROSITA data apply directly to forecasting solar irradiance.

## Contact

🔗 [LinkedIn](https://www.linkedin.com/in/paavai-r-k)  
📧 [Email](mailto:paavai.rk@gmail.com)

MIT License — free to use, adapt, and build on. See LICENSE for details.
