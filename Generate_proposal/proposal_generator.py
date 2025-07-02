import streamlit as st
import time
from datetime import datetime
import os
from Generate_proposal.generate_proposal_css import *
from PresentationWriting.src.main import get_presentation

def render_preview_tab(client_data, seller_data, project_specs):
    """
    Renders the editable details overview and proposal generation interface
    """
    
    st.header("📝 Generate Proposal")
    st.markdown("Review and edit the details below, then generate your professional proposal.")
    
    # Details Overview Section - Editable
    st.subheader("📋 Project Details Overview")
    
    # Create two columns for client and seller details
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 👤 Client Information")
        with st.container():
            client_name = st.text_input("Client Name", value="Growth Sutra", key="client_name")
            client_contact = st.text_input("Contact Person", value="Vishwendra Verma", key="client_contact")
            client_title = st.text_input("Contact Title", value="CEO", key="client_title")
            client_email = st.text_input("Email", value="xyz@gmail.com", key="client_email")
            client_phone = st.text_input("Phone", value="9999999999", key="client_phone")
            client_industry = st.text_input("Industry", value="Technology Solutions", key="client_industry")
    
    with col2:
        st.markdown("#### 🏢 Seller Information")
        with st.container():
            seller_name = st.text_input("Your Company", value="Your Company Name", key="seller_name")
            seller_contact = st.text_input("Your Name", value="Your Name", key="seller_contact")
            seller_title = st.text_input("Your Title", value="Project Manager", key="seller_title")
            seller_email = st.text_input("Your Email", value="your.email@company.com", key="seller_email")
            seller_phone = st.text_input("Your Phone", value="+1 (555) 123-4567", key="seller_phone")
            seller_website = st.text_input("Website", value="www.yourcompany.com", key="seller_website")
    
    # Project Details Section
    st.divider()
    st.markdown("#### 📊 Project Specifications")
    
    proj_col1, proj_col2 = st.columns(2)
    
    with proj_col1:
        service_type = st.selectbox(
            "Service Category",
            ["Web Development", "Mobile App Development", "UI/UX Design", "Digital Marketing", "Consulting", "Other"],
            index=0
        )
        project_value = st.number_input("Project Value ($)", min_value=0, value=12500, step=100)
        timeline = st.text_input("Delivery Timeline", value="8-10 weeks")
    
    with proj_col2:
        payment_terms = st.selectbox(
            "Payment Structure",
            ["50% upfront, 50% completion", "30% upfront, 70% completion", "Monthly payments", "Custom terms"],
            index=0
        )
        support_period = st.text_input("Support Period", value="6 months")
        technology_stack = st.text_input("Technology/Tools", value="React, Node.js, MongoDB")
    
    # Project Description
    st.markdown("#### 📝 Project Description")
    project_description = st.text_area(
        "Detailed Project Description",
        value="Custom web development solution with modern design, responsive layout, and advanced functionality. Includes SEO optimization, content management system, and post-launch support.",
        height=100
    )
    
    # Key Deliverables
    st.markdown("#### 🎯 Key Deliverables")
    deliverables = st.text_area(
        "List of Deliverables (one per line)",
        value="• Custom responsive website\n• Content Management System\n• SEO optimization\n• Mobile optimization\n• 6 months support\n• Training documentation",
        height=120
    )
    
    # Summary Section
    st.divider()
    st.subheader("📊 Proposal Summary")
    
    # Display current values in a nice format
    summary_col1, summary_col2, summary_col3, summary_col4 = st.columns(4)
    
    with summary_col1:
        st.metric("Client", client_name)
    
    with summary_col2:
        st.metric("Service", service_type)
    
    with summary_col3:
        st.metric("Value", f"${project_value:,}")
    
    with summary_col4:
        st.metric("Timeline", timeline)
    
    # Generate Proposal Button Section
    st.divider()
    st.markdown("### 🚀 Generate Proposal")
    
    # Format selection
    format_options = [
        "🎨 Modern Professional", 
        "📊 Classic Business", 
        "🌈 Creative Bold", 
        "⚪ Minimal Clean"
    ]
    
    selected_format = st.selectbox(
        "Select Proposal Format:",
        options=format_options,
        index=0
    )
    
    # Center the generate button
    gen_col1, gen_col2, gen_col3 = st.columns([1, 2, 1])
    
    with gen_col2:
        st.markdown(f"""
        <div style="text-align: center; padding: 20px; background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%); 
                    border-radius: 12px; border: 1px solid #cbd5e1; margin: 20px 0;">
            <h4 style="color: #334155; margin-bottom: 10px;">Ready to Generate</h4>
            <p style="color: #64748b; font-size: 14px; margin-bottom: 20px;">
                Format: <strong>{selected_format}</strong><br>
                Client: <strong>{client_name}</strong><br>
                Value: <strong>${project_value:,}</strong>
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        generate_clicked = st.button(
            "🚀 Generate Professional Proposal",
            type="primary",
            use_container_width=True,
            help=f"Generate comprehensive proposal using {selected_format} format"
        )
    
    # Handle proposal generation
    if generate_clicked:
        with st.container():
            st.markdown("### 🔄 Generating Your Professional Proposal")
            
            # Progress bar and status
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            # Progress stages with actual timing
            stages = [
                ("🔍 Validating project details...", 0.2),
                (f"🎨 Applying {selected_format} template...", 0.4),
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
                    
                    # Generate the actual file during the content generation stage
                    if i == 2:  # During "Generating proposal content..."
                        # Update the client_data, seller_data, project_specs with current form values
                        updated_client_data = {
                            'name': client_name,
                            'contact': client_contact,
                            'title': client_title,
                            'email': client_email,
                            'phone': client_phone,
                            'industry': client_industry
                        }
                        
                        updated_seller_data = {
                            'name': seller_name,
                            'contact': seller_contact,
                            'title': seller_title,
                            'email': seller_email,
                            'phone': seller_phone,
                            'website': seller_website
                        }
                        
                        updated_project_specs = {
                            'service_type': service_type,
                            'project_value': project_value,
                            'timeline': timeline,
                            'payment_terms': payment_terms,
                            'support_period': support_period,
                            'technology_stack': technology_stack,
                            'project_description': project_description,
                            'deliverables': deliverables,
                            'selected_format': selected_format
                        }
                        
                        # Generate the presentation file
                        output_file = get_presentation(
                            client=updated_client_data,
                            seller=updated_seller_data,
                            project_specs=updated_project_specs
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
                    st.session_state.generated_file = output_file
                    st.session_state.generation_success = True
                    st.session_state.client_name = client_name
                    st.session_state.project_value = project_value
                    st.session_state.selected_format = selected_format
                    st.session_state.client_email = client_email
                else:
                    st.error("❌ Error generating proposal file. Please try again.")
                    return
                    
            except Exception as e:
                progress_bar.empty()
                status_text.empty()
                st.error(f"❌ Error during proposal generation: {str(e)}")
                return
    
    # Display success section if generation was successful
    if st.session_state.get('generation_success', False):
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
                    <div><strong>Client:</strong> {st.session_state.get('client_name', 'N/A')}</div>
                    <div><strong>Format:</strong> {st.session_state.get('selected_format', 'N/A')}</div>
                    <div><strong>Value:</strong> ${st.session_state.get('project_value', 0):,}</div>
                    <div><strong>Generated:</strong> {current_time}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Action buttons
        action_col1, action_col2, action_col3 = st.columns(3)
        
        with action_col1:
            # Download button with actual file download
            if st.session_state.get('generated_file') and os.path.exists(st.session_state.generated_file):
                with open(st.session_state.generated_file, "rb") as file:
                    file_data = file.read()
                    
                # Create filename with timestamp
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                filename = f"Proposal_{st.session_state.get('client_name', 'Client').replace(' ', '_')}_{timestamp}.pdf"
                
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
                st.success(f"📧 Proposal sent to {st.session_state.get('client_email', 'client')}")
                
        with action_col3:
            if st.button("👀 Preview", use_container_width=True):
                # Here you would implement preview functionality
                st.success("👀 Opening preview...")
                
        # Add option to generate new proposal
        st.divider()
        if st.button("🔄 Generate New Proposal", use_container_width=True):
            # Clear session state to allow new generation
            st.session_state.generation_success = False
            if 'generated_file' in st.session_state:
                del st.session_state.generated_file
            st.rerun()


def generate_tab(client_data, seller_data, additional_specs):
    """
    Main function for the generate proposal tab
    """
    st.markdown(proposal_css, unsafe_allow_html=True)
    render_preview_tab(client_data, seller_data, additional_specs)