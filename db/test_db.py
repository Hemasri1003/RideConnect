import pymysql

# Database connection
conn = pymysql.connect(
    host="localhost",
    user="root",
    password="",  # Default is empty in XAMPP
    database="ride_connect",
    cursorclass=pymysql.cursors.DictCursor
)

cursor = conn.cursor()

# Fetch users
cursor.execute("SELECT * FROM users;")
users = cursor.fetchall()
print("Users:")
for user in users:
    print(user)

# Fetch drivers
cursor.execute("SELECT * FROM drivers;")
drivers = cursor.fetchall()
print("\nDrivers:")
for driver in drivers:
    print(driver)

# Fetch bookings
cursor.execute("SELECT * FROM bookings;")
bookings = cursor.fetchall()
print("\nBookings:")
for booking in bookings:
    print(booking)

# Close connection
conn.close()
