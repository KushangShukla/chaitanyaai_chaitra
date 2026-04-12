import {useState} from "react";
import { getAuthHeaders } from "../services/api";

const Data=()=> {
    const [file,setFile]=useState<any>(null);
    const [status,setStatus]=useState("");

        const handleUpload=async()=>{
            if (!file) return;

            const formData=new FormData();
            formData.append("file",file);

            setStatus("Uploading...");

            try
            {
                const headers=getAuthHeaders();
                const { ["Content-Type"]: _, ...headersWithoutContentType } = headers; //Important for FormData
                const res=await fetch("http://localhost:8000/upload-csv",{
                    method:"POST",
                    headers: headersWithoutContentType,
                    body:formData,
                });
                const data=await res.json();

                if (data.status === "success"){
                    setStatus(
                        `Uploaded: ${data.table_name} | Rows: ${data.rows}| AutoML Ready`
                    );
                } else {
                    setStatus(data.error || "Upload failed");
                }
            } catch (err){
                console.error(err);
                setStatus("Error uploading file");
            }
        };

        const [pdf,setPdf]=useState<any>(null);

        const handlePDFUpload=async()=> {
            if (!pdf) return;

            const formData=new FormData();
            formData.append("file",pdf);

            const res=await fetch ("http://localhost:8000/upload-pdf",{
                method:"POST",
                body:formData,
            });
            const data=await res.json();
            setStatus(data.message || data.error);
        };
        return (
            <div className="glass" 
            style={{padding:"30px",maxWidth:"600px"}}>
                <h2>Upload Dataset</h2>

                <input 
                    type="file"
                    accept=".csv"
                    onChange={(e) => setFile(e.target.files?.[0])}
                />

                <button onClick={handleUpload} style={{marginTop:"10px"}}>
                    Upload & Train AutoML
                </button>

                <h3 style={{marginTop:"20px"}}>Upload PDF for AI knowledge</h3>

                <input 
                    type="file"
                    accept=".pdf"
                    onChange={(e)=> setPdf(e.target.files?.[0])}
                />

                <button onClick={handlePDFUpload}>Upload PDF</button>

                {status && <p style={{marginTop:"10px"}}>{status}</p>}
            </div>
        );
};

export default Data;