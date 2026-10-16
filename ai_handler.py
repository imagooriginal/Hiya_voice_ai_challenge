import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")

if not API_KEY:
    print("❌ Hiba: Nem találom az OPENAI_API_KEY-t a .env fájlban!")
    exit()

client = OpenAI(api_key=API_KEY)

messages = []
kezdoszoveg = "Szia! Örülök, hogy itt vagy. Látom, kiválasztottál egy szép önéletrajz sablont. Kérlek, kezdjük azzal, hogy bemutatkozol, és mesélsz egy kicsit a szakmai hátteredről, miben vagy a legjobb, és milyen nyelven szeretnéd elkészíteni a CV-t! Nyugodtan beszélj hosszan, elkapjuk a fonalat."

def init_ai(template_text):
    """Inicializálja az AI-t a letöltött sablon ismeretében, flow-alapú interjúhoz"""
    global messages
    
    system_prompt = f"""
    Te egy profi, empatikus HR tanácsadó és karrier-coach vagy. A célod egy természetes, gördülékeny hangalapú interjú lebonyolítása magyar nyelven, hogy adatokat gyűjts a felhasználó önéletrajzához.
    
    A FELHASZNÁLÓ ÁLTAL VÁLASZTOTT SABLON:
    Az alábbi szöveget a felhasználó által feltöltött CV sablonból nyertük ki (tele van mintaadatokkal).
    ---
    {template_text}
    ---
    
    AZ INTERJÚ FILOZÓFIÁJA ÉS MÓDSZERE:
    - Flow-élmény: Hagyd, hogy a felhasználó szabadon beszéljen! Tegyél fel nyitott, átfogó kérdéseket (pl. "Mesélj a legmeghatározóbb munkahelyeidről!"), ahelyett, hogy egyesével kérdeznéd ki a részleteket. 
    - Intelligens adatgyűjtés: A fenti sablon alapján te pontosan látod, mire van szükség (pl. van-e hely a sablonban 10 munkahelynek, vagy inkább csak a 2-3 legfontosabbat érdemes kiemelni; milyen elérhetőségeknek van helye). A beszélgetést finoman tereld úgy, hogy a sablon kitöltéséhez szükséges infókat megkapjuk, anélkül, hogy a felhasználót untatnád a sablon korlátaival.
    - Értsd meg a kontextust: Ha a sablonban van 5 különböző kamu email cím, a józan eszeddel tudd, hogy a valóságban egy embernek csak egyet érdemes megadnia az önéletrajzban.
    - Cél: KIZÁRÓLAG azokat az információtípusokat gyűjtsd, amiknek helye van a sablonban.
    
    MŰKÖDÉS:
    Az interjú során minden válaszod egy JSON objektum legyen:
    {{ "status": "interviewing", "message": "A te természetes, emberi válaszod és a beszélgetést továbbvivő kérdésed." }}
    
    Ha úgy érzed, hogy a beszélgetésből kinyerted a sablon kitöltéséhez szükséges összes lényeges információt, zárd le a folyamatot az alábbi JSON struktúrával (az adatokat fordítsd le a felhasználó által kért nyelvre):
    {{
      "status": "RESUME_GENERATED",
      "personal_info": {{"name": "...", "phone": "...", "email": "...", "address": "...", "contact_header": "..."}},
      "summary": {{"header": "...", "text": "..."}},
      "skills": {{"header": "...", "items": ["...", "..."]}},
      "experience": {{"header": "...", "items": [{{"role": "...", "company": "...", "dates": "...", "details": "..."}}]}},
      "education": {{"header": "...", "items": [{{"degree": "...", "institution": "...", "dates": "..."}}]}}
    }}
    """
    
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "assistant", "content": json.dumps({"status": "interviewing", "message": kezdoszoveg})}
    ]

def chat_with_ai(user_text):
    messages.append({"role": "user", "content": user_text})
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        response_format={ "type": "json_object" } 
    )
    
    ai_reply = response.choices[0].message.content
    messages.append({"role": "assistant", "content": ai_reply})
    return ai_reply