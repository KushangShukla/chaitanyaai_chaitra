let currentAudio: HTMLAudioElement | null = null;
let highlightInterval: any = null;

/* =========================
   🔊 TEXT TO SPEECH (TTS)
========================= */
export const speak = async (
  text: string,
  onWordChange?: (index: number) => void
) => {
  const apiKey = import.meta.env.VITE_ELEVEN_TTS_API_KEY;

  if (!apiKey) {
    const utterance = new SpeechSynthesisUtterance(text);

    utterance.onboundary=(event:any)=>{
      if(event.name === "word" && onWordChange){
        onWord(Math.floor(event.charIndex / 5)); // crude estimation
      }
    };

    speechSynthesis.speak(utterance);
    return;
  }

  try {
    const settings = JSON.parse(
      localStorage.getItem("chaitra_settings") || "{}"
    );

    const voiceId = settings.voice_id || "21m00Tcm4TlvDq8ikWAM";
    const speed = settings.speed || 1;

    if (currentAudio) {
      currentAudio.pause();
      currentAudio.currentTime = 0;
    }

    if (highlightInterval) clearInterval(highlightInterval);

    const response = await fetch(
      `https://api.elevenlabs.io/v1/text-to-speech/${voiceId}`,
      {
        method: "POST",
        headers: {
          "xi-api-key": apiKey,
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          text,
          model_id: "eleven_multilingual_v2",
        }),
      }
    );

    const blob = await response.blob();
    const url = URL.createObjectURL(blob);

    currentAudio = new Audio(url);
    currentAudio.playbackRate = speed;

    //  WORD HIGHLIGHT SIMULATION
    const words = text.split(" ");
    let index = 0;

    highlightInterval = setInterval(() => {
      if (onWordChange) onWordChange(index);
      index++;
      if (index >= words.length) clearInterval(highlightInterval);
    }, 250); // adjust speed

    currentAudio.play();

  } catch (err) {
    console.error("TTS Error:", err);
  }
};

/* =========================
   ⏹ STOP SPEAK
========================= */
export const stopSpeak = () => {
  if (currentAudio) {
    currentAudio.pause();
    currentAudio.currentTime = 0;
  }

  if (highlightInterval) {
    clearInterval(highlightInterval);
  }
};