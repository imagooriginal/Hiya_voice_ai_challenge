"""Manage the conversational AI client and its in-memory interview context.

The conversation history is retained in ``messages`` for the lifetime of this
module so each request can use the prior interview turns as context.
"""

import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")

if not API_KEY:
    print("❌ Hiba: Nem találom az OPENAI_API_KEY-t a .env fájlban!")
    exit()

client = OpenAI(api_key=API_KEY)

system_prompt = """
You are a friendly, conversational HR assistant and career coach.

CRITICAL RULES:
1. INTERVIEW LANGUAGE: The chat/conversation itself MUST ALWAYS BE IN HUNGARIAN. Keep questions and reactions natural, short, and polite.
2. NO NICKNAMES OR FAKE NAMES: NEVER invent nicknames (e.g. do NOT say 'Tóni', 'László', etc.). Use the exact full name provided by the user (e.g. 'Gonda Zoltán').
3. NO INTERROGATION: Do not ask for phone, email, or address.
4. ONE TOPIC PER TURN: React briefly in Hungarian (1-2 sentences), then ask about one topic (Education -> Work Experience -> Skills/Hobbies).
5. TRACK TARGET CV LANGUAGE: In the very first turn, the user specifies the target language for the resume (e.g. English). YOU MUST REMEMBER THIS LANGUAGE FOR THE FINAL OUTPUT!

FINAL GENERATION RULES (CRITICAL):
- When you have enough details, conclude the chat and generate the resume.
- Start your final response with the exact keyword: RESUME_GENERATED
- If the user requested ENGLISH for the resume, the ENTIRE generated resume (every heading, summary, job description, bullet point) MUST BE 100% IN ENGLISH! No Hungarian words in the English resume.
- Use this EXACT format:

RESUME_GENERATED
[BAL_OSZLOP]
# [User's Exact Full Name]
## Contact
- Phone: [Phone number]
- Email: [Email address]
- Address: [Address]
## Skills
- [Skill 1]
- [Skill 2]

[JOBB_OSZLOP]
## Professional Summary
[A 2-3 sentence authentic summary highlighting their education and experience in the TARGET LANGUAGE]
## Experience
- **[Role/Position]**, [Company/University] (Dates)
  [Short description of tasks in TARGET LANGUAGE]
## Education
- **[Degree/Program]**, [Institution] (Dates)
"""

kezdoszoveg = "Szia! Egy többnyelvű AI karrier-coach vagyok. Első lépésként kérlek mondd el a teljes nevedet, és hogy milyen nyelven szeretnéd megkapni a kész önéletrajzodat!"

messages = [
    {"role": "system", "content": system_prompt},
    {"role": "assistant", "content": kezdoszoveg}
]

# Keep both sides of every turn so subsequent requests retain the interview context.
def chat_with_ai(user_text):
    """Send a user turn to the AI and append the resulting turn to the context.

    Args:
        user_text (str): The user's latest interview response.

    Returns:
        Optional[str]: The assistant's response text, or ``None`` if the
            response has no message content.

    Raises:
        Exception: If the OpenAI client cannot create the completion.
    """
    messages.append({"role": "user", "content": user_text})
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages
    )
    ai_reply = response.choices[0].message.content
    messages.append({"role": "assistant", "content": ai_reply})
    return ai_reply