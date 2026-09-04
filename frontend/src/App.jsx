import React, { useState } from "react";
import { sendMessage } from "./services/agentApi";

function App() {
  const [message, setMessage] = useState("");
  const [response, setResponse] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!message.trim()) return;

    setLoading(true);
    setError("");
    setResponse(null);

    try {
      const data = await sendMessage(message);
      setResponse(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }

    setMessage("");
  };

  return (
    <div>
      <h1>Razorpay AI Commerce Agent</h1>

      <p>What are you looking for?</p>

      <form onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="I want running shoes under ₹2000"
          value={message}
          onChange={(e) => setMessage(e.target.value)}
        />

        <button type="submit" disabled={loading}>
          {loading ? "Searching..." : "Search"}
        </button>
      </form>

      {error && (
        <p>
          Error: {error}
        </p>
      )}

      {response && (
        <div>
          <h2>Agent Response</h2>

          <pre>
            {JSON.stringify(response, null, 2)}
          </pre>
        </div>
      )}
    </div>
  );
}

export default App;