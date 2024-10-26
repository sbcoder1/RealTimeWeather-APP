'''import mysql.connector
from datetime import datetime

# Database connection details
connection = mysql.connector.connect(
    host='localhost',
    user='root',
    password='root',
    database='weather_monitoring'
)

cursor = connection.cursor()

def calculate_daily_summary(city_name):
    # Store today's date
    today = datetime.now().date()

    # Query to get today's weather data for a specific city
    query = """
    SELECT temp, weather_condition 
    FROM weather_data 
    WHERE DATE(timestamp) = CURDATE() AND city = %s
    """
    cursor.execute(query, (city_name,))
    results = cursor.fetchall()

    if results:
        # Initialize variables for calculations
        total_temp = 0
        max_temp = float('-inf')
        min_temp = float('inf')
        weather_conditions = {}

        # Process each result
        for row in results:
            temp, weather_condition = row
            total_temp += temp
            max_temp = max(max_temp, temp)
            min_temp = min(min_temp, temp)
            weather_conditions[weather_condition] = weather_conditions.get(weather_condition, 0) + 1

        # Calculate average temperature
        avg_temp = total_temp / len(results)
        
        # Determine dominant weather condition
        dominant_condition = max(weather_conditions, key=weather_conditions.get)

        # Insert daily summary into the database
        summary_query = """
        INSERT INTO daily_summary (city, date, avg_temp, max_temp, min_temp, dominant_condition) 
        VALUES (%s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            avg_temp = VALUES(avg_temp),
            max_temp = VALUES(max_temp),
            min_temp = VALUES(min_temp),
            dominant_condition = VALUES(dominant_condition)
        """
        cursor.execute(summary_query, (city_name, today, avg_temp, max_temp, min_temp, dominant_condition))
        connection.commit()
        print(f"Daily summary stored for {city_name} on {today}: Avg Temp: {avg_temp}, Max Temp: {max_temp}, Min Temp: {min_temp}, Dominant Condition: {dominant_condition}")
    else:
        print(f"No weather data available for {city_name} on {today}.")

if __name__ == "__main__":
    # List of cities to process
    cities = ['Delhi', 'Mumbai', 'Chennai', 'Bangalore', 'Kolkata', 'Hyderabad']
    for city in cities:
        calculate_daily_summary(city)

    cursor.close()
    connection.close()
'''
import mysql.connector
from datetime import datetime

# Database connection details
connection = mysql.connector.connect(
    host='localhost',
    user='root',
    password='root',
    database='weather_monitoring'
)

cursor = connection.cursor()

def calculate_daily_summary(city_name):
    # Store today's date
    today = datetime.now().date()

    # Query to get today's weather data for a specific city
    query = """
    SELECT temp, humidity, weather_condition 
    FROM weather_data 
    WHERE DATE(timestamp) = CURDATE() AND city = %s
    """
    cursor.execute(query, (city_name,))
    results = cursor.fetchall()

    if results:
        # Initialize variables for calculations
        total_temp = 0
        total_humidity = 0  # Initialize total_humidity
        max_temp = float('-inf')
        min_temp = float('inf')
        max_humidity = float('-inf')  # Initialize max_humidity
        min_humidity = float('inf')  # Initialize min_humidity
        weather_conditions = {}

        # Process each result
        for row in results:
            temp, humidity, weather_condition = row
            
            total_temp += temp
            
            # Check for None before adding to total_humidity
            if humidity is not None:
                total_humidity += humidity
                max_humidity = max(max_humidity, humidity)
                min_humidity = min(min_humidity, humidity)

            max_temp = max(max_temp, temp)
            min_temp = min(min_temp, temp)
            weather_conditions[weather_condition] = weather_conditions.get(weather_condition, 0) + 1

        # Calculate averages if we have valid humidity data
        avg_humidity = total_humidity / len(results) if len(results) > 0 else None

        # Calculate average temperature
        avg_temp = total_temp / len(results)

        # Determine dominant weather condition
        dominant_condition = max(weather_conditions, key=weather_conditions.get)

        # Insert daily summary into the database
        summary_query = """
        INSERT INTO daily_summary (city, date, avg_temp, max_temp, min_temp, dominant_condition, avg_humidity, max_humidity, min_humidity) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            avg_temp = VALUES(avg_temp),
            max_temp = VALUES(max_temp),
            min_temp = VALUES(min_temp),
            dominant_condition = VALUES(dominant_condition),
            avg_humidity = VALUES(avg_humidity),
            max_humidity = VALUES(max_humidity),
            min_humidity = VALUES(min_humidity)
        """
        cursor.execute(summary_query, (city_name, today, avg_temp, max_temp, min_temp, dominant_condition, avg_humidity, max_humidity, min_humidity))
        connection.commit()
        print(f"Daily summary stored for {city_name} on {today}: Avg Temp: {avg_temp}, Max Temp: {max_temp}, Min Temp: {min_temp}, Dominant Condition: {dominant_condition}, Avg Humidity: {avg_humidity}, Max Humidity: {max_humidity}, Min Humidity: {min_humidity}")
    else:
        print(f"No weather data available for {city_name} on {today}.")

if __name__ == "__main__":
    # List of cities to process
    cities = ['Delhi', 'Mumbai', 'Chennai', 'Bangalore', 'Kolkata', 'Hyderabad']
    for city in cities:
        calculate_daily_summary(city)

    cursor.close()
    connection.close()
