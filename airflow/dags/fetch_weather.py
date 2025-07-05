import requests
from datetime import datetime, timezone
import psycopg2
import os
from dotenv import load_dotenv
import logging

load_dotenv('/opt/airflow/.env')

API_KEY = os.getenv('OPENWEATHER_API_KEY')
print("API Key is:", API_KEY)

LAT = 42.3865
LON = -71.0228
URL = f"https://api.openweathermap.org/data/2.5/forecast?lat={LAT}&lon={LON}&cnt=40&appid={API_KEY}&mode=json"

DB_CONFIG = {
    'host': os.getenv('POSTGRES_HOST'),
    'port': int(os.getenv('POSTGRES_PORT')),
    'database': os.getenv('POSTGRES_WEATHER_DB'),
    'user': os.getenv('POSTGRES_USER'),
    'password': os.getenv('POSTGRES_PASSWORD')
}


def fetch_weather_data():
    response = requests.get(URL)
    response.raise_for_status()
    return response.json()

def parse_weather_data(raw_data):
    parsed = []
    city = raw_data.get("city", {})
    city_name = city.get("name")
    country = city.get("country")

    for entry in raw_data.get("list", []):
        weather = entry.get("weather", [{}])[0]
        wind = entry.get("wind", {})
        clouds = entry.get("clouds", {})
        rain = entry.get("rain", {}).get("3h", 0.0)
        snow = entry.get("snow", {}).get("3h", 0.0)
        main = entry.get("main", {})

        parsed.append({
            "timestamp": datetime.fromtimestamp(entry["dt"], tz=timezone.utc),
            "temperature": main.get("temp"),
            "temp_min": main.get("temp_min"),
            "temp_max": main.get("temp_max"),
            "feels_like": main.get("feels_like"),
            "humidity": main.get("humidity"),
            "pressure": main.get("pressure"),
            "cloudiness": clouds.get("all"),
            "wind_speed": wind.get("speed"),
            "wind_deg": wind.get("deg"),
            "wind_gust": wind.get("gust", 0),
            "visibility": entry.get("visibility"),
            "pop": entry.get("pop"),
            "rain_3h": rain,
            "snow_3h": snow,
            "weather_main": weather.get("main"),
            "weather_desc": weather.get("description"),
            "city_name": city_name,
            "country": country,
            "ingested_at": datetime.utcnow()
        })
    return parsed

def insert_to_postgres(parsed_data):
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS hourly_forecast (
            timestamp TIMESTAMPTZ PRIMARY KEY,
            temperature FLOAT,
            temp_min FLOAT,
            temp_max FLOAT,
            feels_like FLOAT,
            humidity INT,
            pressure INT,
            cloudiness INT,
            wind_speed FLOAT,
            wind_deg FLOAT,
            wind_gust FLOAT,
            visibility INT,
            pop FLOAT,
            rain_3h FLOAT,
            snow_3h FLOAT,
            weather_main VARCHAR(50),
            weather_desc VARCHAR(100),
            city_name VARCHAR(100),
            country VARCHAR(10),
            ingested_at TIMESTAMPTZ
        );
    """)
    insert_sql = """
        INSERT INTO hourly_forecast (
            timestamp, temperature, temp_min, temp_max, feels_like, humidity, pressure,
            cloudiness, wind_speed, wind_deg, wind_gust, visibility, pop,
            rain_3h, snow_3h, weather_main, weather_desc, city_name, country, ingested_at
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (timestamp) DO UPDATE SET
            temperature = EXCLUDED.temperature,
            temp_min = EXCLUDED.temp_min,
            temp_max = EXCLUDED.temp_max,
            feels_like = EXCLUDED.feels_like,
            humidity = EXCLUDED.humidity,
            pressure = EXCLUDED.pressure,
            cloudiness = EXCLUDED.cloudiness,
            wind_speed = EXCLUDED.wind_speed,
            wind_deg = EXCLUDED.wind_deg,
            wind_gust = EXCLUDED.wind_gust,
            visibility = EXCLUDED.visibility,
            pop = EXCLUDED.pop,
            rain_3h = EXCLUDED.rain_3h,
            snow_3h = EXCLUDED.snow_3h,
            weather_main = EXCLUDED.weather_main,
            weather_desc = EXCLUDED.weather_desc,
            city_name = EXCLUDED.city_name,
            country = EXCLUDED.country,
            ingested_at = EXCLUDED.ingested_at;
    """
    for record in parsed_data:
        cur.execute(insert_sql, tuple(record.values()))
    conn.commit()
    cur.close()
    conn.close()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    
    raw_data = fetch_weather_data()
    logging.info(f"Number of records fetched from API: {len(raw_data.get('list', []))}")

    parsed_data = parse_weather_data(raw_data)
    logging.info(f"Number of parsed records: {len(parsed_data)}")

    insert_to_postgres(parsed_data)
    logging.info("Weather data inserted into Postgres successfully.")
