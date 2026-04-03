import { useState } from "react";
import { sendQuery } from "../services/api";
import { speak } from "../services/voice";

// Safe SpeechRecognition setup
let recognition: any;

if (typeof window !== "undefined") {
  const SpeechRecognition =
    (window as any).SpeechRecognition ||
    (window as any).webkitSpeechRecognition;

  if (SpeechRecognition) {
    recognition = new SpeechRecognition();
    recognition.continuous = true;
    recognition.lang = "en-US";
  }
}

const ChatBox = () => {
  const [query, setQuery] = useState("");
  const [messages, setMessages] = useState<
    { role: string; text: string }[]
  >([]);
  const [isListening, setIsListening] = useState(false);

  // 🎤 START LISTENING
  const startListening = () => {
    if (!recognition) return;

    setIsListening(true);
    recognition.start();

    recognition.onresult = (event: any) => {
      const transcript =
        event.results[event.results.length - 1][0].transcript;

      setQuery(transcript);
      handleSendAuto(transcript); //  auto send
    };

    recognition.onend = () => {
      if (isListening) recognition.start(); //  continuous loop
    };
  };

  // 🛑 STOP LISTENING
  const stopListening = () => {
    setIsListening(false);
    if (recognition) recognition.stop();
  };

  // 🔁 AUTO SEND (VOICE MODE)
  const handleSendAuto = async (voiceText: string) => {
    if (!voiceText) return;

    setMessages((prev) => [...prev, { role: "user", text: voiceText }]);

    setMessages((prev) => [
      ...prev,
      { role: "bot", text: "Thinking..." },
    ]);

    try {
      const res = await sendQuery(voiceText);

      setMessages((prev) => {
        const updated = [...prev];
        updated[updated.length - 1] = {
          role: "bot",
          text: res?.response || "No response from AI",
        };
        return updated;
      });

      speak(res.response); //  speak

    } catch (err) {
      console.error(err);
    }
  };

  //  MANUAL SEND
  const handleSend = async () => {
    if (!query) return;

    setMessages((prev) => [...prev, { role: "user", text: query }]);

    const currentQuery = query;
    setQuery("");

    setMessages((prev) => [
      ...prev,
      { role: "bot", text: "Thinking..." },
    ]);

    try {
      const res = await sendQuery(currentQuery);

      setMessages((prev) => {
        const updated = [...prev];
        updated[updated.length - 1] = {
          role: "bot",
          text: res.response,
        };
        return updated;
      });

      speak(res.response);

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
      {/* Chat Messages */}
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

      {/* Listening Indicator */}
      {isListening && (
        <div style={{ color: "#22c55e", marginBottom: "10px" }}>
          🎤 Listening...
        </div>
      )}

      {/* Input Area */}
      <div>
        <input
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Ask CHAITRA..."
          style={{
            padding: "10px",
            width: "60%",
            borderRadius: "8px",
            border: "none",
          }}
        />

        {/* Send Button */}
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

        {/* 🎤 Start / Stop */}
        {!isListening ? (
          <button
            onClick={startListening}
            style={{
              padding: "10px",
              marginLeft: "10px",
              borderRadius: "8px",
              background: "#16a34a",
              color: "white",
              border: "none",
            }}
          >
            Start
          </button>
        ) : (
          <button
            onClick={stopListening}
            style={{
              padding: "10px",
              marginLeft: "10px",
              borderRadius: "8px",
              background: "#dc2626",
              color: "white",
              border: "none",
            }}
          >
            Stop
          </button>
        )}
      </div>
    </div>
  );
};

export default ChatBox;