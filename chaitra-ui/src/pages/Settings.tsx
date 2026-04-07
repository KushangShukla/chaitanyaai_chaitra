import {useState} from "react";
import { useEffect } from "react";
import { getSettings, updateSettings } from "../services/api";
const Settings=() => {
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
            })
            .catch(() => setStatus("Could not load settings."));
    }, []);

    const handleSave = async () => {
        const res = await updateSettings({
            theme,
            voice_enabled: voice,
            chat_mode: chatMode,
            retention,
        });
        setStatus(res?.status === "success" ? "Settings saved." : (res?.error || "Save failed."));
    };

    return (
        <div className="glass" style={{ maxWidth: "720px", display: "grid", gap: "12px" }}>
            <h2>Settings</h2>

            <label>
                Voice:
                <input type="checkbox" checked={voice} onChange={()=>setVoice(!voice)} />
            </label>

            <label>
                Theme:
                <select value={theme} onChange={e=>setTheme(e.target.value)}>
                    <option value="dark">dark</option>
                    <option value="light">light</option>
                    <option value="system">system</option>
                </select>
            </label>

            <label>
                Chat Mode:
                <select value={chatMode} onChange={e=>setChatMode(e.target.value)}>
                    <option value="auto">auto</option>
                    <option value="rag">rag</option>
                    <option value="llm">llm</option>
                </select>
            </label>

            <label>
                Retention:
                <select value={retention} onChange={e=>setRetention(e.target.value)}>
                    <option value="30_days">30 days</option>
                    <option value="90_days">90 days</option>
                    <option value="forever">forever</option>
                </select>
            </label>

            <div>
                <button onClick={handleSave}>Save Settings</button>
                {status && <span style={{ marginLeft: "10px" }}>{status}</span>}
            </div>
        </div>
    );
};

export default Settings;