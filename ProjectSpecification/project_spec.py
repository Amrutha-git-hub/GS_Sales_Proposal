import streamlit as st
import asyncio
from typing import Tuple, Dict, Optional
from concurrent.futures import ThreadPoolExecutor
import time
from ProjectSpecification.proj_spec_css import proj_spec_css
from Utils.ai_suggestion_utils import render_two_column_selector
from Recommendation.recommendation_utils import get_ai_proj_sepc_recommendations
from Recommendation.prompts import *

# Initialize session state for async results
def init_async_session_state():
    """Initialize session state variables for async AI recommendations"""
    if 'ai_recommendations_loading' not in st.session_state:
        st.session_state.ai_recommendations_loading = True
    if 'ai_recommendations_ready' not in st.session_state:
        st.session_state.ai_recommendations_ready = {}
    if 'ai_recommendation_data' not in st.session_state:
        st.session_state.ai_recommendation_data = {}
    if 'loading_progress' not in st.session_state:
        st.session_state.loading_progress = 0
    if 'current_analysis_step' not in st.session_state:
        st.session_state.current_analysis_step = ""
    if 'current_step' not in st.session_state:
        st.session_state.current_step = 0
    if 'ai_processing_started' not in st.session_state:
        st.session_state.ai_processing_started = False
    if 'analysis_complete' not in st.session_state:
        st.session_state.analysis_complete = False

def get_ai_recommendations_async(section_name, prompt, client_data, seller_data, default_data):
    """
    Async wrapper to get AI recommendations in background
    """
    try:
        ai_data = get_ai_proj_sepc_recommendations(prompt, client_data, seller_data)
        if ai_data and isinstance(ai_data, dict) and len(ai_data) > 0:
            return ai_data
        else:
            return default_data
    except Exception as e:
        # Log the error if needed
        return default_data

def update_progress(step, progress_value, analysis_text):
    """Update the progress bar and analysis text"""
    st.session_state.loading_progress = progress_value
    st.session_state.current_analysis_step = analysis_text
    # Force UI update
    time.sleep(0.1)

# Global variable to store AI processing results (accessible from threads)
ai_processing_results = {}

def start_async_recommendations(client_data, seller_data):
    """
    Start async loading of all AI recommendations with progress tracking
    """
    if st.session_state.ai_recommendations_loading:
        
        # Analysis steps with corresponding messages
        analysis_steps = [
            "🔍 Analyzing client requirements and business context...",
            "🏢 Processing seller capabilities and expertise...", 
            "📋 Generating intelligent scope recommendations...",
            "⏱️ Creating optimized timeline structure...",
            "💪 Calculating effort estimations and resource needs...",
            "👥 Designing optimal team composition...",
            "💰 Formulating competitive pricing strategies...",
            "✨ Finalizing AI-enhanced recommendations..."
        ]
        
        # Default data definitions
        default_data_map = {
            'scope': {
                "Project Planning": "**Project Planning** • Define project objectives and success criteria\n• Create detailed work breakdown structure\n• Establish project milestones and deliverables\n\n",
                "Requirements Analysis": "**Requirements Analysis** • Conduct stakeholder interviews and workshops\n• Document functional and non-functional requirements\n• Create user stories and acceptance criteria\n\n",
                "Solution Design": "**Solution Design** • Develop system architecture and technical specifications\n• Create wireframes and user interface mockups\n• Design database schema and integration points\n\n"
            },
            'timeline': {
                "Phase 1 - Discovery": "**Phase 1 - Discovery (2-3 weeks)** • Stakeholder interviews and requirement gathering\n• Current state analysis and gap assessment\n• Technical feasibility study\n\n",
                "Phase 2 - Design": "**Phase 2 - Design (3-4 weeks)** • System architecture and technical design\n• User experience and interface design\n• Development environment setup\n\n",
                "Phase 3 - Development": "**Phase 3 - Development (8-12 weeks)** • Core functionality development\n• Integration with existing systems\n• Unit testing and code reviews\n\n"
            },
            'effort': {
                "Business Analysis": "**Business Analysis (120-160 hours)** • Requirements gathering and documentation\n• Process mapping and workflow analysis\n• Stakeholder management and communication\n\n",
                "Technical Development": "**Technical Development (400-600 hours)** • Frontend and backend development\n• Database design and implementation\n• API development and integration\n\n",
                "Testing & QA": "**Testing & QA (80-120 hours)** • Test planning and test case creation\n• Manual and automated testing execution\n• Bug fixing and regression testing\n\n"
            },
            'team': {
                "Core Team": "**Core Team (4-6 members)** • Project Manager and Scrum Master\n• Senior Business Analyst\n• Lead Developer and Frontend Developer\n• QA Engineer and DevOps Specialist\n\n",
                "Extended Team": "**Extended Team (2-3 members)** • UI/UX Designer for user experience\n• Database Administrator for data management\n• Security Specialist for compliance review\n\n",
                "Support Team": "**Support Team (1-2 members)** • Technical Writer for documentation\n• Change Management Specialist\n• Subject Matter Experts as needed\n\n"
            },
            'pricing': {
                "Fixed Price Model": "**Fixed Price Model** • Total project cost: $150,000 - $200,000\n• 30% upfront, 40% at milestone delivery, 30% on completion\n• Includes 3 months post-launch support\n\n",
                "Time & Materials": "**Time & Materials Model** • Senior resources: $150-180/hour\n• Mid-level resources: $100-130/hour\n• Junior resources: $70-90/hour\n\n",
                "Hybrid Approach": "**Hybrid Approach** • Fixed price for core deliverables: $120,000\n• T&M for additional features and changes\n• Monthly retainer for ongoing support: $8,000/month\n\n"
            }
        }
        
        prompt_map = {
            'scope': scope_prompt,
            'timeline': timeline_prompt,
            'effort': effort_prompt,
            'team': team_prompt,
            'pricing': pricing_prompt
        }
        
        # Initialize with default data immediately
        for section in default_data_map.keys():
            if section not in st.session_state.ai_recommendation_data:
                st.session_state.ai_recommendation_data[section] = default_data_map[section]
                st.session_state.ai_recommendations_ready[section] = False
        
        # Simulate progress for the first few steps
        current_step = st.session_state.get('current_step', 0)
        
        if current_step < len(analysis_steps):
            progress = min(95, 10 + (current_step * 12))
            update_progress(current_step, progress, analysis_steps[current_step])
            st.session_state.current_step = current_step + 1
            
            # If we're at the processing steps, start AI calls
            if current_step >= 2 and not st.session_state.get('ai_processing_started', False):
                st.session_state.ai_processing_started = True
                
                # Start AI processing in background using ThreadPoolExecutor
                with ThreadPoolExecutor(max_workers=5) as executor:
                    futures = {}
                    for section_name, prompt in prompt_map.items():
                        future = executor.submit(
                            get_ai_recommendations_async,
                            section_name,
                            prompt,
                            client_data,
                            seller_data,
                            default_data_map[section_name]
                        )
                        futures[section_name] = future
                    
                    # Store futures in session state for later processing
                    st.session_state.ai_futures = futures
            
            # Check if AI processing is complete
            if hasattr(st.session_state, 'ai_futures') and current_step >= len(analysis_steps) - 1:
                all_complete = True
                for section_name, future in st.session_state.ai_futures.items():
                    if future.done():
                        try:
                            result = future.result()
                            st.session_state.ai_recommendation_data[section_name] = result
                            st.session_state.ai_recommendations_ready[section_name] = True
                        except Exception as e:
                            # Keep default data if AI fails
                            st.session_state.ai_recommendations_ready[section_name] = True
                    else:
                        all_complete = False
                
                if all_complete:
                    # Final completion - set both flags to False to stop loading
                    update_progress(len(analysis_steps), 100, "🎉 Analysis complete! Loading your personalized recommendations...")
                    st.session_state.ai_recommendations_loading = False
                    st.session_state.analysis_complete = True

def show_loading_screen():
    """Display the loading screen with progress bar and analysis steps"""
    st.markdown("""
        <div style="text-align: center; padding: 2rem;">
            <h2>🤖 AI-Powered Project Analysis</h2>
            <p style="color: #666; margin-bottom: 2rem;">
                Our AI is analyzing your requirements to create personalized recommendations
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # Progress bar
    progress_bar = st.progress(st.session_state.loading_progress / 100)
    
    # Current analysis step
    if st.session_state.current_analysis_step:
        st.markdown(f"""
            <div style="text-align: center; padding: 1rem; background-color: #f8f9fa; 
                        border-radius: 8px; margin: 1rem 0;">
                <p style="margin: 0; font-weight: 500; color: #2c3e50;">
                    {st.session_state.current_analysis_step}
                </p>
            </div>
        """, unsafe_allow_html=True)
    
    # Show estimated time remaining
    if st.session_state.loading_progress < 100:
        estimated_time = max(1, int((100 - st.session_state.loading_progress) / 10))
        st.markdown(f"""
            <div style="text-align: center; margin-top: 1rem;">
                <small style="color: #666;">
                    Estimated time remaining: ~{estimated_time} seconds
                </small>
            </div>
        """, unsafe_allow_html=True)
    
    return progress_bar

def get_section_data(section_name):
    """Get data for a specific section"""
    if section_name in st.session_state.ai_recommendation_data:
        return st.session_state.ai_recommendation_data[section_name]
    else:
        return {}

def proj_specification_tab(client_data, seller_data):
    # Initialize async session state
    init_async_session_state()
    
    # Show loading screen if still loading
    if st.session_state.ai_recommendations_loading:
        show_loading_screen()
        
        # Start async loading if not already started
        start_async_recommendations(client_data, seller_data)
        
        # Auto-refresh every 1 second during loading
        time.sleep(1)
        st.rerun()
        return None  # Don't render the main content yet
    
    # Main content - only shown after loading is complete
    st.markdown(proj_spec_css, unsafe_allow_html=True)
    st.markdown("""
        <style>
        /* Force override all button styling */
        button[kind="secondary"] {
            height: 48px !important;
            border: 2.2px solid #618f8f !important;
            border-radius: 4px !important;
            margin-top: 5px !important;
            transform: translateY(0px) !important;
            background-color: #4a4a4a !important;
            color: white !important;
        }
        
        button[kind="secondary"]:hover {
            border: 2.2px solid #618f8f !important;
            transform: translateY(0px) !important;
            background-color: #5a5a5a !important;
            color: white !important;
        }
        
        button[kind="secondary"]:focus {
            border: 2.2px solid #618f8f !important;
            outline: 2px solid #618f8f !important;
            transform: translateY(0px) !important;
            background-color: #4a4a4a !important;
            color: white !important;
        }
        
        [data-testid] button {
            border: 2.2px solid #618f8f !important;
            height: 48px !important;
            margin-top: 5px !important;
            transform: translateY(0px) !important;
            background-color: #4a4a4a !important;
            color: white !important;
        }
        
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
    
    # Success message
    st.success("✅ AI Analysis Complete! Your personalized project specification is ready.")
    
    # Section 1: Scope of Work
    scope_data = get_section_data('scope')
    scope_content, scope_provided = render_two_column_selector(
        left_title="Scope of Work",
        left_tooltip="Define the detailed scope of work including all tasks, deliverables, and project boundaries.",
        textarea_session_key="scope_content",
        textarea_widget_key="scope_textarea",
        textarea_placeholder="Click/Enter to get the AI suggested Project Scope",
        selected_items_key="scope_selected",
        content_map_key="scope_content_map",
        default_data=scope_data,
        right_title="Scope Options",
        right_tooltip="Select scope elements to include in your project definition.",
        selected_border_color="#4a90e2",
        
    )
    
    st.markdown("---")
    
    # Section 2: Timeline
    timeline_data = get_section_data('timeline')
    timeline_content, timeline_provided = render_two_column_selector(
        left_title="Project Timeline",
        left_tooltip="Outline the project phases, key milestones, and delivery dates.",
        textarea_session_key="timeline_content",
        textarea_widget_key="timeline_textarea",
        textarea_placeholder="Click/Enter to get the AI suggested Project Timeline for detailed breakdown",
        selected_items_key="timeline_selected",
        content_map_key="timeline_content_map",
        default_data=timeline_data,
        right_title="Timeline Phases",
        right_tooltip="Select timeline phases to include in your project schedule.",
        selected_color="#d2ebfb",
        selected_border_color="#4a90e2",
    )
    
    st.markdown("---")
    
    # Section 3: Effort Estimation
    effort_data = get_section_data('effort')
    effort_content, effort_provided = render_two_column_selector(
        left_title="Effort Breakdown",
        left_tooltip="Detail the estimated effort required for each work stream and activity.",
        textarea_placeholder="Click/Enter to get the AI suggested Estimation and effort analysis",
        textarea_session_key="effort_content",
        textarea_widget_key="effort_textarea",
        selected_items_key="effort_selected",
        content_map_key="effort_content_map",
        default_data=effort_data,
        right_title="Effort Categories",
        right_tooltip="Select effort categories to include in your estimation.",
        selected_color="#d2ebfb",
        selected_border_color="#4a90e2"
    )
    
    st.markdown("---")
    
    # Section 4: Team Size
    team_data = get_section_data('team')
    team_content, team_provided = render_two_column_selector(
        left_title="Team Structure",
        left_tooltip="Define the team composition, roles, and responsibilities for the project.",
        textarea_session_key="team_content",
        textarea_widget_key="team_textarea",
        textarea_placeholder="Click/Enter to get the AI suggested Team analysis",
        selected_items_key="team_selected",
        content_map_key="team_content_map",
        default_data=team_data,
        right_title="Team Options",
        right_tooltip="Select team structures to include in your project staffing.",
        selected_color="#d2ebfb",
        selected_border_color="#4a90e2",
    )
    
    st.markdown("---")
    
    # Section 5: Pricing & Commercial
    pricing_data = get_section_data('pricing')
    pricing_content, pricing_provided = render_two_column_selector(
        left_title="Commercial Proposal",
        left_tooltip="Outline pricing models, payment terms, and commercial arrangements.",
        textarea_session_key="pricing_content",
        textarea_widget_key="pricing_textarea",
        selected_items_key="pricing_selected",
        textarea_placeholder="Click/Enter to get the AI suggested Pricing",
        content_map_key="pricing_content_map",
        default_data=pricing_data,
        right_title="Pricing Models",
        right_tooltip="Select pricing models to include in your commercial proposal.",
        selected_color="#d2ebfb",
        selected_border_color="#4a90e2",
    )
    
    st.markdown("---")
    
    # Section 6: Additional Notes
    st.markdown("Use this section for any additional information, special requirements, or comments about the proposal.")
    
    additional_notes = st.text_area(
        label="Additional Notes",
        height=200,
        placeholder="Enter any additional notes, special requirements, assumptions, or comments here...",
        key="additional_notes_textarea"
    )
    
    st.markdown("---")
    return [scope_content, effort_content, timeline_content, team_content, pricing_content,additional_notes]