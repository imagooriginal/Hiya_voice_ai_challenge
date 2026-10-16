import os
import json
from docx import Document
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_word_with_semantic_mapping(user_data_json, template_path="CVtemplate.docx", output_filename="generated_resume.docx"):
    print("🔄 Sablon szerkezetének szemantikus elemzése...")
    doc = Document(template_path)
    
    paragraphs_to_modify = []
    for p in doc.paragraphs:
        if p.text.strip(): paragraphs_to_modify.append(p)
            
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                for p in cell.paragraphs:
                    if p.text.strip(): paragraphs_to_modify.append(p)
                    
    template_lines = {str(i): p.text.strip() for i, p in enumerate(paragraphs_to_modify)}
    
    prompt = f"""
    You are an intelligent CV formatting engine.
    
    Here is a numbered list of text blocks extracted sequentially from a CV dummy template:
    {json.dumps(template_lines, ensure_ascii=False, indent=2)}
    
    Here is the real user's data:
    {json.dumps(user_data_json, ensure_ascii=False)}
    
    TASK: Analyze the semantic purpose of each numbered line in the template (e.g., Is it the Name? Contact info? A job description? A section header?).
    Then, map the user's real data to the correct line numbers.
    - Replace dummy headers with translated Hungarian headers.
    - Replace dummy descriptions with the user's actual descriptions.
    - If the template has extra slots, return an empty string "" for those line numbers to hide them.
    
    Return a JSON object where the KEYS are the exact string line numbers (e.g., "0", "1", "2") and the VALUES are the new replacement text for that line.
    """
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        response_format={ "type": "json_object" },
        messages=[{"role": "user", "content": prompt}]
    )
    
    replacements = json.loads(response.choices[0].message.content)
    print("✅ AI megértette a sablont! Adatok beillesztése...")
    
    for str_idx, new_text in replacements.items():
        idx = int(str_idx)
        if idx < len(paragraphs_to_modify):
            p = paragraphs_to_modify[idx]
            
            if len(p.runs) > 0:
                style_run = p.runs[0]
                font_name = style_run.font.name
                font_size = style_run.font.size
                bold = style_run.bold
                color = style_run.font.color.rgb if style_run.font.color else None
                
                p.text = str(new_text)
                
                if len(p.runs) > 0:
                    for run in p.runs:
                        run.font.name = font_name
                        run.font.size = font_size
                        run.bold = bold
                        if color: run.font.color.rgb = color
            else:
                p.text = str(new_text)
                
    doc.save(output_filename)