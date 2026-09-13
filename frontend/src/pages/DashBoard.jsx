import {
  ShieldCheck,
  ScanSearch,
  Activity,
  ArrowRight,
} from "lucide-react";

import { Link } from "react-router-dom";

export default function Dashboard() {
  return (
    <main className="mx-auto max-w-7xl px-6 py-10">

      {/* Header */}
      <div className="mb-10">
        <p className="text-xs font-semibold uppercase tracking-wider text-slate-400">
          SecureLLM
        </p>

        <h1 className="mt-2 text-3xl font-bold tracking-tight text-slate-900">
          AI Security Dashboard
        </h1>

        <p className="mt-2 max-w-2xl text-sm leading-6 text-slate-500">
          Analyze and protect LLM applications against
          security threats before prompts reach the model.
        </p>
      </div>

      {/* Statistics */}
      <div className="grid gap-5 md:grid-cols-3">

        <StatCard
          icon={ScanSearch}
          title="Security Categories"
          value="6"
        />

        <StatCard
          icon={Activity}
          title="Detection Engine"
          value="Semantic AI"
        />

        <StatCard
          icon={ShieldCheck}
          title="Gateway Status"
          value="Protected"
          success
        />

      </div>

      {/* Main CTA */}
      <div className="mt-8 rounded-xl border border-slate-200 bg-white p-8 shadow-sm">

        <div className="max-w-2xl">

          <h2 className="text-xl font-bold text-slate-900">
            Analyze a prompt
          </h2>

          <p className="mt-2 text-sm leading-6 text-slate-500">
            Run a security analysis against prompt injection,
            jailbreaks, PII, prompt leakage, toxicity and
            malicious intent.
          </p>

          <Link
            to="/analyzer"
            className="mt-6 inline-flex items-center gap-2 rounded-lg bg-slate-900 px-5 py-2.5 text-sm font-semibold text-white transition hover:bg-slate-800"
          >
            Open Analyzer

            <ArrowRight className="h-4 w-4" />
          </Link>

        </div>

      </div>

    </main>
  );
}


function StatCard({
  icon: Icon,
  title,
  value,
  success = false,
}) {
  return (
    <div className="rounded-xl border border-slate-200 bg-white p-6 shadow-sm">

      <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-slate-100">
        <Icon className="h-5 w-5 text-slate-700" />
      </div>

      <p className="mt-5 text-sm font-medium text-slate-500">
        {title}
      </p>

      <p
        className={`mt-1 text-xl font-bold ${
          success ? "text-emerald-600" : "text-slate-900"
        }`}
      >
        {value}
      </p>

    </div>
  );
}