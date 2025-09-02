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
    min-height: 297mm; /* A4 height for PDF */
    background: linear-gradient(135deg, {self.colors["primary"]}f2 0%, {self.colors["secondary"]}f2 50%, {self.colors["accent"]}f2 100%);
    display: flex;
    justify-content: center;
    align-items: center;
    flex-direction: column;
    text-align: center;
    page-break-after: always;
    padding: 2rem;
    box-sizing: border-box;
}}

.cover-main-title {{
    font-family: 'Playfair Display', serif;
    font-size: 4.5rem;
    font-weight: 700;
    color: white;
    margin: 2rem 0;
    line-height: 1.1;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    max-width: 90%;
}}

.cover-for {{
    font-size: 1.8rem;
    font-weight: 300;
    color: rgba(255,255,255,0.9);
    margin: 1.5rem 0;
    text-transform: uppercase;
    letter-spacing: 3px;
}}

.cover-client-name {{
    font-family: 'Playfair Display', serif;
    font-size: 3.8rem;
    font-weight: 600;
    color: white;
    margin: 2rem 0;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    max-width: 90%;
}}

/* Content Pages */
.content-page {{
    page-break-before: always;
}}

.header-container {{
    margin-bottom: 1.5rem;
    background: linear-gradient(135deg, rgba(45, 55, 72, 0.95) 0%, rgba(74, 85, 104, 0.95) 100%);
    padding: 1rem 1.5rem;
    border-radius: 10px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    border: 1px solid rgba(255, 255, 255, 0.1);
}}

.page-header {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 0.8rem;
}}

.header-logo {{
    max-height: 50px;
    max-width: 180px;
    object-fit: contain;
    background: rgba(255, 255, 255, 0.95);
    padding: 8px 12px;
    border-radius: 6px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    border: 1px solid rgba(255, 255, 255, 0.2);
}}

.header-line {{
    width: 100%;
    height: 4px;
    background: linear-gradient(90deg, rgba(255,255,255,0.8), rgba(66, 153, 225, 0.9), rgba(255,255,255,0.8));
    border: none;
    margin: 0;
    border-radius: 2px;
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
        sections = []
        main_title = "Sales Proposal"  # Default fallback
        
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Split content into sections using regex
        section_pattern = r'Title:\s*(.*?)\s*Text:\s*(.*?)(?=Title:|$)'
        matches = re.findall(section_pattern, content, re.DOTALL)
        
        # Look for a title section specifically (case insensitive)
        title_found = False
        for i, (title, text) in enumerate(matches):
            title = title.strip()
            text = text.strip()
            
            # Check if this section is specifically the proposal title
            # Look for patterns like "title of the proposal", "proposal title", etc.
            if re.search(r'\b(title\s+of\s+the\s+.*proposal|proposal\s+title|title\s+of\s+proposal)\b', title, re.IGNORECASE):
                main_title = text.split('\n')[0].strip() if text else title
                title_found = True
                # Don't add this section to content sections since it's just the title
                continue
            # If no specific title section found, use the first section title as main title
            elif i == 0 and not title_found:
                main_title = title
            
            # Add to sections for content pages
            sections.append({"title": title, "content": text})
        
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
    <h1 class="cover-main-title">{doc_title}</h1>
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

    return html_content, f"{base_name}_proposal.html", f"{base_name}_proposal.pdf"


