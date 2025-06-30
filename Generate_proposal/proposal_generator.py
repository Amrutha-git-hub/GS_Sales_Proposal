import streamlit as st
import time
from datetime import datetime
from Generate_proposal.generate_proposal_css import *

def render_preview_tab():
    """
    Renders the professional proposal format preview and generation interface
    """

    
    # Create columns for format previews
    col1, col2 = st.columns(2)
    
    with col1:
        # Modern Professional Format
        with st.container():
            st.markdown("### 🎨 Modern Professional")
            st.caption("Clean, minimalist design with bold typography and subtle gradients")
            
            modern_preview = """
            <div style="background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%); 
                        padding: 20px; border-radius: 12px; border: 1px solid #e5e7eb; margin: 15px 0;
                        box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                <div style="background: white; padding: 20px; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.1);">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
                        <div style="width: 50px; height: 50px; background: #2563eb; border-radius: 6px; display: flex; align-items: center; justify-content: center;">
                            <span style="color: white; font-weight: bold; font-size: 18px;">A</span>
                        </div>
                        <div style="color: #6b7280; font-size: 12px; font-weight: 600;">PROPOSAL #2024-001</div>
                    </div>
                    <div style="height: 10px; background: #2563eb; border-radius: 5px; margin-bottom: 15px;"></div>
                    <div style="margin-bottom: 20px;">
                        <div style="height: 6px; background: #e5e7eb; border-radius: 3px; margin: 3px 0;"></div>
                        <div style="height: 6px; background: #e5e7eb; border-radius: 3px; width: 80%; margin: 3px 0;"></div>
                        <div style="height: 6px; background: #e5e7eb; border-radius: 3px; width: 65%; margin: 3px 0;"></div>
                        <div style="height: 6px; background: #e5e7eb; border-radius: 3px; width: 45%; margin: 3px 0;"></div>
                    </div>
                    <div style="display: flex; justify-content: space-between; align-items: center; padding-top: 15px; border-top: 1px solid #f3f4f6;">
                        <div style="color: #2563eb; font-weight: bold; font-size: 18px;">Proposal</div>
                        <div style="background: #2563eb; color: white; padding: 8px 16px; border-radius: 6px; font-size: 12px; font-weight: 600;">ACCEPT PROPOSAL</div>
                    </div>
                </div>
            </div>
            """
            st.markdown(modern_preview, unsafe_allow_html=True)
        
        # Creative Bold Format
        with st.container():
            st.markdown("### 🌈 Creative Bold")
            st.caption("Eye-catching design with vibrant colors and modern elements")
            
            creative_preview = """
            <div style="background: linear-gradient(135deg, #fdf4ff 0%, #fce7f3 100%); 
                        padding: 20px; border-radius: 12px; border: 1px solid #e5e7eb; margin: 15px 0;
                        box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                <div style="background: white; padding: 20px; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
                    <div style="display: flex; align-items: center; margin-bottom: 20px;">
                        <div style="width: 40px; height: 40px; background: linear-gradient(45deg, #a855f7, #ec4899); 
                                    border-radius: 50%; margin-right: 15px; display: flex; align-items: center; justify-content: center;">
                            <span style="color: white; font-weight: bold;">✨</span>
                        </div>
                        <div style="flex: 1;">
                            <div style="height: 10px; background: linear-gradient(45deg, #a855f7, #ec4899); 
                                        border-radius: 5px; width: 70%;"></div>
                        </div>
                    </div>
                    <div style="margin-bottom: 20px;">
                        <div style="height: 6px; background: #f3f4f6; border-radius: 3px; margin: 3px 0;"></div>
                        <div style="height: 6px; background: #f3f4f6; border-radius: 3px; width: 85%; margin: 3px 0;"></div>
                        <div style="height: 6px; background: #f3f4f6; border-radius: 3px; width: 60%; margin: 3px 0;"></div>
                    </div>
                    <div style="background: linear-gradient(45deg, #a855f7, #ec4899); color: white; 
                                padding: 12px; border-radius: 8px; text-align: center; font-size: 14px; font-weight: bold;
                                box-shadow: 0 2px 4px rgba(168, 85, 247, 0.3);">
                     Proposal
                    </div>
                </div>
            </div>
            """
            st.markdown(creative_preview, unsafe_allow_html=True)
    
    with col2:
        # Classic Business Format
        with st.container():
            st.markdown("### 📊 Classic Business")
            st.caption("Traditional corporate layout with professional styling")
            
            classic_preview = """
            <div style="background: #f8fafc; padding: 20px; border-radius: 8px; border: 2px solid #e2e8f0; margin: 15px 0;">
                <div style="background: white; padding: 20px; border-radius: 4px; border: 1px solid #cbd5e1;">
                    <div style="border-bottom: 2px solid #e2e8f0; padding-bottom: 15px; margin-bottom: 20px;">
                        <div style="height: 16px; background: #1e293b; border-radius: 2px; width: 120px; margin-bottom: 8px;"></div>
                        <div style="height: 10px; background: #64748b; border-radius: 2px; width: 90px;"></div>
                    </div>
                    <div style="margin-bottom: 20px;">
                        <div style="height: 5px; background: #cbd5e1; border-radius: 2px; margin: 5px 0;"></div>
                        <div style="height: 5px; background: #cbd5e1; border-radius: 2px; width: 85%; margin: 5px 0;"></div>
                        <div style="height: 5px; background: #cbd5e1; border-radius: 2px; width: 70%; margin: 5px 0;"></div>
                        <div style="height: 5px; background: #cbd5e1; border-radius: 2px; width: 55%; margin: 5px 0;"></div>
                    </div>
                    <div style="border-top: 2px solid #e2e8f0; padding-top: 15px;">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <span style="color: #475569; font-size: 14px; font-weight: 600;">TOTAL AMOUNT:</span>
                            <div style="color: #1e293b; font-weight: bold; font-size: 18px;">$12,500.00</div>
                        </div>
                    </div>
                </div>
            </div>
            """
            st.markdown(classic_preview, unsafe_allow_html=True)
        
        # Minimal Clean Format
        with st.container():
            st.markdown("### ⚪ Minimal Clean")
            st.caption("Ultra-clean design focusing on content with maximum readability")
            
            minimal_preview = """
            <div style="background: white; padding: 25px; border-radius: 8px; border: 2px solid #f1f5f9; margin: 15px 0;
                        box-shadow: 0 1px 3px rgba(0,0,0,0.05);">
                <div style="padding: 15px;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 25px;">
                        <div style="width: 12px; height: 12px; background: #0f172a; border-radius: 50%;"></div>
                        <div style="color: #94a3b8; font-size: 11px; letter-spacing: 2px; font-weight: 600;">PROPOSAL</div>
                    </div>
                    <div style="margin-bottom: 25px;">
                        <div style="height: 6px; background: #0f172a; border-radius: 1px; width: 45%; margin-bottom: 15px;"></div>
                        <div style="height: 1px; background: #e2e8f0; margin: 6px 0;"></div>
                        <div style="height: 1px; background: #e2e8f0; width: 90%; margin: 6px 0;"></div>
                        <div style="height: 1px; background: #e2e8f0; width: 75%; margin: 6px 0;"></div>
                        <div style="height: 1px; background: #e2e8f0; width: 60%; margin: 6px 0;"></div>
                    </div>
                    <div style="text-align: right; border-top: 1px solid #f1f5f9; padding-top: 15px;">
                        <div style="font-family: 'Courier New', monospace; font-size: 16px; color: #0f172a; font-weight: 600;">
                            $12,500.00
                        </div>
                    </div>
                </div>
            </div>
            """
            st.markdown(minimal_preview, unsafe_allow_html=True)
    
    # Format selection
    st.divider()
    st.subheader("🎯 Select Your Preferred Format")
    
    format_options = [
        "🎨 Modern Professional", 
        "📊 Classic Business", 
        "🌈 Creative Bold", 
        "⚪ Minimal Clean"
    ]
    
    selected_format = st.radio(
        "Choose the format that best suits your brand:",
        options=format_options,
        index=0,
        horizontal=True
    )
    
    # Proposal Summary Section
    st.divider()
    st.subheader("📊 Proposal Overview")
    
    # Create professional metrics display
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Client Organization",
            value="Growth sutra",
            help="Target client company"
        )
    
    with col2:
        st.metric(
            label="Service Category",
            value="Web Development",
            help="Primary service offering"
        )
    
    with col3:
        st.metric(
            label="Project Value",
            value="$12,500",
            help="Total proposal amount"
        )
    
    with col4:
        st.metric(
            label="Delivery Timeline",
            value="8-10 weeks",
            help="Estimated completion time"
        )
    
    # Enhanced details section
    with st.expander("📋 Comprehensive Project Summary", expanded=False):
        detail_col1, detail_col2 = st.columns(2)
        
        with detail_col1:
            st.markdown("**Client Information**")
            st.write("• **Organization:** Growth sutra")
            st.write("• **Primary Contact:** Vishwendra verma, CEO")
            st.write("• **Email:** xyz@gmail.com")
            st.write("• **Phone:** 9999999999")
            st.write("• **Industry:** Technology Solutions")
            
        with detail_col2:
            st.markdown("**Project Specifications**")
            st.write("• **Service Package:** Premium Web Development")
            st.write("• **Payment Structure:** 50% upfront, 50% at completion")
            st.write("• **Post-Launch Support:** 6 months included")
            st.write("• **Key Deliverables:** Custom website, SEO optimization")
            st.write("• **Technology Stack:** React, Node.js, MongoDB")
    
    # Professional Generate Proposal Section
    st.divider()
   
    
    # Professional generate button section
    st.markdown("---")
    
    # Center column for generate button
    gen_col1, gen_col2, gen_col3 = st.columns([1, 2, 1])
    
    with gen_col2:
        st.markdown(f"""
        <div style="text-align: center; padding: 20px; background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%); 
                    border-radius: 12px; border: 1px solid #cbd5e1; margin: 20px 0;">
            <h4 style="color: #334155; margin-bottom: 10px;">Ready to Generate</h4>
            <p style="color: #64748b; font-size: 14px; margin-bottom: 20px;">
                Format: <strong>{selected_format}</strong><br>
                Client: <strong>Growth sutra</strong><br>
                Value: <strong>$12,500</strong>
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        generate_clicked = st.button(
            "🚀 Generate Professional Proposal",
            type="primary",
            use_container_width=True,
            help=f"Generate comprehensive proposal using {selected_format} format"
        )
    
    # Enhanced generation process
    if generate_clicked:
        # Professional loading interface
        with st.container():
            st.markdown("### 🔄 Generating Your Professional Proposal")
            
            # Progress tracking
            progress_container = st.container()
            with progress_container:
                progress_bar = st.progress(0)
                status_container = st.empty()
                detail_container = st.empty()
                
                # Stage 1: Data Validation
                with status_container:
                    st.info("🔍 **Stage 1/5:** Validating client data and project requirements...")
                with detail_container:
                    st.caption("Verifying client information, project scope, and pricing structure")
                time.sleep(1.2)
                progress_bar.progress(20)
                
                # Stage 2: Template Processing
                with status_container:
                    st.info(f"🎨 **Stage 2/5:** Applying {selected_format} template...")
                with detail_container:
                    st.caption("Customizing design elements, branding, and layout structure")
                time.sleep(1.0)
                progress_bar.progress(40)
                
                # Stage 3: Content Generation
                with status_container:
                    st.info("📝 **Stage 3/5:** Generating proposal content...")
                with detail_container:
                    st.caption("Creating executive summary, project details, and pricing breakdown")
                time.sleep(1.3)
                progress_bar.progress(60)
                
                # Stage 4: Legal & Compliance
                with status_container:
                    st.info("⚖️ **Stage 4/5:** Adding legal terms and compliance sections...")
                with detail_container:
                    st.caption("Incorporating terms of service, privacy policy, and contract clauses")
                time.sleep(1.0)
                progress_bar.progress(80)
                
                # Stage 5: Final Review
                with status_container:
                    st.info("✨ **Stage 5/5:** Final review and optimization...")
                with detail_container:
                    st.caption("Quality assurance, formatting verification, and deliverable preparation")
                time.sleep(1.0)
                progress_bar.progress(100)
                
                # Clear progress indicators
                time.sleep(0.5)
                progress_bar.empty()
                status_container.empty()
                detail_container.empty()
        
        # Professional success display
        st.success("✅ **Proposal Generation Complete**")
        
        
        # Generation summary
        current_time = datetime.now().strftime('%B %d, %Y at %I:%M %p')
        
        success_container = st.container()
        with success_container:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #ecfdf5 0%, #d1fae5 100%); 
                        padding: 25px; border-radius: 12px; border: 1px solid #10b981; margin: 20px 0;">
                <h3 style="color: #065f46; margin-bottom: 15px;">📋 Proposal Successfully Generated</h3>
                <div style="background: white; padding: 20px; border-radius: 8px; margin-bottom: 15px;">
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px;">
                        <div>
                            <strong style="color: #374151;">Template:</strong><br>
                            <span style="color: #6b7280;">{selected_format}</span>
                        </div>
                        <div>
                            <strong style="color: #374151;">Client:</strong><br>
                            <span style="color: #6b7280;">Growth sutra</span>
                        </div>
                        <div>
                            <strong style="color: #374151;">Project Value:</strong><br>
                            <span style="color: #6b7280;">$12,500.00</span>
                        </div>
                        <div>
                            <strong style="color: #374151;">Generated:</strong><br>
                            <span style="color: #6b7280;">{current_time}</span>
                        </div>
                    </div>
                </div>
                <div style="background: #f0fdf4; padding: 15px; border-radius: 6px; border-left: 4px solid #10b981;">
                    <strong style="color: #166534;">📄 Document Details:</strong><br>
                    <span style="color: #166534;">15 pages • Professional format • Terms included • Ready for delivery</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Professional action buttons
        st.subheader("📤 Proposal Management")
        
        action_col1, action_col2, action_col3, action_col4 = st.columns(4)
        
        with action_col1:
            if st.button("📧 Send Proposal", use_container_width=True, type="primary"):
                st.success("✅ Proposal sent to john.smith@acme.com")
                st.info("📬 Delivery confirmation and tracking enabled")
                
        with action_col2:
            if st.button("📥 Download PDF", use_container_width=True):
                st.success("📥 Professional PDF ready for download")
                st.info("📊 15-page document with all attachments")
                
        with action_col3:
            if st.button("👀 Preview Document", use_container_width=True):
                st.success("👀 Opening interactive preview...")
                st.info("🔍 Full document preview with navigation")
                
        with action_col4:
            if st.button("📊 Generate Report", use_container_width=True):
                st.success("📊 Proposal analytics generated")
                st.info("📈 Performance metrics and insights available")
        
        # Additional professional features
        st.markdown("---")
        st.subheader("🔧 Advanced Options")
        
        advanced_col1, advanced_col2 = st.columns(2)
        
        with advanced_col1:
            st.markdown("**Client Interaction**")
            if st.button("📅 Schedule Presentation", use_container_width=True):
                st.info("📅 Meeting scheduler opened for client presentation")
            if st.button("💬 Send Follow-up", use_container_width=True):
                st.info("💬 Automated follow-up sequence initiated")
                
        with advanced_col2:
            st.markdown("**Document Management**")
            if st.button("📋 Create Variations", use_container_width=True):
                st.info("📋 Alternative proposal versions created")
            if st.button("🔄 Version Control", use_container_width=True):
                st.info("🔄 Document versioning and history available")

# Professional main function
def generate_tab():
    """
    Professional Streamlit app configuration and execution
    """
    st.markdown(proposal_css,unsafe_allow_html=True)
    
    # Custom CSS for professional styling (optional)
    st.markdown("""
        <style>
        .main > div {
            padding: 2rem 3rem;
        }
        .stButton > button {
            border-radius: 6px;
            border: 1px solid #e5e7eb;
            transition: all 0.2s;
        }
        .stButton > button:hover {
            transform: translateY(-1px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }
        </style>
    """, unsafe_allow_html=True)
    
    render_preview_tab()

