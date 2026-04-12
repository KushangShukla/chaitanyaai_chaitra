import { useEffect, useState } from "react";
import {
  LineChart, Line, XAxis, YAxis, Tooltip,
  CartesianGrid, ResponsiveContainer,
  BarChart, Bar
} from "recharts";
import { getAuthHeaders } from "../services/api";

const Dashboard = () => {
  const [data, setData] = useState<any>(null);

  useEffect(() => {
    fetch("http://localhost:8000/dashboard",{
      headers:getAuthHeaders()
    })
      .then(res => res.json())
      .then(setData);
  }, []);

  if (!data) return <p>Loading dashboard...</p>;

  const trendChart = data.trend_data.map((v: number, i: number) => ({
    name: `T-${i}`,
    sales: v
  }));

  const featureData = data.feature_importance
    ? Object.entries(data.feature_importance).map(([k, v]) => ({
        name: k,
        value: Number(v)
      }))
    : [];

  return (
    <div style={{ padding: "30px", maxWidth: "1200px", margin: "auto" }}>
      <h2> Business Dashboard</h2>

      {/* KPI */}
      <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(180px,1fr))", gap: "15px" }}>
        <div className="glass">Avg: ₹ {data.kpis.avg_sales}</div>
        <div className="glass">Max: ₹ {data.kpis.max_sales}</div>
        <div className="glass">Min: ₹ {data.kpis.min_sales}</div>
        <div className="glass">Records: {data.kpis.total_records}</div>
        <div className="glass">Best: ₹ {data.kpis.best_store}</div>
        <div className="glass">Worst: ₹ {data.kpis.worst_store}</div>
      </div>

      {/* TREND */}
      <div className="glass" style={{ marginTop: "20px", padding: "15px" }}>
        <h3> Trend</h3>
        <ResponsiveContainer width="100%" height={250}>
          <LineChart data={trendChart}>
            <XAxis dataKey="name" />
            <YAxis />
            <Tooltip />
            <CartesianGrid />
            <Line dataKey="sales" stroke="#22c55e" />
          </LineChart>
        </ResponsiveContainer>
      </div>

      {/* FEATURE IMPORTANCE */}
      <div className="glass" style={{ marginTop: "20px", padding: "15px" }}>
        <h3> Feature Importance</h3>
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={featureData}>
            <XAxis dataKey="name" />
            <YAxis />
            <Tooltip />
            <CartesianGrid />
            <Bar dataKey="value" fill="#38bdf8" />
          </BarChart>
        </ResponsiveContainer>
      </div>

      {/* ML CARDS */}
      <div style={{ display: "flex", gap: "15px", marginTop: "20px", flexWrap: "wrap" }}>
        {data.cards?.map((c: any, i: number) => (
          <div key={i} className="glass">
            <b>{c.title}</b>
            <p>{c.value}</p>
          </div>
        ))}
      </div>

      {/* INSIGHTS */}
      <div className="glass" style={{ marginTop: "20px", padding: "15px" }}>
        <h3> Insights</h3>
        {data.insights.map((i: string, idx: number) => (
          <p key={idx}>• {i}</p>
        ))}
      </div>

      {/* LLM */}
      <div className="glass" style={{ marginTop: "20px", padding: "15px" }}>
        <h3> AI Explanation (phi-2)</h3>
        <p>{data.llm_explanation || "No explanation available"}</p>
      </div>
    </div>
  );
};

export default Dashboard;