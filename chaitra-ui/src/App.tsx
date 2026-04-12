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
import Login from "./pages/Login";
import Signup from "./pages/Signup";
import TwoFA from "./pages/TwoFA";
import ForgotPassword from "./pages/ForgotPassword";
import EmailOTP from "./pages/EmailOTP";
import { clearAuthSession, getStoredToken } from "./services/api";

function App() {
  const [page, setPage] = useState("chat");
  const [selectedChat, setSelectedChat] = useState<any>(null);
  const [refreshChatsKey, setRefreshChatsKey] = useState(0);
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [isAuthenticated, setIsAuthenticated] = useState(Boolean(getStoredToken()));
  const [authPage, setAuthPage] = useState<"login" | "signup">("login");
  const [authStep, setAuthStep] = useState("login");

  useEffect(() => {
    const token=localStorage.getItem("auth_token");

    if (token){
      setAuthStep("app");
    } else{
      setAuthStep("login");
    }
  },[]);
  
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
      case "settings":
        return (
          <Settings
            onLogout={() => {
              clearAuthSession();
              setIsAuthenticated(false);
              setPage("chat");
            }}
          />
        );
      default:
        return (
          <Chat
            selectedChat={selectedChat}
            onMessageSent={() => setRefreshChatsKey((v) => v + 1)}
          />
        );
    }
  };

  if (authStep === "login")
  return <Login onSuccess={setAuthStep} onSwitch={() => setAuthStep("signup")} />;

  if (authStep === "signup")
    return <Signup onSuccess={() => setAuthStep("login")} onSwitch={() => setAuthStep("login")} />;

  if (authStep === "2fa")
    return <TwoFA onSuccess={() => setAuthStep("app")} />;

  if (authStep === "forgot")
    return <ForgotPassword onSuccess={() => setAuthStep("login")} />;

  if (authStep === "email-otp")
    return <EmailOTP onSuccess={() => setAuthStep("app")} />;

  return (
    <div className="app-container">
      {!isAuthenticated ? (
        <main className="auth-main">
          {authPage === "login" ? (
            <Login onSuccess={() => setIsAuthenticated(true)} onSwitch={() => setAuthPage("signup")} />
          ) : (
            <Signup onSuccess={() => setIsAuthenticated(true)} onSwitch={() => setAuthPage("login")} />
          )} 
        </main>
      ) : (
        <>
      
      {/* 🔹 Floating Sidebar */}
      <button
        className={`sidebar-toggle glass ${sidebarOpen ? "menu-open" : "menu-closed"}`}
        onClick={() => setSidebarOpen((v) => !v)}
      >
        {sidebarOpen ? "Hide Menu" : "Show Menu"}
      </button>
      <div className={`sidebar-shell ${sidebarOpen ? "open" : "closed"}`}>
        {sidebarOpen && (
          <Sidebar
            setPage={setPage}
            onSelectChat={setSelectedChat}
            refreshChatsKey={refreshChatsKey}
            isCollapsed={false}
          />
        )}
      </div>

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
      </>
      )}

    </div>
  );
}

export default App;