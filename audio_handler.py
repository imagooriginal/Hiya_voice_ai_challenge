"""Capture spoken Hungarian input and convert it to text."""

import speech_recognition as sr

def record_audio_to_text():
    """Record microphone audio and transcribe it as Hungarian text.

    Ambient noise is sampled before recording. Listening continues until speech
    is detected, and a pause of ``pause_threshold`` seconds ends the utterance.

    Args:
        None.

    Returns:
        Optional[str]: The recognized text, or ``None`` if recording or
            transcription fails.
    """
    recognizer = sr.Recognizer()
    
    # Use a fixed energy threshold after calibration; end an utterance after 2.5 s of silence.
    recognizer.pause_threshold = 2.5 
    recognizer.dynamic_energy_threshold = False
    recognizer.energy_threshold = 300
    
    with sr.Microphone() as source:
        print("\n🎙️ Kérlek, beszélj most (maximum 2.5 másodperc szünetet tarthatsz, hallgatlak)...")
        # Calibrate to the current room before applying the configured fixed threshold.
        recognizer.adjust_for_ambient_noise(source, duration=1) 
        
        try:
            audio = recognizer.listen(source, timeout=None)
            print("⏳ Feldolgozás...")
            text = recognizer.recognize_google(audio, language="hu-HU")
            print(f"✅ Te: {text}")
            return text
        except Exception:
            print("❌ Nem hallottam tisztán, kérlek ismételd meg!")
            return None