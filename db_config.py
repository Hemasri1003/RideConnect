import pymysql

# Database connection
conn = pymysql.connect(
    host="localhost",
    user="root",
    password="",  # Default is empty in XAMPP
    database="ride_connect"
)
cursor = conn.cursor()
print("Database connected successfully!")
