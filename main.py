import time
from audio_handler import record_audio_to_text
from ai_handler import chat_with_ai, kezdoszoveg
from document_generator import save_as_word

print("=== Üdvözöl a Resume Whisperer! ===")
print("Indítom a HR interjút...\n")
print(f"🤖 AI: {kezdoszoveg}")

while True:
    user_input = None
    while not user_input:
        user_input = record_audio_to_text()
    
    ai_response = chat_with_ai(user_input)
    
    if "RESUME_GENERATED" in ai_response:
        clean_resume = ai_response.split("RESUME_GENERATED")[-1].strip()
        # Biztonsági tisztítás a markdown jelek ellen
        clean_resume = clean_resume.replace("```markdown", "").replace("```", "").strip()
        
        save_as_word(clean_resume, "generated_resume.docx")
            
        print("\n🤖 AI: Szuper, a cv-d le lett generálva! Nézd meg a generated_resume.docx fájlt a mappában!")
        break
    else:
        print(f"\n🤖 AI: {ai_response}")
    
    time.sleep(1)