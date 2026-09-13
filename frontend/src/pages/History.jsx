import {
  History as HistoryIcon,
} from "lucide-react";

export default function History() {
  return (
    <main className="mx-auto max-w-7xl px-6 py-10">

      <div className="mb-8">

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

      <div className="flex min-h-[350px] flex-col items-center justify-center rounded-xl border border-slate-200 bg-white shadow-sm">

        <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-slate-100">
          <HistoryIcon className="h-5 w-5 text-slate-500" />
        </div>

        <h2 className="mt-4 text-sm font-semibold text-slate-900">
          No analysis history
        </h2>

        <p className="mt-2 max-w-sm text-center text-sm leading-6 text-slate-500">
          Previous security analyses will appear here
          once history storage is connected.
        </p>

      </div>

    </main>
  );
}