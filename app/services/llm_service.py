from anthropic import Anthropic
from app.core.config import ANTHROPIC_API_KEY
import json
import logging
import time

logger = logging.getLogger('app.services.llm_service')

client = Anthropic(api_key=ANTHROPIC_API_KEY)

SYSTEM_PROMPT = """You are Finn, an expert Fintech Assistant embedded in a
financial management platform used by professionals in the Gulf region and Europe.
## Your expertise
You specialise in:
- Personal and corporate financial concepts (budgeting, cash flow, investments)
- Banking products common in GCC and European markets
- Currency exchange, international transfers, and cross-border finance
- Financial regulations relevant to Saudi Arabia and the EU

## Your communication style
- Be concise — financial professionals are busy, get to the point
- Use bullet points and clear structure for complex topics
- Always give a practical example when explaining a concept
- Use numbers and specific figures to illustrate points, not vague language
- When relevant, acknowledge differences between GCC and European financial systems

## Hard boundaries
- Never recommend specific stocks, funds, or investment products
- Never give tax advice for specific situations
- Always recommend a licensed financial advisor for personal financial decisions
- If asked about illegal financial activities (money laundering, fraud), refuse clearly

## Response format
- Keep responses under 200 words unless the topic genuinely requires more
- Use markdown formatting — headers, bullets, bold for key terms
- End complex answers with a one-line summary starting with "Bottom line:"""

# Model Configuration - Centralized so that it can be changed anytime
MAX_TOKENS=1024
MODEL="claude-sonnet-4-5"
TEMPERATURE=0.7


def generate_response(user_message: str, history: list[dict[str, str]] = []) -> str:
    logger.info(
        f"Generating response | "
        f"message_length: {len(user_message)} | "
        f"history_turns: {len(history)} messages"
    )
    start_time = time.time()

    messages = history + [{"role": "user", "content": user_message}]
    try:
        response = client.messages.create(
            model=MODEL,
            max_tokens=MAX_TOKENS,
            system=SYSTEM_PROMPT,
            messages=messages,
            temperature=TEMPERATURE

        )

        duration = time.time() - start_time
        reply = response.content[0].text


        logger.info(
            f"Response generated | "
            f"duration: {duration:.2f}s | "
            f"input_tokens: {response.usage.input_tokens} | "
            f"output_tokens: {response.usage.output_tokens} | "
            f"response_length: {len(reply)}"
        )
        return reply

    except Exception as e:
        duration = time.time() - start_time
        logger.error(
            f"Claude API error | "
            f"duration: {duration:.2f}s | "
            f"error: {str(e)}"
        )
        raise



def generate_streaming_response(user_message: str, history:list[dict[str,str]]):
    logger.info(
        f"Generating streaming response | "
        f"message_length: {len(user_message)} | "
        f"history_turns: {len(history)} messages"
    )

    start_time = time.time()

    messages = history + [{"role": "user", "content": user_message}]

    try:

        with client.messages.stream(
            model=MODEL,
            max_tokens=MAX_TOKENS,
            system=SYSTEM_PROMPT,
            messages=messages,
            temperature=TEMPERATURE
        ) as stream:
            for event in stream:
                if hasattr(event, "delta") and hasattr(event.delta, "text"):
                    text_chunk = event.delta.text
                    yield f"data: {json.dumps({'text': text_chunk})}\n\n"
    

        final_message = stream.get_final_message()
        usage = final_message.usage
        duration = time.time() - start_time

        logger.info(
            f"Streaming response generated | "
            f"duration: {duration:.2f}s | "
            f"input_tokens: {usage.input_tokens} | "
            f"output_tokens: {usage.output_tokens} | "
        )

        yield f"data: {json.dumps({'done': True, 'usage': {'input_tokens': usage.input_tokens, 'output_tokens': usage.output_tokens}})}\n\n"

    except Exception as e:
        logger.error(f"Streaming response error | error: {str(e)}")
        yield f"data: {json.dumps({'error': str(e)})}\n\n"

    