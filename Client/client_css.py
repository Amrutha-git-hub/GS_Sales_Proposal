client_css = """
<style>
    .client-section {
        background: #2a2a2a;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #667eea;
        margin-bottom: 1rem;
        color: #f8f9fa;
    }
    
    .url-section {
        background: #2a2a2a;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #764ba2;
        margin-bottom: 1rem;
        color: #f8f9fa;
    }
    
    .document-section {
        background: #2a2a2a;
        padding: 1.5rem;
        border-radius: 10px;
        border: 2px solid #3a3a3a;
        margin-bottom: 1rem;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
        color: #f8f9fa;
    }
    
    .pain-points-section {
        background: #2a2a2a;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #ffc107;
        color: #f8f9fa;
    }
    
    .roles-section {
        background: #2a2a2a;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #2196f3;
        color: #f8f9fa;
    }
    
    .priorities-section {
        background: #2a2a2a;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #9c27b0;
        color: #f8f9fa;
    }
    
    .ai-suggestion-section {
        background: #2a2a2a;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #00bcd4;
        color: #f8f9fa;
    }
    
    .upload-section {
        border: 2px dashed #667eea;
        border-radius: 10px;
        padding: 2rem;
        text-align: center;
        background: #2a2a2a;
        color: #f8f9fa;
    }
    
    /* Style section headers */
    .section-header {
        color: #f8f9fa;
        font-size: 1.2rem;
        font-weight: 600;
        margin-bottom: 1rem;
    }
    
    /* Mandatory field styling */
    .mandatory-label {
        color: #e74c3c;
        font-weight: 600;
    }
    
    .field-warning {
        color: #e74c3c;
        font-size: 0.85rem;
        margin-top: 0.25rem;
        font-weight: 500;
        background: rgba(231, 76, 60, 0.1);
        padding: 0.5rem;
        border-radius: 4px;
        border-left: 3px solid #e74c3c;
    }
    
    .optional-label {
        color: #95a5a6;
        font-size: 0.8rem;
        font-style: italic;
    }
    
    .ai-label {
        color: #00bcd4;
        font-size: 0.8rem;
        font-style: italic;
    }
    
    /* Custom styling for URL buttons */
    .url-button-container {
        display: flex;
        gap: 5px;
        align-items: center;
    }
    
    .url-button {
        background: #667eea;
        color: white;
        border: none;
        padding: 8px 12px;
        border-radius: 6px;
        cursor: pointer;
        font-size: 14px;
        transition: background-color 0.3s;
    }
    
    .url-button:hover {
        background: #5a6fd8;
    }
    
    /* Summary item styling */
    .summary-item {
        background: #2a2a2a;
        border: 1px solid #3a3a3a;
        border-radius: 8px;
        padding: 12px;
        margin-bottom: 8px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        color: #f8f9fa;
    }
    
    .summary-key {
        font-weight: 600;
        color: #667eea;
    }
    
    .add-button {
        background: #28a745;
        color: white;
        border: none;
        padding: 6px 12px;
        border-radius: 4px;
        cursor: pointer;
        font-size: 12px;
        font-weight: bold;
    }
    
    .add-button:hover {
        background: #218838;
    }
    
    .summary-buttons {
        display: flex;
        gap: 8px;
        margin-bottom: 12px;
    }
    
    .summary-control-btn {
        background: #007bff;
        color: white;
        border: none;
        padding: 6px 12px;
        border-radius: 4px;
        cursor: pointer;
        font-size: 12px;
    }
    
    .summary-control-btn:hover {
        background: #0056b3;
    }
    
    /* Fixed tooltip label alignment */
    .tooltip-label {
        font-size: 16px;
        font-weight: bold;
        margin-bottom: 8px;
        display: flex;
        align-items: center;
        gap: 6px;
        height: 24px;
        line-height: 24px;
        min-height: 32px;
        display: flex;
        align-items: flex-end;
    }
    
    .tooltip-icon {
        position: relative;
        display: inline-block;
        cursor: pointer;
        margin-left: 0;
    }
    
    .tooltip-icon::after {
        content: attr(data-tooltip);
        visibility: hidden;
        width: 250px;
        background-color: #555;
        color: #fff;
        text-align: left;
        border-radius: 6px;
        padding: 8px;
        position: absolute;
        z-index: 1;
        bottom: 125%;
        left: 50%;
        margin-left: -125px;
        opacity: 0;
        transition: opacity 0.3s;
    }
    
    .tooltip-icon:hover::after {
        visibility: visible;
        opacity: 1;
    }



</style>
"""