import os
import pygame
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def speak_text(text):
    """Az OpenAI segítségével hanggá alakítja és lejátssza a szöveget."""
    print("🔊 AI beszél...")
    
    # Hanggá alakítás az OpenAI modellel
    response = client.audio.speech.create(
        model="tts-1",
        voice="nova", # Elérhető hangok: alloy, echo, fable, onyx, nova, shimmer
        input=text
    )
    
    filename = "ai_response.mp3"
    response.stream_to_file(filename)
    
    # Lejátszás a pygame segítségével
    pygame.mixer.init()
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()
    
    # Várakozás, amíg befejezi a beszédet
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
        
    pygame.mixer.quit()
    
    # Fájl törlése, hogy ne foglalja a helyet
    if os.path.exists(filename):
        os.remove(filename)