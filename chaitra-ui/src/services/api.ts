import axios from "axios";

const API= axios.create({
    baseURL: "http://localhost:8000",
});

export const sendQuery=async(query:string) => {
    try {
        const res=await fetch ("http://127.0.0.1:8000/query",{
            method:"POST",
            headers:{
                "Content-Type":"application/json",
            },
            body:JSON.stringify({query}),
        });

        const data=await res.json();
        
        console.log("API SUCCESS:",data);

        return data;

    } catch(err){
    console.error("API ERROR:",err);   
    throw err;
    }    
};