from openai import OpenAI
from app.core.config import OPENAI_API_KEY


conversation_history = []

client = OpenAI(api_key=OPENAI_API_KEY)

def build_messages(user_message:str)-> str:
    return[{"role":"system","content":system_prompt},*conversation_history,{"role":"user","content":user_message}]


def generate_response(user_message: str) -> str:
    global conversation_history

    messages=build_messages(user_message)

    conversation_history.append({"role": "user", "content": user_message})
    system_prompt = """You are a helpful assistant.Answer the users question with proper detailing with examples. If you don't know the answer, say you don't know. Always be concise and to the point. Avoid unnecessary information."""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        temperature=0.7
    )

    ai_message = response.choices[0].message.content
    conversation_history.append({"role": "assistant", "content": ai_message})
    return ai_message