- Real-Time Order Management System

A Flask-based web application that allows admins to manage customer orders and customers to view live order status updates in real-time.
The app uses Socket.IO for instant updates, SQLAlchemy ORM for database management, and Flask-Mail for email notifications.

- Features

Admin Dashboard with two main options:

🧩 Add User – Insert new records into the database.

✏️ Edit User Info – Modify existing order and customer data.

Automatic Email Notification to the customer when their order is updated.

Real-Time Updates using Socket.IO (no page refresh required).

SQLAlchemy ORM Integration with SQLite database.

Secure Environment Variables via .env file.

Modular Flask Application Structure for better readability and scalability.

Bootstrap UI for a clean, responsive interface.

- Approach & Design Choices
- Framework: Flask

Chosen for its simplicity, flexibility, and ease of integration.

Works seamlessly with SQLAlchemy and Flask-Mail.

Ideal for small to medium-scale web applications.

2️⃣ Database: SQLAlchemy ORM

Provides abstraction from raw SQL queries.

Enables Pythonic interaction with the database.

Handles table relationships and schema creation automatically.

3️⃣ Real-Time Communication: Flask-SocketIO

Ensures all connected clients (Admin & Customer) receive instant updates when an order changes.

Removes the need for manual page refresh.

4️⃣ Email Notifications: Flask-Mail

Automatically notifies the customer when their order status is updated.

Uses Gmail’s SMTP service for delivery.

Secure credentials management via .env file.

5️⃣ Security & Configuration

Sensitive data such as email credentials are never hardcoded.

.env file loaded using python-dotenv.

Uses Gmail App Passwords instead of the main account password for added security.

6️⃣ UI / UX Design

Simple and responsive UI using Bootstrap 5.

Two clean sections in the admin panel:

Add new order

Edit existing order

Customer view automatically refreshes with live updates via Socket.IO.

📂 Project Structure
APT_Task/
│
├── main.py                 # Main Flask application entry point
├── models.py               # SQLAlchemy models (Orders, CustomerInfo, etc.)
├── templates/
│   ├── home.html           # Dashboard for viewing live orders
│   ├── login.html          # Customer login page
│   ├── customer.html       # Customer order tracking page
│   ├── add.html            # Admin - Add Order page
│   ├── edit.html           # Admin - Edit Order page
│
├── .env                    # Environment variables (mail credentials)
├── requirements.txt        # Python dependencies
└── README.md               # Project documentation
How to Run the Project
1️⃣ Install Dependencies

Make sure Python 3.8+ is installed, then run:
pip install -r requirements.txt
2️⃣ Set Up Environment Variables

Create a .env file in your project root and add:
MAIL_USERNAME=your_email@gmail.com
MAIL_PASSWORD=your_app_password
3️⃣ Initialize the Database

When you first run the app, it will automatically create the database (orders.db) and insert sample data.

4️⃣ Run the Application
python main.py

