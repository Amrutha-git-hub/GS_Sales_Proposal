from dataclasses import dataclass, field
from typing import List, Dict, Set, Optional, Any
import streamlit as st
import logging

logger = logging.getLogger(__name__)

def set_global_message(message: str, message_type: str = "info"):
    """Set global message for user feedback"""
    st.session_state['global_message'] = message
    st.session_state['global_message_type'] = message_type

@dataclass
class ClientTabState:
    """Dataclass to manage all client tab state with persistence across tab switches."""
    
    # Basic client information
    enterprise_name: str = ""
    website_url: str = ""
    website_urls_list: List[str] = field(default_factory=list)
    enterprise_logo: str = ""
    last_company_name: str = ""
    last_analyzed_url: Optional[str] = None
    
    # Client details and requirements
    enterprise_details_content: str = ""
    client_requirements_content: str = ""
    client_additional_requirements_content: str = ""
    
    # SPOC information
    spoc_name: str = ""
    spoc_linkedin_profile: str = ""
    linkedin_profiles: Dict[str, Dict] = field(default_factory=dict)
    last_searched_spoc: str = ""
    current_selected_profile_url: Optional[str] = None
    
    # File handling
    uploaded_file_path: Optional[str] = None
    uploaded_files_paths: Dict[str, str] = field(default_factory=dict)
    document_analyzed: bool = False
    
    # Pain points and specifications
    rfi_pain_points_items: Dict[str, str] = field(default_factory=dict)
    selected_pain_points: Set[str] = field(default_factory=set)
    pain_point_content_map: Dict[str, str] = field(default_factory=dict)
    
    # Additional specifications
    additional_specs_items: Dict[str, str] = field(default_factory=dict)
    selected_additional_specs: Set[str] = field(default_factory=set)
    additional_specs_content_map: Dict[str, str] = field(default_factory=dict)
    
    # Role and priority management
    selected_target_roles: List[str] = field(default_factory=list)
    selected_business_priorities: List[str] = field(default_factory=list)
    
    # Processing states
    show_validation: bool = False
    processing_rfi: bool = False
    scraping_in_progress: bool = False
    pending_scrape_url: Optional[str] = None
    url_search_in_progress: bool = False
    url_search_company: str = ""
    
    # UI state management
    css_applied: bool = False
    debug_mode: bool = False
    
    def to_session_state(self) -> None:
        """Save all dataclass fields to Streamlit session state."""
        try:
            for field_name, field_value in self.__dict__.items():
                # Handle Set objects by converting to list for JSON serialization
                if isinstance(field_value, set):
                    st.session_state[field_name] = list(field_value)
                else:
                    st.session_state[field_name] = field_value
            logger.debug("Client tab state saved to session state")
        except Exception as e:
            logger.error(f"Error saving client state to session: {str(e)}")
            set_global_message("Failed to save client state. Please try again.", "error")
    
    @classmethod
    def from_session_state(cls) -> 'ClientTabState':
        """Load client tab state from Streamlit session state."""
        try:
            # Get all field names from the dataclass
            field_names = {f.name for f in cls.__dataclass_fields__.values()}
            
            # Create kwargs dict with values from session state or defaults
            kwargs = {}
            for field_name in field_names:
                if field_name in st.session_state:
                    value = st.session_state[field_name]
                    
                    # Handle Set fields by converting from list
                    if field_name in ['selected_pain_points', 'selected_additional_specs']:
                        kwargs[field_name] = set(value) if isinstance(value, list) else value
                    else:
                        kwargs[field_name] = value
            
            instance = cls(**kwargs)
            logger.debug("Client tab state loaded from session state")
            return instance
            
        except Exception as e:
            logger.error(f"Error loading client state from session: {str(e)}")
            set_global_message("Failed to load client state. Using default values.", "error")
            return cls()  # Return default instance on error
    
    def update_field(self, field_name: str, value: Any) -> None:
        """Update a specific field and sync to session state."""
        try:
            if hasattr(self, field_name):
                setattr(self, field_name, value)
                
                # Handle Set objects for session state
                if isinstance(value, set):
                    st.session_state[field_name] = list(value)
                else:
                    st.session_state[field_name] = value
                
                logger.debug(f"Updated client state field: {field_name}")
            else:
                logger.warning(f"Attempted to update non-existent field: {field_name}")
                set_global_message(f"Invalid field update attempted: {field_name}", "error")
        except Exception as e:
            logger.error(f"Error updating field {field_name}: {str(e)}")
            set_global_message(f"Failed to update field {field_name}. Please try again.", "error")
    
    def update_multiple_fields(self, **kwargs) -> None:
        """Update multiple fields at once and sync to session state."""
        try:
            for field_name, value in kwargs.items():
                if hasattr(self, field_name):
                    setattr(self, field_name, value)
                else:
                    logger.warning(f"Attempted to update non-existent field: {field_name}")
            
            # Sync all changes to session state at once
            self.to_session_state()
            logger.debug(f"Updated multiple client state fields: {list(kwargs.keys())}")
            
        except Exception as e:
            logger.error(f"Error updating multiple fields: {str(e)}")
            set_global_message("Failed to update client state. Please try again.", "error")
    
    def clear_url_data(self) -> None:
        """Clear URL-related data when company name changes."""
        try:
            self.website_urls_list = []
            self.last_company_name = ""
            self.url_search_in_progress = False
            self.url_search_company = ""
            self.last_analyzed_url = None
            self.to_session_state()
            logger.debug("URL data cleared")
        except Exception as e:
            logger.error(f"Error clearing URL data: {str(e)}")
            set_global_message("Failed to clear URL data. Please refresh the page.", "error")
    
    def reset_processing_states(self) -> None:
        """Reset all processing-related states."""
        try:
            self.processing_rfi = False
            self.scraping_in_progress = False
            self.url_search_in_progress = False
            self.pending_scrape_url = None
            self.url_search_company = ""
            self.to_session_state()
            logger.debug("Processing states reset")
        except Exception as e:
            logger.error(f"Error resetting processing states: {str(e)}")
            set_global_message("Failed to reset processing states. Please refresh the page.", "error")
    
    def clear_linkedin_data(self) -> None:
        """Clear LinkedIn-related data when SPOC changes."""
        try:
            self.linkedin_profiles = {}
            self.last_searched_spoc = ""
            self.current_selected_profile_url = None
            self.to_session_state()
            logger.debug("LinkedIn data cleared")
        except Exception as e:
            logger.error(f"Error clearing LinkedIn data: {str(e)}")
            set_global_message("Failed to clear LinkedIn data. Please try again.", "error")
    
    def add_pain_point(self, key: str, content: str) -> None:
        """Add a pain point to the collection."""
        try:
            self.rfi_pain_points_items[key] = content
            self.pain_point_content_map[key] = content
            self.to_session_state()
            logger.debug(f"Added pain point: {key}")
        except Exception as e:
            logger.error(f"Error adding pain point: {str(e)}")
            set_global_message("Failed to add pain point. Please try again.", "error")
    
    def add_additional_spec(self, key: str, content: str) -> None:
        """Add an additional specification to the collection."""
        try:
            self.additional_specs_items[key] = content
            self.additional_specs_content_map[key] = content
            self.to_session_state()
            logger.debug(f"Added additional spec: {key}")
        except Exception as e:
            logger.error(f"Error adding additional spec: {str(e)}")
            set_global_message("Failed to add additional specification. Please try again.", "error")
    
    def toggle_pain_point_selection(self, key: str) -> None:
        """Toggle pain point selection state."""
        try:
            if key in self.selected_pain_points:
                self.selected_pain_points.remove(key)
            else:
                self.selected_pain_points.add(key)
            self.to_session_state()
            logger.debug(f"Toggled pain point selection: {key}")
        except Exception as e:
            logger.error(f"Error toggling pain point selection: {str(e)}")
            set_global_message("Failed to update pain point selection. Please try again.", "error")
    
    def toggle_additional_spec_selection(self, key: str) -> None:
        """Toggle additional specification selection state."""
        try:
            if key in self.selected_additional_specs:
                self.selected_additional_specs.remove(key)
            else:
                self.selected_additional_specs.add(key)
            self.to_session_state()
            logger.debug(f"Toggled additional spec selection: {key}")
        except Exception as e:
            logger.error(f"Error toggling additional spec selection: {str(e)}")
            set_global_message("Failed to update additional specification selection. Please try again.", "error")
    
    def validate_mandatory_fields(self) -> Dict[str, bool]:
        """Validate mandatory fields and return validation results."""
        validation_results = {
            'enterprise_name': bool(self.enterprise_name and self.enterprise_name.strip()),
            'client_requirements_content': bool(self.client_requirements_content and self.client_requirements_content.strip())
        }
        
        if self.debug_mode:
            logger.debug(f"Validation results: {validation_results}")
        
        return validation_results
    
    def validate_optional_fields(self) -> Dict[str, bool]:
        """Validate optional fields and return validation results."""
        validation_results = {
            'website_url': bool(self.website_url and self.website_url.strip()),
            'enterprise_details_content': bool(self.enterprise_details_content and self.enterprise_details_content.strip()),
            'spoc_name': bool(self.spoc_name and self.spoc_name.strip()),
            'has_selected_pain_points': bool(self.selected_pain_points),
            'has_selected_additional_specs': bool(self.selected_additional_specs),
            'has_target_roles': bool(self.selected_target_roles),
            'has_business_priorities': bool(self.selected_business_priorities)
        }
        
        return validation_results
    
    def is_mandatory_data_complete(self) -> bool:
        """Check if all mandatory data is complete."""
        validation_results = self.validate_mandatory_fields()
        return all(validation_results.values())
    
    def get_completion_percentage(self) -> float:
        """Get overall completion percentage of client data."""
        mandatory_fields = self.validate_mandatory_fields()
        optional_fields = self.validate_optional_fields()
        
        # Mandatory fields are weighted more heavily
        mandatory_weight = 0.7
        optional_weight = 0.3
        
        mandatory_completion = sum(mandatory_fields.values()) / len(mandatory_fields)
        optional_completion = sum(optional_fields.values()) / len(optional_fields)
        
        total_completion = (mandatory_completion * mandatory_weight) + (optional_completion * optional_weight)
        
        return round(total_completion * 100, 1)
    
    def clear_all_data(self) -> None:
        """Clear all client data and reset to default state."""
        try:
            self.__init__()
            self.to_session_state()
            logger.debug("All client data cleared")
        except Exception as e:
            logger.error(f"Error clearing all data: {str(e)}")
            set_global_message("Failed to clear all data. Please refresh the page.", "error")
    
    def export_summary(self) -> Dict[str, Any]:
        """Export a summary of the current client state."""
        return {
            'basic_info': {
                'enterprise_name': self.enterprise_name,
                'website_url': self.website_url,
                'spoc_name': self.spoc_name
            },
            'content': {
                'enterprise_details_length': len(self.enterprise_details_content),
                'requirements_length': len(self.client_requirements_content),
                'additional_requirements_length': len(self.client_additional_requirements_content)
            },
            'selections': {
                'pain_points_count': len(self.selected_pain_points),
                'additional_specs_count': len(self.selected_additional_specs),
                'target_roles_count': len(self.selected_target_roles),
                'business_priorities_count': len(self.selected_business_priorities)
            },
            'validation': {
                'mandatory_complete': self.is_mandatory_data_complete(),
                'completion_percentage': self.get_completion_percentage()
            }
        }


class ClientTabStateManager:
    """Manager class for handling ClientTabState persistence in Streamlit session state"""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ClientTabStateManager, cls).__new__(cls)
        return cls._instance
    
    def get_state(self) -> ClientTabState:
        """Get current client tab state."""
        return ClientTabState.from_session_state()
    
    def get_client_data(self) -> ClientTabState:
        """Alias for get_state() for backward compatibility."""
        return self.get_state()
    
    def update_field(self, field_name: str, value: Any) -> None:
        """Update a specific field in the client state."""
        state = self.get_state()
        state.update_field(field_name, value)
    
    def update_multiple_fields(self, **kwargs) -> None:
        """Update multiple fields at once."""
        state = self.get_state()
        state.update_multiple_fields(**kwargs)
    
    def update_client_data(self, **kwargs) -> None:
        """Alias for update_multiple_fields() for backward compatibility."""
        self.update_multiple_fields(**kwargs)
    
    def reset_processing_states(self) -> None:
        """Reset all processing states."""
        state = self.get_state()
        state.reset_processing_states()
    
    def clear_all_data(self) -> None:
        """Clear all client data."""
        state = self.get_state()
        state.clear_all_data()
    
    def validate_mandatory_fields(self) -> Dict[str, bool]:
        """Validate mandatory fields."""
        state = self.get_state()
        return state.validate_mandatory_fields()
    
    def is_mandatory_data_complete(self) -> bool:
        """Check if mandatory data is complete."""
        state = self.get_state()
        return state.is_mandatory_data_complete()
    
    def get_completion_percentage(self) -> float:
        """Get completion percentage."""
        state = self.get_state()
        return state.get_completion_percentage()
    
    def export_summary(self) -> Dict[str, Any]:
        """Export state summary."""
        state = self.get_state()
        return state.export_summary()
    
    # Additional backward compatibility methods
    def clear_url_data(self) -> None:
        """Clear URL-related data."""
        state = self.get_state()
        state.clear_url_data()
    
    def clear_linkedin_data(self) -> None:
        """Clear LinkedIn-related data."""
        state = self.get_state()
        state.clear_linkedin_data()
    
    def add_pain_point(self, key: str, content: str) -> None:
        """Add a pain point."""
        state = self.get_state()
        state.add_pain_point(key, content)
    
    def add_additional_spec(self, key: str, content: str) -> None:
        """Add an additional specification."""
        state = self.get_state()
        state.add_additional_spec(key, content)
    
    def toggle_pain_point_selection(self, key: str) -> None:
        """Toggle pain point selection."""
        state = self.get_state()
        state.toggle_pain_point_selection(key)
    
    def toggle_additional_spec_selection(self, key: str) -> None:
        """Toggle additional specification selection."""
        state = self.get_state()
        state.toggle_additional_spec_selection(key)


# Singleton instance
client_state_manager = ClientTabStateManager()

# Utility functions for backwards compatibility
def validate_client_mandatory_fields() -> bool:
    """Validate client mandatory fields using new state management."""
    return client_state_manager.is_mandatory_data_complete()

def get_client_enterprise_name() -> str:
    """Get client enterprise name."""
    state = client_state_manager.get_state()
    return state.enterprise_name

def set_client_enterprise_name(name: str):
    """Set client enterprise name."""
    client_state_manager.update_field('enterprise_name', name)

def get_client_requirements() -> str:
    """Get client requirements."""
    state = client_state_manager.get_state()
    return state.client_requirements_content

def set_client_requirements(requirements: str):
    """Set client requirements."""
    client_state_manager.update_field('client_requirements_content', requirements)

def get_client_website_url() -> str:
    """Get client website URL."""
    state = client_state_manager.get_state()
    return state.website_url

def set_client_website_url(url: str):
    """Set client website URL."""
    client_state_manager.update_field('website_url', url)

def get_client_spoc_name() -> str:
    """Get client SPOC name."""
    state = client_state_manager.get_state()
    return state.spoc_name

def set_client_spoc_name(name: str):
    """Set client SPOC name."""
    client_state_manager.update_field('spoc_name', name)

def get_client_selected_pain_points() -> Set[str]:
    """Get selected pain points."""
    state = client_state_manager.get_state()
    return state.selected_pain_points

def update_client_pain_point_selection(key: str):
    """Toggle pain point selection."""
    state = client_state_manager.get_state()
    state.toggle_pain_point_selection(key)