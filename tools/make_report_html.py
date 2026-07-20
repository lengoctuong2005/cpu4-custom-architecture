# -*- coding: utf-8 -*-
import os
import re
import base64
import markdown
from markdown.extensions.toc import TocExtension

def get_base64_image(img_path):
    if os.path.exists(img_path):
        with open(img_path, 'rb') as f:
            data = f.read()
        ext = os.path.splitext(img_path)[1][1:]
        b64 = base64.b64encode(data).decode('utf-8')
        return 'data:image/{};base64,{}'.format(ext, b64)
    return ''

def build_html():
    md_path = 'Bao_cao_CPU_4bit.md'
    html_path = 'Bao_cao_CPU_4bit.html'
    
    if not os.path.exists(md_path):
        print("MD file not found!")
        return
        
    with open(md_path, 'r', encoding='utf-8') as f:
        md_content = f.read()
        
    # Translate links like file:///c:/... to local relative links for web presentation
    # Replace absolute file paths with relative paths
    md_content = md_content.replace('file:///c:/HK3-25-26/TKVM/sim/', 'sim/')
    md_content = md_content.replace('file:///c:/HK3-25-26/TKVM/report_assets/', 'report_assets/')
    md_content = md_content.replace('file:///c:/HK3-25-26/TKVM/logo.png', 'logo.png')
    md_content = md_content.replace('file:///c:/HK3-25-26/TKVM/anhGDS.jpg', 'anhGDS.jpg')
    md_content = md_content.replace('file:///c:/HK3-25-26/TKVM/cpu_top_schematic.svg', 'cpu_top_schematic.svg')
    md_content = md_content.replace('file:///c:/HK3-25-26/TKVM/', './')

    # Convert markdown to HTML
    md = markdown.Markdown(extensions=[
        'fenced_code',
        'tables',
        TocExtension(permalink=True)
    ])
    html_body = md.convert(md_content)
    
    # Load school logo as base64
    logo_base64 = get_base64_image('logo.png')
    if not logo_base64:
        logo_base64 = 'logo.png' # Fallback
        
    # Read Verilog source code to display in collapsible sections
    sources = [
        ("program_counter.v", "rtl/program_counter.v"),
        ("instruction_memory.v", "rtl/instruction_memory.v"),
        ("register_file.v", "rtl/register_file.v"),
        ("alu_4bit.v", "rtl/alu_4bit.v"),
        ("data_memory.v", "rtl/data_memory.v"),
        ("control_unit.v", "rtl/control_unit.v"),
        ("cpu_top.v", "rtl/cpu_top.v"),
        ("tb_cpu_top.v", "tb/tb_cpu_top.v")
    ]
    
    code_sections = ""
    for label, filepath in sources:
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as sf:
                code = sf.read()
            code_escaped = code.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            code_sections += """
            <details class="code-details">
                <summary><b>{}</b> <span class="file-path">({})</span></summary>
                <pre><code class="language-verilog">{}</code></pre>
            </details>
            """.format(label, filepath, code_escaped)
            
    # Premium CSS & HTML Template
    template = """<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Báo cáo đồ án: Thiết kế bộ vi xử lý CPU 4-bit (TKVM)</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Fira+Code:wght@400;500;600&display=swap" rel="stylesheet">
    <style>
        :root {{
            --primary: #0f2c59;
            --primary-light: #1d4480;
            --secondary: #319795;
            --bg-main: #f8fafc;
            --bg-card: #ffffff;
            --text-main: #1e293b;
            --text-muted: #64748b;
            --border: #e2e8f0;
            --code-bg: #f1f5f9;
        }}
        
        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }}
        
        body {{
            font-family: 'Inter', system-ui, -apple-system, sans-serif;
            background-color: var(--bg-main);
            color: var(--text-main);
            line-height: 1.6;
            padding-bottom: 60px;
        }}
        
        /* Header style */
        .top-header {{
            background: linear-gradient(135deg, var(--primary) 0%, var(--primary-light) 100%);
            color: white;
            padding: 20px 0;
            text-align: center;
            border-bottom: 4px solid var(--secondary);
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        }}
        
        .header-container {{
            max-width: 1200px;
            margin: 0 auto;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 20px;
            padding: 0 20px;
            flex-wrap: wrap;
        }}
        
        .school-logo {{
            width: 80px;
            height: auto;
            filter: drop-shadow(0 2px 4px rgba(0,0,0,0.2));
        }}
        
        .header-text h1 {{
            font-size: 1.25rem;
            font-weight: 700;
            letter-spacing: 0.5px;
        }}
        
        .header-text h2 {{
            font-size: 0.95rem;
            font-weight: 500;
            color: #cbd5e1;
            margin-top: 4px;
        }}
        
        /* Main Layout */
        .container {{
            max-width: 1200px;
            margin: 40px auto 0;
            display: grid;
            grid-template-columns: 280px 1fr;
            gap: 30px;
            padding: 0 20px;
        }}
        
        @media (max-width: 900px) {{
            .container {{
                grid-template-columns: 1fr;
            }}
            .sidebar {{
                display: none;
            }}
        }}
        
        /* Sidebar (TOC) */
        .sidebar {{
            position: sticky;
            top: 40px;
            height: fit-content;
            background: var(--bg-card);
            border-radius: 12px;
            border: 1px solid var(--border);
            padding: 20px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        }}
        
        .sidebar h3 {{
            font-size: 0.9rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            color: var(--primary);
            margin-bottom: 15px;
            border-bottom: 2px solid var(--border);
            padding-bottom: 8px;
        }}
        
        .sidebar ul {{
            list-style: none;
        }}
        
        .sidebar li {{
            margin-bottom: 10px;
        }}
        
        .sidebar a {{
            color: var(--text-muted);
            text-decoration: none;
            font-size: 0.9rem;
            font-weight: 500;
            transition: color 0.2s;
        }}
        
        .sidebar a:hover {{
            color: var(--secondary);
        }}
        
        /* Cover Card */
        .cover-card {{
            background: var(--bg-card);
            border-radius: 16px;
            border: 1px solid var(--border);
            padding: 40px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
            margin-bottom: 30px;
            text-align: center;
            position: relative;
            overflow: hidden;
        }}
        
        .cover-card::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 6px;
            background: linear-gradient(90deg, var(--primary) 0%, var(--secondary) 100%);
        }}
        
        .cover-title {{
            font-size: 2rem;
            font-weight: 800;
            color: var(--primary);
            margin: 20px 0 10px;
            line-height: 1.3;
        }}
        
        .cover-subtitle {{
            font-size: 1.15rem;
            color: var(--text-muted);
            margin-bottom: 30px;
        }}
        
        .metadata-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
            gap: 20px;
            max-width: 800px;
            margin: 0 auto;
            text-align: left;
            background: var(--bg-main);
            padding: 25px;
            border-radius: 12px;
            border: 1px solid var(--border);
        }}
        
        .metadata-item h4 {{
            font-size: 0.8rem;
            font-weight: 700;
            text-transform: uppercase;
            color: var(--text-muted);
            margin-bottom: 4px;
        }}
        
        .metadata-item p {{
            font-size: 0.95rem;
            font-weight: 600;
            color: var(--text-main);
        }}
        
        .action-buttons {{
            margin-top: 30px;
            display: flex;
            justify-content: center;
            gap: 15px;
            flex-wrap: wrap;
        }}
        
        .btn {{
            display: inline-flex;
            align-items: center;
            padding: 10px 20px;
            border-radius: 8px;
            font-weight: 600;
            font-size: 0.9rem;
            text-decoration: none;
            transition: all 0.2s;
            cursor: pointer;
        }}
        
        .btn-primary {{
            background-color: var(--primary);
            color: white;
        }}
        
        .btn-primary:hover {{
            background-color: var(--primary-light);
            transform: translateY(-1px);
        }}
        
        .btn-outline {{
            border: 1px solid var(--primary);
            color: var(--primary);
            background-color: transparent;
        }}
        
        .btn-outline:hover {{
            background-color: #f1f5f9;
            transform: translateY(-1px);
        }}
        
        /* Report Content */
        .report-body {{
            background: var(--bg-card);
            border-radius: 16px;
            border: 1px solid var(--border);
            padding: 40px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        }}
        
        .report-body h2 {{
            font-size: 1.5rem;
            font-weight: 700;
            color: var(--primary);
            margin-top: 35px;
            margin-bottom: 15px;
            border-bottom: 2px solid var(--border);
            padding-bottom: 8px;
        }}
        
        .report-body h3 {{
            font-size: 1.2rem;
            font-weight: 600;
            color: var(--primary-light);
            margin-top: 25px;
            margin-bottom: 12px;
        }}
        
        .report-body h4 {{
            font-size: 1.05rem;
            font-weight: 600;
            color: var(--text-main);
            margin-top: 20px;
            margin-bottom: 8px;
        }}
        
        .report-body p {{
            margin-bottom: 15px;
            line-height: 1.7;
            font-size: 0.975rem;
            text-align: justify;
        }}
        
        .report-body ul, .report-body ol {{
            margin-left: 20px;
            margin-bottom: 15px;
        }}
        
        .report-body li {{
            margin-bottom: 6px;
            font-size: 0.975rem;
        }}
        
        /* Markdown blockquotes */
        blockquote {{
            border-left: 4px solid var(--secondary);
            background-color: var(--bg-main);
            padding: 12px 20px;
            margin: 15px 0;
            border-radius: 0 8px 8px 0;
            font-style: italic;
            color: #475569;
        }}
        
        /* Tables styling */
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
            font-size: 0.9rem;
            border-radius: 8px;
            overflow: hidden;
            border: 1px solid var(--border);
        }}
        
        th {{
            background-color: var(--primary);
            color: white;
            font-weight: 600;
            text-align: left;
            padding: 10px 12px;
        }}
        
        td {{
            padding: 10px 12px;
            border-bottom: 1px solid var(--border);
        }}
        
        tr:nth-child(even) {{
            background-color: var(--bg-main);
        }}
        
        tr:hover {{
            background-color: #f1f5f9;
        }}
        
        /* Image presentation */
        .image-container {{
            margin: 25px 0;
            text-align: center;
            background-color: var(--bg-main);
            padding: 20px;
            border-radius: 12px;
            border: 1px solid var(--border);
        }}
        
        .image-container img, .image-container object {{
            max-width: 100%;
            height: auto;
            border-radius: 6px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        }}
        
        .image-caption {{
            font-size: 0.85rem;
            color: var(--text-muted);
            margin-top: 10px;
            font-style: italic;
        }}
        
        /* Code blocks */
        pre {{
            background-color: var(--code-bg);
            border-radius: 8px;
            padding: 15px;
            overflow-x: auto;
            border: 1px solid var(--border);
            margin: 15px 0;
        }}
        
        code {{
            font-family: 'Fira Code', 'Lucida Console', Monaco, monospace;
            font-size: 0.85rem;
            color: #0f172a;
        }}
        
        /* Collapsible code details */
        .code-details {{
            margin-bottom: 12px;
            border: 1px solid var(--border);
            border-radius: 8px;
            background-color: var(--bg-card);
            overflow: hidden;
            transition: all 0.2s;
        }}
        
        .code-details summary {{
            padding: 12px 18px;
            font-size: 0.95rem;
            font-weight: 600;
            color: var(--primary);
            cursor: pointer;
            background-color: var(--bg-main);
            user-select: none;
            outline: none;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        
        .code-details summary:hover {{
            background-color: #e2e8f0;
        }}
        
        .code-details summary::-webkit-details-marker {{
            display: none;
        }}
        
        .code-details summary::after {{
            content: '▼';
            font-size: 0.8rem;
            transition: transform 0.2s;
        }}
        
        .code-details[open] summary::after {{
            transform: rotate(180deg);
        }}
        
        .code-details pre {{
            margin: 0;
            border-radius: 0;
            border: none;
            border-top: 1px solid var(--border);
        }}
        
        .file-path {{
            font-size: 0.8rem;
            color: var(--text-muted);
            font-weight: normal;
        }}
    </style>
</head>
<body>

    <header class="top-header">
        <div class="header-container">
            <img class="school-logo" src="{logo_base64}" alt="Logo Trường Đại học Khoa học Tự nhiên">
            <div class="header-text">
                <h1>ĐẠI HỌC QUỐC GIA THÀNH PHỐ HỒ CHÍ MINH</h1>
                <h2>TRƯỜNG ĐẠI HỌC KHOA HỌC TỰ NHIÊN - KHOA VẬT LÝ - BỘ MÔN VI MẠCH</h2>
            </div>
        </div>
    </header>

    <div class="container">
        <aside class="sidebar">
            <h3>Nội dung</h3>
            <ul>
                <li><a href="#cover">Trang bìa</a></li>
                <li><a href="#chuong-1-tong-quan-kien-truc-he-thong">1. Tổng quan hệ thống</a></li>
                <li><a href="#chuong-2-kien-truc-tap-lenh-isa-bo-dieu-khien">2. Kiến trúc tập lệnh (ISA)</a></li>
                <li><a href="#chuong-3-thiet-ke-phan-cung-cap-rtl">3. Sơ đồ khối phần cứng</a></li>
                <li><a href="#chuong-4-mo-phong-rtl-kiem-thu-chuc-nang">4. Kết quả mô phỏng RTL</a></li>
                <li><a href="#chuong-5-logic-synthesis-thong-ke-tai-nguyen">5. Logic Synthesis</a></li>
                <li><a href="#chuong-6-bao-cao-dinh-thoi-phan-tich-duong-tre-toi-han">6. Báo cáo định thời</a></li>
                <li><a href="#chuong-7-lich-su-phat-trien-va-han-che-cua-thiet-ke-ban-au-chot-co-vo-ieu-kien">7. Lịch sử phát triển & Hạn chế</a></li>
                <li><a href="#chuong-8-kiem-chung-chuc-nang-thuc-nghiem">8. Kiểm chứng &amp; Thực nghiệm</a></li>
                <li><a href="#ket-luan">Kết luận</a></li>
                <li><a href="#appendix">Phụ lục: Mã nguồn</a></li>
            </ul>
        </aside>

        <main>
            <section id="cover" class="cover-card">
                <p style="text-transform:uppercase; font-size:0.9rem; font-weight:700; color:var(--text-muted)">Đồ án cuối kỳ môn học Thiết kế vi mạch</p>
                <h1 class="cover-title">THIẾT KẾ BỘ VI XỬ LÝ CPU 4-BIT (TKVM)</h1>
                <p class="cover-subtitle">Kiến trúc đơn chu kỳ Harvard RTL &amp; GDS Layout vật lý</p>
                
                <div class="metadata-grid">
                    <div class="metadata-item">
                        <h4>Sinh viên thực hiện</h4>
                        <p>Lê Ngọc Tường</p>
                    </div>
                    <div class="metadata-item">
                        <h4>Mã số sinh viên</h4>
                        <p>22120395</p>
                    </div>
                    <div class="metadata-item">
                        <h4>Lớp / Học kỳ</h4>
                        <p>Môn Thiết kế vi mạch - HK3/2025-2026</p>
                    </div>
                    <div class="metadata-item">
                        <h4>Giáo viên hướng dẫn</h4>
                        <p>Ban Giảng huấn Bộ môn Vi mạch</p>
                    </div>
                </div>
                
                <div class="action-buttons">
                    <a href="Bao_cao_CPU_4bit.pdf" download class="btn btn-primary">Tải báo cáo PDF</a>
                    <a href="#chuong-1-tong-quan-kien-truc-he-thong" class="btn btn-outline">Đọc báo cáo trực tuyến</a>
                </div>
            </section>

            <article id="report-main" class="report-body">
                {html_body}
                
                <hr style="margin:40px 0; border:none; border-top:1px solid var(--border)">
                
                <h2 id="appendix">Phụ lục: Mã nguồn thiết kế RTL và Testbench</h2>
                <p style="margin-bottom:20px">Dưới đây là chi tiết mã nguồn mô tả phần cứng bằng Verilog RTL và testbench mô phỏng hệ thống hoàn chỉnh.</p>
                {code_sections}
            </article>
        </main>
    </div>

    <script>
        // Custom interactive script: replace image tags with interactive object tags for SVG
        document.querySelectorAll('.report-body img').forEach(img => {{
            const src = img.getAttribute('src');
            if (src.endsWith('.svg')) {{
                const obj = document.createElement('object');
                obj.setAttribute('type', 'image/svg+xml');
                obj.setAttribute('data', src);
                obj.style.width = '100%';
                obj.style.height = 'auto';
                
                // Wrap in container
                const container = document.createElement('div');
                container.className = 'image-container';
                
                const parent = img.parentNode;
                if (parent.tagName === 'FIGURE') {{
                    const figcaption = parent.querySelector('figcaption');
                    const captionText = figcaption ? figcaption.innerText : img.getAttribute('alt') || 'Sơ đồ thiết kế';
                    
                    parent.insertBefore(container, img);
                    container.appendChild(obj);
                    
                    const captionDiv = document.createElement('div');
                    captionDiv.className = 'image-caption';
                    captionDiv.innerText = captionText;
                    container.appendChild(captionDiv);
                    
                    img.remove();
                    if (figcaption) figcaption.remove();
                }} else {{
                    parent.insertBefore(container, img);
                    container.appendChild(obj);
                    
                    const captionDiv = document.createElement('div');
                    captionDiv.className = 'image-caption';
                    captionDiv.innerText = img.getAttribute('alt') || 'Sơ đồ thiết kế';
                    container.appendChild(captionDiv);
                    
                    img.remove();
                }}
            }} else if (src.endsWith('.png') || src.endsWith('.jpg') || src.endsWith('.jpeg')) {{
                const container = document.createElement('div');
                container.className = 'image-container';
                
                const parent = img.parentNode;
                if (parent.tagName === 'FIGURE') {{
                    const figcaption = parent.querySelector('figcaption');
                    const captionText = figcaption ? figcaption.innerText : img.getAttribute('alt') || 'Hình ảnh kết quả';
                    
                    parent.insertBefore(container, img);
                    container.appendChild(img);
                    
                    const captionDiv = document.createElement('div');
                    captionDiv.className = 'image-caption';
                    captionDiv.innerText = captionText;
                    container.appendChild(captionDiv);
                    
                    if (figcaption) figcaption.remove();
                }} else {{
                    parent.insertBefore(container, img);
                    container.appendChild(img);
                    
                    const captionDiv = document.createElement('div');
                    captionDiv.className = 'image-caption';
                    captionDiv.innerText = img.getAttribute('alt') || 'Hình ảnh kết quả';
                    container.appendChild(captionDiv);
                }}
            }}
        }});
    </script>
</body>
</html>
"""
    
    full_html = template.format(
        logo_base64=logo_base64,
        html_body=html_body,
        code_sections=code_sections
    )
    
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(full_html)
    print("HTML build completed: {}".format(html_path))

if __name__ == '__main__':
    build_html()
