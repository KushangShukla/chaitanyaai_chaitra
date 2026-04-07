import { motion } from "framer-motion";
import { useState, useEffect } from "react";
import { deleteChat, getChats, getStoredUser, pinChat } from "../services/api";

type ChatItem = { id: number; query: string; response: string; pinned?: boolean };

const Sidebar = ({ setPage, onSelectChat, refreshChatsKey, isCollapsed }: any) => {
  const [active, setActive] = useState("chat");
  const [chats, setChats] = useState<ChatItem[]>([]);
  const [search, setSearch] = useState("");

  const loadChats = () => {
    const user = getStoredUser();
    getChats(user?.id || "default_user")
      .then((data) => setChats(data?.chats || []))
      .catch(() => setChats([]));
  };

  useEffect(() => {
    loadChats();
  }, [refreshChatsKey]);

  //  FILTER CHATS
  const filteredChats = chats.filter((c) => {
    const q = (c?.query || "").toLowerCase();
    const r = (c?.response || "").toLowerCase();
    const term = search.toLowerCase();
    return q.includes(term) || r.includes(term);
  });

  const menuTop = [
    { name: "Dashboard", key: "dashboard" },
    { name: "Predictions", key: "predictions" },
    { name: "Insights", key: "insights" },
    { name: "Data", key: "data" }
  ];

  const menuBottom = [
    { name: "Profile", key: "profile" },
    { name: "Settings", key: "settings" }
  ];

  const handleClick = (key: string) => {
    setActive(key);
    setPage(key);
  };

  return (
    <div className={`sidebar glass ${isCollapsed ? "sidebar-collapsed" : ""}`}>

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
        New Chat
      </motion.div>

      {/*  SEARCH */}
      {!isCollapsed && (
        <input
          className="sidebar-search glass"
          placeholder="Search chats..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          style={{ marginBottom: "10px", width: "100%" }}
        />
      )}

      {/*  CHAT HISTORY */}
      {!isCollapsed && <div className="chat-history">
        {filteredChats.map((chat, i) => (
          <motion.div
            key={chat.id || i}
            whileHover={{ scale: 1.03 }}
            className="menu-item glow chat-history-item"
          >
            <div
              className="chat-history-title"
              onClick={() => {
                onSelectChat?.(chat);
                handleClick("chat");
              }}
            >
              {(chat.query || "Untitled chat").slice(0, 35)}
            </div>
            <div className="chat-actions">
              <button
                onClick={async () => {
                  await pinChat(chat.id, !chat.pinned);
                  loadChats();
                }}
              >
                {chat.pinned ? "Unpin" : "Pin"}
              </button>
              <button
                onClick={async () => {
                  await deleteChat(chat.id);
                  loadChats();
                }}
              >
                Delete
              </button>
            </div>
          </motion.div>
        ))}
      </div>}

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
            <span>{item.name}</span>
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
            <span>{item.name}</span>
          </motion.div>
        ))}
      </div>

    </div>
  );
};

export default Sidebar;