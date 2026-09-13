# SecureLLM Frontend

This directory contains the React and Vite frontend for the SecureLLM prompt security analyzer.

## Run Locally

From this directory:

```powershell
npm ci
npm run dev
```

Open the local URL printed by Vite, normally `http://localhost:5173`. The API gateway must be running separately at `http://localhost:8000`.

To configure another API gateway URL:

```powershell
$env:VITE_API_BASE_URL = "http://localhost:8000"
npm run dev
```

## Checks

```powershell
npm run lint
npm run build
```

The production build is written to `dist/`. Use `npm run preview` to serve that build locally.
