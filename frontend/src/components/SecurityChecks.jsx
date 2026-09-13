import ThreatCard from "./ThreatCard";

export default function SecurityChecks({
  results = [],
}) {
  return (
    <section>

      <div className="mb-4">

        <h2 className="text-base font-semibold text-slate-900">
          Security Checks
        </h2>

        <p className="mt-1 text-sm text-slate-500">
          Semantic analysis across six security categories.
        </p>

      </div>

      <div className="grid gap-4 md:grid-cols-2">

        {results.map((result) => (
          <ThreatCard
            key={result.category}
            category={result.category}
            detected={result.detected}
            confidence={result.confidence}
            severity={result.severity}
          />
        ))}

      </div>

    </section>
  );
}