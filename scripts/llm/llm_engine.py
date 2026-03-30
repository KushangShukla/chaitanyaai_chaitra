import torch
from transformers import AutoTokenizer, AutoModelForCausalLM,BitsAndBytesConfig
from .llm_config import *
from .prompt_templates import business_explanation_prompt, rag_prompt

class LLMEngine:

    def __init__ (self):
        print("Loading tokenizer...")
        self.tokenizer=AutoTokenizer.from_pretrained(MODEL_NAME)

        print("Loading model...")
        bnb_config=BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_compute_dtype=torch.float16,
            bnb_4bit_use_double_quant=True,
            bnb_4bit_quant_type="nf4"
        )

        self.model=AutoModelForCausalLM.from_pretrained(
            MODEL_NAME,
            device_map="auto",
            quantization_config=bnb_config
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
        
        # Remove prompt echo
        response=response.replace(prompt, "").strip()

        # Remove code contamination
        for stop_word in ["return","def","import","class"]:
            if stop_word in response:
                response=response.split(stop_word)[0]
        return response.strip()
    
    def generate_business_response(self,question):
        prompt=business_explanation_prompt(question)
        return self.generate(prompt)
    
    def generate_rag_response(self, context, question):
        prompt=rag_prompt(context,question)
        return self.generate(prompt)