import {
  ShieldCheck,
  ShieldAlert,
} from "lucide-react";

import RiskScore from "./RiskScore";
import SecurityChecks from "./SecurityChecks";

export default function AnalysisResult({
  result,
}) {
  if (!result) {
    return null;
  }

  const blocked = result.blocked;

  return (
    <div className="space-y-6">

      {/* Recommendation */}
      <div
        className={`rounded-xl border p-5 ${
          blocked
            ? "border-red-200 bg-red-50"
            : "border-emerald-200 bg-emerald-50"
        }`}
      >

        <div className="flex items-center gap-4">

          <div
            className={`flex h-11 w-11 items-center justify-center rounded-lg ${
              blocked
                ? "bg-red-100"
                : "bg-emerald-100"
            }`}
          >
            {blocked ? (
              <ShieldAlert className="h-6 w-6 text-red-600" />
            ) : (
              <ShieldCheck className="h-6 w-6 text-emerald-600" />
            )}
          </div>

          <div>

            <h2
              className={`text-base font-bold ${
                blocked
                  ? "text-red-900"
                  : "text-emerald-900"
              }`}
            >
              {blocked
                ? "Prompt Blocked"
                : "Prompt Allowed"}
            </h2>

            <p
              className={`mt-1 text-sm ${
                blocked
                  ? "text-red-700"
                  : "text-emerald-700"
              }`}
            >
              {blocked
                ? `Potential ${result.highest_risk} detected.`
                : "No security policy violations detected."}
            </p>

          </div>

        </div>

      </div>

      {/* Risk */}
      <RiskScore
        score={result.overall_score}
        blocked={blocked}
      />

      {/* Checks */}
      <SecurityChecks
        results={result.results}
      />

    </div>
  );
}