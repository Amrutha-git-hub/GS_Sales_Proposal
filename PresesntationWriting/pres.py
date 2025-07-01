#!/usr/bin/env python3
"""
Professional Sales Proposal Generator - Clean & Corporate Design
"""

import re
import os
from typing import Dict, List, Optional, Tuple

class PresentationConfig:
    """Configuration class for presentation styling"""
    
    def __init__(self, colors: List[str] = None):
        # Professional corporate colors - no fancy gradients
        self.primary_color = "#2c3e50"      # Dark blue-grey
        self.secondary_color = "#34495e"    # Slightly lighter blue-grey  
        self.accent_color = "#3498db"       # Professional blue
        self.success_color = "#27ae60"      # Professional green
        self.text_color = "#2c3e50"
        self.background_color = "#ffffff"
            
    def get_css(self, logo_url: str, logo_url_2: str = None) -> str:
        """Generate clean, professional CSS for sales proposals"""
        return f"""
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
            font-family: 'Arial', 'Helvetica', sans-serif;
            line-height: 1.6;
            color: {self.text_color};
            background: white;
            font-size: 11pt;
        }}

        /* PROFESSIONAL COVER PAGE */
        .cover-page {{
            width: 100vw;
            height: 100vh;
            background: linear-gradient(135deg, {self.primary_color} 0%, {self.secondary_color} 100%);
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            text-align: center;
            position: relative;
            page-break-after: always;
            padding: 40px;
        }}

        .cover-logos {{
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 80px;
            margin-bottom: 80px;
        }}

        .cover-logo {{
            width: 300px;
            height: 180px;
            background-color: white;
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            box-shadow: 0 8px 32px rgba(0,0,0,0.2);
            padding: 25px;
            border: 1px solid #e0e0e0;
        }}

        .cover-logo img {{
            max-width: 100%;
            max-height: 100%;
            object-fit: contain;
        }}

        .cover-logo-1 {{
            background: white url('{logo_url}') no-repeat center;
            background-size: contain;
        }}

        .cover-logo-2 {{
            background: white url('{logo_url_2 or logo_url}') no-repeat center;
            background-size: contain;
        }}

        .cover-title {{
            font-size: 42pt;
            font-weight: 700;
            color: white;
            margin-bottom: 30px;
            text-shadow: 0 2px 8px rgba(0,0,0,0.3);
            max-width: 90%;
            line-height: 1.2;
        }}

        .cover-subtitle {{
            font-size: 18pt;
            color: rgba(255,255,255,0.9);
            margin-bottom: 60px;
            max-width: 80%;
            font-weight: 300;
        }}

        .cover-date {{
            font-size: 14pt;
            color: rgba(255,255,255,0.85);
            background: rgba(255,255,255,0.1);
            padding: 12px 30px;
            border-radius: 4px;
            border: 1px solid rgba(255,255,255,0.2);
        }}

        /* CLEAN CONTENT PAGES - NO LOGOS */
        .content-page {{
            page-break-before: always;
            position: relative;
            padding: 50px;
            min-height: 100vh;
            background: white;
        }}

        .presentation-container {{
            max-width: 100%;
            padding: 0;
            background: white;
            position: relative;
        }}

        .main-title {{
            font-size: 24pt;
            font-weight: 700;
            color: {self.primary_color};
            text-align: center;
            margin-bottom: 50px;
            padding-bottom: 15px;
            border-bottom: 3px solid {self.primary_color};
        }}

        .section {{
            margin-bottom: 40px;
            padding: 25px;
            border-left: 4px solid {self.primary_color};
            background: #fafafa;
            page-break-inside: avoid;
        }}

        .section-title {{
            font-size: 16pt;
            font-weight: 600;
            color: {self.primary_color};
            margin-bottom: 15px;
            border-bottom: 2px solid {self.accent_color};
            padding-bottom: 8px;
        }}

        .section-content {{
            font-size: 11pt;
            line-height: 1.7;
            color: {self.text_color};
        }}

        .section-content p {{
            margin-bottom: 12px;
        }}

        .section-content ul {{
            margin-left: 20px;
            margin-top: 10px;
        }}

        .section-content li {{
            margin-bottom: 6px;
        }}

        .company-info {{
            background: {self.secondary_color};
            color: white;
            padding: 30px;
            margin: 30px 0;
            page-break-inside: avoid;
        }}

        .company-title {{
            font-size: 16pt;
            font-weight: 600;
            margin-bottom: 15px;
            color: white;
        }}

        .company-content {{
            font-size: 11pt;
            line-height: 1.6;
            color: white;
        }}

        .pricing-highlight {{
            background: #f8f9fa;
            border: 3px solid {self.success_color};
            padding: 30px;
            margin: 30px 0;
            text-align: center;
            page-break-inside: avoid;
        }}

        .price-amount {{
            font-size: 28pt;
            font-weight: 700;
            color: {self.success_color};
            margin-bottom: 15px;
        }}

        .cta-section {{
            background: {self.primary_color};
            color: white;
            padding: 30px;
            text-align: center;
            margin-top: 40px;
            page-break-inside: avoid;
        }}

        .cta-title {{
            font-size: 18pt;
            font-weight: 600;
            color: white;
            margin-bottom: 15px;
        }}

        .cta-content {{
            font-size: 12pt;
            line-height: 1.5;
            color: white;
        }}

        .phase-section {{
            background: white;
            border: 2px solid {self.accent_color};
            padding: 25px;
            margin: 20px 0;
            page-break-inside: avoid;
        }}

        .phase-title {{
            font-size: 14pt;
            font-weight: 600;
            color: {self.primary_color};
            margin-bottom: 12px;
        }}

        .timeline-item {{
            background: white;
            border-left: 4px solid {self.success_color};
            margin: 12px 0;
            padding: 15px 20px;
            page-break-inside: avoid;
        }}

        .timeline-week {{
            font-weight: 600;
            color: {self.success_color};
            font-size: 12pt;
        }}

        /* PDF PRINT OPTIMIZATION */
        @media print {{
            .cover-page {{
                width: 210mm !important;
                height: 297mm !important;
                page-break-after: always !important;
                margin: 0 !important;
                padding: 20mm !important;
            }}
            
            .content-page {{
                page-break-before: always !important;
                margin: 20mm !important;
                padding: 0 !important;
                min-height: calc(297mm - 40mm) !important;
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
        }}
        """

def generate_presentation(
    filename: str,
    logo_url: str,
    colors: List[str] = None,
    logo_url_2: str = None,
    output_format: str = "html"
) -> Optional[str]:
    """Generate professional sales proposal presentation"""
    
    config = PresentationConfig(colors)
    
    def parse_txt_file(file_path: str) -> List[Dict[str, str]]:
        sections = []
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
        except FileNotFoundError:
            raise FileNotFoundError(f"File not found: {file_path}")
        
        pattern = r'Title:\s*(.+?)\nText:\s*(.+?)(?=\nTitle:|\Z)'
        matches = re.findall(pattern, content, re.DOTALL)
        
        for title, text in matches:
            sections.append({
                'title': title.strip(),
                'content': text.strip()
            })
        
        if not sections:
            raise ValueError("No valid title-text pairs found")
        
        return sections
    
    def process_content(content: str) -> str:
        content = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', content)
        content = re.sub(r'\*(.*?)\*', r'<em>\1</em>', content)
        
        lines = content.split('\n')
        processed_lines = []
        in_list = False
        
        for line in lines:
            line = line.strip()
            if line.startswith('• ') or line.startswith('* '):
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
    
    def categorize_sections(sections: List[Dict[str, str]]) -> Dict[str, List]:
        categorized = {
            'title': None,
            'main': [],
            'phases': [],
            'company': [],
            'cta': []
        }
        
        for section in sections:
            title_lower = section['title'].lower()
            
            if 'title of the sales proposal' in title_lower or title_lower in ['title', 'main title', 'presentation title']:
                categorized['title'] = section
            elif any(keyword in title_lower for keyword in ['who we are', 'what we do', 'team', 'expertise', 'about us', 'company']):
                categorized['company'].append(section)
            elif any(keyword in title_lower for keyword in ['conclusion', 'call to action', 'contact', 'next steps']):
                categorized['cta'].append(section)
            elif any(keyword in title_lower for keyword in ['scope', 'project breakdown', 'timeline', 'milestone', 'phases']):
                categorized['phases'].append(section)
            else:
                categorized['main'].append(section)
        
        return categorized
    
    def generate_html(sections: List[Dict[str, str]]) -> str:
        categorized = categorize_sections(sections)
        
        if categorized['title']:
            main_title = categorized['title']['content']
        elif sections:
            main_title = sections[0]['content']
        else:
            main_title = "Sales Proposal"
        
        from datetime import datetime
        current_date = datetime.now().strftime("%B %Y")
        
        css = config.get_css(logo_url, logo_url_2)
        
        html_template = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{main_title}</title>
    <style>{css}</style>
</head>
<body>
    <!-- COVER PAGE WITH CLEAR LOGOS -->
    <div class="cover-page">
        <div class="cover-logos">
            <div class="cover-logo cover-logo-1"></div>
            <div class="cover-logo cover-logo-2"></div>
        </div>
        <h1 class="cover-title">{main_title}</h1>
        <p class="cover-subtitle">Professional Sales Proposal</p>
        <p class="cover-date">{current_date}</p>
    </div>
    
    <!-- CLEAN CONTENT PAGES (NO LOGOS) -->
    <div class="content-page">
        <div class="presentation-container">
'''
        
        # Add all sections
        all_sections = categorized['main'] + categorized['phases'] + categorized['company'] + categorized['cta']
        
        for section in all_sections:
            if section == categorized['title']:
                continue
                
            processed_content = process_content(section['content'])
            
            # Handle pricing sections
            if 'pricing' in section['title'].lower() or '$' in section['content']:
                price_match = re.search(r'\$[\d,]+', section['content'])
                if price_match:
                    price = price_match.group()
                    content_without_price = section['content'].replace(price, '').strip()
                    processed_content = f'''
                    <div class="pricing-highlight">
                        <div class="price-amount">{price}</div>
                        <div>{process_content(content_without_price)}</div>
                    </div>
                    '''
            
            # Handle company sections
            if section in categorized['company']:
                html_template += f'''
            <div class="company-info">
                <h3 class="company-title">{section['title']}</h3>
                <div class="company-content">
                    {processed_content}
                </div>
            </div>
'''
            # Handle CTA sections
            elif section in categorized['cta']:
                html_template += f'''
            <div class="cta-section">
                <h3 class="cta-title">{section['title']}</h3>
                <div class="cta-content">
                    {processed_content}
                </div>
            </div>
'''
            # Handle regular sections
            else:
                html_template += f'''
            <div class="section">
                <h2 class="section-title">{section['title']}</h2>
                <div class="section-content">
                    {processed_content}
                </div>
            </div>
'''
        
        html_template += '''
        </div>
    </div>
</body>
</html>'''
        
        return html_template
    
    try:
        sections = parse_txt_file(filename)
        html_content = generate_html(sections)
        
        base_name = os.path.splitext(filename)[0]
        html_filename = f"professional_proposal.html"
        
        with open(html_filename, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"✅ Professional proposal generated: {html_filename}")
        
        if output_format in ['pdf', 'both']:
            try:
                import weasyprint
                pdf_filename = f"professional_proposal.pdf"
                weasyprint.HTML(html_filename).write_pdf(pdf_filename)
                print(f"✅ PDF proposal generated: {pdf_filename}")
                return pdf_filename if output_format == 'pdf' else html_filename
            except ImportError:
                print("⚠️  WeasyPrint not installed. Install with: pip install weasyprint")
                return html_filename
            except Exception as e:
                print(f"⚠️  PDF generation failed: {e}")
                return html_filename
        
        return html_filename
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return None


# # Example usage
# if __name__ == "__main__":
#     result = generate_presentation(
#         filename="output.txt",
#         logo_url='https://static.wixstatic.com/media/cb6b3d_5c8f2b020ebe48b69bc8c163cc480156~mv2.png/v1/fill/w_60,h_60,al_c,q_85,usm_0.66_1.00_0.01,enc_avif,quality_auto/GrowthSutra%20Logo.png',
#         logo_url_2="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRMakCGZDIC1NnpHpIWfCXh7jvtULnbMNjPUQ&s",
#         output_format="pdf"
#     )
    
#     if result:
#         print(f"🎉 Professional sales proposal ready: {result}")
#     else:
#         print("❌ Failed to generate proposal")

# Example usage
if __name__ == "__main__":
    result = generate_presentation(
        filename="output.txt",
        logo_url='https://static.wixstatic.com/media/cb6b3d_5c8f2b020ebe48b69bc8c163cc480156~mv2.png/v1/fill/w_60,h_60,al_c,q_85,usm_0.66_1.00_0.01,enc_avif,quality_auto/GrowthSutra%20Logo.png',
        logo_url_2="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRMakCGZDIC1NnpHpIWfCXh7jvtULnbMNjPUQ&s",
        output_format="pdf"
    )
    
    if result:
        print(f"🎉 Professional sales proposal ready: {result}")
    else:
        print("❌ Failed to generate proposal")