function Section({ title, children }) {
  return (
    <section className="mb-12">
      <div className="mb-5 flex items-center gap-3">
        <div className="h-5 w-1 rounded-full bg-amber-400" />
        <h2 className="text-2xl font-bold tracking-tight text-white">
          {title}
        </h2>
      </div>
      {children}
    </section>
  );
}

export default Section;