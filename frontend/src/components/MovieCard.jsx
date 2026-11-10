const IMAGE_BASE_URL = "https://image.tmdb.org/t/p";

function MovieCard({ movie, onClick }) {
  const year = movie.release_date
    ? movie.release_date.slice(0, 4)
    : "Unknown";

  const rating =
    typeof movie.rating === "number" ? movie.rating.toFixed(1) : movie.rating;

  return (
    <button onClick={onClick} className="group text-left">
      <div className="overflow-hidden rounded-xl bg-zinc-900 shadow-lg ring-1 ring-white/10 transition group-hover:scale-[1.03] group-hover:ring-amber-400/50">
        {movie.poster ? (
          <img
            src={`${IMAGE_BASE_URL}/w500${movie.poster}`}
            alt={movie.title}
            className="aspect-[2/3] w-full object-cover"
          />
        ) : (
          <div className="flex aspect-[2/3] w-full items-center justify-center bg-zinc-800 text-zinc-500">
            No Poster
          </div>
        )}
      </div>

      <div className="mt-3">
        <h3 className="line-clamp-1 font-semibold text-white">
          {movie.title}
        </h3>

        <div className="mt-1 flex items-center gap-2 text-sm text-zinc-400">
          <span>{year}</span>
          <span>·</span>
          <span>⭐ {rating}</span>
        </div>

        {movie.character && (
          <p className="mt-1 line-clamp-1 text-sm text-amber-300">
            as {movie.character}
          </p>
        )}
      </div>
    </button>
  );
}

export default MovieCard;