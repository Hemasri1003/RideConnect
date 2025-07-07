import os
from flask import Flask, render_template, request, session, redirect, url_for
import pymysql

app = Flask(__name__)
app.secret_key = "your_secret_key"

# Folder to save uploaded images
UPLOAD_FOLDER = "static/uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Ensure upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Database connection
conn = pymysql.connect(host="localhost", port=3307, user="root", password="", database="ride_connect")
cursor = conn.cursor()

# 🔷 Home Page
@app.route("/")
def home():
    return render_template("index.html")

# 🔷 About Page
@app.route("/about")
def about():
    return render_template("about.html")

# 🔷 Contact Page
@app.route("/contact")
def contact():
    return render_template("contact.html")

# 🔷 Terms & Conditions Page
@app.route("/terms")
def terms():
    return render_template("terms.html")

# 🔷 Login Page
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    email = request.form["email"]
    password = request.form["password"]

    query = "SELECT * FROM userss WHERE email = %s AND password = %s"
    cursor.execute(query, (email, password))
    user = cursor.fetchone()

    if user:
        session["user_id"] = user[0]
        session["role"] = user[4]

        if user[4] == "driver":
            return redirect(url_for("driver_dashboard"))
        else:
            return redirect(url_for("dashboard"))
    else:
        return "Invalid Email or Password. Try again!"

# 🔷 Register Page
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")

    name = request.form["name"]
    email = request.form["email"]
    password = request.form["password"]
    role = request.form["role"]

    license_photo = None
    vehicle_photo = None

    if role == "driver":
        license_file = request.files.get("license_photo")
        if license_file and license_file.filename != "":
            license_photo_path = os.path.join(app.config["UPLOAD_FOLDER"], license_file.filename)
            license_file.save(license_photo_path)
            license_photo = license_file.filename

        vehicle_file = request.files.get("vehicle_photo")
        if vehicle_file and vehicle_file.filename != "":
            vehicle_photo_path = os.path.join(app.config["UPLOAD_FOLDER"], vehicle_file.filename)
            vehicle_file.save(vehicle_photo_path)
            vehicle_photo = vehicle_file.filename

    query = "INSERT INTO userss (name, email, password, role, license_photo, vehicle_photo) VALUES (%s, %s, %s, %s, %s, %s)"
    try:
        cursor.execute(query, (name, email, password, role, license_photo, vehicle_photo))
        conn.commit()
        return redirect(url_for("login"))
    except pymysql.err.IntegrityError:
        return "Email already exists! Try another email."

# 🔷 Driver Dashboard
@app.route("/driver-dashboard")
def driver_dashboard():
    if "user_id" not in session or session.get("role") != "driver":
        return redirect(url_for("login"))

    cursor.execute("""
        SELECT id, pickup_location, drop_location, booking_type, vehicle_type, contact_details 
        FROM bookings 
        WHERE status = 'pending'
    """)
    ride_requests = cursor.fetchall()

    return render_template("driver-dashboard.html", ride_requests=ride_requests)

# 🔷 User Dashboard
@app.route("/dashboard")
def dashboard():
    if "user_id" not in session or session.get("role") != "user":
        return redirect(url_for("login"))

    user_id = session["user_id"]
    cursor.execute("SELECT * FROM bookings WHERE user_id = %s", (user_id,))
    bookings = cursor.fetchall()

    driver_data = {}
    for booking in bookings:
        driver_id = booking[2]  # driver_id
        status = booking[6]     # status

        if status == "accepted" and driver_id:
            cursor.execute("SELECT name, email, license_photo, vehicle_photo FROM userss WHERE id = %s", (driver_id,))
            driver_info = cursor.fetchone()
            if driver_info:
                driver_data[booking[0]] = driver_info

    return render_template("user-dashboard.html", bookings=bookings, driver_data=driver_data)

# 🔷 Book Trip
@app.route("/book-trip", methods=["GET", "POST"])
def book_trip():
    if "user_id" not in session or session.get("role") != "user":
        return redirect(url_for("login"))

    if request.method == "POST":
        print("🚀 POST request received")  # NEW

        try:
            user_id = session["user_id"]
            pickup = request.form["pickup_location"]
            drop = request.form["drop_location"]
            booking_type_raw = request.form["booking_type"]
            booking_type = "Driver Only" if booking_type_raw == "driver" else "Vehicle + Driver"
            contact_details = request.form["contact_details"]
            vehicle_type = request.form.get("vehicle_type") if booking_type_raw == "driver_vehicle" else "N/A"
            num_seats = request.form.get("num_seats") if booking_type_raw == "driver_vehicle" else 0

            hours = int(request.form.get("hours") or 0)
            minutes = int(request.form.get("minutes") or 0)
            trip_duration = hours * 60 + minutes
            distance = float(request.form.get("distance") or 0)

            # Fare calculation
            base_fare = 50
            booking_fee = 20
            additional_fee = 15
            surge_multiplier = 1.0
            per_minute_cost = 2
            per_distance_cost = 10

            fare = (
                base_fare +
                booking_fee +
                additional_fee +
                surge_multiplier * ((per_minute_cost * trip_duration) + (per_distance_cost * distance))
            )

            query = """
                INSERT INTO bookings (
                    user_id, pickup_location, drop_location, booking_type,
                    vehicle_type, num_seats, contact_details, trip_duration,
                    distance, fare, status
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 'pending')
            """
            cursor.execute(query, (
                user_id, pickup, drop, booking_type,
                vehicle_type, num_seats, contact_details,
                trip_duration, distance, fare
            ))
            conn.commit()

            print("✅ Booking inserted for user ID:", user_id)
            return redirect(url_for("dashboard"))

        except Exception as e:
            print("🔥 Booking Error:", e)
            return f"Booking failed: {str(e)}"

    print("📄 Serving book-trip.html via GET")
    return render_template("book-trip.html")


@app.route("/accepted-user-details", methods=["POST"])
def accepted_user_details():
    if "user_id" not in session or session.get("role") != "driver":
        return redirect(url_for("login"))

    booking_id = request.form.get("booking_id")
    if not booking_id:
        return "Booking ID missing", 400

    driver_id = session["user_id"]

    # Accept the ride
    cursor.execute("UPDATE bookings SET driver_id = %s, status = 'accepted' WHERE id = %s", (driver_id, booking_id))
    conn.commit()

    # Fetch user details
    cursor.execute("""
        SELECT u.name, u.email, u.license_photo, u.vehicle_photo,
               b.pickup_location, b.drop_location, b.contact_details
        FROM bookings b
        JOIN userss u ON b.user_id = u.id
        WHERE b.id = %s
    """, (booking_id,))
    user_info = cursor.fetchone()

    if not user_info:
        return "User information not found", 404

    return render_template("accepted-user-details.html", user_info=user_info)


# 🔷 Logout
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))

# 🔷 Serve uploaded photos
@app.route('/static/uploads/<filename>')
def uploaded_file(filename):
    return redirect(url_for('static', filename=f"uploads/{filename}"))

if __name__ == "__main__":
    app.run(debug=True)
