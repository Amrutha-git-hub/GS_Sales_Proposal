import requests
from io import BytesIO
from colorthief import ColorThief


def rgb_to_hex(rgb):
    return '#{:02x}{:02x}{:02x}'.format(*rgb)

def get_color_from_image(image_url):
    response = requests.get(image_url)
    img_file = BytesIO(response.content)
    color_thief = ColorThief(img_file)
    palette = color_thief.get_palette(color_count=6)
    hex_colors = [rgb_to_hex(color) for color in palette]
    return hex_colors



def clean_to_list(result:str) :
    result = result.strip()
    if result.startswith('```python'):
        result = result[len('```python'):].strip()
    elif result.startswith('```json'):
        result = result[len('```json'):].strip()
    elif result.startswith('```'):
        result = result[len('```'):].strip()
    if result.endswith('```'):
        result = result[:-3].strip()
    return result

import streamlit as st
from datetime import datetime

def inline_editable_html_component(initial_html="", height=800, key=None):
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
def edit_html(html_content):
    edited_html = inline_editable_html_component(
        initial_html=html_content,
        height=800,
        key="main_editor"
    )
    return edited_html
    

