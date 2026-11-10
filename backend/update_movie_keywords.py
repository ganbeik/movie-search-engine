import os
import time
import sqlite3
import requests
from dotenv import load_dotenv

load_dotenv()

TMDB_API_KEY = os.getenv("TMDB_API_KEY")
TMDB_BASE_URL = "https://api.themoviedb.org/3"
DB_NAME = "movies.db"


def add_keywords_column():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("PRAGMA table_info(movies)")
    columns = [column[1] for column in cursor.fetchall()]

    if "keywords" not in columns:
        cursor.execute("ALTER TABLE movies ADD COLUMN keywords TEXT")
        print("Added keywords column.")
    else:
        print("keywords column already exists.")

    conn.commit()
    conn.close()


def get_movie_ids():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM movies")
    rows = cursor.fetchall()

    conn.close()

    return [row[0] for row in rows]


def fetch_keywords(movie_id):
    url = f"{TMDB_BASE_URL}/movie/{movie_id}/keywords"

    params = {
        "api_key": TMDB_API_KEY
    }

    response = requests.get(url, params=params)
    data = response.json()

    keywords = [
        keyword.get("name")
        for keyword in data.get("keywords", [])
        if keyword.get("name")
    ]

    return ", ".join(keywords)


def save_keywords(movie_id, keywords):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE movies
        SET keywords = ?
        WHERE id = ?
        """,
        (keywords, movie_id),
    )

    conn.commit()
    conn.close()


def update_movie_keywords():
    if not TMDB_API_KEY:
        raise ValueError("TMDB_API_KEY not found. Check backend/.env.")

    add_keywords_column()

    movie_ids = get_movie_ids()

    print(f"Found {len(movie_ids)} movies.")

    for index, movie_id in enumerate(movie_ids, start=1):
        print(f"[{index}/{len(movie_ids)}] Fetching keywords for movie {movie_id}...")

        try:
            keywords = fetch_keywords(movie_id)
            save_keywords(movie_id, keywords)
            print(f"Saved keywords: {keywords[:80]}")
        except Exception as e:
            print(f"Error for movie {movie_id}: {e}")

        time.sleep(0.25)

    print("Done updating keywords.")


if __name__ == "__main__":
    update_movie_keywords()