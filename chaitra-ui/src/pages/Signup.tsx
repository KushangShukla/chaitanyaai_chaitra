import { useState } from "react";
import { setAuthSession, signup } from "../services/api";

const Signup = ({ onSuccess, onSwitch }: any) => {
  const [email,setEmail]=useState("");
  const [password,setPassword]=useState("");
  const [fullName, setFullName] = useState("");
  const [company, setCompany] = useState("");
  const [error, setError] = useState("");

  const handleSignup = async () => {
    setError("");
    const data = await signup({
      email,
      password,
      full_name: fullName,
      company,
    });
    if (data?.status !== "success") {
      setError(data?.error || "Signup failed");
      return;
    }
    setAuthSession(data.token, data.user);
    onSuccess?.();
  };

  return (
    <div className="glass glow auth-card">
      <h2>Signup</h2>

      <input className="auth-input" placeholder="Full name" onChange={e=>setFullName(e.target.value)} />
      <input className="auth-input" placeholder="Company" onChange={e=>setCompany(e.target.value)} />
      <input className="auth-input" type="email" placeholder="Email address" onChange={e=>setEmail(e.target.value)} />
      <input className="auth-input" type="password" placeholder="Password" onChange={e=>setPassword(e.target.value)} />
      {error && <p style={{ color: "#f87171", marginTop: "8px" }}>{error}</p>}

      <div style={{ display: "flex", gap: "10px", marginTop: "12px" }}>
        <button onClick={handleSignup}>Signup</button>
        <button onClick={onSwitch}>Already have account</button>
      </div>
    </div>
  );
};

export default Signup;