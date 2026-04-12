import { useEffect, useState } from "react";
import { getPredictions } from "../services/api";

const Predictions = () => {
  const [data, setData] = useState<any>(null);

  const fetchPredictions = () => {
    getPredictions()
      .then((res) => {
        console.log("PREDICTIONS API:", res); // 🔍 debug
        setData(res);
      })
      .catch(() => setData(null));
  };

  useEffect(() => {
    fetchPredictions();
    const interval = setInterval(fetchPredictions, 5000);
    return () => clearInterval(interval);
  }, []);

  if (!data) return <p>Loading predictions...</p>;

  return (
    <div style={{ padding: "30px" }}>
      <h2> Live Predictions</h2>

      {/*  KPI CARDS */}
      <div style={{ display: "flex", gap: "15px", marginBottom: "20px", flexWrap: "wrap" }}>
        <div className="glass" style={{ padding: "10px" }}>
          Avg Prediction: ₹ {data?.kpis?.avg_prediction || 0}
        </div>
        <div className="glass" style={{ padding: "10px" }}>
          Total: {data?.kpis?.total_predictions || 0}
        </div>
      </div>

      {/*  PREDICTION CARDS */}
      {data?.predictions?.length ? (
        data.predictions.map((row: any) => (
          <div
            key={row.id}
            className="glass"
            style={{
              padding: "15px",
              marginBottom: "12px",
              borderRadius: "12px"
            }}
          >
            <b>{row.query}</b>

            <h3 style={{ margin: "5px 0" }}>
              ₹ {row.prediction?.toFixed?.(2) || 0}
            </h3>

            <p> Confidence: {row.confidence || 0}%</p>

            <div>
              {row?.explanation?.length ? (
                row.explanation.map((e: string, i: number) => (
                  <p key={i}>• {e}</p>
                ))
              ) : (
                <p>No explanation available</p>
              )}
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