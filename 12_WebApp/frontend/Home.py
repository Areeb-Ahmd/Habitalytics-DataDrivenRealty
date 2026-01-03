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
       
        /* Main app background - BLACK */
        .stApp {{
            background-color: #000000 !important;
        }}
        
        /* Main content area background - BLACK */
        section.main {{
            background-color: #000000 !important;
        }}
        
        div.block-container {{
            background-color: #000000 !important;
            padding: 1rem 5rem;
            max-width: 95%;
            margin-top: -12px;
        }}
       
        /* Sidebar styling */
        section[data-testid="stSidebar"] {{
            background-color: #001f3f !important;
            color: #ffffff !important;
        }}
        
        /* Remove corner triangles from navigation menu - consolidated */
        section[data-testid="stSidebar"] [class*="option-menu"]::before,
        section[data-testid="stSidebar"] [class*="option-menu"]::after,
        section[data-testid="stSidebar"] [class*="option-menu"] *::before,
        section[data-testid="stSidebar"] [class*="option-menu"] *::after {{
            display: none !important;
            content: none !important;
            visibility: hidden !important;
        }}
        
        section[data-testid="stSidebar"] [class*="option-menu"] {{
            border: none !important;
            box-shadow: none !important;
            border-radius: 0 !important;
        }}
        
        section[data-testid="stSidebar"] [class*="corner"],
        section[data-testid="stSidebar"] [class*="triangle"],
        section[data-testid="stSidebar"] [class*="decoration"] {{
            display: none !important;
        }}
        
        /* Sidebar navigation text color - consolidated */
        section[data-testid="stSidebar"] [class*="nav-link"],
        section[data-testid="stSidebar"] [class*="nav-link"] *,
        section[data-testid="stSidebar"] [class*="option-menu"] a,
        section[data-testid="stSidebar"] [class*="option-menu"] a * {{
            color: #ffffff !important;
        }}
        
        /* Navigation menu title - consolidated */
        section[data-testid="stSidebar"] h3,
        section[data-testid="stSidebar"] [class*="menu-title"],
        section[data-testid="stSidebar"] [class*="menu-title"] *,
        section[data-testid="stSidebar"] [class*="option-menu"] h3 {{
            color: #ffffff !important;
        }}
        
        /* About section text color - consolidated */
        section[data-testid="stSidebar"] .stAlert,
        section[data-testid="stSidebar"] [data-testid="stAlert"] {{
            background-color: #1a1a2e !important;
            border-left-color: #64B5F6 !important;
        }}
        
        section[data-testid="stSidebar"] .stAlert *,
        section[data-testid="stSidebar"] .stMarkdown *,
        section[data-testid="stSidebar"] h3,
        section[data-testid="stSidebar"] h4 {{
            color: #ffffff !important;
        }}
        
        /* Preserve selected nav link green color */
        section[data-testid="stSidebar"] [class*="nav-link-selected"],
        section[data-testid="stSidebar"] [class*="nav-link-selected"] * {{
            color: #5fcf7c !important;
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

        /* ===== INPUT FIELD STYLING FOR DARK THEME ===== */
        
        /* Selectbox styling - Dark background */
        .stSelectbox > div > div {{
            background-color: #1a1a2e !important;
            border: 1px solid #2a2a4e !important;
        }}
        
        .stSelectbox label {{
            color: #ffffff !important;
        }}
        
        .stSelectbox [data-baseweb="select"] {{
            background-color: #1a1a2e !important;
        }}
        
        .stSelectbox [data-baseweb="select"] > div {{
            background-color: #1a1a2e !important;
            color: #ffffff !important;
        }}
        
        /* Selectbox text color */
        .stSelectbox [data-baseweb="select"] * {{
            color: #ffffff !important;
        }}
        
        /* Selectbox dropdown menu */
        [data-baseweb="popover"] {{
            background-color: #1a1a2e !important;
            color: #ffffff !important;
        }}
        
        [data-baseweb="popover"] * {{
            color: #ffffff !important;
        }}
        
        [data-baseweb="menu"] {{
            background-color: #1a1a2e !important;
            color: #ffffff !important;
        }}
        
        [data-baseweb="menu"] * {{
            color: #ffffff !important;
        }}
        
        [data-baseweb="menu"] li {{
            background-color: #1a1a2e !important;
            color: #ffffff !important;
        }}
        
        [data-baseweb="menu"] li:hover {{
            background-color: #2a2a4e !important;
            color: #ffffff !important;
        }}
        
        /* Dropdown menu item text - consolidated */
        [data-baseweb="menu"] li,
        [data-baseweb="menu"] li *,
        [data-baseweb="menu"] [data-baseweb="option"],
        [data-baseweb="menu"] [data-baseweb="option"] *,
        [data-baseweb="popover"] [data-baseweb="menu"] * {{
            color: #ffffff !important;
        }}
        
        [data-baseweb="menu"] li[aria-selected="true"],
        [data-baseweb="menu"] [data-baseweb="option"][aria-selected="true"],
        [data-baseweb="menu"] [data-baseweb="option"]:hover {{
            background-color: #2a2a4e !important;
            color: #ffffff !important;
        }}
        
        /* Number input styling - Dark background */
        .stNumberInput > div > div > input {{
            background-color: #1a1a2e !important;
            color: #ffffff !important;
            border: 1px solid #2a2a4e !important;
        }}
        
        /* Number input background - consolidated */
        input[type="number"],
        .stNumberInput input,
        [data-testid="stNumberInput"] input,
        [data-baseweb="input"] input,
        .stNumberInput > div > div,
        .stNumberInput div {{
            background-color: #1a1a2e !important;
            color: #ffffff !important;
            border: 1px solid #2a2a4e !important;
        }}
        
        .stNumberInput input[type="number"]::-webkit-inner-spin-button,
        .stNumberInput input[type="number"]::-webkit-outer-spin-button {{
            background-color: #1a1a2e !important;
        }}
        
        .stNumberInput label {{
            color: #ffffff !important;
        }}
        
        /* Number input increment/decrement buttons */
        .stNumberInput button {{
            background-color: #1a1a2e !important;
            color: #ffffff !important;
            border: 1px solid #2a2a4e !important;
        }}
        
        .stNumberInput button:hover {{
            background-color: #2a2a4e !important;
            color: #5fcf7c !important;
            border-color: #5fcf7c !important;
        }}
        
        
        /* Text input styling - Dark background */
        .stTextInput > div > div > input {{
            background-color: #1a1a2e !important;
            color: #ffffff !important;
            border: 1px solid #2a2a4e !important;
        }}
        
        .stTextInput label {{
            color: #ffffff !important;
        }}
        
        /* Only style Streamlit default text, not markdown with inline styles */
        /* Don't override inline styles in markdown - removed h1-h6 and p/div/span rules */
        
        /* Change selectbox focus border to green */
        .stSelectbox [data-baseweb="select"]:focus-within > div {{
            border-color: #5fcf7c !important;
            box-shadow: 0 0 0 1px #5fcf7c !important;
        }}
        
        /* Selectbox dropdown text */
        .stSelectbox [data-baseweb="popover"] [data-baseweb="menu"] *,
        div[data-baseweb="popover"] div[data-baseweb="menu"] * {{
            color: #ffffff !important;
        }}

        /* Number input focus state */
        input[type="number"]:focus,
        .stNumberInput input:focus,
        .stNumberInput:focus-within input {{
            border-color: #5fcf7c !important;
            box-shadow: 0 0 0 1px #5fcf7c !important;
            outline: none !important;
        }}
        
        /* Popover button styling (Field Guide) */
        [data-testid="stPopover"] button {{
            background-color: #1a1a2e !important;
            color: #64B5F6 !important;
            border: 1px solid #2a2a4e !important;
        }}
        
        [data-testid="stPopover"] button:hover {{
            background-color: #2a2a4e !important;
            color: #5fcf7c !important;
            border-color: #5fcf7c !important;
        }}
        
        /* Additional popover button selectors for better coverage */
        button[data-testid="baseButton-secondary"] {{
            background-color: #1a1a2e !important;
            color: #64B5F6 !important;
            border: 1px solid #2a2a4e !important;
        }}
        
        button[data-testid="baseButton-secondary"]:hover {{
            background-color: #2a2a4e !important;
            color: #5fcf7c !important;
            border-color: #5fcf7c !important;
        }}
        
        /* Popover content styling (Field Guide) - consolidated */
        [data-testid="stPopover"] div:not(.guide-section),
        [data-baseweb="popover"] div:not(.guide-section) {{
            background-color: #1a1a2e !important;
        }}
        
        [data-testid="stPopover"] .guide-section {{
            background: linear-gradient(135deg, #1a1a2e 0%, #2a2a4e 100%) !important;
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

        html, body {{
            background-color: #000000 !important;
        }}

        /* Root containers (deployment-safe) */
        .stApp,
        div[data-testid="stAppViewContainer"],
        div[data-testid="stAppViewContainer"] > div {{
            background-color: #000000 !important;
        }}

        /* Header + toolbar (multiple fallbacks) */
        header,
        header[data-testid="stHeader"],
        div[data-testid="stToolbar"],
        div[data-testid="stDecoration"] {{
            background-color: #000000 !important;
            box-shadow: none !important;
            border: none !important;
        }}

        /* Kill any gradient / overlay layer */
        div[data-testid="stDecoration"] {{
            display: none !important;
        }}

        /* Prevent top padding gap */
        section.main {{
            padding-top: 0rem !important;
        }}

        /* ================= MOBILE FIXES ================= */
        @media (max-width: 768px) {{

            /* Reduce side padding */
            div.block-container {{
                padding: 1rem 1rem !important;
                max-width: 100% !important;
            }}

            /* Hero title scaling */
            h1 {{
                font-size: 2.4rem !important;
                letter-spacing: 4px !important;
                line-height: 1.1 !important;
                text-align: center !important;
            }}

            /* Subtitle text */
            p {{
                font-size: 1rem !important;
                letter-spacing: 3px !important;
                text-align: center !important;
            }}

            /* Cards padding */
            div[style*="padding: 2rem"] {{
                padding: 1.2rem !important;
            }}

            /* Remove fixed heights */
            div[style*="height: 100%"] {{
                height: auto !important;
            }}

            /* Sidebar width */
            section[data-testid="stSidebar"] {{
                width: 85vw !important;
            }}

            /* Sidebar logo */
            section[data-testid="stSidebar"] img {{
                max-width: 90% !important;
                height: auto !important;
                margin: 0 auto !important;
                display: block !important;
            }}
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
        <h2 style='font-size: 2.2rem; font-weight: 600; margin: 2rem 0 1.5rem 0; color: #ffffff;'>
            What We Offer
        </h2>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3, gap="large")

    with col1:
        st.markdown("""
            <div style='background: #1a1a2e; padding: 2rem; border-radius: 12px; 
                        border: 2px solid #2a2a40;
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
                        border: 2px solid #2a2a40;
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
                        border: 2px solid #2a2a40;
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
        <h2 style='font-size: 2.2rem; font-weight: 600; margin: 2rem 0 1.5rem 0; color: #ffffff;'>
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
        <h2 style='font-size: 2.2rem; font-weight: 600; margin: 2rem 0 1.5rem 0; color: #ffffff;'>
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
    
    # JavaScript to remove corner triangles if CSS doesn't work
    st.markdown("""
    <script>
    (function() {
        function removeTriangles() {
            // Find all elements in the sidebar with option-menu classes
            const sidebar = document.querySelector('section[data-testid="stSidebar"]');
            if (!sidebar) return;
            
            // Find option menu container
            const optionMenus = sidebar.querySelectorAll('[class*="option-menu"]');
            optionMenus.forEach(menu => {
                // Remove all ::before and ::after pseudo-elements
                const style = document.createElement('style');
                style.textContent = `
                    [class*="option-menu"]::before,
                    [class*="option-menu"]::after,
                    [class*="option-menu"] *::before,
                    [class*="option-menu"] *::after {
                        display: none !important;
                        content: none !important;
                        visibility: hidden !important;
                    }
                `;
                document.head.appendChild(style);
                
                // Remove any absolutely positioned small elements (likely triangles)
                const allElements = menu.querySelectorAll('*');
                allElements.forEach(el => {
                    const style = window.getComputedStyle(el);
                    if ((style.position === 'absolute' || style.position === 'fixed') &&
                        (parseInt(style.width) < 20 || parseInt(style.height) < 20)) {
                        el.style.display = 'none';
                    }
                });
            });
        }
        
        // Run immediately and also after a short delay
        removeTriangles();
        setTimeout(removeTriangles, 100);
        setTimeout(removeTriangles, 500);
        
        // Also run when DOM changes
        const observer = new MutationObserver(removeTriangles);
        observer.observe(document.body, { childList: true, subtree: true });
    })();
    </script>
    """, unsafe_allow_html=True)
    
    selected = option_menu(
        menu_title="NAVIGATION",
        options=["Home", "Price Predictor", "Analytics", "Recommend Apartments"],
        icons=["house", "clock", "bar-chart", "cpu"],
        default_index=0,
        orientation="vertical",
        styles={
            "container": {"padding": "0!important", "background-color": "#001f3f", "border": "none", "box-shadow": "none", "border-radius": "0", "outline": "none"},
            "icon": {"color": "white", "font-size": "22px"},
            "nav-link": {"color": "white", "font-size": "18px", "text-align": "left", "margin":"0 0 0 0"},
            "nav-link-selected": {"background-color": "#003366", "color": "#5fcf7c"},
            "menu-title": {"color": "#ffffff", "font-size": "18px", "font-weight": "600"},
        }
    )
    
    # About Section - Modern Design
    st.sidebar.markdown("""
        <div style='margin: 1.5rem 0;'>
            <h3 style='color: #5fcf7c; font-size: 1.2rem; font-weight: 700; 
                       margin: 0 0 0.8rem 0; letter-spacing: 1px;
                       text-transform: uppercase;'>
                About
            </h3>
            <div style='border-left: 3px solid #5fcf7c; padding-left: 1rem; margin-left: 0.3rem;'>
                <p style='color: #e5e7eb; line-height: 1.8; font-size: 0.95rem; 
                          margin: 0; text-align: justify;'>
                    This dashboard leverages advanced analytics and machine learning to deliver 
                    actionable insights and accurate predictions for the Gurgaon real estate market. 
                    Designed for buyers, investors, and analysts, it empowers data-driven property decisions.
                </p>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Contact Developer Section - Modern Design
    st.sidebar.markdown("""
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