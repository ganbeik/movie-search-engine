import os
import time
import sqlite3
import requests
from dotenv import load_dotenv

load_dotenv()

TMDB_API_KEY = os.getenv("TMDB_API_KEY")
TMDB_BASE_URL = "https://api.themoviedb.org/3"
DB_NAME = "movies.db"


def create_database():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS movies (
            id INTEGER PRIMARY KEY,
            title TEXT,
            overview TEXT,
            release_date TEXT,
            rating REAL,
            poster TEXT,
            genres TEXT,
            popularity REAL
        )
    """)

    conn.commit()
    conn.close()


def get_genre_map():
    url = f"{TMDB_BASE_URL}/genre/movie/list"

    params = {
        "api_key": TMDB_API_KEY,
        "language": "en-US"
    }

    response = requests.get(url, params=params)
    data = response.json()

    genre_map = {}

    for genre in data.get("genres", []):
        genre_map[genre["id"]] = genre["name"]

    return genre_map


def fetch_popular_movies(page, genre_map):
    url = f"{TMDB_BASE_URL}/discover/movie"

    params = {
        "api_key": TMDB_API_KEY,
        "language": "en-US",
        "sort_by": "popularity.desc",
        "include_adult": "false",
        "include_video": "false",
        "page": page,
    }

    response = requests.get(url, params=params)
    data = response.json()

    movies = []

    for movie in data.get("results", []):
        genre_names = [
            genre_map.get(genre_id, "")
            for genre_id in movie.get("genre_ids", [])
        ]

        movies.append({
            "id": movie.get("id"),
            "title": movie.get("title"),
            "overview": movie.get("overview"),
            "release_date": movie.get("release_date"),
            "rating": movie.get("vote_average"),
            "poster": movie.get("poster_path"),
            "genres": ", ".join([g for g in genre_names if g]),
            "popularity": movie.get("popularity"),
        })

    return movies


def save_movies(movies):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    for movie in movies:
        cursor.execute("""
            INSERT OR REPLACE INTO movies (
                id,
                title,
                overview,
                release_date,
                rating,
                poster,
                genres,
                popularity
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            movie["id"],
            movie["title"],
            movie["overview"],
            movie["release_date"],
            movie["rating"],
            movie["poster"],
            movie["genres"],
            movie["popularity"],
        ))

    conn.commit()
    conn.close()


def build_movie_database(total_pages=100):
    if not TMDB_API_KEY:
        raise ValueError("TMDB_API_KEY not found. Check your backend/.env file.")

    create_database()
    genre_map = get_genre_map()

    total_saved = 0

    for page in range(1, total_pages + 1):
        print(f"Fetching page {page}/{total_pages}...")

        movies = fetch_popular_movies(page, genre_map)
        save_movies(movies)

        total_saved += len(movies)

        print(f"Saved {len(movies)} movies from page {page}.")

        # Be polite to the API
        time.sleep(0.25)

    print(f"Done. Total movies saved: {total_saved}")
    print(f"Database created: {DB_NAME}")


if __name__ == "__main__":
    build_movie_database(total_pages=100)