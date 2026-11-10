# SceneSeek AI Agent Instructions

## Architecture Overview

**SceneSeek** is a full-stack movie search application with a clear backend/frontend separation:

- **Backend** (`backend/`): FastAPI server serving endpoints that integrate with TMDB API
- **Frontend** (`frontend/`): React + Vite app with Tailwind CSS, consuming backend endpoints
- **Data pipeline**: Optional offline embeddings pipeline using `sentence-transformers` for future semantic search

### Key Data Flow
1. Frontend sends search query to `/search` endpoint
2. Backend queries TMDB API for movies, actors, and directors (filtered by department)
3. Frontend displays results in reactive sections; users can drill into movies/actors/directors
4. Movie detail endpoint (`/movie/{id}`) fetches actor/director credits via TMDB

## Backend Architecture

**File: `backend/main.py`**
- FastAPI app with CORS enabled for frontend consumption
- TMDB_API_KEY loaded from `.env` file (required)
- Core endpoints pattern: minimal transformation of TMDB responses

### Endpoints Structure
- `GET /search?query=...` → Returns `{movies: [], actors: [], directors: []}`
- `GET /movie/{id}` → Full movie detail with cast & director info
- `GET /actor/{id}/movies` → Actor profile + filmography (cast credits)
- `GET /director/{id}/movies` → Director's films (crew credits where job=="Director")

**Critical Pattern**: The backend distinguishes people by `known_for_department` field:
- "Directing" → directors list
- All others → actors list

### Database & Data Preparation
- `build_movie_database.py`: Fetches 100 pages of popular movies from TMDB, stores in `movies.db` (SQLite)
- `build_embeddings.py`: Pre-computes sentence embeddings (all-MiniLM-L6-v2) for movies, saves as `.npy` files
- `check_database.py`: Simple validation script

**Current state**: Database infrastructure exists but embeddings are built but not consumed by endpoints. Semantic search not yet implemented.

## Frontend Architecture

**File: `frontend/src/App.jsx`**
- Single search input state machine: query → loading → results
- Three main result categories: movies, actors, directors
- Drill-down patterns: click actor/director → fetch their filmography
- State isolation: selecting movie detail clears actor/director selections

### Styling Approach
- **Tailwind CSS** with custom color palette: `#D6A85C` (gold), `#F5F1EA` (cream), `#12100E` (dark bg)
- No component CSS files; all classes in JSX
- Pattern: Rounded borders (`rounded-2xl`), ring styles for subtle contrast, `group-` prefixes for hover states

### Component Patterns
- `MovieCard.jsx`: Grid item displaying poster + title/year/rating; shows character name if available
- `PeopleGrid.jsx`: Grid of people with images; "View movies →" CTA
- `Section.jsx`: Reusable section header with left-side accent bar

**Image handling**: All TMDB images use `https://image.tmdb.org/t/p/w500` (movies) or `w300` (people) endpoints

## Developer Workflows

### Setup & Running
```bash
# Backend
cd backend
python -m venv venv
source venv/bin/activate
pip install fastapi uvicorn python-dotenv requests sentence-transformers numpy
# Create .env with TMDB_API_KEY
python build_movie_database.py  # Populates movies.db (one-time, ~25 pages per second)
python main.py  # Starts FastAPI on http://127.0.0.1:8000

# Frontend
cd frontend
npm install
npm run dev  # Starts Vite dev server, defaults to http://localhost:5173
```

### Testing & Validation
- No automated tests; validate via manual UI testing
- Backend validation: `python backend/check_database.py` checks record count
- Network debugging: Both frontend and backend log to console/terminal

### Common Modifications
- **Add a new endpoint**: Follow pattern in `main.py` (fetch from TMDB, transform response)
- **Modify search results**: Update return structure in `/search` endpoint and corresponding frontend state/render
- **Add component styling**: Use existing Tailwind tokens; avoid adding new color definitions
- **Change image sizes**: Modify `w500`/`w300` in `IMAGE_BASE_URL` usage

## Critical Conventions & Constraints

1. **Hardcoded API base**: `http://127.0.0.1:8000` in frontend—currently assumes local backend
2. **TMDB rate limiting**: `build_movie_database.py` includes 0.25s sleep between requests to be respectful
3. **Data shape consistency**: Backend always returns `{id, name/title, profile/poster, ...}` structures; frontend assumes these shapes
4. **Error handling**: Minimal—both backend and frontend catch errors silently and display loading/empty states
5. **No authentication**: Public TMDB API key exposure; not production-safe

## Key Files at a Glance

| File | Purpose | Key Functions |
|------|---------|---|
| `backend/main.py` | API server | `unified_search()`, `get_movie_detail()`, `get_actor_movies()`, `get_director_movies()` |
| `backend/build_movie_database.py` | Data ingestion | `fetch_popular_movies()`, `save_movies()`, `build_movie_database()` |
| `backend/build_embeddings.py` | Offline ML pipeline | `build_embeddings()` (not called by main API) |
| `frontend/src/App.jsx` | Main UI logic | `search()`, `getMovieDetail()`, `getActorMovies()`, `getDirectorMovies()` |
| `frontend/src/components/*` | Reusable UI | Display movie cards, people grids, section headers |

## Future Considerations

- Embeddings pipeline is ready but not integrated; next step is semantic search endpoint
- Hardcoded API URL should be environment-based for production
- Error handling should return meaningful messages instead of silent failures
- Consider caching TMDB responses to reduce API calls and improve performance
