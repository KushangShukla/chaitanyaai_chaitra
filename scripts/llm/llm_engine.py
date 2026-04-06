import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from .llm_config import *
from .prompt_templates import business_explanation_prompt, rag_prompt

class LLMEngine:

    def __init__(self):
        print("Loading tokenizer...")
        self.tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

        print("Loading model...")
        self.model = AutoModelForCausalLM.from_pretrained(
            MODEL_NAME,
            device_map=DEVICE_MAP,
            torch_dtype=TORCH_DTYPE
        )

        print("LLM loaded successfully.")

    def generate(self, prompt):
    
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.model.device)

        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=200,
                temperature=0.7,
                top_p=0.9,
                do_sample=True,
                eos_token_id=self.tokenizer.eos_token_id
            )

        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)

        #  Remove prompt echo
        response = response.replace(prompt, "").strip()

        #  HARD CLEAN (IMPORTANT)
        stop_tokens = ["def ", "class ", "import ", "return ", "if ", "#", "```"]

        for token in stop_tokens:
            if token in response:
                response = response.split(token)[0]

        #  Ensure structured output fallback
        if len(response.strip()) < 5:
            return "I can help with business insights, predictions, and analysis. Please try rephrasing your question."

        return response.strip()
    
    def generate_business_response(self,question):
        prompt=business_explanation_prompt(question)
        return self.generate(prompt)
    
    def generate_rag_response(self, context, question):
        prompt=rag_prompt(context,question)
        return self.generate(prompt)