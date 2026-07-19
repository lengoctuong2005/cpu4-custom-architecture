# -*- coding: utf-8 -*-
import os
import re
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, KeepTogether, Table, TableStyle, Image as RLImage
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from PIL import Image as PILImage
from svglib.svglib import svg2rlg

# Fonts path on Windows
FONTS_DIR = "C:/Windows/Fonts/"

def register_fonts():
    try:
        # Register Times New Roman for Vietnamese support
        pdfmetrics.registerFont(TTFont('Times', os.path.join(FONTS_DIR, 'times.ttf')))
        pdfmetrics.registerFont(TTFont('Times-Bold', os.path.join(FONTS_DIR, 'timesbd.ttf')))
        pdfmetrics.registerFont(TTFont('Times-Italic', os.path.join(FONTS_DIR, 'timesi.ttf')))
        pdfmetrics.registerFont(TTFont('Times-BoldItalic', os.path.join(FONTS_DIR, 'timesbi.ttf')))
        
        # Register Consolas for Code
        pdfmetrics.registerFont(TTFont('Consolas', os.path.join(FONTS_DIR, 'consola.ttf')))
        pdfmetrics.registerFont(TTFont('Consolas-Bold', os.path.join(FONTS_DIR, 'consolab.ttf')))
        return True
    except Exception as e:
        print("Font registration failed: {}".format(e))
        return False

# Setup Document Template
class NumberedCanvas(object):
    def __init__(self, *args, **kwargs):
        self._saved_page_states = []

    def __call__(self, *args, **kwargs):
        canvas_obj = args[0]
        # Intercept showPage to collect info
        canvas_obj.showPage()
        return self

def add_header_footer(canvas, doc):
    canvas.saveState()
    # Draw header (skip page 1 - cover page)
    if doc.page > 1:
        canvas.setFont('Times-Italic', 9)
        canvas.setFillColor(colors.HexColor('#555555'))
        canvas.drawString(54, 750, "Báo cáo đồ án: Thiết kế bộ vi xử lý CPU 4-bit (TKVM)")
        canvas.setStrokeColor(colors.HexColor('#cccccc'))
        canvas.setLineWidth(0.5)
        canvas.line(54, 742, 558, 742)
        
        # Draw footer
        canvas.line(54, 60, 558, 60)
        canvas.drawString(54, 45, "Trường Đại học Khoa học Tự nhiên - ĐHQG-HCM")
        page_num = str(doc.page)
        canvas.drawRightString(558, 45, "Trang {}".format(page_num))
    canvas.restoreState()

def parse_markdown_to_elements(md_path, styles):
    elements = []
    
    with open(md_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Split into lines
    lines = content.split('\n')
    in_code_block = False
    code_content = []
    
    for line in lines:
        stripped = line.strip()
        if stripped.startswith('<div') or stripped.startswith('</div') or stripped.startswith('<img') or stripped.startswith('<a') or stripped.startswith('</a'):
            continue
        
        # Code block toggle
        if stripped.startswith('```'):
            if in_code_block:
                # End of code block
                code_text = '\n'.join(code_content)
                code_text = code_text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
                elements.append(Paragraph(
                    "<pre>{}</pre>".format(code_text),
                    styles['SourceCode']
                ))
                elements.append(Spacer(1, 8))
                in_code_block = False
                code_content = []
            else:
                in_code_block = True
            continue
            
        if in_code_block:
            code_content.append(line)
            continue

        # Check for image: ![alt](path)
        img_match = re.match(r'^!\[(.*?)\]\((.*?)\)$', stripped)
        if img_match:
            alt_text = img_match.group(1)
            img_path = img_match.group(2)
            
            # Clean path
            if img_path.startswith('file:///clean/'):
                img_path = img_path.replace('file:///clean/', '')
            elif img_path.startswith('file:///'):
                img_path = img_path.replace('file:///', '')
            # Resolve relative paths or absolute paths
            if img_path.startswith('/c:/') or img_path.startswith('/C:/'):
                img_path = img_path[1:]
                
            if not os.path.exists(img_path):
                # Try finding in project root or report_assets or sim
                basename = os.path.basename(img_path)
                candidates = [
                    basename,
                    os.path.join('report_assets', basename),
                    os.path.join('sim', basename)
                ]
                for cand in candidates:
                    if os.path.exists(cand):
                        img_path = cand
                        break
            
            if os.path.exists(img_path):
                if img_path.lower().endswith('.svg'):
                    try:
                        drawing = svg2rlg(img_path)
                        if drawing:
                            # Scale drawing to fit page width (504 pt)
                            max_width = 450.0
                            if drawing.width > max_width:
                                factor = max_width / drawing.width
                                drawing.width = max_width
                                drawing.height = drawing.height * factor
                                drawing.scale(factor, factor)
                            elements.append(Spacer(1, 10))
                            elements.append(drawing)
                            elements.append(Spacer(1, 5))
                            elements.append(Paragraph("<font size='9' color='#555555'><i>Hình: {}</i></font>".format(alt_text), styles['CoverSubtitle']))
                            elements.append(Spacer(1, 10))
                    except Exception as e:
                        print("Failed to convert SVG {}: {}".format(img_path, e))
                else:
                    try:
                        # Load image and scale it
                        im = PILImage.open(img_path)
                        orig_w, orig_h = im.size
                        max_width = 450.0
                        if orig_w > max_width:
                            w = max_width
                            h = orig_h * (max_width / orig_w)
                        else:
                            w = orig_w
                            h = orig_h
                        rl_img = RLImage(img_path, width=w, height=h)
                        elements.append(Spacer(1, 10))
                        elements.append(rl_img)
                        elements.append(Spacer(1, 5))
                        elements.append(Paragraph("<font size='9' color='#555555'><i>Hình: {}</i></font>".format(alt_text), styles['CoverSubtitle']))
                        elements.append(Spacer(1, 10))
                    except Exception as e:
                        print("Failed to load image {}: {}".format(img_path, e))
            else:
                print("Image path not found: {}".format(img_path))
            continue

        # Headers
        if stripped.startswith('# '):
            elements.append(Spacer(1, 15))
            text = stripped[2:]
            elements.append(Paragraph(text, styles['H1']))
            elements.append(Spacer(1, 10))
        elif stripped.startswith('## '):
            elements.append(Spacer(1, 12))
            text = stripped[3:]
            elements.append(Paragraph(text, styles['H2']))
            elements.append(Spacer(1, 8))
        elif stripped.startswith('### '):
            elements.append(Spacer(1, 10))
            text = stripped[4:]
            elements.append(Paragraph(text, styles['H3']))
            elements.append(Spacer(1, 6))
        # Bullet list items
        elif stripped.startswith('* ') or stripped.startswith('- '):
            text = stripped[2:]
            # Replace basic markdown format (bold/italic)
            text = format_inline_markdown(text)
            elements.append(Paragraph("&bull; &nbsp; {}".format(text), styles['BulletText']))
            elements.append(Spacer(1, 4))
        # Horizontal rule
        elif stripped == '---':
            elements.append(Spacer(1, 10))
            # Table representing line
            t = Table([['']], colWidths=[504])
            t.setStyle(TableStyle([
                ('LINEABOVE', (0,0), (-1,-1), 0.5, colors.HexColor('#dddddd')),
                ('BOTTOMPADDING', (0,0), (-1,-1), 0),
                ('TOPPADDING', (0,0), (-1,-1), 0),
            ]))
            elements.append(t)
            elements.append(Spacer(1, 10))
        # Regular text or empty lines
        elif stripped:
            text = format_inline_markdown(line)
            elements.append(Paragraph(text, styles['Body']))
            elements.append(Spacer(1, 6))
            
    return elements

def format_inline_markdown(text):
    # 1. Protect inline code
    code_blocks = []
    def placeholder_code(match):
        code_blocks.append(match.group(1))
        return "PLACEHOLDERCODEBLOCK{}".format(len(code_blocks)-1)
    text = re.sub(r'`(.*?)`', placeholder_code, text)

    # 2. Protect links
    links = []
    def placeholder_link(match):
        links.append((match.group(1), match.group(2)))
        return "PLACEHOLDERLINKBLOCK{}".format(len(links)-1)
    text = re.sub(r'\[(.*?)\]\((.*?)\)', placeholder_link, text)

    # 3. Format bold & italic
    text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)
    text = re.sub(r'__(.*?)__', r'<b>\1</b>', text)
    text = re.sub(r'\*(.*?)\*', r'<i>\1</i>', text)
    text = re.sub(r'_(.*?)_', r'<i>\1</i>', text)

    # 4. Restore links
    for i, (link_text, link_url) in enumerate(links):
        formatted_link_text = format_inline_markdown(link_text)
        if link_url.startswith('http://') or link_url.startswith('https://'):
            text = text.replace("PLACEHOLDERLINKBLOCK{}".format(i), '<a href="{}" color="#0056b3"><u>{}</u></a>'.format(link_url, formatted_link_text))
        else:
            text = text.replace("PLACEHOLDERLINKBLOCK{}".format(i), '<b>{}</b>'.format(formatted_link_text))

    # 5. Restore code blocks
    for i, code_val in enumerate(code_blocks):
        escaped_code = code_val.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        text = text.replace("PLACEHOLDERCODEBLOCK{}".format(i), '<font name="Consolas" size="9.5" color="#a71d5d"><b>{}</b></font>'.format(escaped_code))

    return text

def build_pdf(output_pdf_path, md_path, source_files):
    # Target page width A4: 595.27 x 841.89 pt
    # Margin 54pt (0.75 in) -> Printable area width 504pt (7.0 in)
    doc = SimpleDocTemplate(
        output_pdf_path,
        pagesize=A4,
        leftMargin=54,
        rightMargin=54,
        topMargin=72,
        bottomMargin=72
    )

    styles = getSampleStyleSheet()
    
    # Custom styles
    styles.add(ParagraphStyle(
        'CoverTitle',
        parent=styles['Normal'],
        fontName='Times-Bold',
        fontSize=24,
        leading=30,
        alignment=1, # Center
        textColor=colors.HexColor('#0f2c59'),
        spaceAfter=15
    ))
    
    styles.add(ParagraphStyle(
        'CoverSubtitle',
        parent=styles['Normal'],
        fontName='Times',
        fontSize=14,
        leading=18,
        alignment=1, # Center
        textColor=colors.HexColor('#4a5568'),
        spaceAfter=30
    ))
    
    styles.add(ParagraphStyle(
        'CoverMetadata',
        parent=styles['Normal'],
        fontName='Times',
        fontSize=12,
        leading=18,
        alignment=0, # Left
        textColor=colors.HexColor('#2d3748'),
        leftIndent=120
    ))

    styles.add(ParagraphStyle(
        'H1',
        parent=styles['Normal'],
        fontName='Times-Bold',
        fontSize=18,
        leading=22,
        textColor=colors.HexColor('#0f2c59'),
        spaceBefore=16,
        spaceAfter=10,
        keepWithNext=True
    ))

    styles.add(ParagraphStyle(
        'H2',
        parent=styles['Normal'],
        fontName='Times-Bold',
        fontSize=14,
        leading=18,
        textColor=colors.HexColor('#1d4480'),
        spaceBefore=12,
        spaceAfter=8,
        keepWithNext=True
    ))

    styles.add(ParagraphStyle(
        'H3',
        parent=styles['Normal'],
        fontName='Times-Bold',
        fontSize=11.5,
        leading=15,
        textColor=colors.HexColor('#2d3748'),
        spaceBefore=10,
        spaceAfter=6,
        keepWithNext=True
    ))

    styles.add(ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontName='Times',
        fontSize=11,
        leading=16,
        textColor=colors.HexColor('#1a202c'),
        alignment=4 # Justified
    ))

    styles.add(ParagraphStyle(
        'BulletText',
        parent=styles['Normal'],
        fontName='Times',
        fontSize=11,
        leading=15,
        textColor=colors.HexColor('#1a202c'),
        leftIndent=15
    ))

    styles.add(ParagraphStyle(
        'SourceCode',
        parent=styles['Normal'],
        fontName='Consolas',
        fontSize=8.5,
        leading=11.5,
        textColor=colors.HexColor('#000000'),
        backColor=colors.HexColor('#f6f8fa'),
        borderColor=colors.HexColor('#e1e4e8'),
        borderWidth=0.5,
        borderPadding=6,
        spaceBefore=6,
        spaceAfter=6
    ))

    styles.add(ParagraphStyle(
        'SourceHeader',
        parent=styles['Normal'],
        fontName='Consolas-Bold',
        fontSize=9.5,
        leading=13,
        textColor=colors.HexColor('#ffffff'),
        backColor=colors.HexColor('#24292e'),
        borderPadding=4,
        spaceBefore=10,
        keepWithNext=True
    ))

    story = []

    # 1. Cover Page
    story.append(Spacer(1, 20))
    story.append(Paragraph("<b>ĐẠI HỌC QUỐC GIA THÀNH PHỐ HỒ CHÍ MINH</b>", ParagraphStyle('Uni', fontName='Times-Bold', fontSize=12, alignment=1, textColor=colors.HexColor('#333333'))))
    story.append(Paragraph("<b>TRƯỜNG ĐẠI HỌC KHOA HỌC TỰ NHIÊN</b>", ParagraphStyle('School', fontName='Times-Bold', fontSize=13, alignment=1, textColor=colors.HexColor('#0f2c59'))))
    story.append(Paragraph("<b>KHOA VẬT LÝ - VẬT LÝ KỸ THUẬT</b>", ParagraphStyle('Dept', fontName='Times-Bold', fontSize=12, alignment=1, textColor=colors.HexColor('#1d4480'))))
    story.append(Paragraph("<b>BỘ MÔN VẬT LÝ TIN HỌC / THIẾT KẾ VI MẠCH</b>", ParagraphStyle('SubDept', fontName='Times-Bold', fontSize=11, alignment=1, textColor=colors.HexColor('#555555'))))
    
    # Line
    t = Table([['']], colWidths=[220])
    t.setStyle(TableStyle([
        ('LINEABOVE', (0,0), (-1,-1), 1.2, colors.HexColor('#0f2c59')),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 0),
        ('TOPPADDING', (0,0), (-1,-1), 0),
    ]))
    story.append(Spacer(1, 10))
    story.append(t)
    
    # Logo
    if os.path.exists('logo.png'):
        story.append(Spacer(1, 30))
        story.append(RLImage('logo.png', width=120, height=120))
        
    story.append(Spacer(1, 40))
    story.append(Paragraph("BÁO CÁO ĐỒ ÁN MÔN HỌC", ParagraphStyle('ReportType', fontName='Times-Bold', fontSize=15, alignment=1, textColor=colors.HexColor('#333333'), spaceAfter=15)))
    story.append(Paragraph("THIẾT KẾ BỘ VI XỬ LÝ CPU 4-BIT (TKVM)", ParagraphStyle('Title1', parent=styles['CoverTitle'])))
    story.append(Paragraph("Hệ thống xử lý đơn chu kỳ (Single-Cycle) trên RTL & Layout vật lý", ParagraphStyle('Title2', parent=styles['CoverSubtitle'])))
    
    story.append(Spacer(1, 50))
    
    metadata_text = """
    <b>Sinh viên thực hiện:</b> Lê Ngọc Tường<br/>
    <b>Mã số sinh viên:</b> 22120395<br/>
    <b>Lớp:</b> Thiết kế vi mạch điện tử - HK3/2025-2026<br/>
    <b>Giáo viên hướng dẫn:</b> Ban Giảng huấn Bộ môn Vi mạch<br/>
    <b>Hệ thống thiết kế:</b> Kiến trúc Harvard 4-bit Single-Cycle
    """
    story.append(Paragraph(metadata_text, styles['CoverMetadata']))
    
    story.append(Spacer(1, 50))
    story.append(Paragraph("<i>Thành phố Hồ Chí Minh, Tháng 7 năm 2026</i>", ParagraphStyle('Date', fontName='Times-Italic', fontSize=11, alignment=1, textColor=colors.HexColor('#555555'))))
    story.append(PageBreak())

    # 2. Main Report Content
    report_elements = parse_markdown_to_elements(md_path, styles)
    story.extend(report_elements)

    # 3. Source Code Appendix
    story.append(PageBreak())
    story.append(Paragraph("PHỤ LỤC: MÃ NGUỒN THIẾT KẾ RTL VÀ TESTBENCH", styles['H1']))
    story.append(Spacer(1, 10))
    story.append(Paragraph("Dưới đây là toàn bộ mã nguồn mô tả phần cứng (Verilog RTL) và mã nguồn kiểm thử (Testbench) của CPU 4-bit để phục vụ quá trình tổng hợp và mô phỏng logic.", styles['Body']))
    story.append(Spacer(1, 15))

    for label, filepath in source_files:
        if os.path.exists(filepath):
            story.append(Paragraph("Tệp tin: {}".format(label), styles['SourceHeader']))
            with open(filepath, 'r', encoding='utf-8') as f:
                code_content = f.read()
            # Escape HTML characters
            code_content = code_content.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            story.append(Paragraph("<pre>{}</pre>".format(code_content), styles['SourceCode']))
            story.append(Spacer(1, 12))
        else:
            print("Warning: Source file {} not found.".format(filepath))

    # Build Document
    doc.build(story, onFirstPage=lambda c, d: None, onLaterPages=add_header_footer)

if __name__ == "__main__":
    register_fonts()
    
    md_report_path = "Bao_cao_CPU_4bit.md"
    output_pdf = "Bao_cao_CPU_4bit.pdf"
    
    # List of Verilog source files to include
    rtl_files = [
        ("program_counter.v (Bộ đếm chương trình)", "rtl/program_counter.v"),
        ("instruction_memory.v (Bộ nhớ chỉ lệnh ROM)", "rtl/instruction_memory.v"),
        ("register_file.v (Bộ chứa thanh ghi)", "rtl/register_file.v"),
        ("alu_4bit.v (Khối tính toán ALU)", "rtl/alu_4bit.v"),
        ("data_memory.v (Bộ nhớ dữ liệu RAM)", "rtl/data_memory.v"),
        ("control_unit.v (Bộ điều khiển trung tâm)", "rtl/control_unit.v"),
        ("cpu_top.v (Khối tích hợp CPU Top-level)", "rtl/cpu_top.v"),
        ("tb_cpu_top.v (Kiểm thử hệ thống Testbench)", "tb/tb_cpu_top.v")
    ]
    
    print("Building PDF...")
    build_pdf(output_pdf, md_report_path, rtl_files)
    print("PDF build completed: {}".format(output_pdf))
