"""
Sidebar module for the Habitalytics frontend.
Contains navigation menu, about section, and contact information.
"""
import streamlit as st
from streamlit_option_menu import option_menu
import os


def render_sidebar() -> str:
    """
    Render the complete sidebar with logo, navigation, about, and contact sections.
    
    Returns:
        str: The selected menu option
    """
    with st.sidebar:
        # Logo
        st.image(os.path.join("datasets", "logo4_upscaled.jpg"))
        
        # Inject JavaScript for triangle removal
        _inject_sidebar_js()
        
        # Navigation menu
        selected = _render_navigation()
        
        # About section
        _render_about_section()
        
        # Contact section
        _render_contact_section()
    
    return selected


def _inject_sidebar_js():
    """Inject JavaScript to remove corner triangles from option menu."""
    js_path = os.path.join(os.path.dirname(__file__), "static", "sidebar.js")
    with open(js_path, "r", encoding="utf-8") as f:
        st.markdown(f"<script>{f.read()}</script>", unsafe_allow_html=True)


def _render_navigation() -> str:
    """Render the navigation menu and return selected option."""
    return option_menu(
        menu_title="NAVIGATION",
        options=["Home", "Property Valuation", "Analytics Dashboard", "Property Recommender"],
        icons=["house", "clock", "bar-chart", "cpu"],
        default_index=0,
        orientation="vertical",
        styles={
            "container": {
                "padding": "0!important",
                "background-color": "#001f3f",
                "border": "none",
                "box-shadow": "none",
                "border-radius": "0",
                "outline": "none"
            },
            "icon": {"color": "white", "font-size": "22px"},
            "nav-link": {
                "color": "white",
                "font-size": "18px",
                "text-align": "left",
                "margin": "0 0 0 0"
            },
            "nav-link-selected": {
                "background-color": "#003366",
                "color": "#5fcf7c"
            },
            "menu-title": {
                "color": "#ffffff",
                "font-size": "18px",
                "font-weight": "600"
            },
        }
    )


def _render_about_section():
    """Render the About section in the sidebar."""
    st.markdown("""
        <div style='margin: 1.5rem 0;'>
            <h3 style='color: #5fcf7c; font-size: 1.2rem; font-weight: 700; 
                       margin: 0 0 0.8rem 0; letter-spacing: 1px;
                       text-transform: uppercase;'>
                About
            </h3>
            <div style='border-left: 3px solid #5fcf7c; padding-left: 1rem; margin-left: 0.3rem;'>
                <p style='color: #e5e7eb; line-height: 1.8; font-size: 1rem; 
                          margin: 0; text-align: left;'>
                    A machine learning–powered real estate analytics platform for Gurugram, 
                    offering accurate valuations, market insights, 
                    and an intelligent recommender system for properties and similar societies.
                </p>
            </div>
        </div>
    """, unsafe_allow_html=True)


def _render_contact_section():
    """Render the Contact Developer section in the sidebar."""
    st.markdown("""
        <div style='margin: 1.5rem 0;'>
            <h3 style='color: #5fcf7c; font-size: 1.2rem; font-weight: 700; 
                       margin: 0 0 0.8rem 0; letter-spacing: 1px;
                       text-transform: uppercase;'>
                Contact Developer
            </h3>
            <div style='border-left: 3px solid #5fcf7c; padding-left: 1rem; margin-left: 0.3rem;'>
                <p style='color: #ffffff; font-size: 1.05rem; font-weight: 600; 
                          margin: 0 0 1rem 0;'>
                    Syed Areeb Ahmad
                </p>
                <div style='display: flex; gap: 18px; align-items: center; margin-top: 1rem;'>
                    <a href="mailto:ahmad.syedareeb7@gmail.com" 
                       target="_blank" 
                       style="text-decoration: none; 
                              transition: all 0.3s ease;
                              display: inline-block;"
                       onmouseover="this.style.transform='translateY(-3px)'; this.style.opacity='0.8'"
                       onmouseout="this.style.transform='translateY(0)'; this.style.opacity='1'">
                        <img src="https://cdn-icons-png.flaticon.com/512/5968/5968534.png" 
                             width="38" height="38" 
                             style="vertical-align: middle;"
                             alt="Gmail">
                    </a>
                    <a href="https://www.linkedin.com/in/areeb-ahmad7" 
                       target="_blank" 
                       style="text-decoration: none; 
                              transition: all 0.3s ease;
                              display: inline-block;"
                       onmouseover="this.style.transform='translateY(-3px)'; this.style.opacity='0.8'"
                       onmouseout="this.style.transform='translateY(0)'; this.style.opacity='1'">
                        <img src="https://cdn-icons-png.flaticon.com/512/174/174857.png" 
                             width="38" height="38" 
                             style="vertical-align: middle;"
                             alt="LinkedIn">
                    </a>
                    <a href="https://github.com/Areeb-Ahmd" 
                       target="_blank" 
                       style="text-decoration: none; 
                              transition: all 0.3s ease;
                              display: inline-block;"
                       onmouseover="this.style.transform='translateY(-3px)'; this.style.opacity='0.8'"
                       onmouseout="this.style.transform='translateY(0)'; this.style.opacity='1'">
                        <img src="https://cdn-icons-png.flaticon.com/512/25/25231.png" 
                             width="38" height="38" 
                             style="vertical-align: middle;"
                             alt="GitHub">
                    </a>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)
