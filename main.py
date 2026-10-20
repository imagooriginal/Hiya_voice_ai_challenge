"""Run the voice-based interview and generate a resume from the conversation.

The script greets the user, repeatedly records spoken input, sends each response
to the AI interviewer, and saves the generated resume when the completion marker
is returned.
"""

import time
from audio_handler import record_audio_to_text
from ai_handler import chat_with_ai, kezdoszoveg
from document_generator import save_as_word
from voice_output import speak_text

if __name__ == "__main__":
    print("=== Üdvözöl a Resume Whisperer! ===")
    print("Indítom a HR interjút...\n")

    kezdoszoveg = "Szia! Én vagyok a CV asszisztensed. Kérlek, mondd el a neved, és hogy milyen nyelven szeretnéd elkészíteni az önéletrajzodat!"
    print(f"🤖 AI: {kezdoszoveg}")
    speak_text(kezdoszoveg)

    while True:
        user_input = None
        while not user_input:
            user_input = record_audio_to_text()
        
        ai_response = chat_with_ai(user_input)
        
        if "RESUME_GENERATED" in ai_response:
            clean_resume = ai_response.split("RESUME_GENERATED")[-1].strip()
            # Remove optional Markdown code fences before passing the resume to Word.
            clean_resume = clean_resume.replace("```markdown", "").replace("```", "").strip()
            
            save_as_word(clean_resume, "generated_resume.docx")

            zaro_szoveg = "Szuper, a cv-d le lett generálva! Nézd meg a generated_resume.docx fájlt a mappában!"
            print(f"\n🤖 AI: {zaro_szoveg}")
            speak_text(zaro_szoveg)
            break
        else:
            print(f"\n🤖 AI: {ai_response}")
            speak_text(ai_response)
        
        time.sleep(1)