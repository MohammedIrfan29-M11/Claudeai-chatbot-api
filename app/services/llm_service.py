from anthropic import Anthropic
from app.core.config import ANTHROPIC_API_KEY

client = Anthropic(api_key=ANTHROPIC_API_KEY)

SYSTEM_PROMPT = """You are a helpful FinTech assistant for a financial platform.
Help users understand their transactions, budgets, and general financial concepts.
Be concise and clear. Never give specific investment advice.
If a question needs a licensed financial advisor, say so."""

def generate_response(user_message: str, history: list[dict[str, str]] = []) -> str:
    """user_message: The latest message from the user
    history: A list of previous ("role":"user/assistant", "content": message) sent from client. We dont store it in the server anymore."""
    messages = history + [{"role": "user", "content": user_message}]
    response = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=1024,
        system=SYSTEM_PROMPT,
        messages=messages

    )
    return response.content[0].text
