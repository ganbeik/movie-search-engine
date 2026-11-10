from langchain_core.documents import Document
from semantic_search import search_movies_semantically


def retrieve_movie_documents(query: str, top_k: int = 5):
    movies = search_movies_semantically(query, top_k=top_k)

    documents = []

    for movie in movies:
        page_content = f"""
Title: {movie.get("title")}
Genres: {movie.get("genres")}
Overview: {movie.get("overview")}
Release Date: {movie.get("release_date")}
Rating: {movie.get("rating")}
"""

        documents.append(
            Document(
                page_content=page_content,
                metadata={
                    "id": movie.get("id"),
                    "title": movie.get("title"),
                    "poster": movie.get("poster"),
                    "rating": movie.get("rating"),
                    "similarity_score": movie.get("similarity_score"),
                },
            )
        )

    return documents