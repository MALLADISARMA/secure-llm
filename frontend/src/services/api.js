const API_GATEWAY_URL = "http://localhost:8000";
const LLM_SERVICE_URL = "http://localhost:8001";

/*
 * Analyze a prompt using the SecureLLM API Gateway
 */
export async function analyzePrompt(prompt) {
  const response = await fetch(
    `${API_GATEWAY_URL}/chat`,
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
    throw new Error("Security analysis request failed");
  }

  return await response.json();
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