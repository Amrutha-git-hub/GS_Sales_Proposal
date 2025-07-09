import streamlit as st
from datetime import datetime

def inline_editable_html_component(initial_html="", height=600, key=None):
    """
    Advanced HTML editor with direct inline editing, toolbar, and enhanced features.
    
    Args:
        initial_html (str): Initial HTML content to display
        height (int): Height of the component in pixels
        key (str): Unique key for the component (used for session state)
    
    Returns:
        str: The edited HTML content
    """
    
    if key is None:
        key = "inline_html_editor"
    
    # Initialize session state
    if f"{key}_content" not in st.session_state:
        st.session_state[f"{key}_content"] = initial_html
    
    current_content = st.session_state[f"{key}_content"]
    
    # Enhanced editable HTML with toolbar and advanced features
    advanced_html_template = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 20px;
                background-color: #f8f9fa;
            }}
            
            .editor-container {{
                background: white;
                border-radius: 8px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                padding: 20px;
                margin-bottom: 20px;
            }}
            
            .toolbar {{
                position: sticky;
                top: 0;
                background: #343a40;
                color: white;
                padding: 10px;
                border-radius: 5px;
                margin-bottom: 20px;
                display: flex;
                gap: 10px;
                align-items: center;
                z-index: 100;
            }}
            
            .toolbar button {{
                background: #007bff;
                color: white;
                border: none;
                padding: 5px 10px;
                border-radius: 3px;
                cursor: pointer;
                font-size: 12px;
            }}
            
            .toolbar button:hover {{
                background: #0056b3;
            }}
            
            [contenteditable="true"] {{
                outline: none;
                transition: all 0.2s ease;
                border-radius: 4px;
                padding: 2px;
            }}
            
            [contenteditable="true"]:hover {{
                background-color: rgba(0, 123, 255, 0.05);
            }}
            
            [contenteditable="true"]:focus {{
                outline: none;
                background-color: rgba(40, 167, 69, 0.05);
            }}
            
            .status-bar {{
                position: fixed;
                bottom: 20px;
                right: 20px;
                background: #28a745;
                color: white;
                padding: 8px 16px;
                border-radius: 20px;
                font-size: 12px;
                z-index: 1000;
                display: none;
                animation: fadeIn 0.3s ease;
            }}
            
            @keyframes fadeIn {{
                from {{ opacity: 0; transform: translateY(10px); }}
                to {{ opacity: 1; transform: translateY(0); }}
            }}
            
            .edit-mode {{
                border: 2px solid #007bff;
                border-radius: 8px;
                padding: 10px;
                margin: 10px 0;
            }}
        </style>
    </head>
    <body>
        <div class="toolbar">
            <span>🔧 Edit Mode Active</span>
            <button onclick="toggleEditMode()">Toggle Edit Mode</button>
            <button onclick="addParagraph()">+ Add Paragraph</button>
            <button onclick="addHeading()">+ Add Heading</button>
            <button onclick="exportHTML()">Export HTML</button>
            <span id="wordCount">Words: 0</span>
        </div>
        
        <div class="status-bar" id="statusBar">💾 Changes saved automatically!</div>
        
        <div class="editor-container">
            <div id="editableContent" class="edit-mode">
                {current_content}
            </div>
        </div>
        
        <script>
            let editableContent = document.getElementById('editableContent');
            let statusBar = document.getElementById('statusBar');
            let wordCount = document.getElementById('wordCount');
            let saveTimeout;
            let editMode = true;
            
            // Make elements editable
            function makeEditable(element) {{
                let textElements = element.querySelectorAll('p, h1, h2, h3, h4, h5, h6, span, div, td, th, li, a, button, label');
                textElements.forEach(el => {{
                    if (editMode) {{
                        el.setAttribute('contenteditable', 'true');
                        el.addEventListener('input', handleEdit);
                        el.addEventListener('keydown', handleKeyDown);
                    }} else {{
                        el.removeAttribute('contenteditable');
                    }}
                }});
            }}
            
            // Handle edit events
            function handleEdit() {{
                clearTimeout(saveTimeout);
                updateWordCount();
                
                saveTimeout = setTimeout(() => {{
                    statusBar.style.display = 'block';
                    setTimeout(() => {{
                        statusBar.style.display = 'none';
                    }}, 2000);
                    
                    window.editedHTML = editableContent.innerHTML;
                }}, 1000);
            }}
            
            // Handle keyboard shortcuts
            function handleKeyDown(e) {{
                if (e.ctrlKey) {{
                    switch(e.key) {{
                        case 'b':
                            e.preventDefault();
                            document.execCommand('bold');
                            break;
                        case 'i':
                            e.preventDefault();
                            document.execCommand('italic');
                            break;
                        case 'u':
                            e.preventDefault();
                            document.execCommand('underline');
                            break;
                    }}
                }}
            }}
            
            // Toggle edit mode
            function toggleEditMode() {{
                editMode = !editMode;
                makeEditable(editableContent);
                editableContent.className = editMode ? 'edit-mode' : '';
            }}
            
            // Add new paragraph
            function addParagraph() {{
                let p = document.createElement('p');
                p.textContent = 'New paragraph - click to edit';
                p.setAttribute('contenteditable', 'true');
                p.addEventListener('input', handleEdit);
                p.addEventListener('keydown', handleKeyDown);
                editableContent.appendChild(p);
                p.focus();
            }}
            
            // Add new heading
            function addHeading() {{
                let h2 = document.createElement('h2');
                h2.textContent = 'New Heading - click to edit';
                h2.setAttribute('contenteditable', 'true');
                h2.addEventListener('input', handleEdit);
                h2.addEventListener('keydown', handleKeyDown);
                editableContent.appendChild(h2);
                h2.focus();
            }}
            
            // Update word count
            function updateWordCount() {{
                let text = editableContent.textContent || '';
                let words = text.trim().split(/\s+/).filter(word => word.length > 0).length;
                wordCount.textContent = `Words: ${{words}}`;
            }}
            
            // Export HTML
            function exportHTML() {{
                let html = `<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Edited HTML Page</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 20px;
            padding: 0;
            line-height: 1.6;
        }}
    </style>
</head>
<body>
    ${{editableContent.innerHTML}}
</body>
</html>`;
                
                let blob = new Blob([html], {{type: 'text/html'}});
                let url = URL.createObjectURL(blob);
                let a = document.createElement('a');
                a.href = url;
                a.download = 'edited_page.html';
                a.click();
                URL.revokeObjectURL(url);
            }}
            
            // Initialize
            makeEditable(editableContent);
            updateWordCount();
            window.editedHTML = editableContent.innerHTML;
            
            // Auto-save every 30 seconds
            setInterval(() => {{
                window.editedHTML = editableContent.innerHTML;
            }}, 30000);
        </script>
    </body>
    </html>
    """
    

    
    # Render the advanced editor
    st.components.v1.html(
        advanced_html_template,
        height=height,
        scrolling=True
    )
    
    # Download section
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col2:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"edited_page_{timestamp}.html"
        
        download_html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Edited HTML Page</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 20px;
            padding: 0;
            line-height: 1.6;
        }}
    </style>
</head>
<body>
    {current_content}
</body>
</html>"""
        
        st.download_button(
            label="📥 Download Edited HTML",
            data=download_html,
            file_name=filename,
            mime="text/html",
            key=f"{key}_download",
            help="Download the edited HTML as a complete webpage"
        )
    
    return current_content

# Example usage
def main():

    
    # Sample HTML content
    sample_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>title of the sales proposal</title>
    <meta name="description" content="Professional Sales Proposal - title of the sales proposal">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Playfair+Display:wght@400;500;600;700&display=swap');
        
        :root {
            --primary: #1a365d;
            --secondary: #2d3748;
            --accent: #3182ce;
            --success: #38a169;
            --background: #ffffff;
            --surface: #f7fafc;
            --text: #2d3748;
            --text-light: #718096;
            --border: #e2e8f0;
            --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
            --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
            --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
            --shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
            --radius-sm: 0.375rem;
            --radius-md: 0.5rem;
            --radius-lg: 0.75rem;
            --radius-xl: 1rem;
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        @page {
            size: A4;
            margin: 0;
        }

        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
            line-height: 1.6;
            color: var(--text);
            background: var(--background);
            font-size: 16px;
            font-weight: 400;
            -webkit-font-smoothing: antialiased;
            -moz-osx-font-smoothing: grayscale;
        }

        /* ENHANCED PREMIUM COVER PAGE WITH REDUCED TRANSPARENCY */
        .cover-page {
            width: 100vw;
            height: 100vh;
            background: linear-gradient(135deg, 
                #1a365df2 0%, 
                #2d3748f2 50%, 
                #3182cef2 100%),
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
        }

        .cover-page::before {
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
        }

        /* ENHANCED LOGO SECTION */
        .cover-logos {
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 3rem;
            margin-bottom: 3rem;
            z-index: 10;
            position: relative;
            width: 100%;
            max-width: 800px;
        }

        .cover-logo {
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
        }

        .cover-logo:hover {
            transform: translateY(-5px) scale(1.02);
            box-shadow: 0 30px 60px rgba(0, 0, 0, 0.25);
        }

        .cover-logo img {
            max-width: 100%;
            max-height: 100%;
            object-fit: contain;
            filter: drop-shadow(0 4px 6px rgba(0, 0, 0, 0.1));
        }

        .cover-logo-1 {
            background: rgba(255, 255, 255, 0.98) url('https://static.wixstatic.com/media/cb6b3d_5c8f2b020ebe48b69bc8c163cc480156~mv2.png/v1/fill/w_60,h_60,al_c,q_85,usm_0.66_1.00_0.01,enc_avif,quality_auto/GrowthSutra%20Logo.png') no-repeat center;
            background-size: contain;
        }

        .cover-logo-2 {
            background: rgba(255, 255, 255, 0.98) url('https://benori.com/assets/web/images/Benori_Logo.svg') no-repeat center;
            background-size: contain;
        }

        /* ENHANCED TITLE SECTION WITH BETTER VISIBILITY */
        .cover-title {
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
        }

        /* MODERN CONTENT PAGES */
        .content-page {
            page-break-before: always;
            position: relative;
            padding: 3rem;
            min-height: 100vh;
            background: var(--background);
        }

        .presentation-container {
            max-width: 100%;
            padding: 0;
            background: var(--background);
            position: relative;
        }

        .main-title {
            font-family: 'Playfair Display', serif;
            font-size: 2.5rem;
            font-weight: 700;
            color: var(--primary);
            text-align: center;
            margin-bottom: 3rem;
            padding-bottom: 1rem;
            position: relative;
        }

        .main-title::after {
            content: '';
            position: absolute;
            bottom: 0;
            left: 50%;
            transform: translateX(-50%);
            width: 80px;
            height: 4px;
            background: linear-gradient(90deg, var(--accent), var(--success));
            border-radius: 2px;
        }

        .section {
            margin-bottom: 2.5rem;
            padding: 2rem;
            background: var(--surface);
            border-radius: var(--radius-lg);
            border: 1px solid var(--border);
            box-shadow: var(--shadow-sm);
            page-break-inside: avoid;
            position: relative;
            overflow: hidden;
        }

        .section::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 4px;
            height: 100%;
            background: linear-gradient(180deg, var(--accent), var(--success));
        }

        .section-title {
            font-family: 'Inter', sans-serif;
            font-size: 1.5rem;
            font-weight: 600;
            color: var(--primary);
            margin-bottom: 1rem;
            letter-spacing: -0.025em;
        }

        .section-content {
            font-size: 1rem;
            line-height: 1.7;
            color: var(--text);
        }

        .section-content p {
            margin-bottom: 1rem;
        }

        .section-content p:last-child {
            margin-bottom: 0;
        }

        .section-content ul {
            margin-left: 1.5rem;
            margin-top: 0.5rem;
        }

        .section-content li {
            margin-bottom: 0.5rem;
            position: relative;
        }

        .section-content li::marker {
            color: var(--accent);
        }

        .company-info {
            background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
            color: white;
            padding: 2.5rem;
            margin: 2rem 0;
            border-radius: var(--radius-lg);
            box-shadow: var(--shadow-lg);
            page-break-inside: avoid;
            position: relative;
            overflow: hidden;
        }

        .company-info::before {
            content: '';
            position: absolute;
            top: 0;
            right: 0;
            width: 200px;
            height: 200px;
            background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
            border-radius: 50%;
            transform: translate(50%, -50%);
        }

        .company-title {
            font-family: 'Playfair Display', serif;
            font-size: 1.75rem;
            font-weight: 600;
            margin-bottom: 1rem;
            color: white;
            position: relative;
            z-index: 10;
        }

        .company-content {
            font-size: 1rem;
            line-height: 1.6;
            color: rgba(255,255,255,0.95);
            position: relative;
            z-index: 10;
        }

        .pricing-highlight {
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
        }

        .pricing-highlight::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: linear-gradient(90deg, var(--success), var(--accent));
        }

        .price-amount {
            font-family: 'Inter', sans-serif;
            font-size: 3rem;
            font-weight: 800;
            color: var(--success);
            margin-bottom: 1rem;
            text-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }

        .cta-section {
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
        }

        .cta-section::before {
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
        }

        .cta-title {
            font-family: 'Playfair Display', serif;
            font-size: 2rem;
            font-weight: 600;
            color: white;
            margin-bottom: 1rem;
            position: relative;
            z-index: 10;
        }

        .cta-content {
            font-size: 1.1rem;
            line-height: 1.6;
            color: rgba(255,255,255,0.95);
            position: relative;
            z-index: 10;
        }

        .phase-section {
            background: white;
            border: 2px solid var(--border);
            padding: 2rem;
            margin: 1.5rem 0;
            border-radius: var(--radius-lg);
            box-shadow: var(--shadow-sm);
            page-break-inside: avoid;
            transition: box-shadow 0.3s ease;
        }

        .phase-section:hover {
            box-shadow: var(--shadow-md);
        }

        .phase-title {
            font-size: 1.25rem;
            font-weight: 600;
            color: var(--primary);
            margin-bottom: 1rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }

        .phase-title::before {
            content: '';
            width: 8px;
            height: 8px;
            background: var(--accent);
            border-radius: 50%;
        }

        .timeline-item {
            background: white;
            border-left: 4px solid var(--success);
            margin: 1rem 0;
            padding: 1.5rem;
            border-radius: 0 var(--radius-md) var(--radius-md) 0;
            box-shadow: var(--shadow-sm);
            page-break-inside: avoid;
            position: relative;
        }

        .timeline-item::before {
            content: '';
            position: absolute;
            left: -8px;
            top: 1.5rem;
            width: 12px;
            height: 12px;
            background: var(--success);
            border-radius: 50%;
            border: 3px solid white;
        }

        .timeline-week {
            font-weight: 600;
            color: var(--success);
            font-size: 1rem;
            margin-bottom: 0.5rem;
        }

        /* ENHANCED TYPOGRAPHY */
        h1, h2, h3, h4, h5, h6 {
            font-weight: 600;
            line-height: 1.2;
            margin-bottom: 0.5rem;
        }

        strong {
            font-weight: 600;
            color: var(--primary);
        }

        em {
            font-style: italic;
            color: var(--accent);
        }

        /* RESPONSIVE DESIGN */
        @media (max-width: 768px) {
            .cover-logos {
                flex-direction: column;
                gap: 2rem;
                margin-bottom: 2rem;
            }
            
            .cover-logo {
                width: 160px;
                height: 160px;
            }
            
            .cover-title {
                font-size: clamp(1.5rem, 4vw, 2.5rem);
            }
            
            .content-page {
                padding: 2rem;
            }
            
            .section {
                padding: 1.5rem;
            }
        }

        /* PDF PRINT OPTIMIZATION */
        @media print {
            .cover-page {
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
                    #1a365df2 0%, 
                    #2d3748f2 50%, 
                    #3182cef2 100%) !important;
                print-color-adjust: exact !important;
                -webkit-print-color-adjust: exact !important;
            }
            
            .cover-logos {
                margin-bottom: 20mm !important;
            }
            
            .cover-logo {
                width: 80mm !important;
                height: 80mm !important;
                print-color-adjust: exact !important;
                -webkit-print-color-adjust: exact !important;
                background-color: rgba(255, 255, 255, 0.98) !important;
            }
            
            .cover-title {
                font-size: 24pt !important;
                line-height: 1.2 !important;
                color: white !important;
                print-color-adjust: exact !important;
                -webkit-print-color-adjust: exact !important;
                text-shadow: 0 2px 4px rgba(0,0,0,0.5) !important;
                -webkit-text-fill-color: white !important;
                background: none !important;
            }
            
            .content-page {
                page-break-before: always !important;
                margin: 15mm !important;
                padding: 0 !important;
                min-height: calc(297mm - 30mm) !important;
            }
            
            .presentation-container {
                padding: 0 !important;
            }
            
            .section,
            .company-info,
            .pricing-highlight,
            .cta-section,
            .phase-section,
            .timeline-item {
                page-break-inside: avoid !important;
                orphans: 2 !important;
                widows: 2 !important;
            }
            
            .cover-logo:hover {
                transform: none !important;
            }
        }
        </style>
</head>
<body>
    <!-- ENHANCED PREMIUM COVER PAGE WITH PROPER TITLE -->
    <div class="cover-page">
        <div class="cover-logos">
            <div class="cover-logo cover-logo-1"></div>
            <div class="cover-logo cover-logo-2"></div>
        </div>
        <h1 class="cover-title">title of the sales proposal</h1>
    </div>
    
    <!-- MODERN CONTENT PAGES -->
    <div class="content-page">
        <div class="presentation-container">

            <div class="section">
                <h3 class="section-title">title of the sales proposal</h3>
                <div class="section-content">
                    <p>Strategic Growth Partnership Proposal</p>
                </div>
            </div>

            <div class="section">
                <h3 class="section-title">Executive Summary</h3>
                <div class="section-content">
                    <p>This proposal outlines a strategic partnership designed to accelerate your company's growth trajectory. We understand the challenges businesses face in today's dynamic market, from evolving customer expectations to the need for innovative solutions. Our approach focuses on providing tailored strategies and actionable insights that drive measurable results. This partnership is built on a foundation of collaboration, transparency, and a shared commitment to achieving your business objectives. We are confident that our expertise and proven methodologies will empower your organization to reach new heights of success. We look forward to embarking on this journey with you.</p>
                </div>
            </div>

            <div class="section">
                <h3 class="section-title">Understanding Your Needs</h3>
                <div class="section-content">
                    <p>We recognize that every organization has unique challenges and opportunities. While we lack specific details regarding your current needs, we understand that growth and adaptation are paramount for sustained success. Our experience across various industries has equipped us with the ability to quickly assess your specific situation, identify key areas for improvement, and develop customized solutions that address your precise requirements. We're committed to a collaborative discovery process to fully understand your goals, pain points, and aspirations. By working closely with your team, we can ensure that our proposed strategies are perfectly aligned with your overall business objectives and deliver maximum impact.</p>
                </div>
            </div>

            <div class="section">
                <h3 class="section-title">Proposed Solution</h3>
                <div class="section-content">
                    <p>Our proposed solution is a comprehensive and adaptable framework designed to drive sustainable growth. While specific solutions will be tailored to your needs during the discovery phase, our general approach centers around strategic planning, innovative solutions, and data-driven decision-making. We will leverage our expertise in market analysis, customer engagement, and operational efficiency to identify opportunities for improvement and develop actionable strategies. Our team will work closely with you to implement these strategies, track progress, and make necessary adjustments to ensure optimal results. We are committed to providing you with the tools and support you need to achieve your growth objectives and build a more resilient and successful organization.</p>
                </div>
            </div>

            <div class="phase-section">
                <h3 class="phase-title">Scope of Work / Project Breakdown</h3>
                <div class="section-content">
                <p><strong>Phase 1: Discovery & Planning (Week 1-2)</strong></p>
<ul>
<li><strong>Kick-off Meeting:</strong> Conduct a comprehensive kickoff meeting with key stakeholders to establish project goals, timelines, and communication protocols.</li>
<li><strong>Requirements Gathering:</strong> Conduct detailed interviews and workshops to gather specific business requirements, pain points, and desired outcomes.</li>
<li><strong>Market Analysis:</strong> Perform a thorough analysis of the competitive landscape, industry trends, and market opportunities.</li>
<li><strong>Stakeholder Mapping:</strong> Identify and analyze key stakeholders to ensure alignment and effective communication throughout the project.</li>
<li><strong>KPI Definition:</strong> Define key performance indicators (KPIs) to measure the success of the project and track progress towards achieving business objectives.</li>
</ul>
<p><strong>Phase 2: Strategy & Solution Design (Week 3-4)</strong></p>
<ul>
<li><strong>Solution Conceptualization:</strong> Develop innovative solutions that address the identified business challenges and leverage industry best practices.</li>
<li><strong>Strategy Development:</strong> Create a comprehensive growth strategy that aligns with your business goals and market opportunities.</li>
<li><strong>Technology Assessment:</strong> Evaluate existing technology infrastructure and identify potential areas for improvement or integration.</li>
<li><strong>Roadmap Creation:</strong> Develop a detailed roadmap outlining the key milestones, activities, and resources required to implement the proposed solution.</li>
<li><strong>Risk Assessment:</strong> Identify potential risks and develop mitigation strategies to ensure project success.</li>
</ul>
<p><strong>Phase 3: Implementation & Execution (Week 5-8)</strong></p>
<ul>
<li><strong>Project Management:</strong> Utilize agile project management methodologies to ensure efficient execution and timely delivery of project milestones.</li>
<li><strong>Team Coordination:</strong> Coordinate internal and external teams to ensure seamless collaboration and effective communication.</li>
<li><strong>Change Management:</strong> Implement change management strategies to minimize disruption and ensure smooth adoption of the new solution.</li>
<li><strong>Training & Support:</strong> Provide comprehensive training and support to your team to ensure they are equipped to effectively utilize the new solution.</li>
<li><strong>Performance Monitoring:</strong> Continuously monitor performance against defined KPIs and make necessary adjustments to optimize results.</li>
</ul>
<p><strong>Phase 4: Optimization & Reporting (Week 9-12)</strong></p>
<ul>
<li><strong>Data Analysis:</strong> Analyze data to identify areas for improvement and optimize the performance of the implemented solution.</li>
<li><strong>Reporting & Communication:</strong> Provide regular reports and updates to stakeholders on project progress and performance.</li>
<li><strong>Continuous Improvement:</strong> Continuously identify and implement improvements to ensure the solution remains aligned with evolving business needs.</li>
<li><strong>Knowledge Transfer:</strong> Transfer knowledge and best practices to your team to ensure long-term sustainability of the solution.</li>
<li><strong>Post-Implementation Review:</strong> Conduct a post-implementation review to assess the overall success of the project and identify lessons learned.</li>
</ul>
                </div>
            </div>

            <div class="section">
                <h3 class="section-title">Deliverables</h3>
                <div class="section-content">
                    <p>Our engagement will provide several key deliverables designed to drive tangible results. These include a comprehensive strategic plan tailored to your specific needs, a detailed roadmap outlining implementation steps, and regular performance reports to track progress. You will also receive access to our team of experts, who will provide ongoing support and guidance throughout the project. The final deliverable will be a fully implemented solution that addresses your key business challenges and positions you for sustained growth. We are committed to delivering high-quality deliverables that exceed your expectations and provide lasting value. We will also provide documentation and training to ensure your team can successfully manage the solution in the long term.</p>
                </div>
            </div>

            <div class="phase-section">
                <h3 class="phase-title">Timeline</h3>
                <div class="section-content">
                <p>The project timeline is structured to ensure efficient execution and timely delivery of results. The initial phase, Discovery & Planning, will take approximately 2 weeks. This will be followed by Strategy & Solution Design, which will also take around 2 weeks. Implementation & Execution is expected to take 4 weeks, with the final Optimization & Reporting phase spanning 4 weeks. This is a flexible timeline and will be refined based on the specific needs of your organization during the initial discovery phase. We will provide regular updates and maintain open communication throughout the project to ensure everyone is informed of progress and any potential adjustments to the timeline. We are committed to delivering the project on time and within budget.</p>
                </div>
            </div>

            <div class="section">
                <h3 class="section-title">Investment / Pricing</h3>
                <div class="section-content">
                    <p>The investment for this strategic partnership will be customized based on the specific scope of work and your organization's unique requirements. Following the initial Discovery & Planning phase, we will provide a detailed pricing proposal that outlines the costs associated with each phase of the project. Our pricing is transparent and competitive, and we are committed to providing you with the best possible value for your investment. We offer flexible payment options to accommodate your budgetary constraints. We believe that this partnership represents a significant investment in your organization's future and will deliver a substantial return on investment in the form of increased revenue, improved efficiency, and enhanced customer satisfaction.</p>
                </div>
            </div>

            <div class="company-info">
                <h3 class="company-title">Our Team / About Us</h3>
                <div class="company-content">
                    <p>We are a team of experienced consultants, strategists, and technologists dedicated to helping businesses achieve their growth objectives. Our team has a proven track record of success across various industries, and we bring a wealth of knowledge and expertise to every project. We are passionate about innovation and committed to providing our clients with the highest quality service. Our collaborative approach ensures that we work closely with your team to understand your unique needs and develop solutions that are perfectly aligned with your business goals. We pride ourselves on our integrity, transparency, and commitment to delivering exceptional results. We believe that our team's expertise and dedication will be invaluable in helping your organization achieve its full potential.</p>
                </div>
            </div>

            <div class="section">
                <h3 class="section-title">Case Studies / Success Stories</h3>
                <div class="section-content">
                    <p>While we don't have specific case studies readily available, we can share examples of successful engagements we've undertaken in similar industries and with similar challenges. We have helped numerous organizations improve their operational efficiency, increase their revenue, and enhance their customer satisfaction. These engagements have involved developing and implementing strategic plans, optimizing marketing campaigns, and leveraging technology to drive innovation. We are confident that our experience and expertise can be applied to your organization to achieve similar results. During our initial consultation, we can provide more detailed examples of our past successes and discuss how we can help you achieve your specific business objectives. We are committed to providing you with the insights and tools you need to succeed.</p>
                </div>
            </div>

            <div class="section">
                <h3 class="section-title">Terms and Conditions</h3>
                <div class="section-content">
                    <p>This proposal is subject to our standard terms and conditions, which will be provided in a separate agreement. These terms and conditions cover aspects such as confidentiality, intellectual property rights, payment terms, and liability limitations. We are committed to ensuring that our relationship with you is based on transparency and mutual understanding. We encourage you to review the terms and conditions carefully and ask any questions you may have. We are confident that our terms and conditions are fair and reasonable and reflect our commitment to providing you with the best possible service. We are always willing to discuss and negotiate the terms and conditions to ensure they meet your specific needs.</p>
                </div>
            </div>

            <div class="cta-section">
                <h3 class="cta-title">Call to Action</h3>
                <div class="cta-content">
                    <p>We are excited about the opportunity to partner with you and help you achieve your growth objectives. We believe that our proposed solution represents a significant investment in your organization's future and will deliver a substantial return on investment. We encourage you to schedule a follow-up meeting to discuss this proposal in more detail and answer any questions you may have. We are confident that we can develop a customized solution that meets your specific needs and positions you for sustained success. We look forward to hearing from you soon and embarking on this journey together. Let's discuss how we can make this happen.</p>
                </div>
            </div>

        </div>
    </div>
</body>
</html>
    """
    
    # Use the advanced inline editor
    edited_html = inline_editable_html_component(
        initial_html=sample_html,
        height=600,
        key="main_editor"
    )
    


