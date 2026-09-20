const API_GATEWAY_URL = "http://localhost:8000";
const LLM_SERVICE_URL = "http://localhost:8001";
const SESSION_STORAGE_KEY = "securellm_session_id";

function createSessionId() {
  if (typeof crypto !== "undefined" && crypto.randomUUID) {
    return crypto.randomUUID();
  }

  const values = new Uint32Array(4);
  crypto.getRandomValues(values);
  return Array.from(values, (value) => value.toString(36)).join("-");
}

export function getSessionId() {
  let sessionId = localStorage.getItem(SESSION_STORAGE_KEY);

  if (!sessionId) {
    sessionId = createSessionId();
    localStorage.setItem(SESSION_STORAGE_KEY, sessionId);
  }

  return sessionId;
}

function gatewayHeaders() {
  return {
    "Content-Type": "application/json",
    "X-Session-ID": getSessionId(),
  };
}

async function parseResponse(response) {
  const data = await response.json().catch(() => ({}));

  if (!response.ok) {
    throw new Error(data.detail || data.message || "Request failed");
  }

  return data;
}

/*
 * Analyze a prompt using the SecureLLM API Gateway
 */
export async function analyzePrompt(prompt) {
  const response = await fetch(
    `${API_GATEWAY_URL}/chat`,
    {
      method: "POST",
      headers: gatewayHeaders(),
      body: JSON.stringify({
        message: prompt,
      }),
    }
  );

  return parseResponse(response);
}

export async function getHistory() {
  const response = await fetch(`${API_GATEWAY_URL}/history`, {
    headers: gatewayHeaders(),
  });

  return parseResponse(response);
}

export async function clearHistory() {
  const response = await fetch(`${API_GATEWAY_URL}/history`, {
    method: "DELETE",
    headers: gatewayHeaders(),
  });

  return parseResponse(response);
}


/*
 * Generate an LLM response using the local Ollama/Qwen service
 */
export async function generateLLMResponse(prompt) {
  const response = await fetch(
    `${LLM_SERVICE_URL}/generate`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        message: prompt,
      }),
    }
  );

  if (!response.ok) {
    throw new Error("LLM service request failed");
  }

  return await response.json();
}