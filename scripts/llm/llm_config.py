import torch

MODEL_NAME="mistralai/Mistral-7B-Instruct-v0.1"

MAX_NEW_TOKENS=200
TEMPERATURE=0.7
TOP_P=0.9

DEVICE_MAP="auto"
TORCH_DTYPE=torch.float16
LOAD_IN_4BIT=True