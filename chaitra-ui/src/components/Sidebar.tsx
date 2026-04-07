import { motion } from "framer-motion";
import { useState, useEffect } from "react";
import { getChats, getStoredUser } from "../services/api";

type ChatItem = { query: string; response: string };

const Sidebar = ({ setPage, onSelectChat, onLogout }: any) => {
  const [active, setActive] = useState("chat");
  const [chats, setChats] = useState<ChatItem[]>([]);
  const [search, setSearch] = useState("");

  //  FETCH CHAT HISTORY
  useEffect(() => {
    const user = getStoredUser();
    getChats(user?.id || "default_user")
      .then((data) => setChats(data?.chats || []))
      .catch(() => setChats([]));
  }, []);

  //  FILTER CHATS
  const filteredChats = chats.filter((c) => {
    const q = (c?.query || "").toLowerCase();
    const r = (c?.response || "").toLowerCase();
    const term = search.toLowerCase();
    return q.includes(term) || r.includes(term);
  });

  const menuTop = [
    { name: "Dashboard", key: "dashboard", icon: "📊" },
    { name: "Predictions", key: "predictions", icon: "📈" },
    { name: "Insights", key: "insights", icon: "🧠" },
    { name: "Data", key: "data", icon: "📂" }
  ];

  const menuBottom = [
    { name: "Profile", key: "profile", icon: "👤" },
    { name: "Settings", key: "settings", icon: "⚙️" }
  ];

  const handleClick = (key: string) => {
    setActive(key);
    setPage(key);
  };

  return (
    <div className="sidebar glass">

      {/*  LOGO */}
      <motion.div
        whileHover={{ scale: 1.05 }}
        className="logo"
        onClick={() => handleClick("chat")}
      >
        CHAITRA
      </motion.div>

      {/*  NEW CHAT */}
      <motion.div
        whileHover={{ scale: 1.05 }}
        whileTap={{ scale: 0.95 }}
        className="new-chat-btn glow"
        onClick={() => handleClick("chat")}
      >
        ➕ New Chat
      </motion.div>

      {/*  SEARCH */}
      <input
        placeholder="Search chats..."
        value={search}
        onChange={(e) => setSearch(e.target.value)}
        style={{ marginBottom: "10px", width: "100%" }}
      />

      {/*  CHAT HISTORY */}
      <div className="chat-history">
        {filteredChats.map((chat, i) => (
          <motion.div
            key={i}
            whileHover={{ scale: 1.03 }}
            className="menu-item glow"
            onClick={() => {
              onSelectChat?.(chat);
              handleClick("chat");
            }}
          >
            {(chat.query || "Untitled chat").slice(0, 25)}...
          </motion.div>
        ))}
      </div>

      {/*  MENU */}
      <div className="menu">
        {menuTop.map((item) => (
          <motion.div
            key={item.key}
            whileHover={{ scale: 1.05, x: 5 }}
            whileTap={{ scale: 0.95 }}
            onClick={() => handleClick(item.key)}
            className={`menu-item glow ${
              active === item.key ? "active" : ""
            }`}
          >
            <span>{item.icon}</span>
            <span style={{ marginLeft: "10px" }}>{item.name}</span>
          </motion.div>
        ))}
      </div>

      {/*  BOTTOM */}
      <div className="menu-bottom">
        {menuBottom.map((item) => (
          <motion.div
            key={item.key}
            whileHover={{ scale: 1.05, x: 5 }}
            whileTap={{ scale: 0.95 }}
            onClick={() => handleClick(item.key)}
            className={`menu-item glow ${
              active === item.key ? "active" : ""
            }`}
          >
            <span>{item.icon}</span>
            <span style={{ marginLeft: "10px" }}>{item.name}</span>
          </motion.div>
        ))}
        <motion.div
          whileHover={{ scale: 1.05, x: 5 }}
          whileTap={{ scale: 0.95 }}
          onClick={onLogout}
          className="menu-item glow"
        >
          <span>🚪</span>
          <span style={{ marginLeft: "10px" }}>Logout</span>
        </motion.div>
      </div>

    </div>
  );
};

export default Sidebar;