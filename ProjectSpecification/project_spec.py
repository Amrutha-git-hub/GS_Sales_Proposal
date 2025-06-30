import streamlit as st
from typing import Tuple, Dict, Optional
from ProjectSpecification.proj_spec_css import proj_spec_css
from t import render_two_column_selector

def proj_specification_tab():
    st.markdown(proj_spec_css,unsafe_allow_html=True)
    st.markdown("""
                                            <style>
                                            /* Force override all button styling */
                                            button[kind="secondary"] {
                                                height: 48px !important;
                                                border: 2.2px solid #618f8f !important;
                                                border-radius: 4px !important;
                                                margin-top: 5px !important;  /* Move button up */
                                                transform: translateY(0px) !important;  /* Additional upward adjustment */
                                                background-color: #4a4a4a !important;  /* Dark greyish background */
                                                color: white !important;  /* White text */
                                            }
                                            
                                            button[kind="secondary"]:hover {
                                                border: 2.2px solid #618f8f !important;
                                                transform: translateY(0px) !important;  /* Keep position on hover */
                                                background-color: #5a5a5a !important;  /* Slightly lighter on hover */
                                                color: white !important;  /* Keep white text on hover */
                                            }
                                            
                                            button[kind="secondary"]:focus {
                                                border: 2.2px solid #618f8f !important;
                                                outline: 2px solid #618f8f !important;
                                                transform: translateY(0px) !important;  /* Keep position on focus */
                                                background-color: #4a4a4a !important;  /* Keep dark background on focus */
                                                color: white !important;  /* Keep white text on focus */
                                            }
                                            
                                            /* Try targeting by data attributes */
                                            [data-testid] button {
                                                border: 2.2px solid #618f8f !important;
                                                height: 48px !important;
                                                margin-top: 5px !important;  /* Move button up */
                                                transform: translateY(0px) !important;  /* Additional upward adjustment */
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

    scope_data = {
        "Project Planning": "**Project Planning** • Define project objectives and success criteria\n• Create detailed work breakdown structure\n• Establish project milestones and deliverables\n\n",
        "Requirements Analysis": "**Requirements Analysis** • Conduct stakeholder interviews and workshops\n• Document functional and non-functional requirements\n• Create user stories and acceptance criteria\n\n",
        "Solution Design": "**Solution Design** • Develop system architecture and technical specifications\n• Create wireframes and user interface mockups\n• Design database schema and integration points\n\n"
    }
    
    scope_content, scope_provided = render_two_column_selector(
        left_title="Scope of Work",
        left_tooltip="Define the detailed scope of work including all tasks, deliverables, and project boundaries.",
        textarea_session_key="scope_content",
        textarea_widget_key="scope_textarea",
        selected_items_key="scope_selected",
        content_map_key="scope_content_map",
        default_data=scope_data,
        right_title="Scope Options",
        right_tooltip="Select scope elements to include in your project definition.",

    )
    
    st.markdown("---")
    
    # Section 2: Timeline
    #st.header("2. ⏰ Timeline")
    timeline_data = {
        "Phase 1 - Discovery": "**Phase 1 - Discovery (2-3 weeks)** • Stakeholder interviews and requirement gathering\n• Current state analysis and gap assessment\n• Technical feasibility study\n\n",
        "Phase 2 - Design": "**Phase 2 - Design (3-4 weeks)** • System architecture and technical design\n• User experience and interface design\n• Development environment setup\n\n",
        "Phase 3 - Development": "**Phase 3 - Development (8-12 weeks)** • Core functionality development\n• Integration with existing systems\n• Unit testing and code reviews\n\n"
    }
    
    timeline_content, timeline_provided = render_two_column_selector(
        left_title="Project Timeline",
        left_tooltip="Outline the project phases, key milestones, and delivery dates.",
        textarea_session_key="timeline_content",
        textarea_widget_key="timeline_textarea",
        selected_items_key="timeline_selected",
        content_map_key="timeline_content_map",
        default_data=timeline_data,
        right_title="Timeline Phases",
        right_tooltip="Select timeline phases to include in your project schedule.",
        selected_color="#8f00ff"
    )
    
    st.markdown("---")
    
    # Section 3: Effort Estimation
    #st.header("3. 💼 Effort Estimation")
    effort_data = {
        "Business Analysis": "**Business Analysis (120-160 hours)** • Requirements gathering and documentation\n• Process mapping and workflow analysis\n• Stakeholder management and communication\n\n",
        "Technical Development": "**Technical Development (400-600 hours)** • Frontend and backend development\n• Database design and implementation\n• API development and integration\n\n",
        "Testing & QA": "**Testing & QA (80-120 hours)** • Test planning and test case creation\n• Manual and automated testing execution\n• Bug fixing and regression testing\n\n"
    }
    
    effort_content, effort_provided = render_two_column_selector(
        left_title="Effort Breakdown",
        left_tooltip="Detail the estimated effort required for each work stream and activity.",
        textarea_session_key="effort_content",
        textarea_widget_key="effort_textarea",
        selected_items_key="effort_selected",
        content_map_key="effort_content_map",
        default_data=effort_data,
        right_title="Effort Categories",
        right_tooltip="Select effort categories to include in your estimation.",
        selected_color="#1f77b4",
        selected_border_color="#4a90e2"
    )
    
    st.markdown("---")
    
    # Section 4: Team Size
    #st.header("4. 👥 Team Composition")
    team_data = {
        "Core Team": "**Core Team (4-6 members)** • Project Manager and Scrum Master\n• Senior Business Analyst\n• Lead Developer and Frontend Developer\n• QA Engineer and DevOps Specialist\n\n",
        "Extended Team": "**Extended Team (2-3 members)** • UI/UX Designer for user experience\n• Database Administrator for data management\n• Security Specialist for compliance review\n\n",
        "Support Team": "**Support Team (1-2 members)** • Technical Writer for documentation\n• Change Management Specialist\n• Subject Matter Experts as needed\n\n"
    }
    
    team_content, team_provided = render_two_column_selector(
        left_title="Team Structure",
        left_tooltip="Define the team composition, roles, and responsibilities for the project.",
        textarea_session_key="team_content",
        textarea_widget_key="team_textarea",
        selected_items_key="team_selected",
        content_map_key="team_content_map",
        default_data=team_data,
        right_title="Team Options",
        right_tooltip="Select team structures to include in your project staffing.",
        selected_color="#ff7f0e",
        selected_border_color="#ffb366"
    )
    
    st.markdown("---")
    
    # Section 5: Pricing & Commercial
    #st.header("5. 💰 Pricing & Commercial Terms")
    pricing_data = {
        "Fixed Price Model": "**Fixed Price Model** • Total project cost: $150,000 - $200,000\n• 30% upfront, 40% at milestone delivery, 30% on completion\n• Includes 3 months post-launch support\n\n",
        "Time & Materials": "**Time & Materials Model** • Senior resources: $150-180/hour\n• Mid-level resources: $100-130/hour\n• Junior resources: $70-90/hour\n\n",
        "Hybrid Approach": "**Hybrid Approach** • Fixed price for core deliverables: $120,000\n• T&M for additional features and changes\n• Monthly retainer for ongoing support: $8,000/month\n\n"
    }
    
    pricing_content, pricing_provided = render_two_column_selector(
        left_title="Commercial Proposal",
        left_tooltip="Outline pricing models, payment terms, and commercial arrangements.",
        textarea_session_key="pricing_content",
        textarea_widget_key="pricing_textarea",
        selected_items_key="pricing_selected",
        content_map_key="pricing_content_map",
        default_data=pricing_data,
        right_title="Pricing Models",
        right_tooltip="Select pricing models to include in your commercial proposal.",
        selected_color="#ff4f58",
        selected_border_color="#ff6b6b"
    )
    
    st.markdown("---")
    
    # Section 6: Simple Text Box
    #st.header("6. 📝 Additional Notes & Comments")
    st.markdown("Use this section for any additional information, special requirements, or comments about the proposal.")
    
    additional_notes = st.text_area(
        label="Additional Notes",
        height=200,
        placeholder="Enter any additional notes, special requirements, assumptions, or comments here...",
        key="additional_notes_textarea"
    )
    
    st.markdown("---")
    
