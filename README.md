*RideConnect: Online Trip-Based Cab Booking Platform*

RideConnect is a full-stack web application that connects customers directly with travel agencies or individual taxi drivers for trip-based vehicle bookings. Unlike instant ride apps like Uber, RideConnect focuses on pre-planned travel bookings with options for vehicle type, duration, fare calculation, and driver preference.

---

Features

For Customers:

* Secure Registration/Login
* Trip Booking: Pickup & drop, duration, vehicle type
* Automatic Fare Estimation
* Live List of Available Vehicles
* View and Track Accepted Bookings

For Drivers/Agencies:

* Register with License Upload
* Upload Vehicle Details and Photos
* View & Accept Ride Requests
* Get User Details Upon Acceptance

For Admin:

* Monitor Users and Rides
* Verify Driver Documents
* Ban or Flag Suspicious Accounts

---

Tech Stack

| Layer      | Technologies                          |
| ---------- | ------------------------------------- |
| Frontend   | HTML, CSS, JavaScript, Bootstrap      |
| Backend    | Python (Flask / Django)               |
| Database   | MySQL / PostgreSQL                    |
| API & Maps | Google Maps API (for location & fare) |
| UML Tools  | PlantUML, Draw\.io                    |

---

Project Workflow

1. User/Driver Registration

   * Drivers upload license and vehicle photo
2. User Creates Trip Request

   * Enters location, duration, and contact info
3. System Suggests Available Cabs

   * Based on distance, type, and availability
4. User Books Trip

   * Fare calculated automatically
5. Driver Accepts Request

   * Gets user details after acceptance
6. Admin Monitors All Activity

---

UML Diagrams

* Use Case Diagram
* Class Diagram
* Sequence Diagram (Booking Flow)
* ER Diagram (Database Schema)
* Data Flow Diagram (Frontend to Backend)

---

Folder Structure (Suggested)

rideconnect/
├── frontend/
│   ├── index.html
│   ├── login.html
│   └── styles/
├── backend/
│   ├── app.py (or views.py)
│   └── controllers/
├── database/
│   ├── schema.sql
│   └── seed.sql
├── static/
│   └── images/, js/, css/
├── UML\_Diagrams/
├── README.md
└── requirements.txt

---

Setup Instructions

1. Clone the repo

   git clone [https://github.com/your-username/rideconnect.git](https://github.com/your-username/rideconnect.git)
   cd rideconnect

2. Set up virtual environment (for Python projects)

   python -m venv env
   source env/bin/activate  # or env\Scripts\activate on Windows

3. Install dependencies

   pip install -r requirements.txt

4. Run the server

   python app.py

5. Open `localhost:5000` in your browser

---

Contributor

* Hemasri Bandari


---

License

MIT License. Feel free to fork, modify, and build upon RideConnect for personal or academic use.

---

Made with love for Final Year Project 2025
