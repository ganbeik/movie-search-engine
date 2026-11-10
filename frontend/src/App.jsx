import { useState } from "react";
import Section from "./components/Section";
import MovieCard from "./components/MovieCard";
import PeopleGrid from "./components/PeopleGrid";

const IMAGE_BASE_URL = "https://image.tmdb.org/t/p";

function App() {
  const [query, setQuery] = useState("");
  const [searchMode, setSearchMode] = useState("keyword");
  const [movies, setMovies] = useState([]);
  const [actors, setActors] = useState([]);
  const [directors, setDirectors] = useState([]);
  const [selectedMovie, setSelectedMovie] = useState(null);
  const [selectedActor, setSelectedActor] = useState(null);
  const [selectedDirectorName, setSelectedDirectorName] = useState("");
  const [loading, setLoading] = useState(false);

  const search = async () => {
  if (!query.trim()) return;

  setLoading(true);
  setSelectedMovie(null);
  setSelectedActor(null);
  setSelectedDirectorName("");
  setMovies([]);
  setActors([]);
  setDirectors([]);

  try {
    let url = "";

    if (searchMode === "keyword") {
      url = `http://127.0.0.1:8000/search?query=${encodeURIComponent(query)}`;
    } else {
      url = `http://127.0.0.1:8000/semantic-search?query=${encodeURIComponent(query)}`;
    }

    const response = await fetch(url);
    const data = await response.json();

    if (searchMode === "keyword") {
      setMovies(data.movies || []);
      setActors(data.actors || []);
      setDirectors(data.directors || []);
    } else {
      setMovies(data.results || []);
      setActors([]);
      setDirectors([]);
    }
  } catch (error) {
    console.error("Search error:", error);
  } finally {
    setLoading(false);
  }
};

  const getActorMovies = async (actor) => {
    setSelectedMovie(null);
    setSelectedDirectorName("");
    setSelectedActor(actor);

    setActors([]);
    setDirectors([]);
    setMovies([]);

    setLoading(true);

    try {
      const response = await fetch(
        `http://127.0.0.1:8000/actor/${actor.id}/movies`
      );

      const data = await response.json();

      setSelectedActor(data.actor || actor);
      setMovies(data.movies || []);

      setTimeout(() => {
        window.scrollTo({ top: 500, behavior: "smooth" });
      }, 100);
    } catch (error) {
      console.error("Actor movies error:", error);
    } finally {
      setLoading(false);
    }
  };

  const getDirectorMovies = async (director) => {
    setSelectedMovie(null);
    setSelectedActor(null);
    setSelectedDirectorName(director.name);

    setActors([]);
    setDirectors([]);
    setMovies([]);

    setLoading(true);

    try {
      const response = await fetch(
        `http://127.0.0.1:8000/director/${director.id}/movies`
      );

      const data = await response.json();
      setMovies(data.movies || []);

      setTimeout(() => {
        window.scrollTo({ top: 500, behavior: "smooth" });
      }, 100);
    } catch (error) {
      console.error("Director movies error:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen text-[#F5F1EA]">
      <div className="mx-auto max-w-7xl px-6 py-10">
        {/* Hero */}
        <section className="mb-8 rounded-[2rem] border border-[#2A2520] bg-[#12100E]/80 p-6 shadow-2xl shadow-black/30 backdrop-blur md:p-8">
          <p className="mb-4 text-xs font-bold uppercase tracking-[0.35em] text-[#D6A85C]">
            SceneSeek
          </p>

          <h1 className="mb-5 max-w-3xl font-serif text-4xl font-bold leading-tight tracking-tight text-[#F5F1EA] md:text-5xl">
            Find the movie you almost remember.
          </h1>

          <p className="mb-8 max-w-2xl text-lg leading-8 text-stone-400">
            Search by movie title, actor, director, or vague memory. Built for
            moments when you remember the feeling, but not the name.
          </p>
          <div className="mb-3 flex gap-2">
  <button
    type="button"
    onClick={() => setSearchMode("keyword")}
    className={`rounded-full px-4 py-2 text-sm font-semibold transition ${
      searchMode === "keyword"
        ? "bg-[#D6A85C] text-[#0A0908]"
        : "bg-[#1A1715] text-stone-400 hover:text-[#F5F1EA]"
    }`}
  >
    Keyword Search
  </button>

  <button
    type="button"
    onClick={() => setSearchMode("semantic")}
    className={`rounded-full px-4 py-2 text-sm font-semibold transition ${
      searchMode === "semantic"
        ? "bg-[#D6A85C] text-[#0A0908]"
        : "bg-[#1A1715] text-stone-400 hover:text-[#F5F1EA]"
    }`}
  >
    AI Search
  </button>
</div>
          <div className="flex flex-col gap-3 md:flex-row">
            <input
              type="text"
              placeholder={
                            searchMode === "keyword"
                              ? "Try: Interstellar, Leonardo DiCaprio, Christopher Nolan..."
                              : "Try: a lonely but hopeful space movie..."
                          }
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === "Enter") search();
              }}
              className="w-full rounded-2xl border border-[#2A2520] bg-[#080706] px-5 py-4 text-[#F5F1EA] outline-none placeholder:text-stone-500 focus:border-[#D6A85C] focus:ring-2 focus:ring-[#D6A85C]/20"
            />

            <button
              onClick={search}
              className="rounded-2xl bg-[#D6A85C] px-8 py-4 font-bold text-[#0A0908] shadow-lg shadow-black/30 transition hover:bg-[#E8C177]"
            >
              Search
            </button>
          </div>
        </section>

        {loading && (
          <div className="mb-8 rounded-2xl border border-[#2A2520] bg-[#12100E]/80 p-5 text-stone-400">
            Searching movies...
          </div>
        )}

        {/* Selected Movie Detail */}
        {selectedMovie && (
          <section className="mb-10 overflow-hidden rounded-3xl border border-[#2A2520] bg-[#12100E]/90 shadow-2xl shadow-black/40">
            <div className="grid gap-8 p-6 md:grid-cols-[300px_1fr]">
              <div>
                {selectedMovie.poster ? (
                  <img
                    src={`${IMAGE_BASE_URL}/w500${selectedMovie.poster}`}
                    alt={selectedMovie.title}
                    className="w-full rounded-2xl shadow-xl"
                  />
                ) : (
                  <div className="flex h-[450px] items-center justify-center rounded-2xl bg-[#1A1715] text-stone-500">
                    No Poster
                  </div>
                )}
              </div>

              <div>
                <div className="mb-4 flex flex-wrap items-center gap-3">
                  <span className="rounded-full bg-[#D6A85C]/10 px-3 py-1 text-sm font-semibold text-[#D6A85C]">
                    ⭐ {selectedMovie.rating}
                  </span>

                  <span className="rounded-full bg-[#1A1715] px-3 py-1 text-sm text-stone-400">
                    {selectedMovie.release_date}
                  </span>

                  <span className="rounded-full bg-[#1A1715] px-3 py-1 text-sm text-stone-400">
                    {selectedMovie.runtime} min
                  </span>
                </div>

                <h2 className="mb-3 font-serif text-4xl font-bold text-[#F5F1EA]">
                  {selectedMovie.title}
                </h2>

                <div className="mb-4 flex items-center gap-3 text-stone-300">
                  <span className="font-semibold text-[#F5F1EA]">
                    Director:
                  </span>

                  {selectedMovie.director?.id ? (
                    <button
                      type="button"
                      onClick={() => getDirectorMovies(selectedMovie.director)}
                      className="rounded-full bg-[#D6A85C]/10 px-3 py-1 font-semibold text-[#D6A85C] transition hover:bg-[#D6A85C]/20"
                    >
                      {selectedMovie.director.name}
                    </button>
                  ) : (
                    <span>{selectedMovie.director?.name || "Unknown"}</span>
                  )}
                </div>

                <p className="mb-4 text-stone-300">
                  <span className="font-semibold text-[#F5F1EA]">
                    Genres:
                  </span>{" "}
                  {selectedMovie.genres?.join(", ")}
                </p>

                <p className="mb-8 max-w-3xl leading-7 text-stone-300">
                  {selectedMovie.overview}
                </p>

                <h3 className="mb-4 text-2xl font-bold">Cast</h3>

                <div className="grid grid-cols-2 gap-4 sm:grid-cols-3 md:grid-cols-4">
                  {selectedMovie.actors?.map((actor) => (
                    <button
                      type="button"
                      key={actor.id}
                      onClick={() => getActorMovies(actor)}
                      className="group rounded-2xl bg-[#1A1715] p-3 text-left ring-1 ring-[#2A2520] transition hover:-translate-y-1 hover:ring-[#D6A85C]/60"
                    >
                      {actor.profile ? (
                        <img
                          src={`${IMAGE_BASE_URL}/w185${actor.profile}`}
                          alt={actor.name}
                          className="mb-3 aspect-[2/3] w-full rounded-xl object-cover transition group-hover:scale-[1.03]"
                        />
                      ) : (
                        <div className="mb-3 flex aspect-[2/3] w-full items-center justify-center rounded-xl bg-[#12100E] text-sm text-stone-500">
                          No Image
                        </div>
                      )}

                      <p className="line-clamp-1 font-semibold text-[#F5F1EA]">
                        {actor.name}
                      </p>
                      <p className="line-clamp-1 text-sm text-stone-500">
                        {actor.character}
                      </p>

                      <p className="mt-2 text-xs font-semibold uppercase tracking-wide text-[#D6A85C]">
                        View movies →
                      </p>
                    </button>
                  ))}
                </div>
              </div>
            </div>
          </section>
        )}

        {/* Directors */}
        {directors.length > 0 && (
          <Section title="Directors">
            <PeopleGrid people={directors} onClickPerson={getDirectorMovies} />
          </Section>
        )}

        {/* Actors */}
        {actors.length > 0 && (
          <Section title="Actors">
            <PeopleGrid people={actors} onClickPerson={getActorMovies} />
          </Section>
        )}

        {/* Selected Actor */}
        {selectedActor && (
          <section className="mb-10 overflow-hidden rounded-3xl border border-[#2A2520] bg-[#12100E]/90 shadow-2xl shadow-black/40">
            <div className="grid gap-8 p-6 md:grid-cols-[280px_1fr]">
              <div>
                {selectedActor.profile ? (
                  <img
                    src={`${IMAGE_BASE_URL}/w500${selectedActor.profile}`}
                    alt={selectedActor.name}
                    className="w-full rounded-2xl object-cover shadow-xl"
                  />
                ) : (
                  <div className="flex aspect-[2/3] w-full items-center justify-center rounded-2xl bg-[#1A1715] text-stone-500">
                    No Image
                  </div>
                )}
              </div>

              <div>
                <p className="mb-3 text-sm font-semibold uppercase tracking-[0.25em] text-[#D6A85C]">
                  Actor
                </p>

                <h2 className="mb-4 font-serif text-4xl font-bold text-[#F5F1EA]">
                  {selectedActor.name}
                </h2>

                <div className="mb-5 flex flex-wrap gap-3 text-sm">
                  {selectedActor.birthday && (
                    <span className="rounded-full bg-[#1A1715] px-3 py-1 text-stone-400">
                      Birthday: {selectedActor.birthday}
                    </span>
                  )}

                  {selectedActor.place_of_birth && (
                    <span className="rounded-full bg-[#1A1715] px-3 py-1 text-stone-400">
                      {selectedActor.place_of_birth}
                    </span>
                  )}

                  {selectedActor.known_for_department && (
                    <span className="rounded-full bg-[#D6A85C]/10 px-3 py-1 text-[#D6A85C]">
                      {selectedActor.known_for_department}
                    </span>
                  )}
                </div>

                {selectedActor.biography ? (
                  <p className="mb-8 max-w-3xl leading-7 text-stone-300">
                    {selectedActor.biography}
                  </p>
                ) : (
                  <p className="mb-8 text-stone-400">
                    No biography available.
                  </p>
                )}

                <h3 className="text-2xl font-bold">
                  Movies starring{" "}
                  <span className="text-[#D6A85C]">
                    {selectedActor.name}
                  </span>
                </h3>
              </div>
            </div>
          </section>
        )}

        {/* Selected Director */}
        {selectedDirectorName && (
          <h2 className="mb-6 text-2xl font-bold">
            Movies directed by{" "}
            <span className="text-[#D6A85C]">{selectedDirectorName}</span>
          </h2>
        )}

        {/* Movies */}
        {movies.length > 0 && (
          <Section title="Movies">
            <div className="grid grid-cols-2 gap-x-4 gap-y-8 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 xl:grid-cols-6">
              {movies.map((movie) => (
                <MovieCard
                  key={movie.id}
                  movie={movie}
                  onClick={() => getMovieDetail(movie.id)}
                />
              ))}
            </div>
          </Section>
        )}

        {!loading &&
          movies.length === 0 &&
          actors.length === 0 &&
          directors.length === 0 &&
          query && (
            <div className="rounded-2xl border border-[#2A2520] bg-[#12100E]/80 p-6 text-stone-400">
              No results found. Try another keyword.
            </div>
          )}
      </div>
    </div>
  );
}

export default App;