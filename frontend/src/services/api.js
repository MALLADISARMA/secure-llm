const API_GATEWAY_URL =
  import.meta.env.VITE_API_BASE_URL || "http://localhost:8002";
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

async function requestJson(url, options, serviceName) {
  let response;

  try {
    response = await fetch(url, options);
  } catch (error) {
    if (error instanceof TypeError) {
      throw new Error(
        `Cannot reach the ${serviceName} at ${url}. Check that it is running and that the browser can access it.`
      );
    }

    throw error;
  }

  return parseResponse(response);
}

/*
 * Analyze a prompt using the SecureLLM API Gateway
 */
export async function analyzePrompt(prompt) {
  return requestJson(
    `${API_GATEWAY_URL}/chat`,
    {
      method: "POST",
      headers: gatewayHeaders(),
      body: JSON.stringify({
        message: prompt,
      }),
    },
    "API Gateway"
  );
}

export async function getHistory() {
  return requestJson(
    `${API_GATEWAY_URL}/history`,
    { headers: gatewayHeaders() },
    "API Gateway"
  );
}

export async function clearHistory() {
  return requestJson(
    `${API_GATEWAY_URL}/history`,
    {
      method: "DELETE",
      headers: gatewayHeaders(),
    },
    "API Gateway"
  );
}


/*
 * Generate an LLM response using the local Ollama/Qwen service
 */
export async function generateLLMResponse(prompt) {
  return requestJson(
    `${LLM_SERVICE_URL}/generate`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        message: prompt,
      }),
    },
    "LLM service"
  );
}