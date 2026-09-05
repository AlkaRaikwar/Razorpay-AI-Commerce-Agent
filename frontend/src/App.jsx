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
    <div
      style={{
        minHeight: "100vh",
        background: "#f5f7fb",
        fontFamily: "Arial, sans-serif",
        padding: "40px 20px",
      }}
    >
      <div
        style={{
          maxWidth: "900px",
          margin: "auto",
        }}
      >
        {/* HEADER */}
        <div
          style={{
            background: "#111827",
            color: "white",
            padding: "28px",
            borderRadius: "16px",
            marginBottom: "24px",
          }}
        >
          <h1 style={{ margin: 0 }}>
            Razorpay AI Commerce Agent
          </h1>

          <p
            style={{
              marginBottom: 0,
              color: "#cbd5e1",
            }}
          >
            AI-powered shopping assistant with smart
            recommendations and revenue growth
          </p>
        </div>

        {/* SEARCH */}
        <div
          style={{
            background: "white",
            padding: "24px",
            borderRadius: "16px",
            boxShadow: "0 2px 10px rgba(0,0,0,0.06)",
            marginBottom: "24px",
          }}
        >
          <h2 style={{ marginTop: 0 }}>
            What are you looking for?
          </h2>

          <form onSubmit={handleSubmit}>
            <div
              style={{
                display: "flex",
                gap: "10px",
              }}
            >
              <input
                type="text"
                placeholder="I need running shoes under ₹2000"
                value={message}
                onChange={(e) => setMessage(e.target.value)}
                style={{
                  flex: 1,
                  padding: "14px",
                  border: "1px solid #d1d5db",
                  borderRadius: "10px",
                  fontSize: "16px",
                }}
              />

              <button
                type="submit"
                disabled={loading}
                style={{
                  padding: "14px 24px",
                  border: "none",
                  borderRadius: "10px",
                  background: "#2563eb",
                  color: "white",
                  fontSize: "16px",
                  cursor: "pointer",
                }}
              >
                {loading ? "Searching..." : "Search"}
              </button>
            </div>
          </form>

          {/* ERROR */}
          {error && (
            <p
              style={{
                color: "red",
                marginBottom: 0,
              }}
            >
              Error: {error}
            </p>
          )}
        </div>

        {/* RESULTS */}
        {response && response.action === "recommendation" && (
          <>
            {/* RECOMMENDATIONS */}
            <div
              style={{
                background: "white",
                padding: "24px",
                borderRadius: "16px",
                marginBottom: "20px",
              }}
            >
              <h2>🤖 Recommended Products</h2>

              <div
                style={{
                  display: "grid",
                  gridTemplateColumns:
                    "repeat(auto-fit, minmax(250px, 1fr))",
                  gap: "16px",
                }}
              >
                {response.products?.map((product) => (
                  <div
                    key={product.id}
                    style={{
                      border: "1px solid #e5e7eb",
                      borderRadius: "12px",
                      padding: "18px",
                    }}
                  >
                    <h3 style={{ marginTop: 0 }}>
                      {product.name}
                    </h3>

                    <p
                      style={{
                        color: "#6b7280",
                      }}
                    >
                      {product.description}
                    </p>

                    <p
                      style={{
                        fontSize: "20px",
                        fontWeight: "bold",
                      }}
                    >
                      ₹{product.price}
                    </p>

                    <p
                      style={{
                        color: "#16a34a",
                      }}
                    >
                      In Stock: {product.stock}
                    </p>

                    {response.recommended_product?.id ===
                      product.id && (
                      <span
                        style={{
                          background: "#dcfce7",
                          color: "#166534",
                          padding: "6px 10px",
                          borderRadius: "20px",
                          fontSize: "13px",
                        }}
                      >
                        ⭐ Best Match
                      </span>
                    )}
                  </div>
                ))}
              </div>
            </div>

            {/* CROSS SELL */}
            {response.cross_sell?.length > 0 && (
              <div
                style={{
                  background: "#fff7ed",
                  padding: "24px",
                  borderRadius: "16px",
                  marginBottom: "20px",
                  border: "1px solid #fed7aa",
                }}
              >
                <h2>✨ You May Also Like</h2>

                {response.cross_sell.map((item) => (
                  <div
                    key={item.id}
                    style={{
                      background: "white",
                      padding: "16px",
                      borderRadius: "12px",
                    }}
                  >
                    <h3 style={{ marginTop: 0 }}>
                      🧦 {item.name}
                    </h3>

                    <p>
                      <strong>₹{item.price}</strong>
                    </p>

                    <p
                      style={{
                        color: "#6b7280",
                      }}
                    >
                      {item.reason}
                    </p>
                  </div>
                ))}
              </div>
            )}

            {/* CART */}
            {response.cart && (
              <div
                style={{
                  background: "white",
                  padding: "24px",
                  borderRadius: "16px",
                  marginBottom: "20px",
                }}
              >
                <h2>🛒 Your Cart</h2>

                {response.cart.items?.map((item) => (
                  <div
                    key={item.id}
                    style={{
                      display: "flex",
                      justifyContent: "space-between",
                      padding: "12px 0",
                      borderBottom:
                        "1px solid #e5e7eb",
                    }}
                  >
                    <span>
                      {item.name} × {item.quantity}
                    </span>

                    <strong>
                      ₹{item.price * item.quantity}
                    </strong>
                  </div>
                ))}

                <div
                  style={{
                    display: "flex",
                    justifyContent: "space-between",
                    marginTop: "20px",
                    fontSize: "20px",
                  }}
                >
                  <strong>Total</strong>

                  <strong
                    style={{
                      color: "#16a34a",
                    }}
                  >
                    ₹{response.cart.subtotal}
                  </strong>
                </div>
              </div>
            )}

            {/* CONFIRMATION */}
            {response.confirmation && (
              <div
                style={{
                  background: "#eff6ff",
                  border: "1px solid #bfdbfe",
                  padding: "24px",
                  borderRadius: "16px",
                }}
              >
                <h2>💳 Ready for Payment?</h2>

                <p>
                  {response.confirmation.message}
                </p>

                <button
                  style={{
                    padding: "14px 24px",
                    border: "none",
                    borderRadius: "10px",
                    background: "#16a34a",
                    color: "white",
                    fontSize: "16px",
                    cursor: "pointer",
                  }}
                >
                  Proceed to Payment
                </button>
              </div>
            )}
          </>
        )}
      </div>
    </div>
  );
}

export default App;