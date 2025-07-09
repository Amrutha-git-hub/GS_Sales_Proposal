import streamlit as st
import streamlit.components.v1 as components
import time
from datetime import datetime
import os
from Generate_proposal.generate_proposal_css import *
from SalesProposalWriting.src.main import get_presentation
from Common_Utils.logo_creator import create_text_image

def render_template_preview(template_name, template_key):
    """
    Renders a template preview card with actual HTML rendering
    """
    template_styles = {
        "modern_professional": {
            "preview_html": """
                <div style="width: 100%; height: 180px; background: #f8fafc; padding: 12px; border-radius: 8px; font-family: Arial, sans-serif;">
                    <div style="background: linear-gradient(135deg, #3b82f6 0%, #1e40af 100%); padding: 12px; border-radius: 6px; margin-bottom: 12px; color: white; text-align: center;">
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
            (f"🎨 Applying proffessional template...", 0.4),
            ("📝 Generating proposal content...", 0.6),
            ("⚖️ Adding terms and conditions...", 0.8),
            ("✨ Final review and formatting...", 1.0)
        ]
        
        output_file = None
        
        try:
            for i, (stage_text, progress) in enumerate(stages):
                status_text.text(stage_text)
                progress_bar.progress(progress)
                
                # Add realistic delay for user experience
                time.sleep(0.5)
                
                output_file = get_presentation(
                    client=client_data,
                    seller=seller_data,
                    project_specs=project_specs
                )
            
            # Complete the progress
            progress_bar.progress(1.0)
            status_text.text("✅ Proposal generation completed!")
            time.sleep(0.5)
            
            # Clear progress indicators
            progress_bar.empty()
            status_text.empty()
            
            # Store the output file path in session state for download
            if output_file and os.path.exists(output_file):
                st.session_state.proposal_file_path = output_file
                st.session_state.proposal_generation_success = True
            else:
                st.error("❌ Error generating proposal file. Please try again.")
                return
                
        except Exception as e:
            progress_bar.empty()
            status_text.empty()
            st.error(f"❌ Error during proposal generation: {str(e)}")
            return

    # Display success section if generation was successful
    if st.session_state.get('proposal_generation_success', False):
        # Success message
        st.success("✅ **Proposal Generated Successfully!**")
        
        # Current time for generation timestamp
        current_time = datetime.now().strftime('%B %d, %Y at %I:%M %p')
        
        # Success summary
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #ecfdf5 0%, #d1fae5 100%); 
                    padding: 25px; border-radius: 12px; border: 1px solid #10b981; margin: 20px 0;">
            <h3 style="color: #065f46; margin-bottom: 15px;">📋 Proposal Ready</h3>
            <div style="background: white; padding: 20px; border-radius: 8px;">
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px;">
                    <div><strong>Client:</strong> {st.session_state.get('proposal_client_name', 'N/A')}</div>
                    <div><strong>Template:</strong> {st.session_state.get('proposal_selected_format', 'N/A')}</div>
                    <div><strong>Value:</strong> ${st.session_state.get('proposal_project_value', 0):,}</div>
                    <div><strong>Generated:</strong> {current_time}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Action buttons
        action_col1, action_col2, action_col3 = st.columns(3)
        
        with action_col1:
            # Download button with actual file download
            if st.session_state.get('proposal_file_path') and os.path.exists(st.session_state.proposal_file_path):
                with open(st.session_state.proposal_file_path, "rb") as file:
                    file_data = file.read()
                    
                # Create filename with timestamp
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                filename = f"Proposal_{st.session_state.get('proposal_client_name', 'Client').replace(' ', '_')}_{timestamp}.pdf"
                
                st.download_button(
                    label="📥 Download PDF",
                    data=file_data,
                    file_name=filename,
                    mime="application/pdf",
                    use_container_width=True,
                    type="primary"
                )
            else:
                st.error("❌ File not found. Please regenerate the proposal.")
                
        with action_col2:
            if st.button("📧 Send to Client", use_container_width=True):
                # Here you would implement email sending functionality
                st.success(f"📧 Proposal sent to {st.session_state.get('proposal_client_email', 'client')}")
                
        with action_col3:
            if st.button("👀 Preview", use_container_width=True):
                # Here you would implement preview functionality
                st.success("👀 Opening preview...")
                
        # Add option to generate new proposal
        st.divider()
        if st.button("🔄 Generate New Proposal", use_container_width=True):
            # Clear session state to allow new generation
            st.session_state.proposal_generation_success = False
            if 'proposal_file_path' in st.session_state:
                del st.session_state.proposal_file_path
            st.rerun()


def generate_tab(client_data, seller_data, additional_specs):
    """
    Main function for the generate proposal tab
    """
    print(seller_data)
    st.markdown(proposal_css, unsafe_allow_html=True)
    render_preview_tab(client_data, seller_data, additional_specs)