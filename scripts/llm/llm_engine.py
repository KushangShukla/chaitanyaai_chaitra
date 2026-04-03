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

        # dynamic token control
        max_tokens = min(150, len(prompt) // 2 + 50)

        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=max_tokens,   # FIXED
                temperature=0.7,
                top_p=0.9,
                do_sample=True,
                eos_token_id=self.tokenizer.eos_token_id
            )

        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)

        # extract response only
        if "### Response:" in response:
            response = response.split("### Response:")[-1].strip()

        # remove prompt echo
        response = response.replace(prompt, "").strip()

        # remove garbage/code
        for stop_word in ["def ", "class ", "import ", "return "]:
            if stop_word in response:
                response = response.split(stop_word)[0]

        # final length control
        if len(response) > 300:
            response = response[:300] + "..."

        return response.strip()
    
    def generate_business_response(self,question):
        prompt=business_explanation_prompt(question)
        return self.generate(prompt)
    
    def generate_rag_response(self, context, question):
        prompt=rag_prompt(context,question)
        return self.generate(prompt)