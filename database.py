import os
import mysql.connector


def connect_to_db():
    # Get the values of environment variables or use default values if they are not set
    host = os.environ.get("DB_HOST", "localhost")
    port = os.environ.get("DB_PORT", 3306)
    user = os.environ.get("DB_USER", "")
    password = os.environ.get("DB_PASSWORD", "")
    database = os.environ.get("DB_DATABASE", "budget_db")

    # Connect to the database using the obtained values
    conn = mysql.connector.connect(
        host=host,
        port=port,
        user=user,
        password=password,
        database=database,
    )

    # Return the connection object
    return conn
