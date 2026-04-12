import { useEffect, useState } from "react";
import { getInsights } from "../services/api";

const Insights = () => {
  const [data, setData] = useState<any>(null);

  const fetchInsights = () => {
    getInsights()
      .then((res) => {
        console.log("INSIGHTS API:", res); // 🔍 debug
        setData(res);
      })
      .catch(() => setData(null));
  };

  useEffect(() => {
    fetchInsights();
    const interval = setInterval(fetchInsights, 5000);
    return () => clearInterval(interval);
  }, []);

  if (!data) return <p>Loading insights...</p>;

  return (
    <div style={{ padding: "30px" }}>
      <h2>🧠 AI Insights</h2>

      {/*  CARDS */}
      <div style={{ display: "flex", gap: "15px", marginBottom: "20px", flexWrap: "wrap" }}>
        {data?.cards?.length ? (
          data.cards.map((c: any, i: number) => (
            <div key={i} className="glass" style={{ padding: "10px", minWidth: "150px" }}>
              <b>{c.title}</b>
              <p>{c.value}</p>
            </div>
          ))
        ) : (
          <p>No insight cards</p>
        )}
      </div>

      {/*  INSIGHTS LIST */}
      <div className="glass" style={{ padding: "15px" }}>
        {data?.insights?.length ? (
          data.insights.map((item: string, idx: number) => (
            <p key={idx}>• {item}</p>
          ))
        ) : (
          <p>No insights available</p>
        )}
      </div>
    </div>
  );
};

export default Insights;