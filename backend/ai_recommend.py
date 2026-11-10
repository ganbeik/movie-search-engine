import json
import os
from dotenv import load_dotenv
from openai import OpenAI

from semantic_search import search_movies_semantically

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def build_movie_context(movies):
    context_items = []

    for index, movie in enumerate(movies, start=1):
        context_items.append(
            {
                "rank": index,
                "id": movie.get("id"),
                "title": movie.get("title"),
                "genres": movie.get("genres"),
                "overview": movie.get("overview"),
                "rating": movie.get("rating"),
                "release_date": movie.get("release_date"),
                "similarity_score": movie.get("similarity_score"),
            }
        )

    return context_items


def generate_recommendation_reasons(query, top_k=5):
    movies = search_movies_semantically(query, top_k=top_k)
    movie_context = build_movie_context(movies)

    prompt = f"""
You are helping users discover movies through vague memories, moods, and themes.

User query:
{query}

Candidate movies:
{json.dumps(movie_context, ensure_ascii=False, indent=2)}

For each candidate movie, write a short reason explaining why it matches the user's query.

Return ONLY valid JSON in this exact format:
{{
  "results": [
    {{
      "id": 123,
      "reason": "Short explanation in one sentence."
    }}
  ]
}}
"""

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt,
    )

    text = response.output_text

    try:
        reason_data = json.loads(text)
        reasons = reason_data.get("results", [])
    except json.JSONDecodeError:
        reasons = []

    reason_map = {
        item.get("id"): item.get("reason")
        for item in reasons
    }

    final_results = []

    for movie in movies:
        movie_id = movie.get("id")
        movie["reason"] = reason_map.get(
            movie_id,
            "This movie matches the mood, themes, or story elements in your search."
        )
        final_results.append(movie)

    return final_results