import click
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import requests

app = Flask(__name__)

# Set up the SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movie_booking.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Movie Model (Movies Table)
class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    cinema = db.Column(db.String(100), nullable=False)
    timing = db.Column(db.String(100), nullable=False)
    price = db.Column(db.String(50), nullable=False)

# Booking Model (Bookings Table)
class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'), nullable=False)
    movie = db.relationship('Movie', backref='bookings')

# Fetch popular movies from an external API
def fetch_and_add_movies():
    API_KEY = '07f411d65278296ed8b25934ff2fcd91'
    TOKEN = 'eyJhbGciOiJIUzI1NiJ9...'
    url = f'https://api.themoviedb.org/3/movie/popular?api_key={API_KEY}'
    headers = {'Authorization': f'Bearer {TOKEN}'}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Check if request was successful
        data = response.json()

        if 'results' in data and data['results']:
            if Movie.query.count() == 0:  # Only add movies if the table is empty
                for movie in data['results']:
                    movie_entry = Movie(
                        title=movie['title'],
                        cinema='Cinema Hall',  # Default Cinema Hall
                        timing='8:00 PM',  # Default Timing
                        price='$10'  # Default Price
                    )
                    db.session.add(movie_entry)
                db.session.commit()
                print(f"Added {len(data['results'])} movies to the database.")
            else:
                print("Movies already exist in the database.")
        else:
            print("No movies fetched from API.")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching movies: {e}")

# Command to initialize the database and add movies
@app.cli.command("init-db")
def init_db_command():
    """Initialize the database and add movies."""
    db.create_all()  # Create all tables
    print("Tables created!")
    fetch_and_add_movies()  # Fetch and add movies to the database
    print("Movies added!")

@app.route('/')
def index():
    """Render the homepage with navigation options"""
    return render_template('index.html')

@app.route('/user_dashboard')
def user_dashboard():
    """Render the user dashboard page with movie listings"""
    movies = Movie.query.all()
    bookings = Booking.query.all()
    return render_template('user_dashboard.html', movies=movies, bookings=bookings)

@app.route('/book/<int:movie_id>', methods=['POST'])
def book_movie(movie_id):
    """Handle the booking of a movie"""
    movie = Movie.query.get(movie_id)
    if movie:
        booking = Booking(movie_id=movie.id)
        db.session.add(booking)
        db.session.commit()
    return redirect(url_for('user_dashboard'))

@app.route('/admin')
def admin_dashboard():
    """Render the admin dashboard showing movies and bookings"""
    movies = Movie.query.all()
    bookings = Booking.query.all()
    return render_template('admin.html', movies=movies, bookings=bookings)

@app.route('/add_movie', methods=['POST'])
def add_movie():
    """Handle adding a new movie from the admin dashboard"""
    name = request.form.get('name')
    cinema = request.form.get('cinema')
    timing = request.form.get('timing')
    price = request.form.get('price')
    new_movie = Movie(title=name, cinema=cinema, timing=timing, price=price)
    db.session.add(new_movie)
    db.session.commit()
    return redirect(url_for('admin_dashboard'))

@app.route('/delete_movie/<int:movie_id>')
def delete_movie(movie_id):
    """Handle deleting a movie from the admin dashboard"""
    movie = Movie.query.get(movie_id)
    if movie:
        db.session.delete(movie)
        db.session.commit()
    return redirect(url_for('admin_dashboard'))

if __name__ == "__main__":
    # Run the Flask application
    app.run(debug=True)
