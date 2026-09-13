import {
  AlertTriangle,
  CheckCircle2,
} from "lucide-react";

export default function ThreatCard({
  category,
  detected,
  confidence = 0,
  severity,
}) {
  const percentage = Math.round(
    confidence * 100
  );

  return (
    <div className="rounded-xl border border-slate-200 bg-white p-5 shadow-sm">

      <div className="flex items-start justify-between">

        <div className="flex gap-3">

          <div
            className={`flex h-9 w-9 items-center justify-center rounded-lg ${
              detected
                ? "bg-red-50"
                : "bg-emerald-50"
            }`}
          >
            {detected ? (
              <AlertTriangle className="h-4 w-4 text-red-600" />
            ) : (
              <CheckCircle2 className="h-4 w-4 text-emerald-600" />
            )}
          </div>

          <div>
            <h3 className="text-sm font-semibold text-slate-900">
              {category}
            </h3>

            <p className="mt-1 text-xs text-slate-500">
              {detected
                ? "Potential security risk detected."
                : "No significant risk detected."}
            </p>
          </div>

        </div>

        <span
          className={`rounded-full px-2.5 py-1 text-[10px] font-bold ${
            detected
              ? "bg-red-50 text-red-700"
              : "bg-emerald-50 text-emerald-700"
          }`}
        >
          {detected ? severity : "PASS"}
        </span>

      </div>

      <div className="mt-5">

        <div className="mb-2 flex justify-between">

          <span className="text-xs text-slate-400">
            Confidence
          </span>

          <span className="text-xs font-semibold text-slate-700">
            {percentage}%
          </span>

        </div>

        <div className="h-1.5 overflow-hidden rounded-full bg-slate-100">

          <div
            className="h-full rounded-full bg-slate-700 transition-all duration-500"
            style={{
              width: `${percentage}%`,
            }}
          />

        </div>

      </div>

    </div>
  );
}