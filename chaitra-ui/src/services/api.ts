import axios from "axios";

const API= axios.create({
    baseURL: "http://127.0.0.1.8000",
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