import { useState } from "react";
import {
  ScanSearch,
  Trash2,
} from "lucide-react";

export default function PromptEditor({
  onAnalyze,
  loading,
}) {
  const [prompt, setPrompt] = useState("");

  const handleSubmit = (event) => {
    event.preventDefault();

    if (!prompt.trim()) {
      return;
    }

    onAnalyze(prompt);
  };

  const clearPrompt = () => {
    setPrompt("");
  };

  return (
    <form onSubmit={handleSubmit}>

      <div className="overflow-hidden rounded-xl border border-slate-200 bg-white shadow-sm">

        {/* Header */}
        <div className="flex items-center justify-between border-b border-slate-100 px-5 py-4">

          <div>
            <h2 className="text-sm font-semibold text-slate-900">
              Prompt Input
            </h2>

            <p className="mt-1 text-xs text-slate-500">
              Enter the prompt you want SecureLLM to analyze.
            </p>
          </div>

          <button
            type="button"
            onClick={clearPrompt}
            disabled={!prompt}
            className="flex items-center gap-1.5 rounded-md px-2.5 py-1.5 text-xs font-medium text-slate-500 hover:bg-slate-100 disabled:opacity-40"
          >
            <Trash2 className="h-3.5 w-3.5" />

            Clear
          </button>

        </div>

        {/* Text area */}
        <textarea
          value={prompt}
          onChange={(event) =>
            setPrompt(event.target.value)
          }
          placeholder="Enter a prompt to analyze for security risks..."
          maxLength={10000}
          className="min-h-[280px] w-full resize-none border-0 px-5 py-5 text-sm leading-7 text-slate-800 outline-none placeholder:text-slate-400"
        />

        {/* Footer */}
        <div className="flex items-center justify-between border-t border-slate-100 bg-slate-50 px-5 py-3">

          <span className="text-xs text-slate-400">
            {prompt.length.toLocaleString()} / 10,000
          </span>

          <button
            type="submit"
            disabled={!prompt.trim() || loading}
            className="flex items-center gap-2 rounded-lg bg-slate-900 px-5 py-2.5 text-sm font-semibold text-white transition hover:bg-slate-800 disabled:cursor-not-allowed disabled:opacity-50"
          >
            <ScanSearch className="h-4 w-4" />

            {loading
              ? "Analyzing..."
              : "Analyze Prompt"}
          </button>

        </div>

      </div>

    </form>
  );
}