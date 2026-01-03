import streamlit as st
from streamlit_option_menu import option_menu
import os
import importlib
import sys

# Set page config
st.set_page_config(
    page_title="Real Estate Analytics",
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


# Inject custom CSS
def set_background_color_and_text():
    st.markdown(
        f"""
        <style>
       
        /* Sidebar styling */
        section[data-testid="stSidebar"] {{
            background-color: #001f3f !important;
            color: #ffffff !important;
        }}

        /* Remove space above logo */
        section[data-testid="stSidebar"] .block-container {{
            padding-top: 0rem !important;
        }}
        
        section[data-testid="stSidebar"] > div {{
            padding-top: 0rem !important;
        }}
        
        /* Target the first element (logo) */
        section[data-testid="stSidebar"] [data-testid="stImage"] {{
            margin-top: -2rem !important;
            margin-bottom: 1.5rem !important;
        }}

        /* On hover */
        .stButton > button:hover {{
            color: #5fcf7c !important;
            border: 2px solid #000000 !important;
        }}

        /* Adjust the width of the main content */
        div.block-container {{
            padding: 1rem 5rem; /* Adjust padding for better spacing */
            max-width: 95%;    /* Increase the width of the main content */
            margin-top: -12px;
        }}

        /* Change selectbox focus border to green */
        .stSelectbox [data-baseweb="select"]:focus-within > div {{
            border-color: #5fcf7c !important;
            box-shadow: 0 0 0 1px #5fcf7c !important;
        }}

        /* Override ALL possible number input focus states with green */
        input[type="number"]:focus {{
            border-color: #5fcf7c !important;
            box-shadow: 0 0 0 1px #5fcf7c !important;
            outline: none !important;
        }}

        .stNumberInput input:focus {{
            border-color: #5fcf7c !important;
            box-shadow: 0 0 0 1px #5fcf7c !important;
            outline: none !important;
        }}

        .stNumberInput > div > div > input:focus {{
            border-color: #5fcf7c !important;
            box-shadow: 0 0 0 1px #5fcf7c !important;
            outline: none !important;
        }}

        [data-testid="stNumberInput"] input:focus {{
            border-color: #5fcf7c !important;
            box-shadow: 0 0 0 1px #5fcf7c !important;
            outline: none !important;
        }}

        /* Target the wrapper on focus-within */
        .stNumberInput:focus-within input {{
            border-color: #5fcf7c !important;
            box-shadow: 0 0 0 1px #5fcf7c !important;
        }}


        /* Even more subtle version */
        .stButton > button[kind="primary"] {{
            background-color: #1a3a2a !important;
            border: 2px solid #5fcf7c !important;
            color: #5fcf7c !important;
        }}

        .stButton > button[kind="primary"]:hover {{
        background-color: #2d5a3d !important;
            border: 2px solid #5fcf7c !important;
            box-shadow: 0 0 10px rgba(95, 207, 124, 0.3) !important;
        }}

        </style>
        """,
        unsafe_allow_html=True
    )
set_background_color_and_text()

#Display Home Page
def display_home():
    # Hero Section
    st.markdown("""
    <div style='text-align: center; padding: 0 0 1rem 0;'>
        <h1 style='font-size: 4.5rem; font-weight: 900; margin-bottom: 0; 
                   line-height: 1; letter-spacing: 8px;'>
            <span style='color: #ffffff; text-shadow: 2px 2px 4px rgba(0,0,0,0.5);'>HABITA</span><span style='color: #5fcf7c; text-shadow: 2px 2px 4px rgba(95, 207, 124, 0.5);'>LYTICS</span>
        </h1>
        <div style='width: 300px; height: 4px; background: linear-gradient(90deg, #ffffff 0%, #5fcf7c 100%);
                    margin: 1rem auto; border-radius: 2px;'></div>
        <p style='font-size: 1.4rem; color: #5fcf7c; font-weight: 700; 
                  margin-top: 0.5rem; line-height: 1; letter-spacing: 6px;'>
            DATA DRIVEN REALTY
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Introduction
    st.markdown("""
        <div style='background: linear-gradient(135deg, #173b5b 0%, #2a5298 100%); 
                    padding: 2rem; border-radius: 10px; margin: 1.5rem 0;
                    border-left: 5px solid #64B5F6;'>
            <p style='font-size: 1.1rem; line-height: 1.8; color: #ffffff; margin: 0;'>
                Welcome to <strong>Habitalytics</strong>, a cutting-edge platform that combines 
                <strong>Data Science</strong>, <strong>Machine Learning</strong>, and 
                <strong>Real Estate Intelligence</strong> to bring transparency and insight into property decisions.
            </p>
            <p style='font-size: 1.1rem; line-height: 1.8; color: #ffffff; margin-top: 1rem;'>
                Whether you're an investor, home buyer, or simply exploring market trends, 
                <strong>Habitalytics</strong> helps you make <strong>smarter, data-backed decisions</strong>.
            </p>
        </div>
    """, unsafe_allow_html=True)

    # What We Offer Section
    st.markdown("""
        <h2 style='font-size: 2.2rem; font-weight: 600; margin: 2rem 0 1.5rem 0;'>
            What We Offer
        </h2>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3, gap="large")

    with col1:
        st.markdown("""
            <div style='background: #1a1a2e; padding: 2rem; border-radius: 12px; 
                        height: 100%; border: 2px solid #2a2a40;
                        transition: transform 0.3s ease;'>
                <h3 style='color: #64B5F6; font-size: 1.4rem; margin-bottom: 1rem;'>
                    🔹Price Predictor
                </h3>
                <p style='color: #cccccc; line-height: 1.8; font-size: 1rem;'>
                    Predict property prices across Gurugram using ML models trained on location, 
                    area, furnishing, and local amenities.
                    Get an instant estimate before buying or renting.
                </p>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
            <div style='background: #1a1a2e; padding: 2rem; border-radius: 12px; 
                        height: 100%; border: 2px solid #2a2a40;
                        transition: transform 0.3s ease;'>
                <h3 style='color: #64B5F6; font-size: 1.4rem; margin-bottom: 1rem;'>
                    🔹 Analytics Dashboard
                </h3>
                <p style='color: #cccccc; line-height: 1.8; font-size: 1rem;'>
                    Explore <strong>Gurgaon's property landscape</strong> with sector-wise 
                    <strong>interactive visualizations</strong> and <strong>data insights</strong>.
                </p>
            </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
            <div style='background: #1a1a2e; padding: 2rem; border-radius: 12px; 
                        height: 100%; border: 2px solid #2a2a40;
                        transition: transform 0.3s ease;'>
                <h3 style='color: #64B5F6; font-size: 1.4rem; margin-bottom: 1rem;'>
                    🔹 Apartment Recommender
                </h3>
                <p style='color: #cccccc; line-height: 1.8; font-size: 1rem;'>
                    Get <strong>personalized apartment recommendations</strong> based on 
                    your preferred <strong>location and radius</strong> using our 
                    <strong>intelligent recommender system</strong>.
                </p>
            </div>
        """, unsafe_allow_html=True)


    # Why Habitalytics Section
    st.markdown("""
        <h2 style='font-size: 2.2rem; font-weight: 600; margin: 2rem 0 1.5rem 0;'>
            Why Habitalytics?
        </h2>
    """, unsafe_allow_html=True)

    # Feature highlights in a styled box
    st.markdown("""
        <div style='background: linear-gradient(135deg, #0f2027 0%, #203a43 50%, #2c5364 100%); 
                    padding: 2rem; border-radius: 12px; margin: 1rem 0;'>
            <div style='display: grid; gap: 1rem;'>
                <div style='display: flex; align-items: start;'>
                    <span style='color: #64B5F6; font-size: 1.5rem; margin-right: 1rem;'>✓</span>
                    <p style='color: #ffffff; font-size: 1.05rem; margin: 0; line-height: 1.6;'>
                        Built specifically for Gurugram’s real estate landscape
                    </p>
                </div>
                <div style='display: flex; align-items: start;'>
                    <span style='color: #64B5F6; font-size: 1.5rem; margin-right: 1rem;'>✓</span>
                    <p style='color: #ffffff; font-size: 1.05rem; margin: 0; line-height: 1.6;'>
                        Offers transparent, interactive, and accurate insights.
                    </p>
                </div>
                <div style='display: flex; align-items: start;'>
                    <span style='color: #64B5F6; font-size: 1.5rem; margin-right: 1rem;'>✓</span>
                    <p style='color: #ffffff; font-size: 1.05rem; margin: 0; line-height: 1.6;'>
                        Designed for <strong>buyers, sellers, investors, and analysts</strong> alike.
                    </p>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Who Benefits Section
    st.markdown("""
        <h2 style='font-size: 2.2rem; font-weight: 600; margin: 2rem 0 1.5rem 0;'>
            Who Benefits from Habitalytics?
        </h2>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.markdown("""
            <div style='background: #1a1a2e; padding: 2rem; border-radius: 12px; 
                        border-left: 5px solid #64B5F6; margin-bottom: 1.5rem;'>
                <h3 style='color: #5fcf7c; margin-bottom: 1rem;'>Home Buyers</h3>
                <p style='color: #cccccc; line-height: 1.8;'>
                    Make confident purchase decisions with accurate price predictions and comprehensive 
                    neighborhood insights. Compare properties and understand fair market value.
                </p>
            </div>
            
            <div style='background: #1a1a2e; padding: 2rem; border-radius: 12px; 
                        border-left: 5px solid #64B5F6;'>
                <h3 style='color: #5fcf7c; margin-bottom: 1rem;'>Real Estate Investors</h3>
                <p style='color: #cccccc; line-height: 1.8;'>
                    Identify high-ROI opportunities, track appreciation trends, and analyze market dynamics 
                    across Gurugram sectors. Data-driven investment decisions at your fingertips.
                </p>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
            <div style='background: #1a1a2e; padding: 2rem; border-radius: 12px; 
                        border-left: 5px solid #64B5F6; margin-bottom: 1.5rem;'>
                <h3 style='color: #5fcf7c; margin-bottom: 1rem;'>Property Sellers</h3>
                <p style='color: #cccccc; line-height: 1.8;'>
                    Price your property competitively based on real market data. Understand what features 
                    add value and position your listing for maximum returns.
                </p>
            </div>
            
            <div style='background: #1a1a2e; padding: 2rem; border-radius: 12px; 
                        border-left: 5px solid #64B5F6;'>
                <h3 style='color: #5fcf7c; margin-bottom: 1rem;'>Market Analysts</h3>
                <p style='color: #cccccc; line-height: 1.8;'>
                    Access comprehensive market data, visualizations, and trend analysis. Perfect for 
                    research, reporting, and strategic planning in Gurugram's real estate sector.
                </p>
            </div>
        """, unsafe_allow_html=True)

    st.write("")
    st.write("")

    # Call to Action
    st.markdown("""
        <div style='background: linear-gradient(135deg, #0f2027 0%, #203a43 50%, #2c5364 100%); 
                    padding: 1rem; border-radius: 10px; margin: 1rem 0;
                    text-align: center;'>
            <h3 style='color: white; font-size: 1.5rem; margin: 0 0 1rem 0;'>
                Ready to Make Smarter Property Decisions?
            </h3>
            <p style='color: white; font-size: 1.1rem; margin: 0;'>
                <strong>Select an application from the sidebar to get started!</strong>
            </p>
        </div>
    """, unsafe_allow_html=True)

    st.write("")


# Sidebar navigation using streamlit-option-menu
with st.sidebar:
    st.image(os.path.join("datasets", "logo4_upscaled.jpg"))
    
    selected = option_menu(
        menu_title="NAVIGATION",
        options=["Home", "Price Predictor", "Analytics", "Recommend Apartments"],
        icons=["house", "clock", "bar-chart", "cpu"],
        default_index=0,
        orientation="vertical",
        styles={
            "container": {"padding": "0!important", "background-color": "#001f3f"},
            "icon": {"color": "white", "font-size": "22px"},
            "nav-link": {"color": "white", "font-size": "18px", "text-align": "left", "margin":"0 0 0 0"},
            "nav-link-selected": {"background-color": "#003366", "color": "#5fcf7c"},
        }
    )
    
    # About Section
    st.markdown("### About")
    st.sidebar.info(
        "This dashboard leverages advanced analytics and machine learning to deliver "
        "actionable insights and accurate predictions for the Gurgaon real estate market. "
        "Designed for buyers, investors, and analysts, it empowers data-driven property decisions."
    )

    # Contact Section
    st.markdown("### Contact Developer")
    st.sidebar.markdown(
        """
        <div style='line-height: 1.6;'>
            <strong>Syed Areeb Ahmad</strong><br><br>
            <div style='display: flex; gap: 15px; align-items: center;'>
                <a href="mailto:ahmad.syedareeb7@gmail.com" 
                target="_blank" 
                style="text-decoration: none;">
                    <img src="https://cdn-icons-png.flaticon.com/512/5968/5968534.png" 
                        width="32" height="32" 
                        style="vertical-align: middle;"
                        alt="Gmail">
                </a>
                <a href="https://www.linkedin.com/in/areeb-ahmad7" 
                target="_blank" 
                style="text-decoration: none;">
                    <img src="https://cdn-icons-png.flaticon.com/512/174/174857.png" 
                        width="32" height="32" 
                        style="vertical-align: middle;"
                        alt="LinkedIn">
                </a>
                <a href="https://github.com/Areeb-Ahmd" 
                target="_blank" 
                style="text-decoration: none;">
                    <img src="https://cdn-icons-png.flaticon.com/512/25/25231.png" 
                        width="32" height="32" 
                        style="vertical-align: middle;"
                        alt="GitHub">
                </a>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

# Force reload all page modules on every run to ensure live updates
# This ensures changes in page files are immediately reflected
def reload_page_modules():
    """Reload page modules to pick up changes during development"""
    # Import pages package first to ensure it's in sys.modules (required for submodule reload)
    try:
        import pages
    except ImportError:
        pass
    
    page_modules = [
        'pages.Price_Predictor',
        'pages.Analysis_App', 
        'pages.Recommend_Apartments'
    ]
    
    # Reload each page module if it exists
    for module_name in page_modules:
        if module_name in sys.modules:
            try:
                importlib.reload(sys.modules[module_name])
            except (ImportError, KeyError, AttributeError):
                # If reload fails, remove from cache so it gets reimported fresh
                if module_name in sys.modules:
                    del sys.modules[module_name]

reload_page_modules()

# Main content based on selection
if selected == "Home":
    display_home()
elif selected == "Price Predictor":
    from pages.Price_Predictor import show_price_predictor
    show_price_predictor()
elif selected == "Analytics":
    from pages.Analysis_App import show_analysis_app
    show_analysis_app()
elif selected == "Recommend Apartments":
    from pages.Recommend_Apartments import recommendation_model
    recommendation_model()