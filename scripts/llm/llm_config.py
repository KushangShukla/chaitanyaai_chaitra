import os
import torch

HAS_CUDA = torch.cuda.is_available()
DEFAULT_MODEL = "microsoft/phi-2" if HAS_CUDA else "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
MODEL_NAME = os.getenv("LLM_MODEL_NAME", DEFAULT_MODEL)

MAX_NEW_TOKENS = int(os.getenv("LLM_MAX_NEW_TOKENS", "96"))
DO_SAMPLE = False
REPETITION_PENALTY = 1.12
NO_REPEAT_NGRAM_SIZE = 3

DEVICE_MAP = "auto" if HAS_CUDA else None
TORCH_DTYPE = torch.float16 if HAS_CUDA else torch.float32