import mysql.connector

# Constants for Database Credentials
DB_HOST = 'localhost'
DB_USER = 'root'
DB_PASSWORD = 'root'
DB_NAME = 'weather_monitoring'

# Step 1: Establish Database Connection
def get_database_connection():
    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

# Step 2: Insert Alert Data into the Alerts Table
def insert_alert(alert_type, city, message):
    connection = get_database_connection()
    cursor = connection.cursor()  # Create cursor outside of the try block
    try:
        insert_query = """
        INSERT INTO alerts (alert_type, city, message)
        VALUES (%s, %s, %s);
        """
        cursor.execute(insert_query, (alert_type, city, message))
        connection.commit()  # Commit the changes
        print("Alert inserted successfully.")
    except mysql.connector.Error as err:
        print(f"Error inserting alert: {err}")
    finally:
        cursor.close()  # Close the cursor
        connection.close()  # Close the connection

# Step 3: Fetch Alert Data from the Alerts Table
def fetch_alerts():
    connection = get_database_connection()
    cursor = connection.cursor(dictionary=True)  # Use dictionary cursor for named columns
    try:
        fetch_query = "SELECT * FROM alerts ORDER BY created_at DESC;"  # Order by creation time
        cursor.execute(fetch_query)
        results = cursor.fetchall()  # Fetch all results
        return results
    except mysql.connector.Error as err:
        print(f"Error fetching alerts: {err}")
        return []
    finally:
        cursor.close()  # Close the cursor
        connection.close()  # Close the connection

# Main Execution
if __name__ == "__main__":
    # Example: Insert a new alert
    insert_alert('Weather Warning', 'City Name', 'Severe weather warning for City Name.')

    # Fetch and print all alerts
    alerts = fetch_alerts()
    if alerts:
        print("\nAlerts:")
        for alert in alerts:
            print(f"ID: {alert['alert_id']}, Type: {alert['alert_type']}, City: {alert['city']}, Message: {alert['message']}, Created At: {alert['created_at']}")
    else:
        print("No alerts found.")
