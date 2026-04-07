import {useState} from "react";
import { useEffect } from "react";
import { getSettings, updateSettings } from "../services/api";

const applyTheme = (nextTheme: string) => {
    document.body.classList.remove("theme-light", "theme-dark");
    if (nextTheme === "light") document.body.classList.add("theme-light");
    if (nextTheme === "dark") document.body.classList.add("theme-dark");
};

const Settings=({ onLogout }: any) => {
    const[voice,setVoice]=useState(true);
    const[theme,setTheme]=useState("dark");
    const [chatMode, setChatMode] = useState("auto");
    const [retention, setRetention] = useState("90_days");
    const [status, setStatus] = useState("");

    useEffect(() => {
        getSettings()
            .then((res) => {
                const s = res?.settings;
                if (!s) return;
                setVoice(Boolean(s.voice_enabled));
                setTheme(s.theme || "dark");
                setChatMode(s.chat_mode || "auto");
                setRetention(s.retention || "90_days");
                applyTheme(s.theme || "dark");
                localStorage.setItem("chaitra_settings", JSON.stringify(s));
            })
            .catch(() => setStatus("Could not load settings."));
    }, []);

    useEffect(() => {
        applyTheme(theme);
    }, [theme]);

    const handleSave = async () => {
        const res = await updateSettings({
            theme,
            voice_enabled: voice,
            chat_mode: chatMode,
            retention,
        });
        localStorage.setItem(
            "chaitra_settings",
            JSON.stringify({ theme, voice_enabled: voice, chat_mode: chatMode, retention })
        );
        setStatus(res?.status === "success" ? "Settings saved." : (res?.error || "Save failed."));
    };

    return (
        <div className="glass" style={{ maxWidth: "720px", display: "grid", gap: "12px" }}>
            <h2>Settings</h2>

            <div>
                <p>Voice</p>
                <div className="button-group">
                    <button className={`toggle-btn ${voice ? "selected" : ""}`} onClick={() => setVoice(true)}>On</button>
                    <button className={`toggle-btn ${!voice ? "selected" : ""}`} onClick={() => setVoice(false)}>Off</button>
                </div>
            </div>

            <div>
                <p>Theme</p>
                <div className="button-group">
                    {["dark", "light", "system"].map((opt) => (
                        <button key={opt} className={`toggle-btn ${theme === opt ? "selected" : ""}`} onClick={() => setTheme(opt)}>
                            {opt}
                        </button>
                    ))}
                </div>
            </div>

            <div>
                <p>Chat Mode</p>
                <div className="button-group">
                    {["auto", "rag", "llm"].map((opt) => (
                        <button key={opt} className={`toggle-btn ${chatMode === opt ? "selected" : ""}`} onClick={() => setChatMode(opt)}>
                            {opt}
                        </button>
                    ))}
                </div>
            </div>

            <div>
                <p>Retention</p>
                <div className="button-group">
                    {[
                        { key: "30_days", label: "30 days" },
                        { key: "90_days", label: "90 days" },
                        { key: "forever", label: "forever" },
                    ].map((opt) => (
                        <button key={opt.key} className={`toggle-btn ${retention === opt.key ? "selected" : ""}`} onClick={() => setRetention(opt.key)}>
                            {opt.label}
                        </button>
                    ))}
                </div>
            </div>

            <div>
                <button onClick={handleSave}>Save Settings</button>
                <button style={{ marginLeft: "10px" }} onClick={onLogout}>Logout</button>
                {status && <span style={{ marginLeft: "10px" }}>{status}</span>}
            </div>
        </div>
    );
};

export default Settings;