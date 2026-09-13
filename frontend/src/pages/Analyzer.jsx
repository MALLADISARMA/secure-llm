import { useState } from "react";

import PromptEditor from "../components/PromptEditor";
import AnalysisResult from "../components/AnalysisResult";

import { analyzePrompt } from "../services/api";

export default function Analyzer() {

  const [loading, setLoading] = useState(false);

  const [result, setResult] = useState(null);

  const [error, setError] = useState("");

  const handleAnalyze = async (prompt) => {

    try {

      setLoading(true);

      setError("");

      setResult(null);

      const response =
        await analyzePrompt(prompt);

      setResult(response);

    } catch (error) {

      console.error(error);

      setError(
        "Unable to connect to SecureLLM API Gateway."
      );

    } finally {

      setLoading(false);

    }
  };

  return (
    <main className="mx-auto max-w-7xl px-6 py-10">

      {/* Page Header */}
      <div className="mb-8">

        <p className="text-xs font-semibold uppercase tracking-wider text-slate-400">
          Security Analysis
        </p>

        <h1 className="mt-2 text-3xl font-bold tracking-tight text-slate-900">
          Prompt Security Analyzer
        </h1>

        <p className="mt-2 max-w-2xl text-sm leading-6 text-slate-500">
          Analyze prompts for security risks before
          they reach your language model.
        </p>

      </div>

      {/* Main Layout */}
      <div className="grid gap-8 lg:grid-cols-2">

        {/* Input */}
        <section>

          <PromptEditor
            onAnalyze={handleAnalyze}
            loading={loading}
          />

          {error && (
            <div className="mt-4 rounded-lg border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700">
              {error}
            </div>
          )}

        </section>

        {/* Results */}
        <section>

          {loading && (
            <LoadingState />
          )}

          {!loading && result && (
            <AnalysisResult
              result={result}
            />
          )}

          {!loading && !result && (
            <EmptyState />
          )}

        </section>

      </div>

    </main>
  );
}


function LoadingState() {
  return (
    <div className="flex min-h-[350px] items-center justify-center rounded-xl border border-slate-200 bg-white shadow-sm">

      <div className="text-center">

        <div className="mx-auto h-8 w-8 animate-spin rounded-full border-2 border-slate-200 border-t-slate-900" />

        <p className="mt-4 text-sm font-semibold text-slate-700">
          Analyzing prompt
        </p>

        <p className="mt-1 text-xs text-slate-400">
          Running semantic security checks...
        </p>

      </div>

    </div>
  );
}


function EmptyState() {
  return (
    <div className="flex min-h-[350px] items-center justify-center rounded-xl border border-dashed border-slate-300 bg-white">

      <div className="max-w-sm px-6 text-center">

        <div className="mx-auto flex h-12 w-12 items-center justify-center rounded-xl bg-slate-100">
          <span className="text-xl text-slate-500">
            ⌁
          </span>
        </div>

        <h2 className="mt-4 text-sm font-semibold text-slate-900">
          Analysis results
        </h2>

        <p className="mt-2 text-sm leading-6 text-slate-500">
          Enter a prompt and run the security
          analysis to see results here.
        </p>

      </div>

    </div>
  );
}