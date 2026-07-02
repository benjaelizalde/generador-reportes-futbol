import os

from dotenv import load_dotenv
from groq import Groq

load_dotenv()

MODEL = "llama-3.3-70b-versatile"
MAX_TOKENS = 500


def get_client() -> Groq:
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise RuntimeError(
            "No se encontró GROQ_API_KEY. Configurala en el archivo .env del proyecto."
        )
    return Groq(api_key=api_key)


def generate_cronica(prompt: str, client: Groq | None = None) -> str:
    if client is None:
        client = get_client()

    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=MAX_TOKENS,
    )
    return response.choices[0].message.content
