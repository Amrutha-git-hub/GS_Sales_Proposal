import streamlit as st
import streamlit.components.v1 as components
import time
from datetime import datetime
import os
from Proposal_writing_tab.generate_proposal_css import *
from SalesProposalWriting_Agent.src.main import get_presentation,inline_editable_html_component,generate_pdf_from_html
from Common_Utils.logo_creator import create_text_image
from dotenv import load_dotenv

load_dotenv()

OUTPUT_DIR = os.getenv("OUTPUT_PATH")
def render_template_preview(template_name, template_key):
    """
    Renders a template preview card with actual HTML rendering
    """
    template_styles = {
        "modern_professional": {
            "preview_html": """
                <div style="width: 100%; height: 180px; background: #f8fafc; padding: 12px; border-radius: 8px; font-family: Arial, sans-serif;">
                    <div style="background: linear-gradient(135deg, #3b82f6        
        dp[0][0] = dp[0][1] = 0;0%, #1e40af 100%); padding: 12px; border-radius: 6px; margin-bottom: 12px; color: white; text-align: center;">
                        <div style="font-size: 14px; font-weight: bold;">PROJECT PROPOSAL</div>
                        <div style="font-size: 11px; opacity: 0.9;">Modern Professional Template</div>
                    </div>
                    <div style="background: white; padding: 12px; border-radius: 6px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); height: 100px;">
                        <div style="font-size: 12px; font-weight: bold; color: #1e293b; margin-bottom: 8px;">Executive Summary</div>
                        <div style="font-size: 10px; color: #64748b; line-height: 1.4; margin-bottom: 10px;">
                            Clean, professional design with modern typography and subtle gradients. Perfect for corporate clients and established businesses.
                        </div>
                        <div style="display: flex; gap: 4px; align-items: center;">
                            <div style="width: 30px; height: 4px; background: #3b82f6; border-radius: 2px;"></div>
                            <div style="width: 40px; height: 4px; background: #e2e8f0; border-radius: 2px;"></div>
                            <div style="width: 25px; height: 4px; background: #e2e8f0; border-radius: 2px;"></div>
                            <div style="font-size: 8px; color: #94a3b8; margin-left: 8px;">Progress</div>
                        </div>
                    </div>
                </div>
            """
        },
        "classic_business": {
            "preview_html": """
                <div style="width: 100%; height: 180px; background: #fafafa; padding: 12px; border-radius: 8px; font-family: Arial, sans-serif;">
                    <div style="background: #059669; padding: 12px; border-radius: 4px; margin-bottom: 12px; color: white; text-align: center;">
                        <div style="font-size: 14px; font-weight: bold;">BUSINESS PROPOSAL</div>
                        <div style="font-size: 11px; opacity: 0.9;">Classic Business Template</div>
                    </div>
                    <div style="background: white; padding: 12px; border: 1px solid #d1d5db; border-radius: 4px; height: 100px;">
                        <div style="font-size: 12px; font-weight: bold; color: #374151; margin-bottom: 8px;">Project Overview</div>
                        <div style="font-size: 10px; color: #6b7280; line-height: 1.4; margin-bottom: 10px;">
                            Traditional, trustworthy design with clean lines and professional formatting. Ideal for established businesses and formal presentations.
                        </div>
                        <div style="padding: 8px; background: #f9fafb; border-left: 4px solid #059669; font-size: 9px; color: #374151;">
                            <strong>Key Features:</strong> Professional layout, formal structure, corporate styling
                        </div>
                    </div>
                </div>
            """
        },
        "creative_bold": {
            "preview_html": """
                <div style="width: 100%; height: 180px; background: #fef3c7; padding: 12px; border-radius: 8px; font-family: Arial, sans-serif;">
                    <div style="background: linear-gradient(45deg, #f59e0b 0%, #d97706 100%); padding: 12px; border-radius: 8px; margin-bottom: 12px; color: white; text-align: center;">
                        <div style="font-size: 14px; font-weight: bold;">CREATIVE PROPOSAL</div>
                        <div style="font-size: 11px; opacity: 0.9;">Creative Bold Template</div>
                    </div>
                    <div style="background: white; padding: 12px; border-radius: 8px; border: 2px solid #f59e0b; height: 100px;">
                        <div style="font-size: 12px; font-weight: bold; color: #92400e; margin-bottom: 8px;">Innovation Hub</div>
                        <div style="font-size: 10px; color: #b45309; line-height: 1.4; margin-bottom: 10px;">
                            Bold, vibrant design with creative elements and dynamic layouts. Perfect for creative agencies, startups, and innovative projects.
                        </div>
                        <div style="display: flex; gap: 4px; align-items: center;">
                            <div style="width: 12px; height: 12px; background: #f59e0b; border-radius: 50%;"></div>
                            <div style="width: 12px; height: 12px; background: #fbbf24; border-radius: 50%;"></div>
                            <div style="width: 12px; height: 12px; background: #fcd34d; border-radius: 50%;"></div>
                            <div style="font-size: 8px; color: #92400e; margin-left: 8px;">Creative Elements</div>
                        </div>
                    </div>
                </div>
            """
        },
        "minimal_clean": {
            "preview_html": """
                <div style="width: 100%; height: 180px; background: #f8fafc; padding: 12px; border-radius: 8px; font-family: Arial, sans-serif;">
                    <div style="background: #6b7280; padding: 12px; margin-bottom: 12px; color: white; text-align: center;">
                        <div style="font-size: 14px; font-weight: bold;">PROPOSAL</div>
                        <div style="font-size: 11px; opacity: 0.9;">Minimal Clean Template</div>
                    </div>
                    <div style="background: white; padding: 12px; border: 1px solid #e5e7eb; height: 100px;">
                        <div style="font-size: 12px; font-weight: bold; color: #374151; margin-bottom: 8px;">Project Details</div>
                        <div style="font-size: 10px; color: #6b7280; line-height: 1.4; margin-bottom: 10px;">
                            Minimalist design focused on content and readability. Clean typography with plenty of white space for maximum clarity.
                        </div>
                        <div style="width: 100%; height: 3px; background: #e5e7eb; border-radius: 2px;">
                            <div style="width: 45%; height: 3px; background: #6b7280; border-radius: 2px;"></div>
                        </div>
                    </div>
                </div>
            """
        }
    }
    
    return template_styles.get(template_key, template_styles["modern_professional"])["preview_html"]

def render_preview_tab(client_data, seller_data, project_specs):
    
    with st.container():
        st.markdown("""
                                                <style>
                                                /* Force override all button styling */
                                                button[kind="secondary"] {
                                                    height: 60px !important;
                                                    border: 2.2px solid #618f8f !important;
                                                    border-radius: 12px !important;
                                                    background-color: #4a4a4a !important;  /* Dark greyish background */
                                                    color: white !important;  /* White text */
                                                }

                                                button[kind="secondary"]:hover {
                                                    border: 2.2px solid #618f8f !important;
                                                    background-color: #5a5a5a !important;  /* Slightly lighter on hover */
                                                    color: white !important;  /* Keep white text on hover */
                                                }

                                                button[kind="secondary"]:focus {
                                                    border: 2.2px solid #618f8f !important;
                                                    outline: 2px solid #618f8f !important;
                                                    background-color: #4a4a4a !important;  /* Keep dark background on focus */
                                                    color: white !important;  /* Keep white text on focus */
                                                }

                                                /* Try targeting by data attributes */
                                                [data-testid] button {
                                                    border: 2.2px solid #618f8f !important;
                                                    height: 68px !important;
                                                    background-color: #4a4a4a !important;  /* Dark greyish background */
                                                    color: white !important;  /* White text */
                                                }

                                                /* Additional targeting for button text specifically */
                                                button[kind="secondary"] p,
                                                button[kind="secondary"] span,
                                                button[kind="secondary"] div {
                                                    color: white !important;
                                                }

                                                [data-testid] button p,
                                                [data-testid] button span,
                                                [data-testid] button div {
                                                    color: white !important;
                                                }
                                                </style>
                                                """, unsafe_allow_html=True)
        st.markdown("### 🔄 Generating Your Professional Proposal")
        
        # Progress bar and status
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # Progress stages with actual timing
        stages = [
            ("🔍 Validating project details...", 0.2),
            (f"🎨 Applying professional template...", 0.4),
            ("📝 Generating proposal content...", 0.6),
            ("⚖️ Adding terms and conditions...", 0.8),
            ("✨ Final review and formatting...", 1.0)
        ]
        
        output_file = None
        
        try:
            # Show progress stages with realistic timing
            for i, (stage_text, progress) in enumerate(stages):
                status_text.text(stage_text)
                progress_bar.progress(progress)

                # Add realistic delay for user experience
                time.sleep(0.6)

                # Only generate once at the last stage
                if i == len(stages) - 1:
                    # Get HTML + file paths (html_file, pdf_file)
                    result = get_presentation(
                    client=client_data,
                    seller=seller_data,
                    project_specs=project_specs
                )

                    if len(result) == 2:
                        html_content, file_path = result
                        pdf_path = None
                    elif len(result) == 3:
                        html_content, file_path, pdf_path = result
                    else:
                        raise ValueError("Unexpected return format from get_presentation")
                    # Inline editing happens on the raw HTML string
                    edited_html = inline_editable_html_component(html_content)

                    # Overwrite the saved HTML with the edited content
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(edited_html)

                    # If edited content exists, regenerate the PDF from it
                    if edited_html.strip():
                        pdf_path = generate_pdf_from_html(
                            edited_html,
                            output_dir=OUTPUT_DIR,
                            base_filename="salesproposal"
                        )

            # Complete the progress UI
            progress_bar.progress(1.0)
            status_text.text("✅ Proposal generation completed!")
            time.sleep(0.5)

            # Clear progress indicators
            progress_bar.empty()
            status_text.empty()

            # Store paths in session state for later download
            if os.path.exists(file_path) and os.path.exists(pdf_path):
                st.session_state.proposal_file_path = file_path
                st.session_state.proposal_pdf_path = pdf_path
                st.session_state.proposal_generation_success = True
            else:
                st.error("❌ Error generating proposal files. Please try again.")
                return

        except Exception as e:
            progress_bar.empty()
            status_text.empty()
            st.error(f"❌ Error during proposal generation: {str(e)}")
            return


        # --- Display success/download section ---
        if st.session_state.get("proposal_generation_success", False):
            pdf_path = st.session_state.get("proposal_pdf_path")
            if pdf_path and os.path.exists(pdf_path):
                with open(pdf_path, "rb") as f:
                    file_data = f.read()

                pdf_filename = os.path.basename(pdf_path)

                # Center the download button
                col1, col2, col3 = st.columns([1, 1, 1])
                with col2:
                    st.download_button(
                        label="📥 Download PDF",
                        data=file_data,
                        file_name=pdf_filename,
                        mime="application/pdf",
                        use_container_width=True,
                        type="primary",
                    
                    )
            else:
                st.error("❌ PDF file not found. Please regenerate the proposal.")


    # Display success section if generation was successful
    if st.session_state.get('proposal_generation_success', False):
        # Only show download button
        if st.session_state.get('proposal_pdf_path') and os.path.exists(st.session_state.proposal_pdf_path):
            with open(st.session_state.proposal_pdf_path, "rb") as file:
                file_data = file.read()
                
            # Extract just the filename from the full path for the download
            pdf_filename = os.path.basename(st.session_state.proposal_pdf_path)
            
            # Center the download button with limited width
            col1, col2, col3 = st.columns([1, 1, 1])
            with col2:
                st.download_button(
                    label="📥 Download PDF",
                    data=file_data,
                    file_name=pdf_filename,  # Use just the filename, not the full path
                    mime="application/pdf",
                    use_container_width=True,
                    type="primary",
                    key="proposal_pdf_download_button"
                )
        else:
            st.error("❌ PDF file not found. Please regenerate the proposal.")


def generate_tab(client_data, seller_data, additional_specs):
    """
    Main function for the generate proposal tab
    """
    print(seller_data)
    st.markdown(proposal_css, unsafe_allow_html=True)
    render_preview_tab(client_data, seller_data, additional_specs)