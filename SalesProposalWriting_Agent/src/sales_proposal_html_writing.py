#!/usr/bin/env python3
"""
Professional Sales Proposal Generator - With Repeating Page Headers (Fixed Flow)
- Cover page has NO logos.
- All content pages have logos at the top, then a line, then text.
- Page numbers show bottom-right on every page.
- Supports HTML and PDF (WeasyPrint).
"""

import os
import re
from typing import Dict, List, Tuple

try:
    from weasyprint import HTML
    WEASYPRINT_AVAILABLE = True
except ImportError:
    WEASYPRINT_AVAILABLE = False


class ModernPresentationConfig:
    def __init__(self, theme: str = "executive", custom_colors: Dict[str, str] = None):
        self.theme = theme
        self.default_themes = {
            "corporate": {
                "primary": "#1a365d", "secondary": "#2d3748", "accent": "#3182ce",
                "success": "#38a169", "background": "#ffffff", "surface": "#f7fafc",
                "text": "#2d3748", "text_light": "#718096", "border": "#e2e8f0"
            },
            "premium": {
                "primary": "#2d1b69", "secondary": "#553c9a", "accent": "#667eea",
                "success": "#48bb78", "background": "#ffffff", "surface": "#f8fafc",
                "text": "#1a202c", "text_light": "#718096", "border": "#e2e8f0"
            },
            "executive": {
                "primary": "#1a202c", "secondary": "#2d3748", "accent": "#4299e1",
                "success": "#38a169", "background": "#ffffff", "surface": "#f7fafc",
                "text": "#1a202c", "text_light": "#718096", "border": "#e2e8f0"
            }
        }
        base_colors = self.default_themes.get(theme, self.default_themes["corporate"])
        self.colors = {**base_colors, **(custom_colors or {})}

    def get_modern_css(self) -> str:
        return f"""
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Playfair+Display:wght@400;500;600;700&display=swap');
        :root {{
            --primary: {self.colors["primary"]};
            --secondary: {self.colors["secondary"]};
            --accent: {self.colors["accent"]};
            --success: {self.colors["success"]};
            --background: {self.colors["background"]};
            --surface: {self.colors["surface"]};
            --text: {self.colors["text"]};
            --text-light: {self.colors["text_light"]};
            --border: {self.colors["border"]};
        }}

        body {{
            font-family: 'Inter', sans-serif;
            line-height: 1.6;
            color: var(--text);
            background: var(--background);
            font-size: 16px;
        }}

        @page {{
            size: A4;
            margin: 20mm 15mm 20mm 15mm;
            @bottom-right {{
                content: "Page " counter(page);
                font-family: 'Inter', sans-serif;
                font-size: 12px;
                color: var(--text-light);
            }}
        }}

        /* Cover Page */
        .cover-page {{
            height: 100vh;
            background: linear-gradient(135deg, {self.colors["primary"]}f2 0%, {self.colors["secondary"]}f2 50%, {self.colors["accent"]}f2 100%);
            display: flex;
            justify-content: center;
            align-items: center;
            flex-direction: column;
            text-align: center;
            page-break-after: always;
        }}
        .cover-main-title {{
            font-family: 'Playfair Display', serif;
            font-size: 4rem;
            color: white;
            margin: 0;
        }}
        .cover-for {{
            font-size: 1.2rem;
            color: rgba(255,255,255,0.8);
            margin: 0.5rem 0;
        }}
        .cover-client-name {{
            font-family: 'Playfair Display', serif;
            font-size: 3rem;
            color: white;
        }}

        /* Content Pages */
        .content-page {{
            page-break-before: always;
        }}
        .header-container {{
            margin-bottom: 1rem;
        }}
        .page-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 0.5rem;
        }}
        .header-logo {{
            max-height: 45px;
            max-width: 150px;
            object-fit: contain;
        }}
        .header-line {{
            width: 100%;
            height: 3px;
            background: linear-gradient(90deg, var(--primary), var(--accent), var(--primary));
            border: none;
            margin: 0;
        }}

        .section {{
            margin: 2rem 0;
            padding: 1rem;
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 8px;
        }}
        .section-title {{
            font-size: 1.5rem;
            font-weight: 600;
            margin-bottom: 1rem;
            color: var(--primary);
        }}
        .section-content p {{ margin-bottom: 1rem; }}
        """


def generate_modern_presentation(
    filename: str,
    client_name: str,
    seller_logo_url: str,
    client_logo_url: str,
    theme: str = "corporate",
    output_format: str = "html"
) -> None:

    config = ModernPresentationConfig(theme)

    def parse_txt_file(file_path: str) -> Tuple[str, List[Dict[str, str]]]:
        sections, main_title = [], "Sales Proposal"
        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.read().splitlines()

        current_title, current_text = None, []
        for line in lines:
            if line.startswith("Title:"):
                if current_title:
                    sections.append({"title": current_title, "content": "\n".join(current_text)})
                current_title = line[6:].strip()
                current_text = []
                if main_title == "Sales Proposal":
                    main_title = current_title
            elif line.startswith("Text:"):
                current_text.append(line[5:].strip())
            else:
                current_text.append(line)
        if current_title:
            sections.append({"title": current_title, "content": "\n".join(current_text)})

        return main_title, sections

    def process_content(content: str) -> str:
        content = re.sub(r"\*\*(.*?)\*\*", r"<strong>\1</strong>", content)
        content = re.sub(r"\*(.*?)\*", r"<em>\1</em>", content)
        lines = content.split("\n")
        html = []
        for line in lines:
            if not line.strip():
                continue
            html.append(f"<p>{line}</p>")
        return "\n".join(html)

    def generate_html(doc_title: str, sections: List[Dict[str, str]]) -> str:
        css = config.get_modern_css()
        html = f"""<!DOCTYPE html>
<html><head>
<meta charset="utf-8">
<title>{doc_title}</title>
<style>{css}</style>
</head><body>
<div class="cover-page">
    <h1 class="cover-main-title">Sales Proposal</h1>
    <h5 class="cover-for">for</h5>
    <h1 class="cover-client-name">{client_name}</h1>
</div>
"""

        for section in sections:
            processed = process_content(section["content"])
            html += f"""
<div class="content-page">
    <div class="header-container">
        <header class="page-header">
            <img src="{client_logo_url}" alt="Client Logo" class="header-logo">
            <img src="{seller_logo_url}" alt="Seller Logo" class="header-logo">
        </header>
        <hr class="header-line">
    </div>
    <div class="section">
        <h3 class="section-title">{section['title']}</h3>
        <div class="section-content">{processed}</div>
    </div>
</div>
"""
        html += "</body></html>"
        return html

    main_title, sections = parse_txt_file(filename)
    html_content = generate_html(main_title, sections)
    base_name = os.path.splitext(filename)[0]

    if output_format in ["html", "both"]:
        with open(f"{base_name}_proposal.html", "w", encoding="utf-8") as f:
            f.write(html_content)
        print("✅ HTML generated")

    if output_format in ["pdf", "both"] and WEASYPRINT_AVAILABLE:
        HTML(string=html_content).write_pdf(f"{base_name}_proposal.pdf")
        print("✅ PDF generated")
    
    return html_content,f"{base_name}_proposal.html",f"{base_name}_proposal.pdf"

# Example Run
# if __name__ == "__main__":


#     generate_modern_presentation(
#         filename="proposal_data.txt",
#         client_name="Innovate Inc.",
#         seller_logo_url="https://logo.clearbit.com/microsoft.com",
#         client_logo_url="https://logo.clearbit.com/google.com",
#         theme="premium",
#         output_format="both"
#     )
