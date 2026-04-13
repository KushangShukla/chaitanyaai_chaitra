import { useState } from "react";

const ForgotPassword = ({ onSuccess }: any) => {
  const [step, setStep] = useState(1); // 1=email, 2=otp+password

  const [email, setEmail] = useState("");
  const [otp, setOtp] = useState("");
  const [password, setPassword] = useState("");

  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  // =========================
  // STEP 1 → SEND OTP
  // =========================
  const sendOTP = async () => {
    setError("");
    setMessage("");

    try {
      const res = await fetch("http://localhost:8000/forgot-password", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ email }),
      });

      const data = await res.json();

      if (data.error) {
        setError(data.error);
        return;
      }

      setMessage("OTP sent to your email");
      setStep(2);
    } catch {
      setError("Failed to send OTP");
    }
  };

  // =========================
  // STEP 2 → RESET PASSWORD
  // =========================
  const resetPassword = async () => {
    setError("");
    setMessage("");

    try {
      const res = await fetch("http://localhost:8000/reset-password", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          email,
          otp,
          password,
        }),
      });

      const data = await res.json();

      if (data.error) {
        setError(data.error);
        return;
      }

      setMessage("Password reset successful ");

      setTimeout(() => {
        onSuccess(); // go back to login
      }, 1500);
    } catch {
      setError("Reset failed");
    }
  };

  return (
    <div className="auth-main">
      <div className="glass glow auth-card">
        <h2> Forgot Password</h2>

        {/* STEP 1 */}
        {step === 1 && (
          <>
            <input
              className="auth-input"
              placeholder="Enter your email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            />

            <button onClick={sendOTP} style={{ marginTop: "10px" }}>
              Send OTP
            </button>
          </>
        )}

        {/* STEP 2 */}
        {step === 2 && (
          <>
            <input
              className="auth-input"
              placeholder="Enter OTP"
              value={otp}
              onChange={(e) => setOtp(e.target.value)}
            />

            <input
              className="auth-input"
              placeholder="New Password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />

            <button onClick={resetPassword} style={{ marginTop: "10px" }}>
              Reset Password
            </button>
          </>
        )}

        {/* MESSAGES */}
        {message && <p style={{ color: "#4ade80" }}>{message}</p>}
        {error && <p style={{ color: "#f87171" }}>{error}</p>}

        {/* BACK */}
        <p
          style={{
            marginTop: "10px",
            cursor: "pointer",
            fontSize: "12px",
            opacity: 0.7,
          }}
          onClick={() => onSuccess()}
        >
          Back to Login
        </p>
      </div>
    </div>
  );
};

export default ForgotPassword;