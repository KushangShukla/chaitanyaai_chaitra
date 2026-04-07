import { useEffect, useState } from "react";
import { getDashboard, getStoredUser, me, updateProfile } from "../services/api";

const Profile = () => {
  const [fullName, setFullName] = useState("");
  const [company, setCompany] = useState("");
  const [role, setRole] = useState("business");
  const [email, setEmail] = useState("");
  const [createdAt, setCreatedAt] = useState("");
  const [kpis, setKpis] = useState({ total_queries: 0, avg_prediction: 0 });
  const [status, setStatus] = useState("");

  useEffect(() => {
    const bootstrap = async () => {
      const localUser = getStoredUser();
      if (localUser?.email) setEmail(localUser.email);

      const meData = await me();
      if (meData?.status === "success") {
        const u = meData.user;
        setFullName(u.full_name || "");
        setCompany(u.company || "");
        setRole(u.role || "business");
        setEmail(u.email || "");
        setCreatedAt(u.created_at || "");
      }

      const dashboardData = await getDashboard();
      setKpis({
        total_queries: dashboardData?.total_queries || 0,
        avg_prediction: dashboardData?.avg_prediction || 0,
      });
    };

    bootstrap().catch(() => setStatus("Could not load profile data."));
  }, []);

  const handleSave = async () => {
    setStatus("");
    const res = await updateProfile({ full_name: fullName, company, role });
    setStatus(res?.status === "success" ? "Profile updated." : (res?.error || "Update failed."));
  };

  return (
    <div style={{ padding: "30px" }}>
      <h2>Profile</h2>

      <div className="glass" style={{ display: "grid", gap: "12px", maxWidth: "720px" }}>
        <label>
          Full Name
          <input value={fullName} onChange={(e) => setFullName(e.target.value)} />
        </label>
        <label>
          Email
          <input value={email} disabled />
        </label>
        <label>
          Company
          <input value={company} onChange={(e) => setCompany(e.target.value)} />
        </label>
        <label>
          Role
          <select value={role} onChange={(e) => setRole(e.target.value)}>
            <option value="business">Business</option>
            <option value="admin">Admin</option>
          </select>
        </label>

        <div style={{ marginTop: "8px" }}>
          <p>Total Queries: {kpis.total_queries}</p>
          <p>Avg Prediction: {kpis.avg_prediction}</p>
          <p>Joined: {createdAt ? new Date(createdAt).toLocaleString() : "-"}</p>
        </div>

        <div>
          <button onClick={handleSave}>Save Profile</button>
          {status && <span style={{ marginLeft: "10px" }}>{status}</span>}
        </div>
      </div>
    </div>
  );
};

export default Profile;