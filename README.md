# Smart-Agricultural-Equipment-Rental-System
A web application for renting agricultural equipment with booking management and admin dashboard.
# 🌾 FarmRental – Smart Agricultural Equipment Rental Management System

## Overview

FarmRental is a web-based application developed as a Semester 4 Mini Project for the Bachelor of Engineering (Artificial Intelligence & Machine Learning) program under Mumbai University.

The main objective of this project is to simplify the process of renting agricultural equipment by providing a centralized platform where farmers can browse available machinery, make bookings, and manage rentals without visiting multiple rental centers. Equipment owners can list their machinery, while administrators can manage users, equipment, and bookings through an admin dashboard.

This project was developed to address common challenges faced by farmers, such as limited access to expensive machinery, lack of rental information, and inefficient manual booking systems.

---

## Problem Statement

Many farmers, especially those with small land holdings, cannot afford to purchase costly agricultural equipment such as tractors, rotavators, seed drills, and harvesters. Renting machinery is often a better alternative, but the traditional rental process is mostly manual, time-consuming, and lacks transparency.

The FarmRental system aims to digitize this process by providing an online platform that makes equipment discovery, booking, and management simple and efficient.

---

## Objectives

* Provide an easy-to-use platform for agricultural equipment rentals.
* Reduce the dependency on manual booking systems.
* Improve transparency in equipment availability.
* Allow users to view equipment details before booking.
* Help administrators efficiently manage users and rental records.
* Promote better utilization of agricultural machinery.

---

## Features

### User Module

* User Registration
* Secure Login
* View Available Equipment
* Equipment Details Page
* Equipment Booking
* View Booking History
* Profile Management

### Equipment Management

* Add Equipment
* Update Equipment Information
* Remove Equipment
* Equipment Availability Status
* Rental Pricing

### Booking System

* Online Booking
* Booking Confirmation
* Rental Duration Selection
* Booking History
* Booking Status Tracking

### Admin Panel

* Dashboard
* Manage Users
* Manage Equipment
* Manage Bookings
* Update Equipment Availability
* View System Records

---

## Technology Stack

### Frontend

* HTML5
* CSS3
* JavaScript
* Bootstrap

### Backend

* Python
* Flask

### Database

* MySQL

### Development Tools

* Visual Studio Code
* Git
* GitHub
* MySQL Workbench

---

## System Workflow

1. A new user registers on the platform.
2. The user logs into the application.
3. Available agricultural equipment is displayed.
4. The user selects the desired equipment.
5. Rental details are entered.
6. Booking is confirmed and stored in the database.
7. The administrator manages equipment and booking records through the admin dashboard.

---

## Project Structure

```text
FarmRental/
│
├── app.py
├── requirements.txt
├── README.md
├── static/
│   ├── css/
│   ├── js/
│   └── images/
│
├── templates/
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── booking.html
│   └── admin/
│
├── database/
├── screenshots/
└── models/
```

---

## Installation

### Clone the Repository

```bash
git clone https://github.com//FarmRental.git
```

### Navigate to the Project Folder

```bash
cd FarmRental
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Configure Database

* Create a MySQL database.
* Import the SQL file (if provided).
* Update the database credentials in the project configuration.

### Run the Application

```bash
python app.py
```

The application will start on:

```
http://127.0.0.1:5000
```

---

## Screenshots

Add screenshots of the following pages inside the `screenshots` folder.

* Home Page
* Login Page
* Registration Page
* Equipment Listing
* Booking Page
* User Dashboard
* Admin Dashboard

Example:


## Future Improvements

Some enhancements that can be added in future versions include:

* Online payment integration
* GPS-based equipment tracking
* Mobile application
* Real-time equipment availability
* Machine learning-based equipment recommendation
* AI chatbot for customer support
* SMS and email notifications
* User ratings and reviews
* Predictive demand analysis for equipment

---

## Learning Outcomes

Through this project, I gained practical experience in:

* Building full-stack web applications
* Database design and management
* CRUD operations
* User authentication
* Backend development using Flask
* Working with MySQL
* Version control using Git and GitHub
* Debugging and application testing

---

## Challenges Faced

While developing this project, a few challenges were encountered:

* Designing a structured database for bookings and equipment.
* Managing relationships between users, equipment, and bookings.
* Implementing user authentication securely.
* Preventing duplicate booking records.
* Integrating frontend pages with backend routes.

These challenges helped improve my understanding of web development and problem-solving.

---

## Conclusion

FarmRental demonstrates how technology can improve the agricultural equipment rental process by making it more accessible, organized, and efficient. The project combines frontend development, backend programming, and database management to deliver a practical solution that can be expanded further with modern technologies such as mobile applications and artificial intelligence.

---

## Author

**Vibhas Mahajan**

Bachelor of Engineering (Artificial Intelligence & Machine Learning)

Mumbai University

---

## License

This project is intended for educational and learning purposes. Feel free to explore, learn from, and modify the code for non-commercial use.
