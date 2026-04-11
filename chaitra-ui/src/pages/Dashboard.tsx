import { useEffect, useState } from "react";
import {
  LineChart, Line, XAxis, YAxis, Tooltip, CartesianGrid,
  ResponsiveContainer, BarChart, Bar
} from "recharts";
import { motion } from "framer-motion";

const Dashboard = () => {
  const [data, setData] = useState<any>(null);

  const fetchData = () => {
    fetch("http://localhost:8000/dashboard")
      .then(res => res.json())
      .then(setData);
  };

  useEffect(() => {
    fetchData();

    //  AUTO REFRESH (LIVE DEMO)
    const interval = setInterval(fetchData, 5000);

    return () => clearInterval(interval);
  }, []);

  if (!data) return <p>Loading dashboard...</p>;

  const isPositiveTrend = data.trend > 0;

  //  FORMAT TREND DATA
  const trendData = data.trend_series?.map((val: number, i: number) => ({
    name: `T-${data.trend_series.length - i}`,
    sales: val
  })) || [];

  //  FORMAT FEATURE IMPORTANCE
  const featureData = data.feature_importance?.map((f: any) => ({
    feature: f[0],
    value: Number((f[1] * 100).toFixed(2))
  })) || [];

  return (
    <div style={{ maxWidth: "1100px", margin: "auto", display: "grid", gap: "20px", padding: "20px" }}>
      
      <h2> Business Dashboard</h2>

      {/* KPI CARDS */}
      <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(180px, 1fr))", gap: "16px" }}>
        {[
          { label: "Avg Sales", value: data.kpis.avg_sales },
          { label: "Max Sales", value: data.kpis.max_sales },
          { label: "Min Sales", value: data.kpis.min_sales },
          { label: "Records", value: data.kpis.total_records }
        ].map((card, idx) => (
          <motion.div key={idx} className="glass glow" whileHover={{ scale: 1.05 }}>
            <h4>{card.label}</h4>
            <h2>₹ {card.value}</h2>
          </motion.div>
        ))}
      </div>

      {/* TREND */}
      <div className="glass">
        <h3> Sales Trend</h3>
        <p style={{ color: isPositiveTrend ? "#22c55e" : "#ef4444" }}>
          {isPositiveTrend ? "Increasing " : "Decreasing "} ({data.trend})
        </p>
      </div>

      {/*  REAL TIME TREND CHART */}
      <motion.div className="glass glow" initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
        <h3> Real Sales Trend (Last Data Points)</h3>

        <ResponsiveContainer width="100%" height={300}>
          <LineChart data={trendData}>
            <XAxis dataKey="name" stroke="#94a3b8" />
            <YAxis stroke="#94a3b8" />
            <Tooltip />
            <CartesianGrid stroke="#1e293b" />
            <Line
              type="monotone"
              dataKey="sales"
              stroke="#22c55e"
              strokeWidth={3}
              dot={{ r: 3 }}
            />
          </LineChart>
        </ResponsiveContainer>
      </motion.div>

      {/*  FEATURE IMPORTANCE */}
      <motion.div className="glass glow" initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
        <h3> Feature Importance (Model Explainability)</h3>

        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={featureData}>
            <XAxis dataKey="feature" stroke="#94a3b8" />
            <YAxis stroke="#94a3b8" />
            <Tooltip />
            <CartesianGrid stroke="#1e293b" />
            <Bar dataKey="value" />
          </BarChart>
        </ResponsiveContainer>
      </motion.div>

      {/* INSIGHTS */}
      <div className="glass">
        <h3> AI Insights</h3>
        {data.insights.map((i: string, idx: number) => (
          <p key={idx}>• {i}</p>
        ))}
      </div>

      {/* EXPLANATION */}
      <div className="glass">
        <h3> Business Explanation</h3>
        <p>{data.explanation}</p>
      </div>

    </div>
  );
};

export default Dashboard;