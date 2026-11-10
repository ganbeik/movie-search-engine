const IMAGE_BASE_URL = "https://image.tmdb.org/t/p";

function PeopleGrid({ people, onClickPerson }) {
  return (
    <div className="grid grid-cols-2 gap-4 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6">
      {people.map((person) => (
        <button
          type="button"
          key={person.id}
          onClick={() => onClickPerson(person)}
          className="group overflow-hidden rounded-2xl bg-zinc-900 text-left ring-1 ring-white/10 transition hover:-translate-y-1 hover:ring-amber-400/50"
        >
          {person.profile ? (
            <img
              src={`${IMAGE_BASE_URL}/w300${person.profile}`}
              alt={person.name}
              className="aspect-[2/3] w-full object-cover transition duration-300 group-hover:scale-105"
            />
          ) : (
            <div className="flex aspect-[2/3] w-full items-center justify-center bg-zinc-800 text-zinc-500">
              No Image
            </div>
          )}

          <div className="p-3">
            <h3 className="line-clamp-1 font-semibold text-white">
              {person.name}
            </h3>

            <p className="mt-1 line-clamp-2 text-sm text-zinc-400">
              {person.known_for?.join(", ")}
            </p>

            <p className="mt-3 text-xs font-semibold uppercase tracking-wide text-amber-300">
              View movies →
            </p>
          </div>
        </button>
      ))}
    </div>
  );
}

export default PeopleGrid;