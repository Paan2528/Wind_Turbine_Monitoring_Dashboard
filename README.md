# Wind Turbine Monitoring Dashboard

> 🚧 **Work in progress** — Alert system in development

A Python-based monitoring system that combines real wind turbine data with live weather data to track performance, estimate power output, and detect anomalies automatically.

---

## Features

- [x] **Turbine Data Pipeline** — open dataset ingestion, data cleaning, stored in SQLite
- [x] **Weather Data Pipeline** — live wind speed from Open-Meteo API, stored in `weather_data` table
- [x] **Energy Analysis** — rotor area calculation, estimated power output, wind speed vs power correlation
- [x] **Visualisation** — charts for turbine locations, power output over time, wind speed vs power
- [ ] **Alert System** — automatic alerts based on wind speed thresholds *(in progress)*
- [ ] **Dashboard** — real-time monitoring dashboard

---

## Data Sources

- **Turbine data** — open wind turbine dataset (locations, rotor diameter, capacity)
- **Weather data** — [Open-Meteo API](https://open-meteo.com/) — `wind_speed` by timestamp

---

## Energy Analysis

Estimated power output is calculated from rotor area and wind speed:

```
Rotor Area = π × (diameter / 2)²
Estimated Power = 0.5 × air_density × rotor_area × wind_speed³ × efficiency
```

---

## Alert System (in progress)

Wind speed thresholds stored in the `alerts` table:

| Condition | Threshold | Alert |
|---|---|---|
| Low wind | < 3 m/s | Low Wind Alert |
| High wind | > 20 m/s | High Wind Warning |
| Extreme wind | > 25 m/s | Emergency Shutdown Alert |

---

## Visualisations

- Top 10 Cities with Wind Turbines
- Estimated Power Output Over Time
- Wind Speed vs Estimated Power Output

---

## Tech Stack

- **Python** — core language
- **Pandas** — data cleaning and analysis
- **SQLite** — local database (`turbine_data`, `weather_data`, `alerts`)
- **Open-Meteo API** — live weather data
- More tools to be added for dashboard

---

## Related Projects

- [Solar Energy Monitoring System](https://github.com/Paan2528/Solar-Energy-Monitoring-System) — completed monitoring system with anomaly detection and Streamlit dashboard
