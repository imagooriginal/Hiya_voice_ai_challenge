"""Generate and synchronously play spoken responses using OpenAI TTS."""

import os
import pygame
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def speak_text(text):
    """Synthesize text with OpenAI and play the resulting audio.

    Speech is written to a temporary MP3 file, loaded by ``pygame``, and played
    synchronously; this function returns after playback completes and the
    temporary file is removed.

    Args:
        text (str): Text to synthesize.

    Raises:
        Exception: If speech synthesis, file writing, mixer initialization, or
            audio playback fails.

    Returns:
        None: This function does not return a value.
    """
    print("🔊 AI beszél...")
    
    # Request synthesized audio before initializing playback.
    response = client.audio.speech.create(
        model="tts-1",
        voice="nova", # Available voices include alloy, echo, fable, onyx, nova, and shimmer.
        input=text
    )
    
    filename = "ai_response.mp3"
    response.stream_to_file(filename)
    
    # pygame reads the generated file and plays it synchronously below.
    pygame.mixer.init()
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()
    
    # Poll playback state so the temporary audio is not removed before playback ends.
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
        
    pygame.mixer.quit()
    
    # Remove the generated audio after successful playback to avoid retaining it.
    if os.path.exists(filename):
        os.remove(filename)