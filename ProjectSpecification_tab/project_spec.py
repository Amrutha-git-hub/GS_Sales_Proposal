import streamlit as st
import time
from ProjectSpecification_tab.proj_spec_css import proj_spec_css
from Common_Utils.ai_suggestion_utils import render_two_column_selector
from Recommendation.recommendation_utils import get_ai_proj_sepc_recommendations
from Recommendation.prompts import *
from Common_Utils.common_utils import *

# Initialize session state for loading
def init_session_state():
    """Initialize session state variables"""
    if 'ai_recommendations_loading' not in st.session_state:
        st.session_state.ai_recommendations_loading = True
    if 'ai_recommendation_data' not in st.session_state:
        st.session_state.ai_recommendation_data = {}
    if 'data_loaded' not in st.session_state:
        st.session_state.data_loaded = False

def get_ai_recommendations_sync(section_name, prompt, client_data, seller_data, default_data):
    """
    Synchronous function to get AI recommendations
    """
    try:
        ai_data = get_ai_proj_sepc_recommendations(prompt, client_data, seller_data)
        if ai_data and isinstance(ai_data, dict) and len(ai_data) > 0:
            return ai_data
        else:
            return default_data
    except Exception as e:
        return default_data

def load_all_data(client_data, seller_data):
    """
    Load all AI recommendations synchronously
    """
    if st.session_state.data_loaded:
        return
    
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
    
    # Load data for each section
    sections = list(default_data_map.keys())
    
    for section_name in sections:
        # Load AI data for this section
        ai_data = get_ai_recommendations_sync(
            section_name,
            prompt_map[section_name],
            client_data,
            seller_data,
            default_data_map[section_name]
        )
        
        st.session_state.ai_recommendation_data[section_name] = ai_data
    
    # Mark as loaded
    st.session_state.ai_recommendations_loading = False
    st.session_state.data_loaded = True

def show_simple_spinner():
    """Display a simple spinner that only blocks the main content area"""
    st.markdown("""
        <style>
        /* Only hide the main content container, not headers/tabs */
        [data-testid="block-container"] > div:not(.stTabs) {
            opacity: 0.3;
            pointer-events: none;
        }
        
        /* Create spinner overlay only for the main content area */
        .spinner-overlay {
            position: relative;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 400px;
            width: 100%;
            background-color: rgba(255, 255, 255, 0.9);
            border-radius: 8px;
            z-index: 100;
        }
        
        /* Spinner animation */
        .spinner {
            border: 4px solid #f3f3f3;
            border-top: 4px solid #3498db;
            border-radius: 50%;
            width: 50px;
            height: 50px;
            animation: spin 1s linear infinite;
            margin: 0 auto 20px auto;
        }
        
        .spinner-text {
            color: #666;
            font-size: 16px;
            margin: 0;
            text-align: center;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Display the spinner in the main content area
    with st.container():
        st.markdown("""
            <div class="spinner-overlay">
                <div style="text-align: center;">
                    <div class="spinner"></div>
                    <p class="spinner-text">Analysing Client Requirements ...</p>
                </div>
            </div>
        """, unsafe_allow_html=True)

def get_section_data(section_name):
    """Get data for a specific section"""
    if section_name in st.session_state.ai_recommendation_data:
        return st.session_state.ai_recommendation_data[section_name]
    else:
        return {}

def proj_specification_tab(client_data, seller_data, is_locked):
    # Initialize session state
    init_session_state()
    
    # Show simple spinner and load data if not already loaded
    if st.session_state.ai_recommendations_loading and not st.session_state.data_loaded:
        show_simple_spinner()
        load_all_data(client_data, seller_data)
        st.rerun()
        return None

    # Main content - only shown after loading is complete
    content_area_css = """
            <style>
            /* More aggressive targeting for Streamlit's structure */
            .stApp > div:first-child > div:first-child > div:first-child {
                background-color: #f7f7f7 !important;
            }

            /* Target the main content area */
            .main {
                background-color: #f7f7f7 !important;
            }

            /* Primary targeting for block container with full height and width control */
            [data-testid="block-container"] {
                background-color: #f7f7f7 !important;
                padding: 2rem !important;
                border-radius: 8px !important;
                margin-top: 1rem !important;
                margin-left: auto !important;
                margin-right: auto !important;
                width: 80% !important;
                max-width: 80% !important;
                min-height: 250vh !important;
                height: auto !important;
                padding-bottom: 5rem !important; /* Extra padding at bottom */
            }

            /* Alternative targeting for older Streamlit versions */
            .block-container {
                background-color: #f7f7f7 !important;
                padding: 2rem !important;
                border-radius: 8px !important;
                margin-top: 1rem !important;
                margin-left: auto !important;
                margin-right: auto !important;
                width: 80% !important;
                max-width: 80% !important;
                min-height: 250vh !important;
                height: auto !important;
                padding-bottom: 5rem !important;
            }

            /* Target the element that contains your tab content */
            .stApp .main .block-container {
                background-color: #f7f7f7 !important;
                padding: 2rem !important;
                border-radius: 8px !important;
                margin-top: 1rem !important;
                margin-left: auto !important;
                margin-right: auto !important;
                width: 80% !important;
                max-width: 80% !important;
                min-height: 250vh !important;
                height: auto !important;
                padding-bottom: 5rem !important;
            }

            /* Ensure the main container expands to content */
            .main > div {
                min-height: 250vh !important;
                height: auto !important;
            }

            /* Target specific Streamlit containers that might override height */
            div[data-testid="stVerticalBlock"] {
                min-height: inherit !important;
                height: auto !important;
            }

            /* Ensure tabs container has proper height */
            .stTabs [data-baseweb="tab-panel"] {
                min-height: 80vh !important;
                height: auto !important;
                padding-bottom: 3rem !important;
            }

            /* Style form elements to stand out on the background */
            .stSelectbox > div,
            .stTextInput > div,
            .stTextArea > div,
            .stNumberInput > div,
            .stDateInput > div,
            .stTimeInput > div {
                background-color: white !important;
                border-radius: 4px !important;
            }

            /* Style expander containers */
            .streamlit-expanderHeader,
            .streamlit-expanderContent {
                background-color: rgba(255, 255, 255, 0.9) !important;
                border-radius: 4px !important;
            }

            /* Style metric containers */
            [data-testid="metric-container"] {
                background-color: rgba(255, 255, 255, 0.9) !important;
                border-radius: 4px !important;
                padding: 8px !important;
            }

            /* Additional fallback for main content area */
            section[data-testid="stSidebar"] ~ div {
                background-color: #f7f7f7 !important;
                width: 80% !important;
                margin-left: auto !important;
                margin-right: auto !important;
                min-height: 250vh !important;
                height: auto !important;
            }

            /* Ensure columns maintain proper height */
            div[data-testid="column"] {
                min-height: inherit !important;
                height: auto !important;
            }

            /* Additional height coverage for dynamic content */
            .stApp {
                min-height: 250vh !important;
                height: auto !important;
            }

            /* Fallback for very long content */
            @media screen and (min-height: 800px) {
                [data-testid="block-container"] {
                    min-height: 250vh !important;
                }
                
                .block-container {
                    min-height: 250vh !important;
                }
                
                .stApp .main .block-container {
                    min-height: 250vh !important;
                }
            }

            /* For extra long content (like many form fields) */
            @media screen and (min-height: 1200px) {
                [data-testid="block-container"] {
                    min-height: 150vh !important;
                }
                
                .block-container {
                    min-height: 150vh !important;
                }
                
                .stApp .main .block-container {
                    min-height: 150vh !important;
                }
            }
            </style>
            """

    st.markdown(content_area_css, unsafe_allow_html=True)
    st.markdown(proj_spec_css, unsafe_allow_html=True)
    st.markdown("""
        <style>
        /* Force override all button styling */
        button[kind="secondary"] {
            height: 48px !important;
            border: 2.2px solid #ececec !important;
            border-radius: 4px !important;
            margin-top: 5px !important;
            transform: translateY(0px) !important;
            background-color: #d3d3d3 !important;
            color: black !important;
        }
        
        button[kind="secondary"]:hover {
            border: 2.2px solid #ececec !important;
            transform: translateY(0px) !important;
            background-color: #5a5a5a !important;
            color: white !important;
        }
        
        button[kind="secondary"]:focus {
            border: 2.2px solid #ececec !important;
            outline: 2px solid #ececec !important;
            transform: translateY(0px) !important;
            background-color: #d3d3d3 !important;
            color: black !important;
        }
        
        [data-testid] button {
            border: 2.2px solid #ececec !important;
            height: 48px !important;
            margin-top: 5px !important;
            transform: translateY(0px) !important;
            background-color: #d3d3d3 !important;
            color: black !important;
        }
        
        button[kind="secondary"] p,
        button[kind="secondary"] span,
        button[kind="secondary"] div {
            color: black !important;
        }
        
        [data-testid] button p,
        [data-testid] button span,
        [data-testid] button div {
            color: black !important;
        }
        
        button[kind="secondary"]:hover p,
        button[kind="secondary"]:hover span,
        button[kind="secondary"]:hover div {
            color: white !important;
        }
        </style>
    """, unsafe_allow_html=True)
    
    
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
        selected_color="#d2ebfb",
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
        key="additional_notes_textarea",
        disabled=is_locked  # Disable if tab is locked
    )
    
    st.markdown("---")
    return [scope_content, effort_content, timeline_content, team_content, pricing_content, additional_notes]