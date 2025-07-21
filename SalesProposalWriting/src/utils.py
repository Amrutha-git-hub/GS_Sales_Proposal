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
    Advanced HTML editor with direct inline editing, bottom toolbar, and enhanced features.
    
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
    
    # Enhanced editable HTML with bottom toolbar and advanced features
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
                display: flex;
                flex-direction: column;
                min-height: 100vh;
            }}
            
            .editor-container {{
                background: white;
                border-radius: 8px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                padding: 20px;
                flex: 1;
                margin-bottom: 20px;
                min-height: 500px;
            }}
            
            .toolbar {{
                position: fixed;
                bottom: 0;
                left: 0;
                right: 0;
                background: #343a40;
                color: white;
                padding: 15px 20px;
                display: flex;
                gap: 15px;
                align-items: center;
                z-index: 100;
                box-shadow: 0 -2px 10px rgba(0,0,0,0.2);
                flex-wrap: wrap;
            }}
            
            .toolbar button {{
                background: #007bff;
                color: white;
                border: none;
                padding: 10px 15px;
                border-radius: 6px;
                cursor: pointer;
                font-size: 14px;
                font-weight: 500;
                transition: all 0.2s ease;
                white-space: nowrap;
            }}
            
            .toolbar button:hover {{
                background: #0056b3;
                transform: translateY(-2px);
            }}
            
            .toolbar-status {{
                margin-left: auto;
                font-size: 12px;
                color: #adb5bd;
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
                content: "✏️ Edit Mode Active - Click on any text to edit";
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
            
            .save-button {{
                background: #28a745 !important;
                font-weight: bold;
                box-shadow: 0 2px 8px rgba(40, 167, 69, 0.3);
            }}
            
            .save-button:hover {{
                background: #218838 !important;
                box-shadow: 0 4px 12px rgba(40, 167, 69, 0.4);
            }}
            
            .toggle-button {{
                background: #6c757d !important;
            }}
            
            .toggle-button:hover {{
                background: #5a6268 !important;
            }}
            
            .add-button {{
                background: #17a2b8 !important;
            }}
            
            .add-button:hover {{
                background: #138496 !important;
            }}
            
            .export-button {{
                background: #fd7e14 !important;
            }}
            
            .export-button:hover {{
                background: #e8630c !important;
            }}
            
            /* Add padding to body to prevent content from being hidden behind toolbar */
            body {{
                padding-bottom: 80px;
            }}
            
            .word-count {{
                background: #495057;
                padding: 8px 12px;
                border-radius: 15px;
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
            <button onclick="toggleEditMode()" class="toggle-button">
                <span id="toggleText">🔒 Lock Edit Mode</span>
            </button>
            <button onclick="addParagraph()" class="add-button">+ Add Paragraph</button>
            <button onclick="addHeading()" class="add-button">+ Add Heading</button>
            <button onclick="saveToStreamlit()" class="save-button">💾 Save Changes</button>
            <button onclick="exportHTML()" class="export-button">📄 Export HTML</button>
            
            <div class="toolbar-status">
                <span class="word-count" id="wordCount">Words: 0</span>
            </div>
        </div>
        
        <!-- Hidden input to communicate with Streamlit -->
        <input type="hidden" id="hiddenContent" value="">
        
        <script>
            let editableContent = document.getElementById('editableContent');
            let statusNotification = document.getElementById('statusNotification');
            let wordCount = document.getElementById('wordCount');
            let hiddenContent = document.getElementById('hiddenContent');
            let toggleText = document.getElementById('toggleText');
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
                        el.removeEventListener('input', handleEdit);
                        el.removeEventListener('keydown', handleKeyDown);
                    }}
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
            
            // Save to Streamlit session state
            function saveToStreamlit() {{
                hiddenContent.value = editableContent.innerHTML;
                
                // Trigger a form submission to update Streamlit
                let form = document.createElement('form');
                form.method = 'POST';
                form.action = '';
                form.style.display = 'none';
                
                let input = document.createElement('input');
                input.type = 'hidden';
                input.name = 'edited_content';
                input.value = editableContent.innerHTML;
                
                form.appendChild(input);
                document.body.appendChild(form);
                
                showNotification('💾 Changes saved to Streamlit!');
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
                        case 's':
                            e.preventDefault();
                            saveToStreamlit();
                            break;
                    }}
                }}
            }}
            
            // Toggle edit mode
            function toggleEditMode() {{
                editMode = !editMode;
                makeEditable(editableContent);
                
                if (editMode) {{
                    editableContent.className = 'edit-mode';
                    toggleText.textContent = '🔒 Lock Edit Mode';
                    showNotification('✏️ Edit mode activated!');
                }} else {{
                    editableContent.className = '';
                    toggleText.textContent = '✏️ Enable Edit Mode';
                    showNotification('🔒 Edit mode locked!');
                }}
            }}
            
            // Add new paragraph
            function addParagraph() {{
                if (!editMode) {{
                    showNotification('❌ Please enable edit mode first!');
                    return;
                }}
                
                let p = document.createElement('p');
                p.textContent = 'New paragraph - click to edit';
                p.setAttribute('contenteditable', 'true');
                p.addEventListener('input', handleEdit);
                p.addEventListener('keydown', handleKeyDown);
                editableContent.appendChild(p);
                p.focus();
                
                // Select all text in the new paragraph
                let range = document.createRange();
                range.selectNodeContents(p);
                let selection = window.getSelection();
                selection.removeAllRanges();
                selection.addRange(range);
                
                showNotification('📝 New paragraph added!');
            }}
            
            // Add new heading
            function addHeading() {{
                if (!editMode) {{
                    showNotification('❌ Please enable edit mode first!');
                    return;
                }}
                
                let h2 = document.createElement('h2');
                h2.textContent = 'New Heading - click to edit';
                h2.setAttribute('contenteditable', 'true');
                h2.addEventListener('input', handleEdit);
                h2.addEventListener('keydown', handleKeyDown);
                editableContent.appendChild(h2);
                h2.focus();
                
                // Select all text in the new heading
                let range = document.createRange();
                range.selectNodeContents(h2);
                let selection = window.getSelection();
                selection.removeAllRanges();
                selection.addRange(range);
                
                showNotification('📝 New heading added!');
            }}
            
            // Update word count
            function updateWordCount() {{
                let text = editableContent.textContent || '';
                let words = text.trim().split(/\s+/).filter(word => word.length > 0).length;
                wordCount.textContent = `Words: ${{words}}`;
            }}
            
            // Export HTML
            function exportHTML() {{
                // Create timestamp for filename
                const now = new Date();
                const timestamp = now.getFullYear().toString() + 
                                (now.getMonth() + 1).toString().padStart(2, '0') + 
                                now.getDate().toString().padStart(2, '0') + '_' +
                                now.getHours().toString().padStart(2, '0') + 
                                now.getMinutes().toString().padStart(2, '0') + 
                                now.getSeconds().toString().padStart(2, '0');
                
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
                
                try {{
                    let blob = new Blob([html], {{type: 'text/html'}});
                    let url = URL.createObjectURL(blob);
                    let a = document.createElement('a');
                    a.href = url;
                    a.download = `edited_page_${{timestamp}}.html`;
                    a.style.display = 'none';
                    document.body.appendChild(a);
                    a.click();
                    document.body.removeChild(a);
                    URL.revokeObjectURL(url);
                    
                    showNotification('📄 HTML file exported successfully!');
                    
                    // Also save to session state for Streamlit
                    hiddenContent.value = editableContent.innerHTML;
                    window.editedHTML = editableContent.innerHTML;
                    
                }} catch (error) {{
                    console.error('Export failed:', error);
                    showNotification('❌ Export failed. Please use the Streamlit download button below.');
                }}
            }}
            
            // Make exportHTML globally accessible
            window.exportHTML = exportHTML;
            
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
    
    # Render the advanced editor
    component_value = st.components.v1.html(
        advanced_html_template,
        height=height,
        scrolling=True
    )
    
    # Add a text area to capture the edited content
    # st.markdown("---")
    # st.markdown("**💾 Save and Download Options:**")
    
    # col1, col2 = st.columns([1, 1])
    
    # with col1:
    #     # Button to manually update the content
    #     if st.button("🔄 Update Content", key=f"{key}_update"):
    #         st.info("Click the 'Save Changes' button in the editor above to capture your edits.")
    
    # with col2:
    #     # Text area for manual content editing (hidden by default)
    #     with st.expander("📝 Manual Content Edit (Advanced)"):
    #         manual_content = st.text_area(
    #             "Edit HTML content directly:",
    #             value=current_content,
    #             height=200,
    #             key=f"{key}_manual"
    #         )
            
    #         if st.button("Apply Manual Changes", key=f"{key}_apply_manual"):
    #             st.session_state[f"{key}_content"] = manual_content
    #             st.rerun()
    
    # # Download section
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col2:
        # Use JavaScript to trigger the export function when clicked
        if st.button("📥 Download Current HTML", key=f"{key}_download", help="Click to download the current HTML content"):
            # Inject JavaScript to trigger the exportHTML function
            st.components.v1.html(
                """
                <script>
                    // Try to find the parent window's exportHTML function
                    if (window.parent && window.parent.exportHTML) {
                        window.parent.exportHTML();
                    } else {
                        // Fallback: try to find the function in any iframe
                        const iframes = window.parent.document.querySelectorAll('iframe');
                        for (let iframe of iframes) {
                            try {
                                if (iframe.contentWindow && iframe.contentWindow.exportHTML) {
                                    iframe.contentWindow.exportHTML();
                                    break;
                                }
                            } catch(e) {
                                // Continue searching if cross-origin error
                            }
                        }
                    }
                </script>
                """,
                height=0
            )
            st.success("🎉 Download started! Check your browser's download folder.")
        

    return current_content