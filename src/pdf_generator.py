from fpdf import FPDF
import datetime


def clean_text(text: str) -> str:
    replacements = {
        '\u2014': '-', '\u2013': '-', '\u2018': "'", '\u2019': "'",
        '\u201c': '"', '\u201d': '"', '\u2026': '...', '\u00e9': 'e',
        '\u00e8': 'e', '\u00ea': 'e', '\u00e0': 'a', '\u00e2': 'a',
        '\u00f4': 'o', '\u00fb': 'u', '\u00ee': 'i', '\u00e7': 'c',
        '\u00fc': 'u', '\u00f6': 'o', '\u00e4': 'a', '\u00df': 'ss',
    }
    for orig, repl in replacements.items():
        text = text.replace(orig, repl)
    return text


def parse_sections(report_text: str):
    sections = []
    current_title = None
    current_lines = []
    for line in report_text.split('\n'):
        if line.startswith('## '):
            if current_title is not None:
                sections.append((current_title, '\n'.join(current_lines).strip()))
            current_title = line.replace('## ', '').strip()
            current_lines = []
        else:
            current_lines.append(line)
    if current_title:
        sections.append((current_title, '\n'.join(current_lines).strip()))
    return sections


def generate_pdf(user_query: str, report_text: str, image_urls: list = []) -> bytes:
    pdf = FPDF(orientation='P', unit='mm', format='A4')
    pdf.set_auto_page_break(auto=True, margin=20)
    pdf.add_page()

    # page width usable
    W = 170  # 210 - 20 margins on each side

    # --- HEADER ---
    pdf.set_font('Helvetica', 'I', 7)
    pdf.set_text_color(160, 160, 160)
    pdf.set_xy(20, 8)
    pdf.cell(W, 5, 'Research Assistant  |  AI-Generated Report  |  LLaMA 3.3 & Groq', align='C')
    pdf.set_draw_color(200, 200, 200)
    pdf.set_line_width(0.3)
    pdf.line(20, 14, 190, 14)

    # --- TITLE ---
    pdf.set_xy(20, 20)
    pdf.set_font('Helvetica', 'B', 20)
    pdf.set_text_color(15, 15, 15)
    pdf.multi_cell(W, 9, clean_text(user_query.title()), align='C')

    pdf.set_x(20)
    pdf.set_font('Helvetica', '', 8)
    pdf.set_text_color(130, 130, 130)
    date = datetime.datetime.now().strftime("%B %d, %Y")
    pdf.cell(W, 6, f'AI Research Report  |  {date}  |  Powered by LLaMA 3.3 & Groq', align='C')
    pdf.ln(5)

    # title dividers
    y = pdf.get_y()
    pdf.set_draw_color(15, 15, 15)
    pdf.set_line_width(0.8)
    pdf.line(20, y, 190, y)
    pdf.ln(1.5)
    y = pdf.get_y()
    pdf.set_line_width(0.3)
    pdf.line(20, y, 190, y)
    pdf.ln(8)

    # --- SECTIONS ---
    sections = parse_sections(report_text)

    for title, content in sections:
        is_sources = 'source' in title.lower() or 'reference' in title.lower()

        # section heading
        pdf.set_x(20)
        pdf.set_font('Helvetica', 'B', 10)
        pdf.set_text_color(15, 15, 15)
        pdf.set_fill_color(230, 230, 230)
        pdf.cell(W, 7, '  ' + clean_text(title.upper()), fill=True, ln=True)
        pdf.ln(3)

        # section content
        if is_sources:
            pdf.set_font('Helvetica', '', 8)
            pdf.set_text_color(80, 80, 80)
        else:
            pdf.set_font('Helvetica', '', 10)
            pdf.set_text_color(40, 40, 40)

        for para in content.split('\n\n'):
            para = clean_text(para.strip())
            if not para:
                continue
            pdf.set_x(20)
            pdf.multi_cell(W, 5.5, para)
            pdf.ln(2)

        pdf.ln(4)

    # # --- FOOTER on each page is handled manually ---
    # # add footer to last page
    # pdf.set_y(-15)
    # pdf.set_draw_color(200, 200, 200)
    # pdf.set_line_width(0.3)
    # pdf.line(20, pdf.get_y(), 190, pdf.get_y())
    # pdf.set_font('Helvetica', 'I', 7)
    # pdf.set_text_color(160, 160, 160)
    # pdf.cell(W, 6, f'{date}  |  Page {pdf.page_no()}', align='C')

    return bytes(pdf.output())