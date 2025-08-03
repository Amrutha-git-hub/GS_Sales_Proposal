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
import streamlit as st
from datetime import datetime

def inline_editable_html_component(initial_html="", height=800, key=None):
    """
    Simplified HTML editor with inline editing capabilities.
    
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
    
    # Simplified editable HTML without toolbar
    simplified_html_template = f"""
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
                min-height: 100vh;
            }}
            
            .editor-container {{
                background: white;
                border-radius: 8px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                padding: 20px;
                min-height: 500px;
            }}
            
            [contenteditable="true"] {{
                outline: none;
                transition: all 0.2s ease;
                border-radius: 4px;
                padding: 4px;
                min-height: 20px;
            }}
            
            [contenteditable="true"]:hover {{
                background-color: rgba(0, 123, 255, 0.05);
                box-shadow: 0 0 0 2px rgba(0, 123, 255, 0.1);
            }}
            
            [contenteditable="true"]:focus {{
                outline: none;
                background-color: rgba(40, 167, 69, 0.05);
                box-shadow: 0 0 0 2px rgba(40, 167, 69, 0.2);
            }}
            
            .status-notification {{
                position: fixed;
                top: 20px;
                right: 20px;
                background: #28a745;
                color: white;
                padding: 12px 20px;
                border-radius: 25px;
                font-size: 14px;
                z-index: 1000;
                display: none;
                animation: slideIn 0.3s ease;
                box-shadow: 0 4px 15px rgba(40, 167, 69, 0.3);
            }}
            
            @keyframes slideIn {{
                from {{ opacity: 0; transform: translateX(100px); }}
                to {{ opacity: 1; transform: translateX(0); }}
            }}
            
            .edit-mode {{
                border: 2px solid #007bff;
                border-radius: 8px;
                padding: 15px;
                margin: 10px 0;
                position: relative;
            }}
            
            .edit-mode::before {{
                content: "✏️ Click on any text to edit";
                position: absolute;
                top: -10px;
                left: 15px;
                background: #007bff;
                color: white;
                padding: 4px 12px;
                border-radius: 12px;
                font-size: 12px;
                font-weight: 500;
            }}
        </style>
    </head>
    <body>
        <div class="status-notification" id="statusNotification">💾 Changes saved automatically!</div>
        
        <div class="editor-container">
            <div id="editableContent" class="edit-mode">
                {current_content}
            </div>
        </div>
        
        <div class="toolbar">
            <button disabled class="toggle-button">
                <span id="toggleText">🔒 Lock Edit Mode</span>
            </button>
            <button disabled class="add-button">+ Add Paragraph</button>
            <button disabled class="add-button">+ Add Heading</button>
            <button disabled class="save-button">💾 Save Changes</button>
            <button disabled class="export-button">📄 Export HTML</button>
            
            <div class="toolbar-status">
                <span class="word-count" id="wordCount">Words: 0</span>
            </div>
        </div>
        
        <!-- Hidden input to communicate with Streamlit -->
        <input type="hidden" id="hiddenContent" value="">
        
        <script>
            let editableContent = document.getElementById('editableContent');
            let statusNotification = document.getElementById('statusNotification');
            let hiddenContent = document.getElementById('hiddenContent');
            let saveTimeout;
            
            // Make elements editable
            function makeEditable(element) {{
                let textElements = element.querySelectorAll('p, h1, h2, h3, h4, h5, h6, span, div, td, th, li, a, button, label');
                textElements.forEach(el => {{
                    el.setAttribute('contenteditable', 'true');
                    el.addEventListener('input', handleEdit);
                    el.addEventListener('keydown', handleKeyDown);
                }});
            }}
            
            // Handle edit events
            function handleEdit() {{
                clearTimeout(saveTimeout);
                updateWordCount();
                
                // Update hidden field immediately
                hiddenContent.value = editableContent.innerHTML;
                
                saveTimeout = setTimeout(() => {{
                    showNotification('💾 Changes auto-saved!');
                    window.editedHTML = editableContent.innerHTML;
                }}, 1000);
            }}
            
            // Show notification
            function showNotification(message) {{
                statusNotification.innerHTML = message;
                statusNotification.style.display = 'block';
                setTimeout(() => {{
                    statusNotification.style.display = 'none';
                }}, 3000);
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
            
            // Update word count
            function updateWordCount() {{
                let text = editableContent.textContent || '';
                let words = text.trim().split(/\s+/).filter(word => word.length > 0).length;
                wordCount.textContent = `Words: ${{words}}`;
            }}
            
            // Initialize
            makeEditable(editableContent);
            updateWordCount();
            window.editedHTML = editableContent.innerHTML;
            hiddenContent.value = editableContent.innerHTML;
            
            // Auto-save every 30 seconds
            setInterval(() => {{
                hiddenContent.value = editableContent.innerHTML;
                window.editedHTML = editableContent.innerHTML;
            }}, 30000);
            
            // Show welcome message
            setTimeout(() => {{
                showNotification('🎉 HTML Editor ready! Click on any text to edit.');
            }}, 1000);
        </script>
    </body>
    </html>
    """
    
    # Render the simplified editor
    component_value = st.components.v1.html(
        simplified_html_template,
        height=height,
        scrolling=True
    )
    
    return current_content