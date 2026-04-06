import { useState } from "react";

const Signup = () => {
  const [email,setEmail]=useState("");
  const [password,setPassword]=useState("");

  const handleSignup = async () => {
    await fetch("http://localhost:8000/signup/", {
      method:"POST",
      headers:{ "Content-Type":"application/json"},
      body: JSON.stringify({email,password})
    });
  };

  return (
    <div className="glass">
      <h2>Signup</h2>

      <input onChange={e=>setEmail(e.target.value)} />
      <input type="password" onChange={e=>setPassword(e.target.value)} />

      <button onClick={handleSignup}>Signup</button>
    </div>
  );
};

export default Signup;