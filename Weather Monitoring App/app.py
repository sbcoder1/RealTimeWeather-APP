import requests
import mysql.connector
from datetime import datetime, timedelta
import time

# Configurations
API_KEY = '8e6d355869e7725e2b3940b97f3d7246'
CITIES = ['Delhi', 'Mumbai', 'Chennai', 'Bangalore', 'Kolkata', 'Hyderabad']
INTERVAL = 300  # 5 minutes

# User-configurable alert thresholds
ALERT_THRESHOLD_TEMP = 35.0  # in Celsius
ALERT_CONSECUTIVE_COUNT = 2  # Number of consecutive readings for alert

# MySQL connection setup
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="weather_monitoring"
)
cursor = conn.cursor()

# Convert Kelvin to Celsius
def kelvin_to_celsius(temp_kelvin):
    return temp_kelvin - 273.15

# Get weather data from OpenWeatherMap API
def get_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}"
    response = requests.get(url)
    data = response.json()
    
    temp = kelvin_to_celsius(data['main']['temp'])
    feels_like = kelvin_to_celsius(data['main']['feels_like'])
    humidity = data['main']['humidity']  # New addition
    wind_speed = data['wind']['speed']  # New addition
    weather_condition = data['weather'][0]['main']
    timestamp = datetime.now()
    
    return city, temp, feels_like, humidity, wind_speed, weather_condition, timestamp

# Store weather data in the database
def store_weather_data(city, temp, feels_like, humidity, wind_speed, weather_condition, timestamp):
    query = """
    INSERT INTO weather_data (city, temp, feels_like, humidity, wind_speed, weather_condition, timestamp)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    cursor.execute(query, (city, temp, feels_like, humidity, wind_speed, weather_condition, timestamp))
    conn.commit()

# Calculate daily weather summary
def calculate_daily_summary():
    for city in CITIES:
        today = datetime.now().date()
        query = """
        SELECT AVG(temp), MAX(temp), MIN(temp), AVG(humidity), MAX(humidity), MIN(humidity), AVG(wind_speed), MAX(wind_speed), MIN(wind_speed), weather_condition 
        FROM weather_data 
        WHERE city = %s AND DATE(timestamp) = %s
        """
        cursor.execute(query, (city, today))
        result = cursor.fetchall()
        
        if result and result[0]:
            avg_temp, max_temp, min_temp, avg_humidity, max_humidity, min_humidity, avg_wind_speed, max_wind_speed, min_wind_speed, dominant_condition = result[0]
            
            if dominant_condition is not None:
                query_summary = """
                INSERT INTO daily_summary (city, date, avg_temp, max_temp, min_temp, avg_humidity, max_humidity, min_humidity, avg_wind_speed, max_wind_speed, min_wind_speed, dominant_condition)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                    avg_temp = VALUES(avg_temp),
                    max_temp = VALUES(max_temp),
                    min_temp = VALUES(min_temp),
                    avg_humidity = VALUES(avg_humidity),
                    max_humidity = VALUES(max_humidity),
                    min_humidity = VALUES(min_humidity),
                    avg_wind_speed = VALUES(avg_wind_speed),
                    max_wind_speed = VALUES(max_wind_speed),
                    min_wind_speed = VALUES(min_wind_speed),
                    dominant_condition = VALUES(dominant_condition)
                """
                cursor.execute(query_summary, (city, today, avg_temp, max_temp, min_temp, avg_humidity, max_humidity, min_humidity, avg_wind_speed, max_wind_speed, min_wind_speed, dominant_condition))
                conn.commit()
                print(f"Daily summary stored for {city} on {today}")

# Check for alerting conditions (e.g., temperature > 35°C for two consecutive updates)
def check_alerts(city, temp, timestamp):
    query = """
    SELECT temp FROM weather_data 
    WHERE city = %s 
    ORDER BY timestamp DESC LIMIT %s
    """
    cursor.execute(query, (city, ALERT_CONSECUTIVE_COUNT))
    results = cursor.fetchall()
    
    if len(results) == ALERT_CONSECUTIVE_COUNT and all(t[0] > ALERT_THRESHOLD_TEMP for t in results):
        print(f"ALERT: Temperature in {city} exceeded {ALERT_THRESHOLD_TEMP}°C for {ALERT_CONSECUTIVE_COUNT} consecutive updates.")
        store_alert(city, f'Temperature exceeded {ALERT_THRESHOLD_TEMP}°C', timestamp)

# Store triggered alerts in the database
def store_alert(city, condition_triggered, timestamp):
    query = """
    INSERT INTO alerts (city, condition_triggered, timestamp)
    VALUES (%s, %s, %s)
    """
    cursor.execute(query, (city, condition_triggered, timestamp))
    conn.commit()

# Main loop to fetch, store, and process weather data
def fetch_and_process_weather():
    while True:
        for city in CITIES:
            city_data = get_weather(city)
            store_weather_data(*city_data)
            print(f"Stored data for {city} at {city_data[-1]}")
            check_alerts(city, city_data[1], city_data[-1])  # Check for alerts after storing data
        
        # Calculate daily summaries at the end of the day
        if datetime.now().hour == 23 and datetime.now().minute >= 55:
            calculate_daily_summary()

        time.sleep(INTERVAL)

if __name__ == "__main__":
    fetch_and_process_weather()
