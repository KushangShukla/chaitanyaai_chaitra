import { motion } from "framer-motion";
import { useState } from "react";

const Sidebar = ({ setPage }: any) => {
  const [active, setActive] = useState("chat");

  const menuTop = [
    { name: "New Chat", key: "chat" },
    { name: "Dashboard", key: "dashboard" },
    { name: "Predictions", key: "predictions" },
    { name: "Insights", key: "insights"},
    { name: "Data", key: "data"}
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
    <div className="sidebar glass">

      {/*  LOGO */}
      <motion.div
        whileHover={{ scale: 1.05 }}
        className="logo"
        onClick={() => handleClick("chat")}
      >
        CHAITRA
      </motion.div>

      {/*  NEW CHAT BUTTON */}
      <motion.div
        whileHover={{ scale: 1.05 }}
        whileTap={{ scale: 0.95 }}
        className="new-chat-btn glow"
        onClick={() => handleClick("chat")}
      >
          New Chat
      </motion.div>

      {/*  TOP MENU */}
      <div className="menu">
        {menuTop.slice(1).map((item) => (
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

      {/*  BOTTOM MENU */}
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
      </div>

    </div>
  );
};

export default Sidebar;