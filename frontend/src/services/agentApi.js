// API client for AI Agent endpoints.
const API_BASE_URL = "http://localhost:8000";

export async function sendMessage(message) {
  const response = await fetch(`${API_BASE_URL}/agent`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      message: message,
    }),
  });

  if (!response.ok) {
    throw new Error(`Agent API failed: ${response.status}`);
  }

  return await response.json();
}