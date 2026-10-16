import speech_recognition as sr

def record_audio_to_text():
    """Ez a függvény rögzíti a mikrofont, és szöveggé alakítja"""
    recognizer = sr.Recognizer()
    
    recognizer.pause_threshold = 2.5 
    recognizer.dynamic_energy_threshold = False
    recognizer.energy_threshold = 300
    
    with sr.Microphone() as source:
        print("\n🎙️ Kérlek, beszélj most (maximum 2.5 másodperc szünetet tarthatsz, hallgatlak)...")
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