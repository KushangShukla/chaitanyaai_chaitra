import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from .llm_config import *
from .prompt_templates import business_explanation_prompt, rag_prompt

class LLMEngine:

    def __init__(self):
        print("Loading tokenizer...")
        self.tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, use_fast=True)
        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token

        print("Loading model...")
        model_kwargs = {"torch_dtype": TORCH_DTYPE}
        if DEVICE_MAP is not None:
            model_kwargs["device_map"] = DEVICE_MAP
        self.model = AutoModelForCausalLM.from_pretrained(MODEL_NAME, **model_kwargs)
        self.model.eval()

        print("LLM loaded successfully.")

    def generate(self, prompt):
        inputs = self.tokenizer(prompt, return_tensors="pt", truncation=True, max_length=1024)
        inputs = {k: v.to(self.model.device) for k, v in inputs.items()}

        with torch.inference_mode():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=MAX_NEW_TOKENS,
                do_sample=DO_SAMPLE,
                repetition_penalty=REPETITION_PENALTY,
                no_repeat_ngram_size=NO_REPEAT_NGRAM_SIZE,
                use_cache=True,
                eos_token_id=self.tokenizer.eos_token_id,
                pad_token_id=self.tokenizer.eos_token_id,
            )

        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)

        # Remove prompt echo
        response = response.replace(prompt, "").strip()

        # If model echoes instruction blocks, keep content after "Answer:"
        if "Answer:" in response:
            response = response.split("Answer:", 1)[-1].strip()

        # Hard clean only for obvious code artifacts
        stop_tokens = ["def ", "class ", "import ", "```"]

        for token in stop_tokens:
            if token in response:
                response = response.split(token)[0]

        # Clean placeholders that leak from prompt templates
        for placeholder in ["📊 Key Insight:", "📈 Recommendation:", "⚠️ Risk:", "..."]:
            response = response.replace(placeholder, "").strip()

        # Ensure structured output fallback
        if len(response.strip()) < 5:
            return "I could not generate a clean answer this time. Please retry with a slightly more specific question."

        return response.strip()
    
    def generate_business_response(self,question):
        prompt=business_explanation_prompt(question)
        return self.generate(prompt)
    
    def generate_rag_response(self, context, question):
        prompt=rag_prompt(context,question)
        return self.generate(prompt)