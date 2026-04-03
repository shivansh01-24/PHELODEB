import os
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "your_openrouter_api_key_here")
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1/chat/completions"

# Model configuration — primary + fallbacks
AI_MODELS = [
    "google/gemma-2-9b-it:free",                # Primary
    "meta-llama/llama-3.1-8b-instruct",         # Fallback 1
    "mistralai/mistral-7b-instruct",            # Fallback 2
]

AI_MODEL = AI_MODELS[0]
JUDGE_MODEL = AI_MODELS[0]

# Token limits
MAX_OPPONENT_TOKENS = 200
MAX_JUDGE_TOKENS = 250
