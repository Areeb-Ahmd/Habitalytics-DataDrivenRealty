import streamlit as st
import os
import importlib
import sys

# Import sidebar module
from sidebar import render_sidebar

# Set page config
st.set_page_config(
    page_title="Habitalytics - Real Estate Analytics Platform",
    layout="wide"
)

# Hide Streamlit default sidebar nav, main menu and footer
st.markdown(
    """
    <style>
    /* hide top-right hamburger menu */
    #MainMenu {visibility: hidden;}
    /* hide footer (Made with Streamlit) */
    footer {visibility: hidden;}
    /* hide default Pages navigation in the sidebar (multipage) */
    [data-testid="stSidebarNav"] {display: none;}
    </style>
    """,
    unsafe_allow_html=True,
)


# Inject custom CSS from external file
def set_background_color_and_text():
    css_path = os.path.join(os.path.dirname(__file__), "static", "theme.css")
    with open(css_path, "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
set_background_color_and_text()


# Display Home Page
def display_home():
    # Hero Section
    st.markdown("""
    <div style='text-align: center; padding: 0 0 1rem 0;'>
        <h1 style="
            font-size: clamp(2.4rem, 6vw, 4.5rem);
            font-weight: 900;
            margin-bottom: 0;
            line-height: 1.1;
            letter-spacing: clamp(3px, 1vw, 8px);
            text-align: center;">
            <span style='color: #ffffff; text-shadow: 2px 2px 4px rgba(0,0,0,0.5);'>HABITA</span><span style='color: #5fcf7c; text-shadow: 2px 2px 4px rgba(95, 207, 124, 0.5);'>LYTICS</span>
        </h1>
        <div style='width: 300px; height: 4px; background: linear-gradient(90deg, #ffffff 0%, #5fcf7c 100%);
                    margin: 1rem auto; border-radius: 2px;'></div>
        <p style='font-size: 1.4rem; color: #5fcf7c; font-weight: 700; 
                  margin-top: 0.5rem; line-height: 1; letter-spacing: 6px;'>
            Real Estate Analytics Platform
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Introduction
    st.markdown("""
        <div style='background: linear-gradient(135deg, #173b5b 0%, #2a5298 100%); 
                    padding: 2rem; border-radius: 10px; margin: 1.5rem 0;
                    border-left: 5px solid #64B5F6;'>
            <p style='font-size: 1.25rem; line-height: 1.8; color: #ffffff; margin: 0;'>
                <strong>Habitalytics</strong> is a machine learning–powered real estate analytics platform focused on the 
                Gurugram property market, designed to analyze, visualize, and predict real estate trends.
            </p>
            <p style='font-size: 1.25rem; line-height: 1.8; color: #ffffff; margin-top: 1rem;'>
                By integrating predictive modeling, exploratory data analysis, and intelligent recommendation systems, 
                the platform delivers accurate property valuations, sector-wise market insights, and personalized 
                property recommendations to support <strong>data-driven decision-making</strong>.
            </p>
        </div>
    """, unsafe_allow_html=True)

    # What We Offer Section
    st.markdown("""
        <h2 style='font-size: 2.2rem; font-weight: 600; margin: 2rem 0 1.5rem 0; color: #64B5F6;'>
            Platform Features
        </h2>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3, gap="large")

    with col1:
        st.markdown("""
            <div style='background: #1a1a2e; padding: 2rem; border-radius: 12px; 
                        border: 2px solid #2a2a40;
                        transition: transform 0.3s ease;'>
                <h3 style='color: #5fcf7c; font-size: 1.5rem; margin-bottom: 1rem; text-align: center;'>
                    Property Valuation
                </h3>
                <p style='color: #ffffff; line-height: 1.8; font-size: 1.1rem;'>
                    Predict property prices across Gurugram using machine learning models, 
                    giving you quick, estimates before buying or renting.
                </p>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
            <div style='background: #1a1a2e; padding: 2rem; border-radius: 12px; 
                        border: 2px solid #2a2a40;
                        transition: transform 0.3s ease;'>
                <h3 style='color: #5fcf7c; font-size: 1.5rem; margin-bottom: 1rem; text-align: center;'>
                    Analytics Dashboard
                </h3>
                <p style='color: #ffffff; line-height: 1.8; font-size: 1.1rem;'>
                    Explore Gurugram’s real estate market through sector-wise 
                    interactive visualizations and clear insights into pricing and trends.
                </p>
            </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
            <div style='background: #1a1a2e; padding: 2rem; border-radius: 12px; 
                        border: 2px solid #2a2a40;
                        transition: transform 0.3s ease;'>
                <h3 style='color: #5fcf7c; font-size: 1.5rem; margin-bottom: 1rem; text-align: center;'>
                    Property Recommender
                </h3>
                <p style='color: #ffffff; line-height: 1.8; font-size: 1.1rem;'>
                    Get property recommendations based on location and radius, 
                    along with similar society suggestions tailored to your preferences.
                </p>
            </div>
        """, unsafe_allow_html=True)


    # Why Habitalytics Section
    st.markdown("""
        <h2 style='font-size: 2.2rem; font-weight: 600; margin: 2rem 0 1.5rem 0; color: #64B5F6;'>
            Why Choose Habitalytics
        </h2>
    """, unsafe_allow_html=True)

    # Feature highlights in a styled box
    st.markdown("""
        <div style='background: linear-gradient(135deg, #0f2027 0%, #203a43 50%, #2c5364 100%); 
                    padding: 2rem; border-radius: 12px; margin: 1rem 0;'>
            <div style='display: grid; gap: 1rem;'>
                <div style='display: flex; align-items: start;'>
                    <span style='color: #64B5F6; font-size: 1.5rem; margin-right: 1rem;'>✓</span>
                    <p style='color: #ffffff; font-size: 1.2rem; margin: 0; line-height: 1.6;'>
                        Built specifically for the Gurugram real estate market  
                    </p>
                </div>
                <div style='display: flex; align-items: start;'>
                    <span style='color: #64B5F6; font-size: 1.5rem; margin-right: 1rem;'>✓</span>
                    <p style='color: #ffffff; font-size: 1.2rem; margin: 0; line-height: 1.6;'>
                        Delivers transparent, interactive, and data-backed insights  
                    </p>
                </div>
                <div style='display: flex; align-items: start;'>
                    <span style='color: #64B5F6; font-size: 1.5rem; margin-right: 1rem;'>✓</span>
                    <p style='color: #ffffff; font-size: 1.2rem; margin: 0; line-height: 1.6;'>
                        Designed for buyers, investors, and analysts alike
                    </p>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Who Benefits Section
    st.markdown("""
        <h2 style='font-size: 2.2rem; font-weight: 600; margin: 2rem 0 1.5rem 0; color: #64B5F6;'>
            Who It’s For
        </h2>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.markdown("""
            <div style='background: #1a1a2e; padding: 2rem; border-radius: 12px; 
                        border-left: 5px solid #64B5F6; margin-bottom: 1.5rem;'>
                <h3 style='color: #5fcf7c; margin-bottom: 1rem; text-align: center;'>Home Buyers</h3>
                <p style='color: #ffffff; line-height: 1.8; font-size: 1.1rem;'>
                    Make confident purchase decisions with accurate price predictions 
                    and clear neighborhood insights. 
                    Compare properties and understand fair market value with ease.
                </p>
            </div>
            
            <div style='background: #1a1a2e; padding: 2rem; border-radius: 12px; 
                        border-left: 5px solid #64B5F6;'>
                <h3 style='color: #5fcf7c; margin-bottom: 1rem; text-align: center;'>Real Estate Investors</h3>
                <p style='color: #ffffff; line-height: 1.8; font-size: 1.1rem;'>
                    Identify high-ROI opportunities, track appreciation trends, 
                    and analyze sector-wise market dynamics across Gurugram 
                    for smarter investments.
                </p>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
            <div style='background: #1a1a2e; padding: 2rem; border-radius: 12px; 
                        border-left: 5px solid #64B5F6; margin-bottom: 1.5rem;'>
                <h3 style='color: #5fcf7c; margin-bottom: 1rem; text-align: center;'>Property Sellers</h3>
                <p style='color: #ffffff; line-height: 1.8; font-size: 1.1rem;'>
                    Price your property competitively using real market data. 
                    Understand which features add value and position your listing for better returns.
                </p>
            </div>
            
            <div style='background: #1a1a2e; padding: 2rem; border-radius: 12px; 
                        border-left: 5px solid #64B5F6;'>
                <h3 style='color: #5fcf7c; margin-bottom: 1rem; text-align: center;'>Market Analysts</h3>
                <p style='color: #ffffff; line-height: 1.8; font-size: 1.1rem;'>
                    Access comprehensive market data, interactive visualizations, 
                    and trend analysis for research, reporting, 
                    and strategic planning in Gurugram’s real estate market.
                </p>
            </div>
        """, unsafe_allow_html=True)

    st.write("")

    # Call to Action
    st.markdown("""
        <div style='background: linear-gradient(135deg, #0f2027 0%, #203a43 50%, #2c5364 100%); 
                    padding: 1rem; border-radius: 10px; margin: 1rem 0;
                    text-align: center;'>
            <h3 style='color: #64B5F6; font-size: 2rem; margin: 0 0 0 0;'>
                Ready to Make Smarter Property Decisions?
            </h3>
            <p style='color: white; font-size: 1.1rem; margin: 0;'>
                <strong>Explore the tools from the sidebar and start 
                analyzing Gurugram’s real estate market.</strong>
            </p>
        </div>
    """, unsafe_allow_html=True)

    st.write("")

# Render sidebar and get selected page
selected = render_sidebar()

# Force reload all page modules on every run to ensure live updates
def reload_page_modules():
    """Reload page modules to pick up changes during development"""
    try:
        import pages
    except ImportError:
        pass
    
    page_modules = [
        'pages.Property_Valuation',
        'pages.Analytics_Dashboard', 
        'pages.Property_Recommender'
    ]
    
    for module_name in page_modules:
        if module_name in sys.modules:
            try:
                importlib.reload(sys.modules[module_name])
            except (ImportError, KeyError, AttributeError):
                if module_name in sys.modules:
                    del sys.modules[module_name]

reload_page_modules()


# Main content based on selection
if selected == "Home":
    display_home()
elif selected == "Property Valuation":
    from pages.Property_Valuation import show_property_valuation
    show_property_valuation()
elif selected == "Analytics Dashboard":
    from pages.Analytics_Dashboard import show_analytics_dashboard
    show_analytics_dashboard()
elif selected == "Property Recommender":
    from pages.Property_Recommender import property_recommender_model
    property_recommender_model()