import { useState } from "react";
import { sendQuery } from "../services/api";

const ChatBox = () => {
  const [query, setQuery] = useState("");
  const [messages, setMessages] = useState<
    { role: string; text: string }[]
  >([]);

  const handleSend = async () => {
    if (!query) return;

    // Add user message
    setMessages((prev) => [...prev, { role: "user", text: query }]);

    const currentQuery = query;
    setQuery("");

    // Add loading
    setMessages((prev) => [
      ...prev,
      { role: "bot", text: "Thinking..." },
    ]);

    try {
      const res = await sendQuery(currentQuery);

      // Replace last message (loading)
      setMessages((prev) => {
        const updated = [...prev];
        updated[updated.length - 1] = {
          role: "bot",
          text: res.response,
        };
        return updated;
      });
    } catch (err) {
      console.error(err);

      setMessages((prev) => {
        const updated = [...prev];
        updated[updated.length - 1] = {
          role: "bot",
          text: "Error connecting to server",
        };
        return updated;
      });
    }
  };

  return (
    <div style={{ padding: "20px" }}>
      <div
        style={{
          height: "400px",
          overflowY: "auto",
          marginBottom: "20px",
        }}
      >
        {messages.map((msg, i) => (
          <div
            key={i}
            style={{
              textAlign: msg.role === "user" ? "right" : "left",
              margin: "10px 0",
            }}
          >
            <span
              style={{
                background:
                  msg.role === "user" ? "#2563eb" : "#1e293b",
                padding: "10px",
                borderRadius: "10px",
                display: "inline-block",
              }}
            >
              {msg.text}
            </span>
          </div>
        ))}
      </div>

      <div>
        <input
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Ask CHAITRA..."
          style={{
            padding: "10px",
            width: "70%",
            borderRadius: "8px",
            border: "none",
          }}
        />

        <button
          onClick={handleSend}
          style={{
            padding: "10px",
            marginLeft: "10px",
            borderRadius: "8px",
            background: "#2563eb",
            color: "white",
            border: "none",
          }}
        >
          Send
        </button>
      </div>
    </div>
  );
};

export default ChatBox;