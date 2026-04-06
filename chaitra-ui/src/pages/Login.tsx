import { useState } from "react";

const Login=()=>{
    const[email,setEmail]=useState("");
    const[password,setPassword]=useState("");

    const handleLogin=async()=> {
        await fetch("https://localhost:8000/login/",{
            method:"POST",
            headers:{
                "Content-Type":"application/json",
            },
            body:JSON.stringify({email,password}),
        });
    };

    return (
        <div className="glass">
            <h2>Login</h2>

            <input placeholder="Email" onChange={e=>setEmail(e.target.value)}/>
            <input placeholder="Password" type="password" onChange={e=>setPassword(e.target.value)}/>

            <button onClick={handleLogin}>Login</button>
        </div>
    );
};

export default Login;