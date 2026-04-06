import { useEffect, useState } from "react";
import { CartesianGrid, LineChart, Tooltip, XAxis, YAxis, Line } from "recharts";

const Dashboard=() => {
    const [data,setData]=useState<any>({});
    const [charData,setCharData]=useState<any[]>([]);

    useEffect(() => {
        fetch("http://localhost:8000/dashboard/")
            .then(res =>res.json())
            .then(resData =>{
                setData(resData);
            
            // Convert backend Data -> chart format
            if (resData.trend) {
                setCharData(resData.trend);
            } else {
                // fallback demo data
                setCharData([
                    {name: "Week 1", sales: 12000},
                    {name: "Week 2", sales: 15000},
                    {name: "Week 3", sales: 18000},
                ]);
            }
        });
    }, []);

    return (
        <div style={{padding: "30px" }}>
            <h2> Business Dashboard</h2>

            {/* KPI Cards */}
            <div style={{display:"flex", gap:"20px",marginTop:"20px"}}>
                <div className="glass">
                    <h3>Avg Prediction</h3>
                    <p>{data.avg_prediction || 0}</p>
                </div>

                <div className="glass">
                    <h3>Total Queries</h3>
                    <p>{data.total_queries || 0}</p>
                </div>
            </div>

            {/* Chart */}
            <div className="glass glow" style={{marginTop:"30px"}}>
                <h3>Sales Trend</h3>

                <LineChart width={700} height={300} data={charData}>
                    <XAxis dataKey="name" stroke="#94a3b8"/>
                    <YAxis stroke="#94a3b8" />
                    <Tooltip />
                    <CartesianGrid stroke="#1ee293b" />
                    <Line type="monotone" dataKey="sales" stroke="#38bdf8" />
                </LineChart>
            </div>
        </div>
    );
};

export default Dashboard;