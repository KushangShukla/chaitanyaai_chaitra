import { useEffect, useState } from "react";
import { getInsights } from "../services/api";

const Insights = () => {
  const [insights, setInsights] = useState<string[]>([]);

  useEffect(() => {
    getInsights()
      .then((res) => setInsights(res?.insights || []))
      .catch(() => setInsights([]));
  }, []);

  return (
    <div style={{ padding: "30px" }}>
      <h2>AI Insights</h2>

      <div className="glass" style={{ padding: "16px" }}>
        {insights.length === 0 ? (
          <p>No insights available.</p>
        ) : (
          insights.map((item, idx) => <p key={idx}>{item}</p>)
        )}
      </div>
    </div>
  );
};

export default Insights;