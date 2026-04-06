import { useState, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";

import Sidebar from "./components/Sidebar";

import Chat from "./pages/Chat";
import Dashboard from "./pages/Dashboard";
import Predictions from "./pages/Predictions";
import Insights from "./pages/Insights";
import Data from "./pages/Data";
import Profile from "./pages/Profile";
import Settings from "./pages/Settings";

function App() {
  const [page, setPage] = useState("chat");

  //  Cursor Glow Tracking (BACKGROUND EFFECT)
  useEffect(() => {
    const move = (e: any) => {
      document.body.style.setProperty("--x", e.clientX + "px");
      document.body.style.setProperty("--y", e.clientY + "px");
    };

    window.addEventListener("mousemove", move);
    return () => window.removeEventListener("mousemove", move);
  }, []);

  //  Page Routing
  const renderPage = () => {
    switch (page) {
      case "dashboard": return <Dashboard />;
      case "predictions": return <Predictions />;
      case "insights": return <Insights />;
      case "data": return <Data />;
      case "profile": return <Profile />;
      case "settings": return <Settings />;
      default: return <Chat />;
    }
  };

  return (
    <div className="app-container">
      
      {/* 🔹 Floating Sidebar */}
      <Sidebar setPage={setPage} />

      {/* 🔹 Main Content with Animation */}
      <main className="main-content">
        <AnimatePresence mode="wait">
          <motion.div
            key={page}
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -10 }}
            transition={{ duration: 0.3 }}
          >
            {renderPage()}
          </motion.div>
        </AnimatePresence>
      </main>

    </div>
  );
}

export default App;