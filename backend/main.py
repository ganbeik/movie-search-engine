from semantic_search import search_movies_semantically
import os
import requests
from dotenv import load_dotenv

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from ai_recommend import generate_recommendation_reasons

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

TMDB_API_KEY = os.getenv("TMDB_API_KEY")
print("TMDB_API_KEY:", TMDB_API_KEY)
TMDB_BASE_URL = "https://api.themoviedb.org/3"


@app.get("/")
def home():
    return {"message": "Movie Search API Running"}


@app.get("/search")
def unified_search(query: str):
    # -------------------------
    # 1. Search movies
    # -------------------------
    movie_url = f"{TMDB_BASE_URL}/search/movie"

    movie_params = {
        "api_key": TMDB_API_KEY,
        "query": query,
        "language": "en-US",
        "page": 1,
    }
@app.get("/semantic-search")
def semantic_search_endpoint(query: str):
    results = search_movies_semantically(query, top_k=10)

    return {
        "query": query,
        "results": results
    }
@app.get("/ai-recommend")
def ai_recommend_endpoint(query: str):
    results = generate_recommendation_reasons(query, top_k=5)

    return {
        "query": query,
        "results": results
    }
    movie_response = requests.get(movie_url, params=movie_params)
    movie_data = movie_response.json()

    movies = []

    for movie in movie_data.get("results", [])[:8]:
        movies.append({
            "id": movie.get("id"),
            "title": movie.get("title"),
            "overview": movie.get("overview"),
            "release_date": movie.get("release_date"),
            "rating": movie.get("vote_average"),
            "poster": movie.get("poster_path"),
        })

    # -------------------------
    # 2. Search people
    # -------------------------
    person_url = f"{TMDB_BASE_URL}/search/person"

    person_params = {
        "api_key": TMDB_API_KEY,
        "query": query,
        "language": "en-US",
        "page": 1,
    }

    person_response = requests.get(person_url, params=person_params)
    person_data = person_response.json()

    actors = []
    directors = []

    for person in person_data.get("results", [])[:8]:
        person_item = {
            "id": person.get("id"),
            "name": person.get("name"),
            "profile": person.get("profile_path"),
            "known_for_department": person.get("known_for_department"),
            "known_for": [
                item.get("title") or item.get("name")
                for item in person.get("known_for", [])
            ],
        }

        if person.get("known_for_department") == "Directing":
            directors.append(person_item)
        else:
            actors.append(person_item)

    return {
        "query": query,
        "movies": movies,
        "actors": actors,
        "directors": directors,
    }

@app.get("/actor/{actor_id}/movies")
def get_actor_movies(actor_id: int):
    # Get actor detail
    actor_url = f"{TMDB_BASE_URL}/person/{actor_id}"

    actor_params = {
        "api_key": TMDB_API_KEY,
        "language": "en-US",
    }

    actor_response = requests.get(actor_url, params=actor_params)
    actor_data = actor_response.json()

    # Get actor movies
    credits_url = f"{TMDB_BASE_URL}/person/{actor_id}/movie_credits"

    credits_params = {
        "api_key": TMDB_API_KEY,
        "language": "en-US",
    }

    credits_response = requests.get(credits_url, params=credits_params)
    credits_data = credits_response.json()

    movies = []

    for movie in credits_data.get("cast", [])[:40]:
        movies.append({
            "id": movie.get("id"),
            "title": movie.get("title"),
            "character": movie.get("character"),
            "release_date": movie.get("release_date"),
            "rating": movie.get("vote_average"),
            "overview": movie.get("overview"),
            "poster": movie.get("poster_path"),
        })

    return {
        "actor": {
            "id": actor_data.get("id"),
            "name": actor_data.get("name"),
            "profile": actor_data.get("profile_path"),
            "biography": actor_data.get("biography"),
            "birthday": actor_data.get("birthday"),
            "place_of_birth": actor_data.get("place_of_birth"),
            "known_for_department": actor_data.get("known_for_department"),
        },
        "movies": movies,
    }
@app.get("/director/{director_id}/movies")
def get_director_movies(director_id: int):
    credits_url = f"{TMDB_BASE_URL}/person/{director_id}/movie_credits"

    params = {
        "api_key": TMDB_API_KEY,
        "language": "en-US",
    }

    response = requests.get(credits_url, params=params)
    data = response.json()

    movies = []

    for movie in data.get("crew", []):
        if movie.get("job") == "Director":
            movies.append({
                "id": movie.get("id"),
                "title": movie.get("title"),
                "release_date": movie.get("release_date"),
                "rating": movie.get("vote_average"),
                "overview": movie.get("overview"),
                "poster": movie.get("poster_path"),
            })

    movies = sorted(
        movies,
        key=lambda x: x.get("release_date") or "",
        reverse=True
    )

    return {
        "director_id": director_id,
        "movies": movies[:30],
    }

    response = requests.get(credits_url, params=params)
    data = response.json()

    movies = []

    for movie in data.get("cast", [])[:40]:
        movies.append({
            "id": movie.get("id"),
            "title": movie.get("title"),
            "character": movie.get("character"),
            "release_date": movie.get("release_date"),
            "rating": movie.get("vote_average"),
            "overview": movie.get("overview"),
            "poster": movie.get("poster_path"),
        })

    return {
        "actor_id": actor_id,
        "movies": movies,
    }


@app.get("/movie/{movie_id}")
def get_movie_detail(movie_id: int):
    # -------------------------
    # 1. Movie basic detail
    # -------------------------
    movie_url = f"{TMDB_BASE_URL}/movie/{movie_id}"

    movie_params = {
        "api_key": TMDB_API_KEY,
        "language": "en-US",
    }

    movie_response = requests.get(movie_url, params=movie_params)
    movie_data = movie_response.json()

    # -------------------------
    # 2. Movie credits
    # -------------------------
    credits_url = f"{TMDB_BASE_URL}/movie/{movie_id}/credits"

    credits_params = {
        "api_key": TMDB_API_KEY,
        "language": "en-US",
    }

    credits_response = requests.get(credits_url, params=credits_params)
    credits_data = credits_response.json()

    actors = []

    for actor in credits_data.get("cast", [])[:40]:
        actors.append({
        "id": actor.get("id"),
        "name": actor.get("name"),
        "character": actor.get("character"),
        "profile": actor.get("profile_path")
    })

    director = {
        "id": None,
        "name": "Unknown",
        "profile": None
    }

    for crew in credits_data.get("crew", []):
        if crew.get("job") == "Director":
            director = {
                "id": crew.get("id"),
                "name": crew.get("name"),
                "profile": crew.get("profile_path")
            }
            break

    return {
        "id": movie_data.get("id"),
        "title": movie_data.get("title"),
        "overview": movie_data.get("overview"),
        "release_date": movie_data.get("release_date"),
        "rating": movie_data.get("vote_average"),
        "runtime": movie_data.get("runtime"),
        "genres": [genre.get("name") for genre in movie_data.get("genres", [])],
        "poster": movie_data.get("poster_path"),
        "director": director,
        "actors": actors,
    }