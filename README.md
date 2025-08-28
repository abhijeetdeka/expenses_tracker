# expenses_tracker
Simple Daily Expense Tracker
Expense Tracker - Python, Tkinter & MySQL
📌 Project Overview

The Expense Tracker is a desktop application built using Python, Tkinter, and MySQL to manage and track daily expenses efficiently.
It provides a user-friendly interface for adding, deleting, and viewing expenses, along with a password-protected system for data security.

🚀** Features**

🔑 Secure Admin Login with password authentication

➕ Add Expenses with date, category, description, and amount

🗑️ Delete Expenses securely after password verification

📜 View All Expenses in a sortable table

💾 MySQL Database Integration for reliable data storage

🔒 Default Admin Password (can be changed)

🛠️ Automatic Database & Table Creation on first run

🛠️ Tech Stack

Programming Language: Python

GUI Framework: Tkinter

Database: MySQL

Date Picker: tkcalendar

Library Used: mysql-connector-python

📂 Project Structure
Expense-Tracker/
│── expense_tracker.py   # Main application file
│── requirements.txt     # Required Python libraries
│── README.md            # Project documentation
└── screenshots/         # App screenshots (optional)

🗄️ Database Setup
Step 1 — Create Database

The app automatically creates the database and tables,
but you can also create it manually in MySQL:

CREATE DATABASE expenses_db;
USE expenses_db;

CREATE TABLE expenses (
    id INT AUTO_INCREMENT PRIMARY KEY,
    date DATE,
    category VARCHAR(100),
    description VARCHAR(255),
    amount DECIMAL(10,2)
);

CREATE TABLE admin_password (
    id INT AUTO_INCREMENT PRIMARY KEY,
    password VARCHAR(255) NOT NULL
);

INSERT INTO admin_password (password) VALUES ('admin123');

⚙️ Installation
Step 1 — Clone the Repository
git clone https://github.com/your-username/expense-tracker.git
cd expense-tracker

Step 2 — Install Required Libraries
pip install -r requirements.txt

Step 3 — Configure Database

Open expense_tracker.py and update:

user="root"
password="your_mysql_password"

Step 4 — Run the Application
python expense_tracker.py

📸 Screenshots
Dashboard	Add Expense	View Expenses

	
	

(You can capture your app screens and save them inside a screenshots/ folder.)

🔐 Default Login

Username: (not required)
Password: admin123

You can update the password directly from the database.

🔮 Future Enhancements

📊 Add expense analytics with graphs

📤 Export expenses to CSV & PDF

📱 Make it mobile-friendly with Kivy

👥 Multi-user login system
