# 🌦️ Weather Data Ingestion Pipeline (Airflow + Docker)

This project automates the ingestion of **hourly weather forecast data** from the OpenWeatherMap API using **Apache Airflow**, containerized with **Docker**, and stores it in a **PostgreSQL** database for analytics.

All components — DAGs, scripts, Dockerfiles — are located under the `airflow/` directory.

---

## 📌 Project Objectives

- Schedule and orchestrate weather data ingestion with Airflow
- Containerize the entire workflow using Docker
- Persist weather data in a PostgreSQL database
- Enable future extension for analytics and visualization

---

## 🧱 Tech Stack

| Component          | Description                                 |
|------------------  |---------------------------------------------|
| **Apache Airflow** | Task scheduling and pipeline orchestration  |
| **Docker Compose** | Multi-service orchestration                 |
| **PostgreSQL**     | Data storage                                |
| **Python**         | API interaction and data transformation     |
| **OpenWeatherMap** | Weather data source                         |

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/HarshaM98/weather_api_ingestion.git
cd weather_api_ingestion/airflow
```
---

### 2. Add Your Environment Variables
Create a .env file inside the airflow/ folder with the following:

OPENWEATHER_API_KEY=your_api_key
LATITUDE= 
LONGITUDE= 

## 🔗 API Reference

This project uses the **5-day / 3-hour forecast API** from [OpenWeatherMap](https://openweathermap.org/forecast5). The request URL format used in the DAG is:

```python
URL = f"https://api.openweathermap.org/data/2.5/forecast?lat={LAT}&lon={LON}&cnt=40&appid={API_KEY}&mode=json"

```
---

### 3. Start the Services

```
docker-compose up --build
```

This will spin up Airflow, PostgreSQL, and related services.
Access the Airflow UI at:
🔗 http://localhost:8080
🔐 Username: airflow | Password: airflow

---

### 4. Trigger the Weather DAG

Navigate to the Airflow UI

Unpause the DAG named weather_ingest_dag

Click Trigger DAG (▶) to run it

Monitor logs via the Airflow interface

---

### 📂 Project Structure

```
weather_api_ingestion/
└── airflow/
    ├── dags/
    │   ├── fetch_weather.py             # Fetches API data
    │   └── weather_ingest_dag.py        # Main Airflow DAG
    ├── logs/                            # DAG run logs
    │   ├── dag_id=weather_ingest_dag/
    │   └── scheduler/YYYY-MM-DD/
    ├── .env                             # API keys & location
    ├── Dockerfile                       # Custom Airflow image
    ├── docker-compose.yml               # Service definitions
    ├── insert_to_postgres.py            # DB load script
    ├── requirements.txt                 # Python dependencies
    └── .gitignore                       # Ignored files

```
---


### 🗃️ PostgreSQL Schema

| Column Name    | Data Type    | Description                            |
| -------------- | ------------ | -------------------------------------- |
| `timestamp`    | TIMESTAMPTZ  | **Primary key**. Forecast time in UTC  |
| `temperature`  | FLOAT        | Temperature in Kelvin                  |
| `temp_min`     | FLOAT        | Minimum forecasted temperature         |
| `temp_max`     | FLOAT        | Maximum forecasted temperature         |
| `feels_like`   | FLOAT        | Perceived temperature                  |
| `humidity`     | INT          | Humidity (%)                           |
| `pressure`     | INT          | Atmospheric pressure (hPa)             |
| `cloudiness`   | INT          | Cloud coverage (%)                     |
| `wind_speed`   | FLOAT        | Wind speed (m/s)                       |
| `wind_deg`     | FLOAT        | Wind direction (degrees)               |
| `wind_gust`    | FLOAT        | Wind gust (m/s)                        |
| `visibility`   | INT          | Visibility in meters                   |
| `pop`          | FLOAT        | Probability of precipitation (0–1)     |
| `rain_3h`      | FLOAT        | Rain volume over the last 3 hours (mm) |
| `snow_3h`      | FLOAT        | Snow volume over the last 3 hours (mm) |
| `weather_main` | VARCHAR(50)  | Weather category (e.g., Clear, Rain)   |
| `weather_desc` | VARCHAR(100) | Detailed weather description           |

---

### 🔄 DAG Workflow

Start → Fetch from API → Transform Data → Insert into PostgreSQL → End


## 📄 License

This project is licensed under the [MIT License](./LICENSE).

