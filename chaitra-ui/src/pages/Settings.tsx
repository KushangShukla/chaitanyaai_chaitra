import {useState} from "react";
const Settings=() => {
    const[voice,setVoice]=useState(true);
    const[theme,setTheme]=useState("dark");

    return (
        <div className="glass">
            <h2>Settings</h2>

            <label>
                Voice:
                <input type="checkbox" checked={voice} onChange={()=>setVoice(!voice)} />
            </label>

            <label>
                Theme:
                <select onChange={e=>setTheme(e.target.value)}>
                    <option>dark</option>
                    <option>light</option>
                </select>
            </label>
        </div>
    );
};

export default Settings;