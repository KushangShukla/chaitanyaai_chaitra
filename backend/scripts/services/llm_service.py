from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

class LLMService:
    def __init__(self):
        self.model = None
        self.tokenizer = None

    def load(self):
        try:
            self.tokenizer = AutoTokenizer.from_pretrained("microsoft/phi-2")
            self.model = AutoModelForCausalLM.from_pretrained(
                "microsoft/phi-2",
                torch_dtype=torch.float32
            )
            self.model.eval()
            print("✅ phi-2 loaded")
        except Exception as e:
            print(" LLM Load Failed:", e)

    def generate(self, prompt):
        if not self.model:
            return "LLM not available"

        try:
            inputs = self.tokenizer(prompt, return_tensors="pt")
            outputs = self.model.generate(
                **inputs,
                max_length=120,
                do_sample=True,
                temperature=0.7
            )
            return self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        except Exception as e:
            print("LLM Error:", e)
            return "LLM generation failed"


# GLOBAL INSTANCE
llm_service = LLMService()