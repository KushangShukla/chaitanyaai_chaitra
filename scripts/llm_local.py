import torch
from transformers import AutoTokenizer,AutoModelForCausalLM

MODEL_NAME="microsoft/phi-2"

device=torch.device("cuda" if torch.cuda.is_available() else "cpu")

print("Loading tokenizer...")
tokenizer=AutoTokenizer.from_pretrained(MODEL_NAME)

print("Loading model...")
model=AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    torch_dtype=torch.float16,
    device_map="auto"
)

model.eval()

print("Model loaded successfully.")

def generate_response(prompt,max_new_tokens=200):

    inputs=tokenizer(prompt,return_tensors="pt").to(device)

    with torch.no_grad():
        outputs=model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            temperature=0.7,
            top_p=0.9,
            do_sample=True
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