import os
import requests


OLLAMA_URL = os.getenv(
    "OLLAMA_URL",
    "http://localhost:11434/api/generate"
)

MODEL_NAME = "llama3.2"


def generate_response(prompt: str) -> str:
    """
    Send a prompt to Llama 3.2 through Ollama.

    Locally:
        uses localhost:11434

    In Docker:
        OLLAMA_URL is supplied as an environment variable.
    """

    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False
    }

    response = requests.post(
        OLLAMA_URL,
        json=payload,
        timeout=120
    )

    response.raise_for_status()

    return response.json()["response"]