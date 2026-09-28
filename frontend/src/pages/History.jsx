import { useEffect, useState } from "react";
import { History as HistoryIcon, Trash2 } from "lucide-react";

import { clearHistory, getHistory } from "../services/api";

export default function History() {
  const [records, setRecords] = useState([]);
  const [loading, setLoading] = useState(true);
  const [clearing, setClearing] = useState(false);
  const [error, setError] = useState("");

  const loadHistory = async () => {
    try {
      const data = await getHistory();

      if (data.status === "unavailable") {
        setError("History storage is currently unavailable.");
        setRecords([]);
      } else {
        setRecords(data.records || []);
      }
    } catch (requestError) {
      setError(
        requestError instanceof Error
          ? requestError.message
          : "Unable to load history.",
      );
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadHistory();
  }, []);

  const handleClearHistory = async () => {
    if (!window.confirm("Are you sure you want to clear your analysis history?")) {
      return;
    }

    setClearing(true);
    setError("");

    try {
      const data = await clearHistory();

      if (data.status === "unavailable") {
        setError("History storage is currently unavailable.");
      } else {
        setRecords([]);
      }
    } catch (requestError) {
      setError(
        requestError instanceof Error
          ? requestError.message
          : "Unable to clear history.",
      );
    } finally {
      setClearing(false);
    }
  };

  if (loading) {
    return (
      <main className="mx-auto max-w-7xl px-6 py-10">
        <h1 className="text-3xl font-bold tracking-tight text-slate-900">
          Analysis History
        </h1>
        <p className="mt-4 text-sm text-slate-500">Loading history...</p>
      </main>
    );
  }

  return (
    <main className="mx-auto max-w-7xl px-6 py-10">
      <div className="mb-8 flex flex-col justify-between gap-4 sm:flex-row sm:items-end">
        <div>
          <p className="text-xs font-semibold uppercase tracking-wider text-slate-400">
            Security Logs
          </p>

          <h1 className="mt-2 text-3xl font-bold tracking-tight text-slate-900">
            Analysis History
          </h1>

          <p className="mt-2 text-sm text-slate-500">
            Review previously analyzed prompts.
          </p>
        </div>

        {records.length > 0 && (
          <button
            type="button"
            onClick={handleClearHistory}
            disabled={clearing}
            className="inline-flex items-center justify-center gap-2 rounded-lg border border-slate-200 bg-white px-4 py-2 text-sm font-semibold text-slate-700 shadow-sm transition hover:bg-slate-50 disabled:cursor-not-allowed disabled:opacity-60"
          >
            <Trash2 className="h-4 w-4" />
            {clearing ? "Clearing..." : "Clear history"}
          </button>
        )}
      </div>

      {error && (
        <div className="mb-6 rounded-lg border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700">
          {error}
        </div>
      )}

      {records.length === 0 && !error && (
        <div className="flex min-h-[350px] flex-col items-center justify-center rounded-xl border border-slate-200 bg-white shadow-sm">
          <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-slate-100">
            <HistoryIcon className="h-5 w-5 text-slate-500" />
          </div>

          <h2 className="mt-4 text-sm font-semibold text-slate-900">
            No analysis history
          </h2>

          <p className="mt-2 max-w-sm text-center text-sm leading-6 text-slate-500">
            Analyze a prompt to see your security analysis history here.
          </p>
        </div>
      )}

      {records.length > 0 && (
        <div className="space-y-4">
          {records.map((record) => {
            const detectedCategories = (record.analysis?.results || [])
              .filter((item) => item.detected)
              .map((item) => item.category);

            return (
              <article
                key={record.id}
                className="rounded-xl border border-slate-200 bg-white p-6 shadow-sm"
              >
                <div className="flex flex-col justify-between gap-3 sm:flex-row sm:items-center">
                  <span
                    className={`w-fit rounded-full px-3 py-1 text-xs font-semibold ${
                      record.status === "blocked"
                        ? "bg-red-100 text-red-700"
                        : "bg-emerald-100 text-emerald-700"
                    }`}
                  >
                    {record.status === "blocked" ? "Blocked" : "Allowed"}
                  </span>

                  <time
                    className="text-xs text-slate-400"
                    dateTime={record.created_at}
                  >
                    {new Date(record.created_at).toLocaleString()}
                  </time>
                </div>

                <p className="mt-4 whitespace-pre-wrap break-words text-sm leading-6 text-slate-700">
                  {record.prompt}
                </p>

                <div className="mt-5 grid gap-3 sm:grid-cols-2">
                  <Metric
                    label="Risk score"
                    value={`${record.overall_score}%`}
                  />
                  <Metric
                    label="Highest risk"
                    value={record.highest_risk || "None"}
                  />
                </div>

                <div className="mt-5">
                  <p className="text-xs font-semibold uppercase tracking-wider text-slate-400">
                    Detected categories
                  </p>

                  {detectedCategories.length > 0 ? (
                    <div className="mt-2 flex flex-wrap gap-2">
                      {detectedCategories.map((category) => (
                        <span
                          key={category}
                          className="rounded-full bg-slate-100 px-3 py-1 text-xs text-slate-600"
                        >
                          {category}
                        </span>
                      ))}
                    </div>
                  ) : (
                    <p className="mt-2 text-sm text-slate-500">
                      No security threats detected.
                    </p>
                  )}
                </div>
              </article>
            );
          })}
        </div>
      )}
    </main>
  );
}

function Metric({ label, value }) {
  return (
    <div className="rounded-lg bg-slate-50 p-3">
      <p className="text-xs text-slate-400">{label}</p>
      <p className="mt-1 text-sm font-semibold text-slate-800">{value}</p>
    </div>
  );
}
