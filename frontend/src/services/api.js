import axios from "axios";

const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL ||
  "http://localhost:8000";

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    "Content-Type": "application/json",
  },
});

export async function analyzePrompt(message) {

  const response = await api.post(
    "/chat",
    {
      message,
    }
  );

  return response.data;
}

export async function healthCheck() {

  const response =
    await api.get("/");

  return response.data;
}

export default api;