import { useEffect, useState } from "react";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  ResponsiveContainer,
  BarChart,
  Bar
} from "recharts";

const Dashboard = () => {
  const [data, setData] = useState<any>(null);

  useEffect(() => {
    fetch("http://localhost:8000/dashboard")
      .then(res => res.json())
      .then(setData);
  }, []);

  if (!data) return <p>Loading dashboard...</p>;

  const isPositiveTrend = data.trend > 0;

  //  Trend chart
  const trendChart = data.trend_data.map((v: number, i: number) => ({
    name: `T-${i}`,
    sales: v
  }));

  //  Feature importance chart
  const featureData = data.feature_importance
    ? Object.entries(data.feature_importance).map(([k, v]) => ({
        name: k,
        value: Number(v)
      }))
    : [];

  return (
    <div style={{ padding: "30px", maxWidth: "1200px", margin: "auto" }}>
      <h2> Business Dashboard</h2>

      {/*  KPI CARDS */}
      <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(180px,1fr))", gap: "15px" }}>
        <div className="glass">Avg: ₹ {data.kpis.avg_sales}</div>
        <div className="glass">Max: ₹ {data.kpis.max_sales}</div>
        <div className="glass">Min: ₹ {data.kpis.min_sales}</div>
        <div className="glass">Records: {data.kpis.total_records}</div>
        <div className="glass">Best Store: ₹ {data.kpis.best_store}</div>
        <div className="glass">Worst Store: ₹ {data.kpis.worst_store}</div>
      </div>

      {/*  TREND */}
      <div className="glass" style={{ marginTop: "20px", padding: "15px" }}>
        <h3> Sales Trend</h3>
        <p style={{ color: isPositiveTrend ? "green" : "red" }}>
          {isPositiveTrend ? "Increasing " : "Decreasing "} ({data.trend})
        </p>

        <ResponsiveContainer width="100%" height={250}>
          <LineChart data={trendChart}>
            <XAxis dataKey="name" />
            <YAxis />
            <Tooltip />
            <CartesianGrid />
            <Line type="monotone" dataKey="sales" stroke="#22c55e" />
          </LineChart>
        </ResponsiveContainer>
      </div>

      {/*  FEATURE IMPORTANCE */}
      <div className="glass" style={{ marginTop: "20px", padding: "15px" }}>
        <h3> Feature Importance</h3>

        {featureData.length === 0 ? (
          <p>No feature importance available</p>
        ) : (
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={featureData}>
              <XAxis dataKey="name" />
              <YAxis />
              <Tooltip />
              <CartesianGrid />
              <Bar dataKey="value" fill="#38bdf8" />
            </BarChart>
          </ResponsiveContainer>
        )}
      </div>

      {/*  INSIGHTS */}
      <div className="glass" style={{ marginTop: "20px", padding: "15px" }}>
        <h3> AI Insights</h3>
        {data.insights.map((i: string, idx: number) => (
          <p key={idx}>• {i}</p>
        ))}
      </div>

      {/*  EXPLANATION */}
      <div className="glass" style={{ marginTop: "20px", padding: "15px" }}>
        <h3> Business Explanation</h3>
        <p>{data.explanation}</p>
      </div>
    </div>
  );
};

export default Dashboard;