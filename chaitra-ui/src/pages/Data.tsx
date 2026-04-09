import {useState} from "react";

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
                const res=await fetch("http://localhost:8000/upload-csv",{
                    method:"POST",
                    body:formData,
                });
                const data=await res.json();

                if (data.status === "success"){
                    setStatus(
                        'Uploaded: $ {data.table_name} | Rows: ${data.rows}| AutoML Ready'
                    );
                } else {
                    setStatus(data.error || "Upload failed");
                }
            } catch (err){
                console.error(err);
                setStatus("Error uploading file");
            }
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

                {status && <p style={{marginTop:"10px"}}>{status}</p>}
            </div>
        );
};

export default Data;