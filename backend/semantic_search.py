import json
import sqlite3
import numpy as np
from sentence_transformers import SentenceTransformer

DB_NAME = "movies.db"
EMBEDDINGS_FILE = "movie_embeddings.npy"
MOVIE_IDS_FILE = "movie_ids.json"
MODEL_NAME = "all-MiniLM-L6-v2"

model = SentenceTransformer(MODEL_NAME)

movie_embeddings = np.load(EMBEDDINGS_FILE)

with open(MOVIE_IDS_FILE, "r") as f:
    movie_ids = json.load(f)


def cosine_similarity(query_embedding, movie_embeddings):
    query_norm = query_embedding / np.linalg.norm(query_embedding)
    movie_norms = movie_embeddings / np.linalg.norm(
        movie_embeddings, axis=1, keepdims=True
    )

    return np.dot(movie_norms, query_norm)


def get_movies_by_ids(ids):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    placeholders = ",".join(["?"] * len(ids))

    cursor.execute(
        f"""
        SELECT id, title, overview, release_date, rating, poster, genres
        FROM movies
        WHERE id IN ({placeholders})
        """,
        ids,
    )

    rows = cursor.fetchall()
    conn.close()

    movie_map = {}

    for row in rows:
        movie_id, title, overview, release_date, rating, poster, genres = row

        movie_map[movie_id] = {
            "id": movie_id,
            "title": title,
            "overview": overview,
            "release_date": release_date,
            "rating": rating,
            "poster": poster,
            "genres": genres,
        }

    return movie_map


def search_movies_semantically(query, top_k=10):
    query_embedding = model.encode(query, convert_to_numpy=True)

    scores = cosine_similarity(query_embedding, movie_embeddings)

    top_indices = np.argsort(scores)[::-1][:top_k]

    top_movie_ids = [movie_ids[index] for index in top_indices]
    movie_map = get_movies_by_ids(top_movie_ids)

    results = []

    for index in top_indices:
        movie_id = movie_ids[index]
        movie = movie_map.get(movie_id)

        if movie:
            movie["similarity_score"] = float(scores[index])
            results.append(movie)

    return results