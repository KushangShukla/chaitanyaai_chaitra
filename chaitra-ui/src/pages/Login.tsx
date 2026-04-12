import { useState } from "react";
import { login, setAuthSession } from "../services/api";

const Login = ({ onSuccess, onSwitch }: any) => {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState("");

    const handleLogin = async () => {
    setError("");

    const data = await login({ email, password });

    if (!data) {
        setError("Server error");
        return;
    }

    //  ERROR
    if (data?.error || data?.status === "error") {
        setError(data?.error || "Login failed");
        return;
    }

    //  EMAIL OTP FLOW
    if (data?.status === "otp_sent") {
        localStorage.setItem("otp_user", data.user_id);
        onSuccess?.("email-otp");   // 👈 switch screen
        return;
    }

    //  2FA FLOW (FIXED KEY NAME)
    if (data?.["2fa_required"]) {
        localStorage.setItem("2fa_user", data.user_id);
        onSuccess?.("2fa");
        return;
    }

    //  NORMAL LOGIN
    setAuthSession(data.token, data.user);

    //  STORE USER ID (IMPORTANT FOR 2FA LATER)
    localStorage.setItem("user_id", data.user.id);

    onSuccess?.("app");
    };

    return (
  <div className="auth-main">
    <div className="glass glow auth-card">
      <h2>Login</h2>

      <input className="auth-input" type="email" placeholder="Email address"
        onChange={e => setEmail(e.target.value)} />

      <input className="auth-input" type="password" placeholder="Password"
        onChange={e => setPassword(e.target.value)} />

        <p
            style={{ marginTop: "8px", cursor: "pointer", fontSize: "12px", opacity: 0.7 }}
            onClick={() => onSuccess?.("forgot")}
            >
            Forgot Password?
        </p>

      {/* Forgot Password */}
      <p
        style={{ marginTop: "8px", cursor: "pointer", fontSize: "12px", opacity: 0.7 }}
        onClick={() => onSuccess?.("forgot")}
      >
        Forgot Password?
      </p>

      {error && <p style={{ color: "#f87171" }}>{error}</p>}

      <div style={{ display: "flex", gap: "10px", marginTop: "12px" }}>
        <button onClick={handleLogin}>Login</button>
        <button onClick={onSwitch}>Create account</button>
      </div>
    </div>
  </div>
);
};

export default Login;