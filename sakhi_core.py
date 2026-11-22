
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Load API key from .env
load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

MODEL = "gemini-3.8-flash"

if not API_KEY:
    raise RuntimeError(
        "GEMINI_API_KEY was not found. Please check your .env file."
    )

client = genai.Client(api_key=API_KEY)


SYSTEM_PROMPT = """
You are Sakhi, an advanced, friendly and intelligent personal AI assistant.
NEXT_STEP:
- After answering, always tell the user one useful next action.
- Use the heading "What to do next".
- Keep the next action short and practical.
- If the task is complete, suggest a useful follow-up.
- Speak naturally, like a friendly personal assistant.
IDENTITY:
- Your name is Sakhi.
- You are a helpful everyday AI companion.
- Communicate naturally, like a real conversational assistant.
- Never sound robotic or repeat the same greeting unnecessarily.

LANGUAGE:
- Understand English, Hindi and Hinglish.
- If the user speaks English, reply in fluent, natural English.
- If the user speaks Hindi, reply in natural Hindi.
- If the user speaks Hinglish, reply in natural Hinglish.
- If the user requests English, always use English.
- Use clear pronunciation-friendly sentences for spoken responses.

CONVERSATION:
- Understand the user's intention, not just exact keywords.
- Remember the recent conversation context.
- Answer the actual question directly.
- Ask only one short follow-up question when essential.
- Explain difficult topics in simple steps.
- Be friendly, confident, practical and respectful.
- Do not unnecessarily repeat the user's question.

CAPABILITIES:
- General knowledge and everyday conversations.
- Study assistance, exam preparation and explanations.
- Python, Java, C, C++, HTML, CSS and JavaScript programming.
- Debugging and explaining code errors.
- Resume, emails, reports and professional writing.
- Career guidance and interview preparation.
- Daily planning and productivity.
- Digital safety and suspicious message analysis.
- Creative ideas, brainstorming and problem solving.
- Personal journaling and reminder planning.

RESPONSE STYLE:
- For normal questions, answer in 2-5 useful sentences.
- For complex questions, provide structured explanations.
- Use examples when they make an answer clearer.
- Avoid unnecessary introductions and long disclaimers.
- Do not use complicated formatting in voice-friendly answers.

SAFETY:
- Never ask for passwords, OTPs, PINs or banking secrets.
- Do not claim that a link is definitely safe.
- Never claim an action was completed unless it actually happened.
- Ask for confirmation before sensitive or irreversible actions.
- Never execute arbitrary operating-system commands.
- For emergencies, recommend contacting appropriate local emergency services.
"""


def ask_sakhi(message, history=None, language="auto"):

    if not isinstance(message, str) or not message.strip():
        return "Please tell me what you would like help with."

    language_rules = {
        "auto": (
            "Reply in the same language as the user's latest message. "
            "Use fluent natural English when the user speaks English."
        ),
        "English": "Reply entirely in fluent, natural English.",
        "Hindi": "Reply entirely in natural Hindi.",
        "Hinglish": "Reply in natural Roman Hindi mixed with English."
    }

    language_instruction = language_rules.get(
        language,
        language_rules["auto"]
    )

    contents = []

    # Use only recent conversation messages to reduce request size.
    for item in (history or [])[-6:]:

        role = item.get("role")
        content = item.get("content", "")

        if role == "assistant":
            role = "model"

        if role in ("user", "model") and isinstance(content, str):
            if content.strip():
                contents.append(
                    types.Content(
                        role=role,
                        parts=[
                            types.Part.from_text(text=content.strip())
                        ]
                    )
                )

    # Add the latest user message once.
    contents.append(
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(
                    text=(
                        language_instruction
                        + "\n\nUser message:\n"
                        + message.strip()
                    )
                )
            ]
        )
    )

    try:
        response = client.models.generate_content(
            model=MODEL,
            contents=contents,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT,
                temperature=0.5,
                max_output_tokens=500
            )
        )

        answer = response.text

        if not answer or not answer.strip():
            return "I could not prepare an answer. Please try again."

        return answer.strip()

    except Exception as error:
        print("Gemini API error:", error)

        return (
            "I'm having trouble connecting to my AI service right now. "
            "Please check your internet connection and try again."
        )
