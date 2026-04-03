import { useState } from "react";
import Sidebar from "./components/Sidebar";
import ChatBox from "./components/ChatBox";
import Dashboard from "./pages/Dashboard";

function App() {
  return (
    <div style={{height:"100vh", background:"#0f172a",color:"white"}}>
      <h1 style={{padding:"20px"}}>CHAITRA AI</h1>
      <ChatBox />
    </div>
  );
}

export default App;