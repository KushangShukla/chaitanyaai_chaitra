import { useState } from "react";
import { sendQuery } from "../services/api";
import { speak } from "../services/voice";
import { motion } from "framer-motion";

// Speech Recognition Setup
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

  //  AI Typing Effect
  const typeText = (text: string, index: number) => {
    let i = 0;
    let temp = "";

    const interval = setInterval(() => {
      temp += text[i];
      i++;

      setMessages((prev) => {
        const updated = [...prev];
        updated[index] = { role: "bot", text: temp };
        return updated;
      });

      if (i >= text.length) clearInterval(interval);
    }, 12);
  };

  //  START LISTENING
  const startListening = () => {
    if (!recognition) return;

    setIsListening(true);
    recognition.start();

    recognition.onresult = (event: any) => {
      const transcript =
        event.results[event.results.length - 1][0].transcript;

      handleSendAuto(transcript);
    };

    recognition.onend = () => {
      if (isListening) recognition.start();
    };
  };

  //  STOP
  const stopListening = () => {
    setIsListening(false);
    recognition?.stop();
  };

  //  AUTO SEND (VOICE)
  const handleSendAuto = async (voiceText: string) => {
    if (!voiceText) return;

    setMessages((prev) => [
      ...prev,
      { role: "user", text: voiceText },
      { role: "bot", text: "Thinking..." },
    ]);

    const botIndex = messages.length + 1;

    try {
      const res = await sendQuery(voiceText);

      typeText(res?.response || "No response", botIndex);
      speak(res.response);

    } catch (err) {
      console.error(err);
    }
  };

  //  MANUAL SEND
  const handleSend = async () => {
    if (!query) return;

    const currentQuery = query;

    setMessages((prev) => [
      ...prev,
      { role: "user", text: currentQuery },
      { role: "bot", text: "Thinking..." },
    ]);

    setQuery("");

    const botIndex = messages.length + 1;

    try {
      const res = await sendQuery(currentQuery);

      typeText(res.response, botIndex);
      speak(res.response);

    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div style={{ padding: "20px" }}>

      {/*  CHAT AREA */}
      <div
        style={{
          height: "500px",
          overflowY: "auto",
          marginBottom: "20px",
        }}
      >
        {messages.map((msg, i) => (
          <motion.div
            key={i}
            initial={{ opacity: 0, y: 8 }}
            animate={{ opacity: 1, y: 0 }}
            style={{
              textAlign: msg.role === "user" ? "right" : "left",
              margin: "12px 0",
            }}
          >
            <span
              className={`glass ${msg.role === "bot" ? "typing" : ""}`}
              style={{
                background:
                  msg.role === "user"
                    ? "#2563eb"
                    : "rgba(255,255,255,0.05)",
                padding: "12px",
                borderRadius: "12px",
                display: "inline-block",
                maxWidth: "70%",
              }}
            >
              {msg.text}
            </span>
          </motion.div>
        ))}
      </div>

      {/*  LISTENING UI */}
      {isListening && (
        <div style={{ display: "flex", gap: "10px", marginBottom: "10px" }}>
          <div className="pulse"></div>
          <div className="wave"></div>
          <span style={{ color: "#22c55e" }}>Listening...</span>
        </div>
      )}

      {/* INPUT AREA */}
      <div>
        <input
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Ask CHAITRA..."
        />

        <button onClick={handleSend}>Send</button>

        {!isListening ? (
          <button onClick={startListening}>🎤</button>
        ) : (
          <button onClick={stopListening}>🛑</button>
        )}
      </div>
    </div>
  );
};

export default ChatBox;