import { useState } from "react";

const TwoFA = ({ onSuccess }: any) => {
  const [otp, setOtp] = useState("");
  const [error, setError] = useState("");

  const userId = localStorage.getItem("user_id");

  const verify = async () => {
    setError("");

    const res = await fetch("http://localhost:8000/generate-2fa", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        user_id: userId,
        otp:otp
      }),
    });

    const data = await res.json();

    if (data.error) {
      setError(data.error);
      return;
    }

    //  SUCCESS
    localStorage.removeItem("2fa_user");
    localStorage.setItem("auth_token", data.token);

    onSuccess();
  };

  return (
    <div className="auth-main">
      <div className="glass glow auth-card">
        <h2> 2FA Verification</h2>

        <p style={{ opacity: 0.7 }}>
          Enter code from Google Authenticator
        </p>

        <p style={{ fontSize: "12px", opacity: 0.6 }}>
          Code refreshes every 30 seconds
        </p>

        <input
          className="auth-input"
          placeholder="Enter 6-digit OTP"
          value={otp}
          onChange={(e) => setOtp(e.target.value)}
        />

        {error && <p style={{ color: "#f87171" }}>{error}</p>}

        <button onClick={verify} style={{ marginTop: "10px" }}>
          Verify
        </button>
      </div>
    </div>
  );
};

export default TwoFA;