#!/usr/bin/env python3
"""
Professional Sales Proposal Generator - Fixed Parsing for Main Title
Now properly extracts the main proposal title from the first Title: line
"""

import re
import os
from typing import Dict, List, Optional, Tuple
from datetime import datetime

class ModernPresentationConfig:
    """Enhanced configuration class for modern presentation styling with dynamic colors"""
    
    def __init__(self, theme: str = "executive", custom_colors: Dict[str, str] = None):
        self.theme = theme
        
        # Default color schemes
        self.default_themes = {
            "corporate": {
                "primary": "#1a365d",
                "secondary": "#2d3748", 
                "accent": "#3182ce",
                "success": "#38a169",
                "background": "#ffffff",
                "surface": "#f7fafc",
                "text": "#2d3748",
                "text_light": "#718096",
                "border": "#e2e8f0"
            },
            "premium": {
                "primary": "#2d1b69",
                "secondary": "#553c9a",
                "accent": "#667eea",
                "success": "#48bb78",
                "background": "#ffffff",
                "surface": "#f8fafc",
                "text": "#1a202c",
                "text_light": "#718096",
                "border": "#e2e8f0"
            },
            "executive": {
                "primary": "#1a202c",
                "secondary": "#2d3748",
                "accent": "#4299e1",
                "success": "#38a169",
                "background": "#ffffff",
                "surface": "#f7fafc",
                "text": "#1a202c",
                "text_light": "#718096",
                "border": "#e2e8f0"
            }
        }
        
        # Use custom colors if provided, otherwise use theme defaults
        if custom_colors:
            # Merge custom colors with default theme colors
            base_colors = self.default_themes.get(theme, self.default_themes["corporate"])
            self.colors = {**base_colors, **custom_colors}
        else:
            self.colors = self.default_themes.get(theme, self.default_themes["corporate"])
            
    def get_modern_css(self, logo_url: str, logo_url_2: str = None) -> str:
        """Generate modern, professional CSS with enhanced cover page design and reduced transparency"""
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
            --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
            --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
            --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
            --shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
            --radius-sm: 0.375rem;
            --radius-md: 0.5rem;
            --radius-lg: 0.75rem;
            --radius-xl: 1rem;
        }}

        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        @page {{
            size: A4;
            margin: 0;
        }}

        body {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
            line-height: 1.6;
            color: var(--text);
            background: var(--background);
            font-size: 16px;
            font-weight: 400;
            -webkit-font-smoothing: antialiased;
            -moz-osx-font-smoothing: grayscale;
        }}

        /* ENHANCED PREMIUM COVER PAGE WITH REDUCED TRANSPARENCY */
        .cover-page {{
            width: 100vw;
            height: 100vh;
            background: linear-gradient(135deg, 
                {self.colors["primary"]}f2 0%, 
                {self.colors["secondary"]}f2 50%, 
                {self.colors["accent"]}f2 100%),
                radial-gradient(circle at center, rgba(255,255,255,0.1) 0%, transparent 70%);
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            text-align: center;
            position: relative;
            page-break-after: always;
            padding: 2rem;
            overflow: hidden;
        }}

        .cover-page::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: 
                radial-gradient(circle at 20% 20%, rgba(255,255,255,0.05) 0%, transparent 50%),
                radial-gradient(circle at 80% 80%, rgba(255,255,255,0.03) 0%, transparent 50%);
            pointer-events: none;
        }}

        /* ENHANCED LOGO SECTION */
        .cover-logos {{
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 3rem;
            margin-bottom: 3rem;
            z-index: 10;
            position: relative;
            width: 100%;
            max-width: 800px;
        }}

        .cover-logo {{
            width: 200px;
            height: 200px;
            background: rgba(255, 255, 255, 0.98);
            border-radius: var(--radius-xl);
            display: flex;
            align-items: center;
            justify-content: center;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.2);
            padding: 1.5rem;
            border: 2px solid rgba(255, 255, 255, 0.5);
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            position: relative;
            overflow: hidden;
        }}

        .cover-logo:hover {{
            transform: translateY(-5px) scale(1.02);
            box-shadow: 0 30px 60px rgba(0, 0, 0, 0.25);
        }}

        .cover-logo img {{
            max-width: 100%;
            max-height: 100%;
            object-fit: contain;
            filter: drop-shadow(0 4px 6px rgba(0, 0, 0, 0.1));
        }}

        .cover-logo-1 {{
            background: rgba(255, 255, 255, 0.98) url('{logo_url}') no-repeat center;
            background-size: contain;
        }}

        .cover-logo-2 {{
            background: rgba(255, 255, 255, 0.98) url('{logo_url_2 or logo_url}') no-repeat center;
            background-size: contain;
        }}

        /* ENHANCED TITLE SECTION WITH BETTER VISIBILITY */
        .cover-title {{
            font-family: 'Playfair Display', serif;
            font-size: clamp(2rem, 4vw, 3.5rem);
            font-weight: 700;
            color: #ffffff;
            margin-bottom: 0;
            text-shadow: 
                0 2px 4px rgba(0,0,0,0.5),
                0 4px 8px rgba(0,0,0,0.3),
                0 8px 16px rgba(0,0,0,0.2);
            max-width: 90%;
            line-height: 1.3;
            letter-spacing: -0.025em;
            z-index: 10;
            position: relative;
            text-align: center;
            background: linear-gradient(135deg, #ffffff 0%, #f0f8ff 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            filter: drop-shadow(0 2px 4px rgba(0,0,0,0.3));
        }}

        /* MODERN CONTENT PAGES */
        .content-page {{
            page-break-before: always;
            position: relative;
            padding: 3rem;
            min-height: 100vh;
            background: var(--background);
        }}

        .presentation-container {{
            max-width: 100%;
            padding: 0;
            background: var(--background);
            position: relative;
        }}

        .main-title {{
            font-family: 'Playfair Display', serif;
            font-size: 2.5rem;
            font-weight: 700;
            color: var(--primary);
            text-align: center;
            margin-bottom: 3rem;
            padding-bottom: 1rem;
            position: relative;
        }}

        .main-title::after {{
            content: '';
            position: absolute;
            bottom: 0;
            left: 50%;
            transform: translateX(-50%);
            width: 80px;
            height: 4px;
            background: linear-gradient(90deg, var(--accent), var(--success));
            border-radius: 2px;
        }}

        .section {{
            margin-bottom: 2.5rem;
            padding: 2rem;
            background: var(--surface);
            border-radius: var(--radius-lg);
            border: 1px solid var(--border);
            box-shadow: var(--shadow-sm);
            page-break-inside: avoid;
            position: relative;
            overflow: hidden;
        }}

        .section::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 4px;
            height: 100%;
            background: linear-gradient(180deg, var(--accent), var(--success));
        }}

        .section-title {{
            font-family: 'Inter', sans-serif;
            font-size: 1.5rem;
            font-weight: 600;
            color: var(--primary);
            margin-bottom: 1rem;
            letter-spacing: -0.025em;
        }}

        .section-content {{
            font-size: 1rem;
            line-height: 1.7;
            color: var(--text);
        }}

        .section-content p {{
            margin-bottom: 1rem;
        }}

        .section-content p:last-child {{
            margin-bottom: 0;
        }}

        .section-content ul {{
            margin-left: 1.5rem;
            margin-top: 0.5rem;
        }}

        .section-content li {{
            margin-bottom: 0.5rem;
            position: relative;
        }}

        .section-content li::marker {{
            color: var(--accent);
        }}

        .company-info {{
            background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
            color: white;
            padding: 2.5rem;
            margin: 2rem 0;
            border-radius: var(--radius-lg);
            box-shadow: var(--shadow-lg);
            page-break-inside: avoid;
            position: relative;
            overflow: hidden;
        }}

        .company-info::before {{
            content: '';
            position: absolute;
            top: 0;
            right: 0;
            width: 200px;
            height: 200px;
            background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
            border-radius: 50%;
            transform: translate(50%, -50%);
        }}

        .company-title {{
            font-family: 'Playfair Display', serif;
            font-size: 1.75rem;
            font-weight: 600;
            margin-bottom: 1rem;
            color: white;
            position: relative;
            z-index: 10;
        }}

        .company-content {{
            font-size: 1rem;
            line-height: 1.6;
            color: rgba(255,255,255,0.95);
            position: relative;
            z-index: 10;
        }}

        .pricing-highlight {{
            background: linear-gradient(135deg, var(--surface) 0%, white 100%);
            border: 2px solid var(--success);
            padding: 2.5rem;
            margin: 2rem 0;
            text-align: center;
            border-radius: var(--radius-xl);
            box-shadow: var(--shadow-lg);
            page-break-inside: avoid;
            position: relative;
            overflow: hidden;
        }}

        .pricing-highlight::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: linear-gradient(90deg, var(--success), var(--accent));
        }}

        .price-amount {{
            font-family: 'Inter', sans-serif;
            font-size: 3rem;
            font-weight: 800;
            color: var(--success);
            margin-bottom: 1rem;
            text-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}

        .cta-section {{
            background: linear-gradient(135deg, var(--accent) 0%, var(--primary) 100%);
            color: white;
            padding: 2.5rem;
            text-align: center;
            margin-top: 2.5rem;
            border-radius: var(--radius-lg);
            box-shadow: var(--shadow-lg);
            page-break-inside: avoid;
            position: relative;
            overflow: hidden;
        }}

        .cta-section::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: 
                radial-gradient(circle at 30% 30%, rgba(255,255,255,0.1) 0%, transparent 50%),
                radial-gradient(circle at 70% 70%, rgba(255,255,255,0.05) 0%, transparent 50%);
            pointer-events: none;
        }}

        .cta-title {{
            font-family: 'Playfair Display', serif;
            font-size: 2rem;
            font-weight: 600;
            color: white;
            margin-bottom: 1rem;
            position: relative;
            z-index: 10;
        }}

        .cta-content {{
            font-size: 1.1rem;
            line-height: 1.6;
            color: rgba(255,255,255,0.95);
            position: relative;
            z-index: 10;
        }}

        .phase-section {{
            background: white;
            border: 2px solid var(--border);
            padding: 2rem;
            margin: 1.5rem 0;
            border-radius: var(--radius-lg);
            box-shadow: var(--shadow-sm);
            page-break-inside: avoid;
            transition: box-shadow 0.3s ease;
        }}

        .phase-section:hover {{
            box-shadow: var(--shadow-md);
        }}

        .phase-title {{
            font-size: 1.25rem;
            font-weight: 600;
            color: var(--primary);
            margin-bottom: 1rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }}

        .phase-title::before {{
            content: '';
            width: 8px;
            height: 8px;
            background: var(--accent);
            border-radius: 50%;
        }}

        .timeline-item {{
            background: white;
            border-left: 4px solid var(--success);
            margin: 1rem 0;
            padding: 1.5rem;
            border-radius: 0 var(--radius-md) var(--radius-md) 0;
            box-shadow: var(--shadow-sm);
            page-break-inside: avoid;
            position: relative;
        }}

        .timeline-item::before {{
            content: '';
            position: absolute;
            left: -8px;
            top: 1.5rem;
            width: 12px;
            height: 12px;
            background: var(--success);
            border-radius: 50%;
            border: 3px solid white;
        }}

        .timeline-week {{
            font-weight: 600;
            color: var(--success);
            font-size: 1rem;
            margin-bottom: 0.5rem;
        }}

        /* ENHANCED TYPOGRAPHY */
        h1, h2, h3, h4, h5, h6 {{
            font-weight: 600;
            line-height: 1.2;
            margin-bottom: 0.5rem;
        }}

        strong {{
            font-weight: 600;
            color: var(--primary);
        }}

        em {{
            font-style: italic;
            color: var(--accent);
        }}

        /* RESPONSIVE DESIGN */
        @media (max-width: 768px) {{
            .cover-logos {{
                flex-direction: column;
                gap: 2rem;
                margin-bottom: 2rem;
            }}
            
            .cover-logo {{
                width: 160px;
                height: 160px;
            }}
            
            .cover-title {{
                font-size: clamp(1.5rem, 4vw, 2.5rem);
            }}
            
            .content-page {{
                padding: 2rem;
            }}
            
            .section {{
                padding: 1.5rem;
            }}
        }}

        /* PDF PRINT OPTIMIZATION */
        @media print {{
            .cover-page {{
                width: 210mm !important;
                height: 297mm !important;
                page-break-after: always !important;
                margin: 0 !important;
                padding: 15mm !important;
                display: flex !important;
                flex-direction: column !important;
                justify-content: center !important;
                align-items: center !important;
                background: linear-gradient(135deg, 
                    {self.colors["primary"]}f2 0%, 
                    {self.colors["secondary"]}f2 50%, 
                    {self.colors["accent"]}f2 100%) !important;
                print-color-adjust: exact !important;
                -webkit-print-color-adjust: exact !important;
            }}
            
            .cover-logos {{
                margin-bottom: 20mm !important;
            }}
            
            .cover-logo {{
                width: 80mm !important;
                height: 80mm !important;
                print-color-adjust: exact !important;
                -webkit-print-color-adjust: exact !important;
                background-color: rgba(255, 255, 255, 0.98) !important;
            }}
            
            .cover-title {{
                font-size: 24pt !important;
                line-height: 1.2 !important;
                color: white !important;
                print-color-adjust: exact !important;
                -webkit-print-color-adjust: exact !important;
                text-shadow: 0 2px 4px rgba(0,0,0,0.5) !important;
                -webkit-text-fill-color: white !important;
                background: none !important;
            }}
            
            .content-page {{
                page-break-before: always !important;
                margin: 15mm !important;
                padding: 0 !important;
                min-height: calc(297mm - 30mm) !important;
            }}
            
            .presentation-container {{
                padding: 0 !important;
            }}
            
            .section,
            .company-info,
            .pricing-highlight,
            .cta-section,
            .phase-section,
            .timeline-item {{
                page-break-inside: avoid !important;
                orphans: 2 !important;
                widows: 2 !important;
            }}
            
            .cover-logo:hover {{
                transform: none !important;
            }}
        }}
        """

def generate_modern_presentation(
    filename: str,
    logo_url: str,
    theme: str = "corporate",
    custom_colors: Dict[str, str] = None,
    logo_url_2: str = None,
    output_format: str = "html",
    cover_title: str = None
) -> Optional[str]:
    """
    Generate modern, professional sales proposal presentation
    
    Args:
        filename: Path to the input text file
        logo_url: URL for the first logo
        theme: Theme name (corporate, premium, executive)
        custom_colors: Dictionary of custom colors to override theme defaults
        logo_url_2: URL for the second logo (optional)
        output_format: Output format ('html', 'pdf', 'both')
        cover_title: Custom title for cover page (if None, extracts from file)
    """
    
    config = ModernPresentationConfig(theme, custom_colors)
    
    def parse_txt_file(file_path: str) -> Tuple[str, List[Dict[str, str]]]:
        """
        Parse the text file with the SPECIFIC format where:
        - First 'Title:' line contains the main proposal title
        - Subsequent sections have 'Title:' and 'Text:' pairs
        """
        sections = []
        main_title = None
        
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read().strip()
        except FileNotFoundError:
            raise FileNotFoundError(f"File not found: {file_path}")
        
        # Split into lines and process sequentially
        lines = content.split('\n')
        i = 0
        current_section_title = None
        current_section_text = []
        first_title_found = False

        while i < len(lines):
            line = lines[i].strip()
            
            if not line:  # Skip empty lines
                i += 1
                continue
            
            if line.startswith('Title:'):
                # Save previous section if exists
                if current_section_title and current_section_text:
                    text_content = '\n'.join(current_section_text).strip()
                    if text_content:
                        sections.append({
                            'title': current_section_title,
                            'content': text_content
                        })
                        print(f"📄 Added section: {current_section_title}")
                
                # Extract title and set as main title if it's the first one
                title_text = line[6:].strip()  # Remove "Title:" prefix
                if not first_title_found:
                    main_title = title_text  # Use first title for cover page
                    first_title_found = True
                    print(f"📋 Found main title for cover: {main_title}")
                
                # Start new section (including the first one)
                current_section_title = title_text
                current_section_text = []
                
            elif line.startswith('Text:'):
                # Extract text content (remove "Text:" prefix)
                text_content = line[5:].strip()  # Remove "Text:" prefix
                if text_content:
                    current_section_text.append(text_content)
            else:
                # This is continuation text (multiline content)
                if current_section_title:  # Only add if we have a current section
                    current_section_text.append(line)
            
            i += 1
        
        # Don't forget the last section
        if current_section_title and current_section_text:
            text_content = '\n'.join(current_section_text).strip()
            if text_content:
                sections.append({
                    'title': current_section_title,
                    'content': text_content
                })
                print(f"📄 Added final section: {current_section_title}")
        
        if not sections:
            raise ValueError("No valid sections found in the document")
        
        print(f"✅ Parsed {len(sections)} sections with main title: '{main_title}'")
        return main_title, sections
        
    def process_content(content: str) -> str:
        """Enhanced content processing with better formatting"""
        # Clean up any remaining "Title:" or "Text:" artifacts
        content = re.sub(r'^(Title|Text):\s*', '', content, flags=re.MULTILINE)
        
        # Enhanced markdown processing
        content = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', content)
        content = re.sub(r'\*(.*?)\*', r'<em>\1</em>', content)
        content = re.sub(r'`(.*?)`', r'<code>\1</code>', content)
        
        lines = content.split('\n')
        processed_lines = []
        in_list = False
        
        for line in lines:
            line = line.strip()
            if not line:
                if in_list:
                    processed_lines.append('</ul>')
                    in_list = False
                processed_lines.append('')
                continue
                
            if line.startswith('• ') or line.startswith('* ') or line.startswith('- '):
                if not in_list:
                    processed_lines.append('<ul>')
                    in_list = True
                bullet_text = line[2:].strip()
                processed_lines.append(f'<li>{bullet_text}</li>')
            else:
                if in_list:
                    processed_lines.append('</ul>')
                    in_list = False
                if line:
                    processed_lines.append(f'<p>{line}</p>')
        
        if in_list:
            processed_lines.append('</ul>')
        
        return '\n'.join(processed_lines)
    
    def generate_html(main_title: str, sections: List[Dict[str, str]]) -> str:
        # Use provided cover_title or the extracted main_title
        title_for_cover = cover_title or main_title
        
        css = config.get_modern_css(logo_url, logo_url_2)
        
        html_template = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_for_cover}</title>
    <meta name="description" content="Professional Sales Proposal - {title_for_cover}">
    <style>{css}</style>
</head>
<body>
    <!-- ENHANCED PREMIUM COVER PAGE WITH PROPER TITLE -->
    <div class="cover-page">
        <div class="cover-logos">
            <div class="cover-logo cover-logo-1"></div>
            <div class="cover-logo cover-logo-2"></div>
        </div>
        <h1 class="cover-title">{title_for_cover}</h1>
    </div>
    
    <!-- MODERN CONTENT PAGES -->
    <div class="content-page">
        <div class="presentation-container">
'''
        
        # Process all sections normally
        for section in sections:
            processed_content = process_content(section['content'])
            
            # Enhanced pricing section detection and styling
            if any(keyword in section['title'].lower() for keyword in ['pricing', 'cost', 'investment', 'budget']) or '$' in section['content']:
                price_match = re.search(r'\$[\d,]+(?:\.\d{2})?', section['content'])
                if price_match:
                    price = price_match.group()
                    content_without_price = section['content'].replace(price, '').strip()
                    html_template += f'''
            <div class="pricing-highlight">
                <div class="price-amount">{price}</div>
                <div class="section-content">
                    {process_content(content_without_price)}
                </div>
            </div>
'''
                    continue
            
            # Enhanced section categorization and styling
            title_lower = section['title'].lower()
            
            if any(keyword in title_lower for keyword in ['who we are', 'what we do', 'team', 'expertise', 'about us', 'company', 'our services', 'capabilities', 'enterprise', 'organization', 'business', 'firm', 'corporate', 'details', 'profile', 'overview']):
                html_template += f'''
            <div class="company-info">
                <h3 class="company-title">{section['title']}</h3>
                <div class="company-content">
                    {processed_content}
                </div>
            </div>
'''
            elif any(keyword in title_lower for keyword in ['conclusion', 'call to action', 'contact', 'next steps', 'get started', 'ready to begin']):
                html_template += f'''
            <div class="cta-section">
                <h3 class="cta-title">{section['title']}</h3>
                <div class="cta-content">
                    {processed_content}
                </div>
            </div>
'''
            elif any(keyword in title_lower for keyword in ['scope', 'project breakdown', 'timeline', 'milestone', 'phases', 'roadmap', 'schedule']):
                html_template += f'''
            <div class="phase-section">
                <h3 class="phase-title">{section['title']}</h3>
                <div class="section-content">
                {processed_content}
                </div>
            </div>
'''
            else:
                # Standard section styling
                html_template += f'''
            <div class="section">
                <h3 class="section-title">{section['title']}</h3>
                <div class="section-content">
                    {processed_content}
                </div>
            </div>
'''
        
        # Close the HTML template
        html_template += '''
        </div>
    </div>
</body>
</html>'''
        
        return html_template
    
    try:
        # Parse the input file
        main_title, sections = parse_txt_file(filename)
        
        # Generate HTML
        html_content = generate_html(main_title, sections)
        
        # Determine output filename
        base_name = os.path.splitext(filename)[0]
        html_filename = f"{base_name}_proposal.html"
        
        # Write HTML file
        with open(html_filename, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"✅ Generated HTML proposal: {html_filename}")
        
        # Optional: Generate PDF using weasyprint if available
        if output_format in ['pdf', 'both']:
            try:
                import weasyprint
                pdf_filename = f"{base_name}_proposal.pdf"
                weasyprint.HTML(string=html_content).write_pdf(pdf_filename)
                print(f"✅ Generated PDF proposal: {pdf_filename}")
            except ImportError:
                print("⚠️  PDF generation requires 'weasyprint' package. Install with: pip install weasyprint")
        
        return html_filename
        
    except Exception as e:
        print(f"❌ Error generating proposal: {str(e)}")
        return None

