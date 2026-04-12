import { useEffect, useState } from "react";
import { getPredictions } from "../services/api";

const Predictions = () => {
  const [data, setData] = useState<any>(null);

  useEffect(() => {
    const fetchData = () => {
      getPredictions()
        .then((res) => {
          console.log("PREDICTIONS API:", res);
          setData(res);
        })
        .catch(() => setData(null));
    };

    fetchData();
    const interval = setInterval(fetchData, 5000);
    return () => clearInterval(interval);
  }, []);

  if (!data) return <p>Loading predictions...</p>;

  return (
    <div style={{ padding: "30px" }}>
      <h2>🔮 Live Predictions</h2>

      {/* ================= KPI ================= */}
      <div style={{ display: "flex", gap: "15px", marginBottom: "20px" }}>
        <div className="glass">
          Avg: ₹ {data?.kpis?.avg_prediction || 0}
        </div>
        <div className="glass">
          Total: {data?.kpis?.total_predictions || 0}
        </div>
      </div>

      {/* ================= CARDS ================= */}
      {data?.predictions?.length ? (
        data.predictions.map((row: any) => (
          <div
            key={row.id}
            className="glass"
            style={{
              marginTop: "15px",
              padding: "15px",
              borderRadius: "12px"
            }}
          >
            <b>{row.query}</b>

            <h3>₹ {row.prediction?.toFixed?.(2) || 0}</h3>

            <p>Confidence: {row.confidence || 0}%</p>

            {/* RULE EXPLANATION */}
            <div>
              {row?.explanation?.length ? (
                row.explanation.map((e: string, i: number) => (
                  <p key={i}>• {e}</p>
                ))
              ) : (
                <p>No explanation available</p>
              )}
            </div>

            {/* LLM BLOCK */}
            <div style={{ marginTop: "10px" }}>
              <b> AI Explanation (phi-2)</b>
              <p style={{ opacity: 0.85 }}>
                {row.llm_explanation || "No AI explanation"}
              </p>
            </div>
          </div>
        ))
      ) : (
        <p>No predictions available</p>
      )}
    </div>
  );
};

export default Predictions;