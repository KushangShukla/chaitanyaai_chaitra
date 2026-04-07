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
    <div className="glass">
      <h2>Signup</h2>

      <input placeholder="Full name" onChange={e=>setFullName(e.target.value)} />
      <input placeholder="Company" onChange={e=>setCompany(e.target.value)} />
      <input onChange={e=>setEmail(e.target.value)} />
      <input type="password" onChange={e=>setPassword(e.target.value)} />
      {error && <p style={{ color: "#f87171", marginTop: "8px" }}>{error}</p>}

      <button onClick={handleSignup}>Signup</button>
      <button onClick={onSwitch} style={{ marginLeft: "8px" }}>Already have account</button>
    </div>
  );
};

export default Signup;