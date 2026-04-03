import { useEffect, useState } from "react";

const Dashboard=() => {
    const [data,setData]=useState<any>({});

    useEffect(() => {
        fetch("http://localhost:8000/dashboard/")
            .then(res =>res.json())
            .then(data =>setData(data));
    }, []);

    return (
        <div style ={{ padding:"20px"}}>
            <h2>Business Dashboard</h2>

            <p>Average Prediction: {data.avg_prediction}</p>
            <p>Total Queries: {data.total_queries}</p>
        </div>
    );
};

export default Dashboard;