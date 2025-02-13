# ticket_booking_movie_website
Movie Booking System
A Flask-based web application for booking movie tickets with real-time movie data integration from TMDB API. This system provides both user and admin interfaces for managing movie bookings efficiently.
🎬 Features

Real-time movie data fetching from TMDB API
User dashboard for browsing and booking movies
Admin panel for movie management
SQLite database integration
Secure booking system
Responsive web interface

🛠️ Technical Stack

Backend: Flask (Python)
Database: SQLite with SQLAlchemy ORM
External API: TMDB (The Movie Database)
Frontend: HTML/Templates
Dependencies: Flask-SQLAlchemy, Requests

🚀 Getting Started

Clone the repository:

bashCopygit clone [repository-url]
cd movie-booking-system

Install dependencies:

bashCopypip install -r requirements.txt

Initialize the database:

bashCopyflask init-db

Run the application:

bashCopypython app.py
💡 Key Features
For Users

Browse latest movies from TMDB
View movie schedules and pricing
Book movie tickets
Track booking history

For Administrators

Add/Delete movies
Manage movie schedules
View booking statistics
Update movie information

🔧 Configuration
Configure your TMDB API credentials in app.py:
pythonCopyAPI_KEY = 'your-api-key'
TOKEN = 'your-token'
📝 Database Schema
Movies Table

id (Primary Key)
title
cinema
timing
price

Bookings Table

id (Primary Key)
movie_id (Foreign Key)

🤝 Contributing
Feel free to fork this repository and submit pull requests. For major changes, please open an issue first to discuss what you would like to change.
