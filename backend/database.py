import psycopg2
from psycopg2 import sql

# Connect to PostgreSQL database
def get_db_connection():
    conn = psycopg2.connect(
        host="localhost",  # Add your PostgreSQL server IP
        database="resume_db",  # your database name
        user="postgres",  # your database username
        password="1234"  # your database password
    )
    return conn
