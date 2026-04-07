import { useEffect, useState } from "react";
import {
  CartesianGrid,
  LineChart,
  Tooltip,
  XAxis,
  YAxis,
  Line,
  ResponsiveContainer
} from "recharts";
import { motion } from "framer-motion";
import { getDashboard } from "../services/api";

const Dashboard = () => {
  const [data, setData] = useState<any>({});
  const [chartData, setChartData] = useState<any[]>([]);

  useEffect(() => {
    getDashboard()
      .then((resData) => {
        setData(resData);

        //  Convert backend → chart format
        if (resData.recent_predictions) {
          const formatted = resData.recent_predictions.map(
            (val: number, index: number) => ({
              name: `#${index + 1}`,
              sales: val
            })
          );
          setChartData(formatted);
        } else {
          // fallback demo
          setChartData([
            { name: "1", sales: 12000 },
            { name: "2", sales: 15000 },
            { name: "3", sales: 18000 }
          ]);
        }
      })
      .catch(() => {
        setData({});
        setChartData([]);
      });
  }, []);

  return (
    <div style={{ padding: "30px" }}>
      <h2>📊 Business Dashboard</h2>

      {/*  KPI CARDS */}
      <div
        style={{
          display: "flex",
          gap: "20px",
          marginTop: "20px",
          flexWrap: "wrap"
        }}
      >
        <motion.div className="glass glow" whileHover={{ scale: 1.05 }}>
          <h3>Avg Prediction</h3>
          <p style={{ fontSize: "24px", fontWeight: "bold" }}>
            {data.avg_prediction || 0}
          </p>
        </motion.div>

        <motion.div className="glass glow" whileHover={{ scale: 1.05 }}>
          <h3>Total Queries</h3>
          <p style={{ fontSize: "24px", fontWeight: "bold" }}>
            {data.total_queries || 0}
          </p>
        </motion.div>
      </div>

      {/*  CHART */}
      <motion.div
        className="glass glow"
        style={{ marginTop: "30px", padding: "20px" }}
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
      >
        <h3> Sales Trend</h3>

        <ResponsiveContainer width="100%" height={300}>
          <LineChart data={chartData}>
            <XAxis dataKey="name" stroke="#94a3b8" />
            <YAxis stroke="#94a3b8" />
            <Tooltip />
            <CartesianGrid stroke="#1e293b" />
            <Line
              type="monotone"
              dataKey="sales"
              stroke="#38bdf8"
              strokeWidth={2}
              dot={{ r: 4 }}
            />
          </LineChart>
        </ResponsiveContainer>
      </motion.div>
    </div>
  );
};

export default Dashboard;