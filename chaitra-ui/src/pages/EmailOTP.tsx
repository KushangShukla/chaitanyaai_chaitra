import { useState } from "react";

const EmailOTP = ({ onSuccess }: any) => {
  const [otp, setOtp] = useState("");
  const [error, setError] = useState("");

  const userId = localStorage.getItem("otp_user");

  const verifyOTP = async () => {
    setError("");

    try {
      const res = await fetch("http://localhost:8000/verify-email-otp", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          user_id: userId,
          otp: otp,
        }),
      });

      const data = await res.json();

      if (data.error) {
        setError(data.error);
        return;
      }

      // ✅ SUCCESS
      localStorage.removeItem("otp_user");
      localStorage.setItem("auth_token", data.token);

      onSuccess(); // go to app
    } catch (err) {
      setError("Something went wrong");
    }
  };

  return (
    <div className="auth-main">
      <div className="glass glow auth-card">
        <h2>📩 Email Verification</h2>

        <p style={{ opacity: 0.7 }}>
          Enter the OTP sent to your email
        </p>

        <input
          className="auth-input"
          placeholder="Enter 6-digit OTP"
          value={otp}
          onChange={(e) => setOtp(e.target.value)}
        />

        <p style={{ fontSize: "12px", opacity: 0.6 }}>
          OTP valid for limited time
        </p>

        {error && <p style={{ color: "#f87171" }}>{error}</p>}

        <button onClick={verifyOTP} style={{ marginTop: "10px" }}>
          Verify OTP
        </button>
      </div>
    </div>
  );
};

export default EmailOTP;