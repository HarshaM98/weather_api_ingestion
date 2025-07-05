import psycopg2
from psycopg2.extras import execute_values
from Weather_Api_Project.airflow.dags.fetch_weather import fetch_weather_data, parse_weather_data

# DB config
DB_HOST = "localhost"
DB_PORT = 5432
DB_NAME = "weather"
DB_USER = "airflow"
DB_PASSWORD = "airflow_password"

TABLE_NAME = "hourly_forecast"

CREATE_TABLE_QUERY = f"""
CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMPTZ NOT NULL,
    temperature FLOAT NOT NULL,
    humidity INT NOT NULL,
    wind_speed FLOAT NOT NULL,
    weather_main VARCHAR(50) NOT NULL,
    weather_desc VARCHAR(100) NOT NULL,
    inserted_at TIMESTAMPTZ DEFAULT now()
);
"""

INSERT_QUERY = f"""
INSERT INTO {TABLE_NAME} (
    timestamp, temperature, humidity, wind_speed, weather_main, weather_desc
) VALUES %s;
"""

def connect_db():
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )

def create_table(conn):
    with conn.cursor() as cur:
        cur.execute(CREATE_TABLE_QUERY)
        conn.commit()

def insert_weather_data(conn, records):
    data = [
        (
            record["timestamp"],
            record["temperature"],
            record["humidity"],
            record["wind_speed"],
            record["weather_main"],
            record["weather_desc"]
        )
        for record in records
    ]
    with conn.cursor() as cur:
        execute_values(cur, INSERT_QUERY, data)
        conn.commit()

if __name__ == "__main__":
    print("Starting weather data fetch...")
    raw_data = fetch_weather_data()
    if raw_data:
        print("Parsing weather data...")
        weather_records = parse_weather_data(raw_data)
        if weather_records:
            print(f"Parsed {len(weather_records)} records. Connecting to DB...")
            conn = connect_db()
            print("Creating table if not exists...")
            create_table(conn)
            print("Inserting data...")
            insert_weather_data(conn, weather_records)
            conn.close()
            print(f"✅ Inserted {len(weather_records)} records into Postgres.")
        else:
            print("⚠️ No weather records parsed.")
    else:
        print("❌ Weather data fetch failed.")
