import streamlit as st
from typing import Dict, Optional, Set, Tuple

def render_two_column_pain_points_section(
    # Column configuration
    column_ratio: Tuple[float, float] = (1, 1),
    column_gap: str = "medium",
    
    # Left column (text area) configuration
    left_title: str = "Client Requirements",
    left_tooltip: str = "Define the core client requirements, technical specifications, project scope, deliverables, and expected outcomes. This forms the foundation of your proposal and helps ensure all client needs are addressed.",
    left_required: bool = True,
    textarea_height: int = 200,
    textarea_placeholder: str = "Enter client name first to enable this field",
    textarea_session_key: str = "client_requirements_content",
    textarea_widget_key: str = "client_requirements_textarea",
    
    # Right column (pain points) configuration  
    right_title: str = "Client Pain Points",
    right_tooltip: str = "This area displays extracted pain points from RFI documents or website analysis. You can also manually enter client's business challenges, current pain points, and organizational details that will help customize your proposal.",
    selected_items_key: str = "selected_pain_points",
    content_map_key: str = "pain_point_content_map",
    data_source_key: Optional[str] = "rfi_pain_points_items",
    
    # Enable/disable conditions
    client_enabled_condition: bool = True,
    client_name_provided: bool = True,
    
    # Default data
    default_data: Optional[Dict[str, str]] = None,
    
    # Pain points styling
    button_column_width: float = 0.5,
    content_column_width: float = 9,
    show_success_messages: bool = False,
    selected_color: str = "#2e7d32",
    selected_border_color: str = "#4caf50", 
    unselected_color: str = "#404040",
    unselected_border_color: str = "#404040",
    text_color: str = "#ffffff"
) -> Tuple[str, bool]:
    """
    Renders a two-column section with text area on left and pain points selection on right.
    
    Args:
        column_ratio: Tuple defining the width ratio of left and right columns
        column_gap: Gap between columns ("small", "medium", "large")
        
        left_title: Title for the left column (text area)
        left_tooltip: Tooltip text for the left column
        left_required: Whether to show asterisk for required field
        textarea_height: Height of the text area in pixels
        textarea_placeholder: Placeholder text when disabled
        textarea_session_key: Session state key for storing text area content
        textarea_widget_key: Widget key for the text area
        
        right_title: Title for the right column (pain points)
        right_tooltip: Tooltip text for the right column
        selected_items_key: Session state key tracking selected items
        content_map_key: Session state key mapping items to content
        data_source_key: Session state key containing pain points data
        
        client_enabled_condition: Whether functionality is enabled
        client_name_provided: Whether client name is provided (for textarea)
        
        default_data: Default pain points data
        
        button_column_width: Width ratio for pain point buttons
        content_column_width: Width ratio for pain point content display
        show_success_messages: Whether to show add/remove messages
        selected_color: Background color for selected items
        selected_border_color: Border color for selected items  
        unselected_color: Background color for unselected items
        unselected_border_color: Border color for unselected items
        text_color: Text color for items
        
    Returns:
        Tuple of (textarea_content, requirements_provided_bool)
    """
    
    # Default pain points data
    if default_data is None:
        default_data = {
            "Revenue Challenges": "**Revenue Challenges** • Sales declined by 15% year-over-year despite market growth\n• Missed quarterly revenue targets by $2.3M for three consecutive quarters\n• Average deal size decreased by 22% due to increased price competition\n• Customer churn rate increased to 18%, up from 12% previous year\n• Revenue per customer dropped 8% as clients downgraded service tiers\n• New product launches generated only 60% of projected revenue\n• Seasonal revenue fluctuations creating 40% variance between peak and low periods\n• Pipeline conversion rates fell from 35% to 24% over past 12 months\n\n",
            
            "Cost and Margin Pressure": "**Cost and Margin Pressure** • Cost of Goods Sold increased by 12% due to supply chain disruptions\n• Labor costs rose 18% while productivity remained flat\n• Raw material prices up 25% with limited ability to pass costs to customers\n• Operational efficiency decreased by 14% due to outdated processes\n• Procurement costs increased 20% from supplier consolidation issues\n• Technology infrastructure costs grew 30% without proportional business benefits\n• Regulatory compliance expenses added $1.8M in unexpected annual costs\n• Facility and overhead costs up 16% while revenue remained stagnant\n\n",
            
            "Market Expansion and Customer Acquisition": "**Market Expansion and Customer Acquisition**\n\n • Win rate on new business opportunities dropped from 42% to 28%\n• Customer acquisition cost increased 35% while customer lifetime value declined\n• Expansion into new geographic markets yielding only 40% of projected results\n• Lack of local market knowledge resulting in 60% longer sales cycles\n• Digital marketing campaigns generating 50% fewer qualified leads\n• Competition from new market entrants capturing 25% of target customer segment\n• Limited brand recognition in new markets requiring 3x marketing investment\n• Difficulty penetrating enterprise accounts with average sales cycle extending to 18 months\n\n"
        }
    
    # Initialize session state variables
    if selected_items_key not in st.session_state:
        st.session_state[selected_items_key] = set()
    
    if content_map_key not in st.session_state:
        st.session_state[content_map_key] = {}
    
    if textarea_session_key not in st.session_state:
        st.session_state[textarea_session_key] = ""
    
    # Create two columns
    col_left, col_right = st.columns(column_ratio, gap=column_gap)
    
    # LEFT COLUMN - Text Area
    with col_left:
        # Title with tooltip and required indicator
        required_asterisk = ' <span style="color:red;">*</span>' if left_required else ''
        st.markdown(f'''
        <div class="tooltip-label">
            {left_title}{required_asterisk}
            <div class="tooltip-icon" data-tooltip="{left_tooltip}">ⓘ</div>
        </div>
        ''', unsafe_allow_html=True)
        
        # Text area
        client_requirements = st.text_area(
            label=left_title,
            value=st.session_state[textarea_session_key] if client_name_provided else "",
            height=textarea_height,
            key=textarea_widget_key,
            label_visibility="collapsed",
            disabled=not client_name_provided,
            placeholder=textarea_placeholder if not client_name_provided else ""
        )
        
        # Update session state when text area changes (only if enabled)
        if client_name_provided:
            st.session_state[textarea_session_key] = client_requirements
        
        client_requirements_provided = bool(client_name_provided and client_requirements.strip())
    
    # RIGHT COLUMN - Pain Points Selection
    with col_right:
        # Title with tooltip
        st.markdown(f'''
        <div class="tooltip-label">
            {right_title}
            <div class="tooltip-icon" data-tooltip="{right_tooltip}">ⓘ</div>
        </div>
        ''', unsafe_allow_html=True)
        
        # Get pain points data from session state or use default data
        if (client_enabled_condition and 
            data_source_key and 
            st.session_state.get(data_source_key)):
            pain_points_items = st.session_state[data_source_key]
        else:
            pain_points_items = default_data
        
        # Container for pain points items
        with st.container():
            # Display pain points items with add/remove buttons
            for i, (key, value) in enumerate(pain_points_items.items()):
                # Check if this item is selected
                is_selected = key in st.session_state[selected_items_key]
                
                # Create button and content columns
                col_button, col_content = st.columns([button_column_width, content_column_width], gap="small")
                
                with col_button:
                    # Button styling
                    st.markdown("""
                    <style>
                    div[data-testid="column"] > div > div > button {
                        height: 48px !important;
                        margin-top: 5px !important;
                    }
                    </style>
                    """, unsafe_allow_html=True)
                    
                    # Button appearance based on selection state
                    button_text = "❌" if is_selected else "➕"
                    button_help = f"Remove '{key}' from {left_title.lower()}" if is_selected else f"Add '{key}' to {left_title.lower()}"
                    
                    if st.button(button_text,
                            key=f"toggle_{selected_items_key}_{i}",
                            help=button_help,
                            type="secondary",
                            disabled=not client_enabled_condition):
                        
                        if is_selected:
                            # REMOVE FUNCTIONALITY
                            current_content = st.session_state.get(textarea_session_key, '')
                            original_content = st.session_state[content_map_key].get(key, value)
                            
                            # Remove content patterns
                            patterns_to_remove = [
                                f"\n\n{original_content}",
                                f"{original_content}\n\n", 
                                original_content
                            ]
                            
                            updated_content = current_content
                            for pattern in patterns_to_remove:
                                updated_content = updated_content.replace(pattern, "")
                            
                            # Clean up excessive newlines
                            updated_content = '\n\n'.join([section.strip() for section in updated_content.split('\n\n') if section.strip()])
                            
                            # Update session state
                            st.session_state[textarea_session_key] = updated_content
                            st.session_state[selected_items_key].discard(key)
                            if key in st.session_state[content_map_key]:
                                del st.session_state[content_map_key][key]
                            
                            if show_success_messages:
                                st.success(f"🗑️ '{key}' removed!")
                        
                        else:
                            # ADD FUNCTIONALITY
                            current_content = st.session_state.get(textarea_session_key, '')
                            new_content = current_content + f"\n\n{value}" if current_content else value
                            
                            # Update session state
                            st.session_state[textarea_session_key] = new_content
                            st.session_state[content_map_key][key] = value
                            st.session_state[selected_items_key].add(key)
                            
                            if show_success_messages:
                                st.success(f"✅ '{key}' added!")
                        
                        st.rerun()
                
                with col_content:
                    # Styling based on selection state
                    if is_selected:
                        background_color = selected_color
                        border_color = selected_border_color
                        icon = "✅"
                        box_shadow = f"0 2px 8px rgba({int(selected_border_color[1:3], 16)}, {int(selected_border_color[3:5], 16)}, {int(selected_border_color[5:7], 16)}, 0.3)"
                    else:
                        background_color = unselected_color
                        border_color = unselected_border_color
                        icon = "📋"
                        box_shadow = "0 2px 4px rgba(0,0,0,0.1)"
                    
                    # Apply disabled styling if not enabled
                    if not client_enabled_condition:
                        background_color = "#666666"
                        border_color = "#666666"
                        text_color = "#999999"
                    
                    st.markdown(f"""
                    <div style="
                        padding: 12px;
                        border-radius: 6px;
                        margin: 5px 0;
                        background-color: {background_color};
                        border: 2px solid {border_color};
                        color: {text_color};
                        font-weight: 500;
                        box-shadow: {box_shadow};
                        min-height: 24px;
                        display: flex;
                        align-items: center;
                        transition: all 0.3s ease;
                        opacity: {'0.6' if not client_enabled_condition else '1'};
                    ">
                        {icon} {key}
                    </div>
                    """, unsafe_allow_html=True)
    
    return client_requirements, client_requirements_provided


# Example usage functions
def example_basic_usage():
    """Replace your original col5, col6 code with this single function call"""
    
    client_requirements, client_requirements_provided = render_two_column_pain_points_section(
        client_enabled_condition=True,  # Replace with your actual condition
        client_name_provided=True,      # Replace with your actual condition
        show_success_messages=False     # Since you had these commented out
    )
    
    # Now you can use client_requirements and client_requirements_provided
    # just like in your original code
    return client_requirements, client_requirements_provided


def example_custom_usage():
    """Example with custom configuration"""
    
    # Custom pain points for different use case
    technical_pain_points = {
        "Infrastructure Issues": "**Infrastructure Issues**\n• Server downtime increased by 40%\n• Database performance degraded\n\n",
        "Security Concerns": "**Security Concerns**\n• Multiple security vulnerabilities identified\n• Compliance issues detected\n\n"
    }
    
    tech_requirements, tech_provided = render_two_column_pain_points_section(
        # Column configuration
        column_ratio=(1.2, 0.8),  # Make left column slightly larger
        
        # Left column customization
        left_title="Technical Requirements",
        left_tooltip="Define technical specifications and system requirements",
        textarea_session_key="technical_requirements_content",
        textarea_widget_key="tech_requirements_textarea",
        textarea_height=250,
        
        # Right column customization
        right_title="Technical Pain Points", 
        selected_items_key="selected_tech_points",
        content_map_key="tech_content_map",
        data_source_key=None,  # Use default_data instead
        default_data=technical_pain_points,
        
        # Styling
        selected_color="#1976d2",  # Blue theme
        selected_border_color="#42a5f5",
        show_success_messages=True,
        
        # Conditions
        client_enabled_condition=True,
        client_name_provided=True
    )
    
    return tech_requirements, tech_provided


