# 🌿 PolliWeather – Analytics Service

This is the **Analytics microservice** for the PolliWeather system – an AI-based platform for analyzing and forecasting the allergenic hazard of ragweed pollen in Kyiv.

Created as part of the bachelor’s thesis:  
**“Artificial Intelligence System for Trends Analysis in Allergenic Hazard and Allergen Spread in Kyiv City”**  
by Danil Brovko (NTUU "KPI", 2024)

---

## 📚 Table of Contents

- [🚀 Overview](#-overview)
- [🧠 Functionality](#-functionality)
- [🧮 Forecasting Model](#-forecasting-model)
- [🔗 REST API](#-rest-api)
- [🏗️ Architecture](#️-architecture)
- [📦 Project Structure](#-project-structure)
- [🔗 Related Services](#-related-services)

---

## 🚀 Overview

This Python Flask application is responsible for:

- Defining districts for ragweed plants based on geolocation
- Calculating the **Weather Factor** from raw weather data
- Training and applying deep learning models (NeuralProphet / AR-Net)
- Forecasting allergenic hazard trends at multiple granularities
- Returning statistical plots and predictions through REST API

---

## 🧠 Functionality

- Uses the `kyiv_districts.geojson` file to map coordinates to districts
- Computes **Weather Factor**:  
  **F = (t × P) / H**
  where:  
  • *t* — temperature in °C  
  • *P* — pressure in mmHg  
  • *H* — relative humidity in %
- Trains different models per frequency: `month`, `day`, and `3h`  
  (to capture yearly, weekly, and daily seasonality)
- Returns time series trends of allergenic hazard up to `10` years into the future

---

## 🧮 Forecasting Model

- Core model: **NeuralProphet** (a hybrid of AR, Fourier terms, and neural networks)
- Trained using **Mean Squared Error (MSE)**
- Forecasts seasonality components:
  - 📅 Yearly: ragweed bloom (Aug–Sep), pollen (Apr–Oct)
  - 🗓️ Weekly: traffic-linked hazard rise during weekdays
  - 🕐 Daily: peak hazard from 10:00 to 15:00

---

## 🔗 REST API

### 🌿 Ragweed Statistics

| Endpoint | Method | Description |
|---------|--------|-------------|
| `/ragweed/define-districts` | `GET` | Assign district for each plant |
| `/ragweed/statistics/spread` | `GET` | Show count of plants per district |
| `/ragweed/statistics/size` | `GET` | Show sizes of plant clusters |
| `/ragweed/statistics/spread?allLocations=true` | `GET` | Spread across all Ukraine |

### 🌡️ Prediction API

| Endpoint | Method | Parameters | Description |
|----------|--------|------------|-------------|
| `/predict-pollinosis` | `GET` | `freq=month/day/3h`, `years=5`, `retrain=true/false` | Predict allergenic hazard trend |

---

## 🏗️ Architecture

This microservice operates as the **core analytics engine** within the PolliWeather ecosystem. It communicates with the Scraper Service and the Web UI via REST and is responsible for **data transformation, statistical modeling, and AI-powered forecasting**.

<img width="468" alt="image" src="https://github.com/user-attachments/assets/f86d1468-1def-4045-b307-8ca18cf9063a" />

---

## 📦 Project Structure

```
pw-analytics-service/
├── main.py                             # Flask entry point
├── database/mysql_db.py               # MySQL connection
├── dto/                               # Data transfer objects
│   ├── ragweed_dto.py
│   ├── district_dto.py
│   ├── weather_dto.py
│   └── weather_factor_dto.py
├── dao/                               # Data access objects
│   ├── ragweed_dao.py
│   ├── district_dao.py
│   ├── weather_dao.py
│   └── weather_factor_dao.py
├── controller/                        # API endpoints
│   ├── ragweed_controller.py
│   ├── weather_factor_controller.py
│   └── neural_net_controller.py
├── service/                           # Core services
│   ├── ragweed_service.py
│   ├── weather_factor_service.py
│   └── neural_net_service.py
├── resources/kyiv_districts.geojson  # Kyiv district boundaries
└── README.md
```
---

## 🔗 Related Services

- [`Scraper Service`](https://github.com/BrovkoD/pw-scraper-service)  
  → Operates as the data ingestion layer
