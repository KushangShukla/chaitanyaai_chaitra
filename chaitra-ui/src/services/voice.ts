//import axios from "axios";

let currentAudio: HTMLAudioElement | null=null;

export const speak=async (text:string) => {
    const apiKey=import.meta.env.VITE_ELEVEN_API_KEY;

    if (currentAudio){
        currentAudio.pause(); //interrupt
    }

    const response=await fetch(
        "https://api.elevenlabs.io/v1/text-to-speech/21m00Tcm4TlvDq8ikWAM",
        {
            method:"POST",
            headers: {
                "xi-api-key":apiKey,
                "Content-Type":"application/json",
            },
            body:JSON.stringify({
            text,
            model_id:"eleven_monolingual_v1",
            })
        },
    );
    const audioBlob=await response.blob();
    const audioUrl=URL.createObjectURL(audioBlob);

    currentAudio=new Audio (audioUrl);
    currentAudio.play();
};