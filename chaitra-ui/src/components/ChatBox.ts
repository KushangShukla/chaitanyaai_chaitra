import { useState } from "react";

const ChatBox=() => {
    const[query,setQuery]=useState("");
    const[message,setMessages]=useState<string[]>([]);

    const handleSend=() => {
        if (!query) return;

        setMessages((prev) => [...prev," " +query]);
        setMessages((prev) => [...prev," Loading..."]);

        setQuery("");
    };

    return (
        <div style={{padding:"20px"}}>
            <div style={{minHeight:"400px",marginBottom:"20x"}}>
                {messages.map((msg,i) => (
                    <div key={i}>{msg}</div>
                ))}
                </div>

                <input
                    value={query}
                    onChange={(e) => setQuery(e.target.value)}
                    placeholder="Ask CHAITRA..."
                    style={{padding:"10px",width:"70%"}}
                />

                <button onClick={handleSend} style={{padding: "10px" }}>
                    Send
                </button>
            </div>
    );
};

export default ChatBox;