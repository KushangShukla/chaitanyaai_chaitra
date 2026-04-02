import axios from "axios";

const API= axios.create({
    baseURL: "http://localhost:8000",
});

export const sendQuery=async(query:string) => {
    try {
        const res=await API.post("/query",{query});
        console.log("API RESPONSE:",res.data); //debug
        return res.data;
    }   catch (err:any) {
        console.error("API ERROR:",err);
        throw err;
    }
};