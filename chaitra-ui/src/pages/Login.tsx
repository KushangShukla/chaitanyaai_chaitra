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
        setAuthSession(data.token, data.user);
        onSuccess?.();
    };

    return (
        <div className="glass">
            <h2>Login</h2>

            <input placeholder="Email" onChange={e=>setEmail(e.target.value)}/>
            <input placeholder="Password" type="password" onChange={e=>setPassword(e.target.value)}/>
            {error && <p style={{ color: "#f87171", marginTop: "8px" }}>{error}</p>}

            <button onClick={handleLogin}>Login</button>
            <button onClick={onSwitch} style={{ marginLeft: "8px" }}>Create account</button>
        </div>
    );
};

export default Login;