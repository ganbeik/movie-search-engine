import json
import sqlite3
import numpy as np
from sentence_transformers import SentenceTransformer

DB_NAME = "movies.db"
EMBEDDINGS_FILE = "movie_embeddings.npy"
MOVIE_IDS_FILE = "movie_ids.json"

MODEL_NAME = "all-MiniLM-L6-v2"


def load_movies():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, title, overview, genres
        FROM movies
        WHERE overview IS NOT NULL
        AND overview != ''
    """)

    rows = cursor.fetchall()
    conn.close()

    movies = []

    for row in rows:
        movie_id, title, overview, genres = row

        text = f"""
        Title: {title}
        Genres: {genres}
        Overview: {overview}
        """

        movies.append({
            "id": movie_id,
            "text": text
        })

    return movies


def build_embeddings():
    movies = load_movies()

    print(f"Loaded {len(movies)} movies.")

    if not movies:
        raise ValueError("No movies found. Make sure movies.db has data.")

    model = SentenceTransformer(MODEL_NAME)

    texts = [movie["text"] for movie in movies]
    movie_ids = [movie["id"] for movie in movies]

    print("Building embeddings...")

    embeddings = model.encode(
        texts,
        show_progress_bar=True,
        convert_to_numpy=True
    )

    np.save(EMBEDDINGS_FILE, embeddings)

    with open(MOVIE_IDS_FILE, "w") as f:
        json.dump(movie_ids, f)

    print("Done.")
    print(f"Saved embeddings to {EMBEDDINGS_FILE}")
    print(f"Saved movie ids to {MOVIE_IDS_FILE}")


if __name__ == "__main__":
    build_embeddings()