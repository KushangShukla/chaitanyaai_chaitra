import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from .llm_config import *
from .prompt_templates import business_explanation_prompt, rag_prompt

class LLMEngine:

    def __init__ (self):
        print("Loading tokenizer...")
        self.tokenizer=AutoTokenizer.from_pretrained(MODEL_NAME)

        print("Loading model...")
        self.model=AutoModelForCausalLM.from_pretrained(
            MODEL_NAME,
            device_map=DEVICE_MAP,
            torch_dtype=TORCH_DTYPE
        )

        print("LLM loaded successfully.")

    def generate(self,prompt):
        
        inputs=self.tokenizer(prompt,return_tensors="pt").to(self.model.device)

        with torch.no_grad():
            outputs=self.model.generate(
                **inputs,
                max_new_tokens=MAX_NEW_TOKENS,
                temperature=TEMPERATURE,
                top_p=TOP_P,
                do_sample=True
            )

        response=self.tokenizer.decode(outputs[0],skip_special_tokens=True)
        response=response.split("### Response:")[-1].strip()
        return response
    
    def generate_business_response(self,question):
        prompt=business_explanation_prompt(question)
        return self.generate(prompt)
    
    def generate_rag_response(self, context, question):
        prompt=rag_prompt(context,question)
        return self.generate(prompt)