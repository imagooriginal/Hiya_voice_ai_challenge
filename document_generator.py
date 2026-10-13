from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.shared import OxmlElement
from docx.oxml.ns import qn

def set_cell_background(cell, fill_color):
    """Fejlett XML trükk a sötét bal oszlop hátteréhez (Word OXML)"""
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), fill_color)
    tcPr.append(shd)

def _add_formatted_text(paragraph, text, font_color=None):
    """Félkövér szövegek és egyedi betűszínek (pl. fehér a fekete háttéren)"""
    parts = text.split('**')
    for i, part in enumerate(parts):
        run = paragraph.add_run(part)
        if font_color:
            run.font.color.rgb = font_color
        if i % 2 != 0:
            run.bold = True

def save_as_word(text, filename="generated_resume.docx"):
    doc = Document()
    
    # 1. Margók nullázása a modern megjelenéshez
    for section in doc.sections:
        section.top_margin = Cm(1.0)
        section.bottom_margin = Cm(1.0)
        section.left_margin = Cm(1.0)
        section.right_margin = Cm(1.0)
        
    # 2. Szöveg szétvágása a két oszlopra
    left_text = ""
    right_text = ""
    if "[JOBB_OSZLOP]" in text:
        parts = text.split("[JOBB_OSZLOP]")
        left_text = parts[0].replace("[BAL_OSZLOP]", "").strip()
        right_text = parts[1].strip()
    else:
        left_text = text # Biztonsági tartalék
        
    # 3. Kétoszlopos táblázat létrehozása
    table = doc.add_table(rows=1, cols=2)
    table.autofit = False
    
    cell_left = table.cell(0, 0)
    cell_right = table.cell(0, 1)
    
    # Oszlopszélességek beállítása (~35% bal, 65% jobb)
    cell_left.width = Cm(6.5)
    cell_right.width = Cm(12.5)
    
    # BAL OSZLOP SÖTÉTRE FESTÉSE (#333333 szürke)
    set_cell_background(cell_left, '333333')
    
    def write_to_cell(md_text, cell, is_left=False):
        # Bal oldalon FEHÉR, jobb oldalon FEKETE betűk
        text_color = RGBColor(255, 255, 255) if is_left else RGBColor(0, 0, 0)
        
        if is_left:
            # Fénykép placeholder a bal oszlop tetején
            p = cell.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            run = p.add_run("\n[ 📷 FÉNYKÉP ]\n(Kattints ide)\n\n")
            run.font.color.rgb = text_color
            run.bold = True
            
        lines = md_text.split('\n')
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            if line.startswith('# '): # Név
                p = cell.add_paragraph()
                r = p.add_run(line.replace('# ', '').upper())
                r.bold = True
                r.font.size = Pt(16)
                r.font.color.rgb = text_color
                p.paragraph_format.space_before = Pt(12)
                p.paragraph_format.space_after = Pt(12)
            elif line.startswith('## '): # Szekció címek
                p = cell.add_paragraph()
                r = p.add_run(line.replace('## ', '').upper())
                r.bold = True
                r.font.size = Pt(12)
                r.font.color.rgb = text_color
                p.paragraph_format.space_before = Pt(10)
            elif line.startswith('- ') or line.startswith('* '): # Listák
                p = cell.add_paragraph()
                _add_formatted_text(p, "• " + line[2:], font_color=text_color)
                p.paragraph_format.left_indent = Cm(0.5) # Behúzás a pöttyöknek
            else: # Sima szöveg (pl. Bemutatkozás)
                p = cell.add_paragraph()
                _add_formatted_text(p, line, font_color=text_color)
                
    # Szövegek beírása a cellákba
    write_to_cell(left_text, cell_left, is_left=True)
    write_to_cell(right_text, cell_right, is_left=False)
    
    doc.save(filename)