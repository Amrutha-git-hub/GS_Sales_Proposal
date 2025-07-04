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
            # Use client_data attributes with fallbacks
            client_name = st.text_input(
                "Client Name", 
                value=getattr(client_data, 'enterprise_name', '') or "Growth Sutra", 
                key="client_name"
            )
            client_contact = st.text_input(
                "Contact Person", 
                value=getattr(client_data, 'spoc_name', '') or "Contact Person", 
                key="client_contact"
            )
            client_title = st.text_input(
                "Contact Title", 
                value="CEO",  # This might need to be extracted from LinkedIn profile data
                key="client_title"
            )
            # Extract email from LinkedIn profiles if available
            client_email_default = ""
            if hasattr(client_data, 'linkedin_profiles') and client_data.linkedin_profiles:
                for profile_data in client_data.linkedin_profiles.values():
                    if isinstance(profile_data, dict) and profile_data.get('email'):
                        client_email_default = profile_data['email']
                        break
            
            client_email = st.text_input(
                "Email", 
                value=client_email_default or "contact@client.com", 
                key="client_email"
            )
            client_phone = st.text_input(
                "Phone", 
                value="Phone Number", 
                key="client_phone"
            )
            # Extract industry from enterprise details if available
            client_industry_default = "Technology Solutions"
            if hasattr(client_data, 'enterprise_details_content') and client_data.enterprise_details_content:
                # You might want to use AI to extract industry from enterprise details
                client_industry_default = "Technology Solutions"  # Placeholder
            
            client_industry = st.text_input(
                "Industry", 
                value=client_industry_default, 
                key="client_industry"
            )
            
            # Display client website if available
            if hasattr(client_data, 'website_url') and client_data.website_url:
                st.info(f"🌐 Client Website: {client_data.website_url}")
    
    with col2:
        st.markdown("#### 🏢 Seller Information")
        with st.container():
            # Use seller_data attributes with fallbacks
            seller_name = st.text_input(
                "Your Company", 
                value=getattr(seller_data, 'seller_enterprise_name', '') or "Your Company Name", 
                key="seller_name"
            )
            # Extract contact name from LinkedIn profiles if available
            seller_contact_default = "Your Name"
            if hasattr(seller_data, 'seller_linkedin_profiles') and seller_data.seller_linkedin_profiles:
                for profile_data in seller_data.seller_linkedin_profiles.values():
                    if isinstance(profile_data, dict) and profile_data.get('name'):
                        seller_contact_default = profile_data['name']
                        break
            
            seller_contact = st.text_input(
                "Your Name", 
                value=seller_contact_default, 
                key="seller_contact"
            )
            seller_title = st.text_input(
                "Your Title", 
                value="Project Manager", 
                key="seller_title"
            )
            # Extract email from seller LinkedIn profiles if available
            seller_email_default = "your.email@company.com"
            if hasattr(seller_data, 'seller_linkedin_profiles') and seller_data.seller_linkedin_profiles:
                for profile_data in seller_data.seller_linkedin_profiles.values():
                    if isinstance(profile_data, dict) and profile_data.get('email'):
                        seller_email_default = profile_data['email']
                        break
            
            seller_email = st.text_input(
                "Your Email", 
                value=seller_email_default, 
                key="seller_email"
            )
            seller_phone = st.text_input(
                "Your Phone", 
                value="+1 (555) 123-4567", 
                key="seller_phone"
            )
            seller_website = st.text_input(
                "Website", 
                value=getattr(seller_data, 'seller_website_url', '') or "www.yourcompany.com", 
                key="seller_website"
            )
            
            # Display seller additional info if available
            if hasattr(seller_data, 'seller_enterprise_details_content') and seller_data.seller_enterprise_details_content:
                with st.expander("📋 Company Details"):
                    st.text_area(
                        "Enterprise Details", 
                        value=seller_data.seller_enterprise_details_content[:500] + "..." if len(seller_data.seller_enterprise_details_content) > 500 else seller_data.seller_enterprise_details_content,
                        height=100,
                        disabled=True
                    )
    
    # Project Details Section
    st.divider()
    st.markdown("#### 📊 Project Specifications")
    
    proj_col1, proj_col2 = st.columns(2)
    
    with proj_col1:
        # Extract service type from seller services items and add default options
        base_options = ["Web Development", "Mobile App Development", "UI/UX Design", "Digital Marketing", "Consulting", "Other"]
        seller_services = []
        
        if hasattr(seller_data, 'seller_services_items') and seller_data.seller_services_items:
            seller_services = list(seller_data.services_content_map.keys())
        
        # Combine seller services with base options, removing duplicates while preserving order
        service_options = seller_services + [option for option in base_options if option not in seller_services]
        
        default_service = service_options[0] if service_options else "Web Development"
        
        # If there are selected services, use the first one as default
        if hasattr(seller_data, 'selected_services_offered') and seller_data.selected_services_offered:
            if isinstance(seller_data.selected_services_offered, dict):
                selected_services = [service for service, selected in seller_data.selected_services_offered.items() if selected]
            else:
                # Handle case where it's a set or list
                selected_services = list(seller_data.selected_services_offered)
            
            if selected_services and selected_services[0] in service_options:
                default_service = selected_services[0]
        
        service_type = st.selectbox(
            "Service Category",
            service_options,
            index=service_options.index(default_service)
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
        
        # Extract technology stack from seller capabilities if available
        tech_stack_default = "React, Node.js, MongoDB"
        if hasattr(seller_data, 'selected_additional_capabilities') and seller_data.selected_additional_capabilities:
            if isinstance(seller_data.selected_additional_capabilities, dict):
                selected_capabilities = [cap for cap, selected in seller_data.selected_additional_capabilities.items() if selected]
            else:
                # Handle case where it's a set or list
                selected_capabilities = list(seller_data.selected_additional_capabilities)
            
            if selected_capabilities:
                tech_stack_default = ", ".join(selected_capabilities[:3])  # Take first 3 capabilities
        
        technology_stack = st.text_input("Technology/Tools", value=tech_stack_default)
    
    # Project Description - Use client requirements if available
    st.markdown("#### 📝 Project Description")
    default_description = "Custom web development solution with modern design, responsive layout, and advanced functionality. Includes SEO optimization, content management system, and post-launch support."
    
    if hasattr(client_data, 'client_requirements_content') and client_data.client_requirements_content:
        default_description = client_data.client_requirements_content
    
    project_description = st.text_area(
        "Detailed Project Description",
        value=default_description,
        height=100
    )
    
    # Key Deliverables - Use client additional requirements if available
    st.markdown("#### 🎯 Key Deliverables")
    default_deliverables = "• Custom responsive website\n• Content Management System\n• SEO optimization\n• Mobile optimization\n• 6 months support\n• Training documentation"
    
    if hasattr(client_data, 'client_additional_requirements_content') and client_data.client_additional_requirements_content:
        # Format the additional requirements as bullet points
        additional_reqs = client_data.client_additional_requirements_content.split('\n')
        default_deliverables = '\n'.join([f"• {req.strip()}" for req in additional_reqs if req.strip()])
    
    deliverables = st.text_area(
        "List of Deliverables (one per line)",
        value=default_deliverables,
        height=120
    )
    
    # Display Pain Points if available
    if hasattr(client_data, 'selected_pain_points') and client_data.selected_pain_points:
        st.markdown("#### 🎯 Addressing Client Pain Points")
        with st.expander("View Selected Pain Points"):
            for pain_point in client_data.selected_pain_points:
                pain_point_content = client_data.pain_point_content_map.get(pain_point, pain_point)
                st.write(f"• **{pain_point}**: {pain_point_content}")
    
    # Display Additional Specifications if available
    if hasattr(client_data, 'selected_additional_specs') and client_data.selected_additional_specs:
        st.markdown("#### 📋 Additional Specifications")
        with st.expander("View Additional Specifications"):
            for spec in client_data.selected_additional_specs:
                spec_content = client_data.additional_specs_content_map.get(spec, spec)
                st.write(f"• **{spec}**: {spec_content}")
    
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
    
    # Template Selection with Visual Previews
    st.markdown("#### 🎨 Choose Your Template")
    
    # Initialize selected template in session state
    if 'selected_template' not in st.session_state:
        st.session_state.selected_template = "modern_professional"
    
    # Template options
    st.markdown("""
    <style>
    /* Selected button style */
    .stButton > button[data-testid="baseButton-primary"] {
        background-color: #599cd4 !important;
        border: 1px solid #599cd4 !important;
        color: white !important;
    }

    .stButton > button[data-testid="baseButton-primary"]:hover {
        background-color: #4a8bc2 !important;
        border: 1px solid #4a8bc2 !important;
    }

    /* Unselected button style */
    .stButton > button[data-testid="baseButton-secondary"] {
        background-color: #f0f2f6 !important;
        border: 1px solid #d1d5db !important;
        color: #374151 !important;
    }

    .stButton > button[data-testid="baseButton-secondary"]:hover {
        background-color: #e5e7eb !important;
        border: 1px solid #9ca3af !important;
    }
    </style>
    """, unsafe_allow_html=True)

    templates = {
        "modern_professional": "Modern Professional",
        "classic_business": "Classic Business", 
        "creative_bold": "Creative Bold",
        "minimal_clean": "Minimal Clean"
    }

    # Create 2x2 grid for template selection
    row1_col1, row1_col2 = st.columns(2)
    row2_col1, row2_col2 = st.columns(2)

    template_keys = list(templates.keys())

    with row1_col1:
        st.markdown(f"**{templates[template_keys[0]]}**")
        components.html(render_template_preview(templates[template_keys[0]], template_keys[0]), height=200)
        is_selected = st.session_state.selected_template == template_keys[0]
        button_type = "primary" if is_selected else "secondary"
        button_text = "✓ Selected" if is_selected else "Select"
        if st.button(button_text, key=f"select_{template_keys[0]}", use_container_width=True, type=button_type):
            st.session_state.selected_template = template_keys[0]
            st.rerun()

    with row1_col2:
        st.markdown(f"**{templates[template_keys[1]]}**")
        components.html(render_template_preview(templates[template_keys[1]], template_keys[1]), height=200)
        is_selected = st.session_state.selected_template == template_keys[1]
        button_type = "primary" if is_selected else "secondary"
        button_text = "✓ Selected" if is_selected else "Select"
        if st.button(button_text, key=f"select_{template_keys[1]}", use_container_width=True, type=button_type):
            st.session_state.selected_template = template_keys[1]
            st.rerun()

    with row2_col1:
        st.markdown(f"**{templates[template_keys[2]]}**")
        components.html(render_template_preview(templates[template_keys[2]], template_keys[2]), height=200)
        is_selected = st.session_state.selected_template == template_keys[2]
        button_type = "primary" if is_selected else "secondary"
        button_text = "✓ Selected" if is_selected else "Select"
        if st.button(button_text, key=f"select_{template_keys[2]}", use_container_width=True, type=button_type):
            st.session_state.selected_template = template_keys[2]
            st.rerun()

    with row2_col2:
        st.markdown(f"**{templates[template_keys[3]]}**")
        components.html(render_template_preview(templates[template_keys[3]], template_keys[3]), height=200)
        is_selected = st.session_state.selected_template == template_keys[3]
        button_type = "primary" if is_selected else "secondary"
        button_text = "✓ Selected" if is_selected else "Select"
        if st.button(button_text, key=f"select_{template_keys[3]}", use_container_width=True, type=button_type):
            st.session_state.selected_template = template_keys[3]
            st.rerun()
    # Show selected template
    selected_template_name = templates[st.session_state.selected_template]
    st.info(f"✅ **Selected Template:** {selected_template_name}")
    
    # Center the generate button
    gen_col1, gen_col2, gen_col3 = st.columns([1, 2, 1])
    
    with gen_col2:

        generate_clicked = st.button(
            "🚀 Generate Professional Proposal",
            type="primary",
            use_container_width=True,
            help=f"Generate comprehensive proposal using {selected_template_name} template"
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
                (f"🎨 Applying {selected_template_name} template...", 0.4),
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
                            'industry': client_industry,
                            'website': getattr(client_data, 'website_url', ''),
                            'enterprise_details': getattr(client_data, 'enterprise_details_content', ''),
                            'requirements': getattr(client_data, 'client_requirements_content', ''),
                            'additional_requirements': getattr(client_data, 'client_additional_requirements_content', ''),
                            'pain_points': list(getattr(client_data, 'selected_pain_points', [])),
                            'additional_specs': list(getattr(client_data, 'selected_additional_specs', []))
                        }
                        
                        updated_seller_data = {
                            'name': seller_name,
                            'contact': seller_contact,
                            'title': seller_title,
                            'email': seller_email,
                            'phone': seller_phone,
                            'website': seller_website,
                            'enterprise_details': getattr(seller_data, 'seller_enterprise_details_content', ''),
                            'services_offered': list(getattr(seller_data, 'selected_services_offered', set())) if hasattr(seller_data, 'selected_services_offered') else [],
                            'capabilities': list(getattr(seller_data, 'selected_additional_capabilities', set())) if hasattr(seller_data, 'selected_additional_capabilities') else []
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
                            'selected_format': selected_template_name,
                            'template_key': st.session_state.selected_template
                        }
                        
                        # Generate the presentation file
                        if client_data.enterprise_logo == "":
                            client_data.enterprise_logo = create_text_image(client_data.enterprise_name,"client_logo.jpg")
                        if seller_data.enterprise_logo == "":
                            seller_data.enterprise_logo = create_text_image(seller_data.seller_enterprise_name,"seller_logo.jpg")
                        output_file = get_presentation(
                            client=client_data,
                            seller=seller_data,
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
                    st.session_state.proposal_file_path = output_file
                    st.session_state.proposal_generation_success = True
                    st.session_state.proposal_client_name = client_name
                    st.session_state.proposal_project_value = project_value
                    st.session_state.proposal_selected_format = selected_template_name
                    st.session_state.proposal_client_email = client_email
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