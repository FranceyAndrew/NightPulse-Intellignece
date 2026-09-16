# NightPulse-Intellignece
![Python Badge](https://img.shields.io/badge/Python-3.12-blue.svg)
![FastAPI Badge](https://img.shields.io/badge/FastAPI-API%20Framework-teal.svg)
![Pandas Badge](https://img.shields.io/badge/Pandas-Data%20Processing-yellow.svg)
![NumPy Badge](https://img.shields.io/badge/NumPy-Scientific%20Computing-orange.svg)
![Scikit-learn Badge](https://img.shields.io/badge/Scikit--learn-ML-green.svg)
![Time Series Badge](https://img.shields.io/badge/Time--Series-Forecasting-purple.svg)
![XGBoost Badge](https://img.shields.io/badge/XGBoost-Gradient%20Boosting-red.svg)
![Prophet Badge](https://img.shields.io/badge/Prophet-Forecasting-blueviolet.svg)
![Status Active Badge](https://img.shields.io/badge/Status-Active-success.svg)
![License MIT Badge](https://img.shields.io/badge/License-MIT-lightgrey.svg)
![SaaS Ready Badge](https://img.shields.io/badge/SaaS-Ready-blue.svg)
![Operational Intelligence Badge](https://img.shields.io/badge/Operational-Intelligence-navy.svg)
![Forecast Engine Badge](https://img.shields.io/badge/Forecast-Engine-cyan.svg)


NightPulse Intelligence is a modular machine-learning system designed to forecast daily sales for nightlife venuse using historical data, weather, university and sports calendars, and other contectual signals. It provides demand predictions and staffing optimization to help bar owners plan each night with confidence.

## Features 
* Multi-source data ingestion (Sales, weather, campus, events, sports schedules, holidays)
* Automated preprocessing and feature engineering
* Time-series forecasting models (Prophet, XGBoost, LSTM)
* Ensemble prediction pipeline
* Staffing optimization engine
* REST API for forecasts and staffing recommendations
* Dashboard for visualizing weekly demand and operational instights

## Repository Structure
nightpulse-intelligence/\
── config/               # Settings, logging, credentials templates\
── data/                 # Raw, processed, external, and feature data\
├── notebooks/            # Exploration and prototyping\
├── src/\
│   ├── ingestion/        # Weather, calendar, and sales loaders\
│   ├── preprocessing/    # Cleaning, merging, feature engineering\
│   ├── models/           # Forecasting models + evaluation\
│   ├── optimization/     # Staffing optimizer\
│   ├── api/              # FastAPI service\
│   ├── dashboard/        # UI components and app\
│   └── utils/            # Logging, validation, helpers\
├── tests/                # Unit and integration tests\
└── deployment/           # Docker, cloud configs, infrastructure\

## Architecture Overview
NightPulse Intelligence follows a modular pipeline: \
<picture>
  <!-- Dark mode -->
  <source 
    srcset="docs/images/Architecture-diagram-dark.png" 
    media="(prefers-color-scheme: dark)"
  />

  <!-- Light mode -->
  <source 
    srcset="docs/images/Architecture-diagram-light.png" 
    media="(prefers-color-scheme: light)"
  />

  <!-- Fallback (light mode) -->
  <img 
    src="docs/images/Architecture-diagram-light.png" 
    alt="NightPulse Intelligence Architecture Diagram"
    width="800"
  />
</picture>

## Module Responsibilities

| Module            | Purpose / Responsibilities |
|-------------------|----------------------------|
| **ingestion/**    | Load external data sources (weather, calendar, sales, events). Validate schemas and normalize raw inputs. |
| **preprocessing/**| Clean, merge, and transform datasets. Handle feature engineering and dataset preparation for modeling. |
| **models/**       | Train forecasting models, run evaluation, manage model artifacts, and generate predictions. |
| **optimization/** | Compute staffing schedules using constraints, forecasts, and optimization logic. |
| **api/**          | Expose predictions, schedules, and metadata through FastAPI endpoints. Handles request/response validation. |
| **dashboard/**    | Visualize forecasts, staffing plans, KPIs, and analytics. Front‑end logic and UI components. |
| **utils/**        | Shared helpers: logging, configuration loading, validation, common utilities used across modules. |
| **tests/**        | Unit and integration tests mirroring the structure of `src/`. Ensures reliability and regression protection. |




