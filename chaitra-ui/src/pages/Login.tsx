import { useState } from "react";
import { login, setAuthSession } from "../services/api";

const Login = ({ onSuccess, onSwitch }: any) => {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState("");

    const handleLogin = async () => {
        setError("");
        const data = await login({ email, password });
        if (data?.status !== "success") {
            setError(data?.error || "Login failed");
            return;
        }

        // 2FA Required
        if (data?.two_fa_required) {
            localStorage.setItem("2fa_user", data.user.id);
            onSuccess("2fa"); // switch screen to 2FA verification
            return;
        }

        // Normal Login
        setAuthSession(data.token, data.user);
        onSuccess?.();
    };

    return (
        <div className="glass glow auth-card">
            <h2>Login</h2>

            <input className="auth-input" type="email" placeholder="Email address" onChange={e=>setEmail(e.target.value)}/>
            <input className="auth-input" placeholder="Password" type="password" onChange={e=>setPassword(e.target.value)}/>
            {error && <p style={{ color: "#f87171", marginTop: "8px" }}>{error}</p>}

            <div style={{ display: "flex", gap: "10px", marginTop: "12px" }}>
                <button onClick={handleLogin}>Login</button>
                <button onClick={onSwitch}>Create account</button>
            </div>
        </div>
    );
};

export default Login;