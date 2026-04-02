import axios from "axios";

const ELEVEN_API_KEY=;

export const speak=async (text:string) => {
    const response=await axios.post(
        "https://api.elevenlabs.io/v1/text-to-speech/21m00Tcm4TlvDq8ikWAM",
        {
            text:text,
            model_id:"eleven_monolingual_v1",
        },
        {
            headers: {
                "xi-api-key":ELEVEN_API_KEY,
                "Content-Type":"application/json",
            },
            responseType:"arraybuffer",
        }
    );
    const audioBlob=new Blob ([response.data], {type:"audio/mpeg"});
    const audioUrl=URL.createObjectURL(audioBlob);

    const audio=new Audio (audioUrl);
    audio.play();
};