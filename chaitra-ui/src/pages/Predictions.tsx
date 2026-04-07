import { useEffect, useState } from "react";
import { getPredictions } from "../services/api";

type PredictionRow = {
  id: number;
  prediction: number;
  query: string;
};

const Predictions = () => {
  const [rows, setRows] = useState<PredictionRow[]>([]);

  useEffect(() => {
    getPredictions()
      .then((res) => setRows(res?.predictions || []))
      .catch(() => setRows([]));
  }, []);

  return (
    <div style={{ padding: "30px" }}>
      <h2>Predictions</h2>

      <div className="glass" style={{ padding: "16px" }}>
        {rows.length === 0 ? (
          <p>No prediction records found.</p>
        ) : (
          rows.map((row) => (
            <p key={row.id}>
              {row.query ? `${row.query.slice(0, 60)} - ` : ""}
              {row.prediction.toFixed(2)}
            </p>
          ))
        )}
      </div>
    </div>
  );
};

export default Predictions;