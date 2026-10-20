# Resume Whisperer - Hiya Voice AI Challenge

**Track:** Productivity & Accessibility  
**Builder:** Zoltán Sebestyén Gonda

### What I built
I built the "Resume Whisperer", an interactive, voice-driven career coach. It runs locally in the terminal, initiates a conversation with the user, asks professional interview questions, and dynamically generates a perfectly formatted, multilingual Word (.docx) resume. 

### Who it is for
This tool is built for two distinct groups:
1. **Engineers and Students (Productivity):** People who hate formatting documents, or struggle to translate their daily coding tasks into HR-friendly "corporate" language.
2. **People with Writing Difficulties (Accessibility):** Individuals who have dyslexia, lack advanced typing skills, are visually impaired, or are non-native English speakers applying for international jobs. 

### What problem it solves
Creating a resume is traditionally a high-friction task. The Resume Whisperer completely removes this friction by solving several key pain points:
*   **Zero Typing Required:** Users can build a resume entirely hands-free (which also makes it perfect for future mobile adaptations).
*   **Natural Storytelling:** For most people, it is fundamentally easier to talk about their achievements than to write them down. 
*   **No "Corporate Jargon" Needed:** The user can speak casually; the AI automatically translates everyday, unstructured speech into professional, HR-approved phrasing.
*   **Automated Guidance:** Users don't need to research what information a CV requires; the AI actively guides them by asking the right questions.
*   **AI Enhancement (STAR method):** The assistant actively supplements the resume by asking probing questions (e.g., *"What specific frameworks did you use, and what was the performance impact?"*) to ensure high-quality, data-driven content.
*   **Instant Localization:** Users can speak in their native language, and the AI translates the final CV into the desired output language automatically.
*   **Zero Formatting Hassle:** The output is a ready-to-use `.docx` file, bypassing the clipboard and manual design work completely.
*   **Accessibility:** It empowers visually impaired users to create professional resumes completely independently through simple voice interactions.

### What I would do next with more time
1. **Local Whisper Model:** Currently, the prototype uses the Google Web Speech API for quick STT. I would integrate OpenAI's Whisper model locally (via `whisper.cpp`) to handle stuttering, background noise, and thick accents more reliably without internet latency.
2. **Interview Prep Mode:** I would expand the conversational AI's capabilities to not only write the CV but also conduct mock technical and HR interviews to prepare the user for the real thing.
3. **Direct PDF/FlowCV Export:** Expand the output generation to automatically compile the document into a styled PDF or export the JSON directly into a resume-building API.
4. **Scalable Template Database:** I would implement a robust database architecture to store various professional CV templates. This scalable solution would allow users to select their preferred resume style, layout, or industry-specific format before the voice interview begins.