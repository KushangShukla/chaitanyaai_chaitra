import { useEffect, useState } from "react";
import { sendQuery } from "../services/api";
import { speak, stopSpeak } from "../services/voice";
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

const ChatBox = ({ selectedChat, onMessageSent }: any) => {
  const [query, setQuery] = useState("");
  const [messages, setMessages] = useState<
    { role: string; text: string }[]
  >([]);
  const [isListening, setIsListening] = useState(false);
  const hasMessages = messages.length > 0;
  const [voiceEnabled, setVoiceEnabled] = useState(true);
  const [editingIndex, setEditingIndex] = useState<number | null>(null);

  // 🔥 NEW: highlight state
  const [highlightIndex, setHighlightIndex] = useState<number | null>(null);

  useEffect(() => {
    const raw = localStorage.getItem("chaitra_settings");
    if (!raw) return;
    try {
      const parsed = JSON.parse(raw);
      setVoiceEnabled(parsed.voice_enabled !== false);
    } catch {
      setVoiceEnabled(true);
    }
  }, []);

  useEffect(() => {
    if (!selectedChat?.query && !selectedChat?.response) return;

    setMessages([
      { role: "user", text: selectedChat.query || "" },
      { role: "bot", text: selectedChat.response || "" },
    ]);
  }, [selectedChat]);

  // 🔥 Typing effect
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

  // 🎤 START LISTENING
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

  // 🛑 STOP LISTENING
  const stopListening = () => {
    setIsListening(false);
    recognition?.stop();
  };

  // 🔁 RE-RUN EDIT
  const reRunQuery = async (index: number) => {
    const newQuery = messages[index].text;

    try {
      const res = await sendQuery(newQuery);

      const updated = [...messages];
      updated[index + 1] = {
        role: "bot",
        text: res?.response || "No response",
      };

      setMessages(updated);
      setEditingIndex(null);
    } catch (err) {
      console.error(err);
    }
  };

  // 🎤 AUTO SEND
  const handleSendAuto = async (voiceText: string) => {
    if (!voiceText) return;

    const newMessages = [
      ...messages,
      { role: "user", text: voiceText },
      { role: "bot", text: "Thinking..." },
    ];

    setMessages(newMessages);

    const botIndex = newMessages.length - 1;

    try {
      const res = await sendQuery(voiceText);

      typeText(res?.response || "No response", botIndex);
      onMessageSent?.();
    } catch (err) {
      console.error(err);
    }
  };

  // ⌨️ MANUAL SEND
  const handleSend = async () => {
    if (!query) return;

    const newMessages = [
      ...messages,
      { role: "user", text: query },
      { role: "bot", text: "Thinking..." },
    ];

    setMessages(newMessages);
    setQuery("");

    const botIndex = newMessages.length - 1;

    try {
      const res = await sendQuery(query);

      typeText(res?.response || "No response", botIndex);
      onMessageSent?.();
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div className="chat-shell">

      {/*  CHAT AREA */}
      <div
        className="chat-messages"
        style={{
          height: "500px",
          overflowY: "auto",
          marginBottom: "20px"
        }}
      >
        {messages.map((msg, i) => {
          const words = msg.text.split(" ");

          return (
            <motion.div
              key={i}
              initial={{ opacity: 0, y: 8 }}
              animate={{ opacity: 1, y: 0 }}
              style={{
                textAlign: msg.role === "user" ? "right" : "left",
                margin: "12px 0",
              }}
            >
           <div className="msg-wrapper">
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

            {/*  EDIT MODE */}
            {editingIndex === i ? (
              <>
                <input
                value={msg.text}
                onChange={(e) => {
                const updated = [...messages];
                updated[i].text = e.target.value;
                setMessages(updated);
            }}
            style={{
              width: "100%",
              padding: "6px",
              borderRadius: "6px",
        }}
        />

        <div className="controls">
          <button className="glass" onClick={() => reRunQuery(i)}>✅</button>
        </div>
      </>
    ) : (
      <>
        {/*  TEXT WITH HIGHLIGHT */}
        {msg.text.split(" ").map((word, idx) => (
          <span
            key={idx}
            style={{
              background:
                idx === highlightIndex
                  ? "rgba(56,189,248,0.4)"
                  : "transparent",
              borderRadius: "4px",
              padding: "2px",
              marginRight: "2px",
            }}
          >
            {word}
          </span>
        ))}

        {/*  HOVER CONTROLS */}
        <div className="controls">
          {msg.role === "bot" && (
            <>
              <button
                className="glass"
                onClick={() =>
                  speak(msg.text, (i) => setHighlightIndex(i))
                }
              >
                🔊
              </button>

              <button className="glass" onClick={stopSpeak}>
                ⏹
              </button>
            </>
          )}

          {msg.role === "user" && (
            <button
              className="glass"
              onClick={() => setEditingIndex(i)}
            >
              ✏️
            </button>
          )}
        </div>
      </>
    )}
              </span>
            </div>      
            </motion.div>
          );
        })}
      </div>

      {/* 🎤 LISTENING UI */}
      {isListening && (
        <div style={{ display: "flex", gap: "10px", marginBottom: "10px" }}>
          <div className="pulse"></div>
          <span style={{ color: "#22c55e" }}>Listening...</span>
        </div>
      )}

      {/* ⌨️ INPUT AREA */}
      <div className={'chat-input-wrap ' + (hasMessages ? "sticky-bottom" : "floating-top") + " glass"}>
        <input
          className="chat-main-input"
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