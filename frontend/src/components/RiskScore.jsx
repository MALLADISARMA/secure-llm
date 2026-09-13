export default function RiskScore({
  score = 0,
  blocked = false,
}) {
  const safeScore = Math.min(
    Math.max(score, 0),
    100
  );

  let riskLabel = "Low Risk";

  if (safeScore >= 70) {
    riskLabel = "High Risk";
  } else if (safeScore >= 40) {
    riskLabel = "Medium Risk";
  }

  return (
    <div className="rounded-xl border border-slate-200 bg-white p-6 shadow-sm">

      <div className="flex items-start justify-between">

        <div>
          <p className="text-sm font-medium text-slate-500">
            Overall Risk
          </p>

          <div className="mt-2 flex items-baseline gap-2">
            <span className="text-4xl font-bold text-slate-900">
              {Math.round(safeScore)}
            </span>

            <span className="text-sm text-slate-400">
              / 100
            </span>
          </div>
        </div>

        <span
          className={`rounded-full px-3 py-1 text-xs font-semibold ${
            blocked
              ? "bg-red-50 text-red-700"
              : "bg-emerald-50 text-emerald-700"
          }`}
        >
          {blocked ? "BLOCKED" : riskLabel}
        </span>

      </div>

      <div className="mt-6 h-2 overflow-hidden rounded-full bg-slate-100">

        <div
          className="h-full rounded-full bg-slate-900 transition-all duration-500"
          style={{
            width: `${safeScore}%`,
          }}
        />

      </div>

    </div>
  );
}