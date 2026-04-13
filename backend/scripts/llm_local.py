import torch
from transformers import AutoTokenizer,AutoModelForCausalLM
import os

MODEL_NAME = os.getenv("LLM_MODEL_NAME", "microsoft/phi-2")

device=torch.device("cuda" if torch.cuda.is_available() else "cpu")

print("Loading tokenizer...")
tokenizer=AutoTokenizer.from_pretrained(MODEL_NAME)

print("Loading model...")
model_kwargs = {
    "torch_dtype": torch.float16 if torch.cuda.is_available() else torch.float32
}
if torch.cuda.is_available():
    model_kwargs["device_map"] = "auto"
model=AutoModelForCausalLM.from_pretrained(MODEL_NAME, **model_kwargs)

model.eval()

print("Model loaded successfully.")

def generate_response(prompt,max_new_tokens=96):

    inputs=tokenizer(prompt,return_tensors="pt", truncation=True, max_length=1024).to(device)

    with torch.inference_mode():
        outputs=model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            do_sample=False,
            repetition_penalty=1.12,
            no_repeat_ngram_size=3,
            use_cache=True
        )
    
    response=tokenizer.decode(outputs[0], skip_special_tokens=True)
    return response

if __name__=="__main__":

    prompt="""
    You are a business AI assistant.
    Explain why revenue increased in Q4.
    """
    
    response=generate_response(prompt)
    print("\nGenerated Response:\n")
    print(response)