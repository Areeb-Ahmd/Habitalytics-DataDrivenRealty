import streamlit as st
import pickle
import requests
import os
from pathlib import Path

@st.cache_data(show_spinner=False)
def _load_dropdown_df():
    """
    Load the dataframe used to populate dropdowns.
    """
    candidates = [
        Path("df.pkl"),
        Path(__file__).with_name("df.pkl"),
        Path(__file__).resolve().parents[1] / "df.pkl",
    ]

    for p in candidates:
        if p.exists():
            with p.open("rb") as f:
                return pickle.load(f)

    raise FileNotFoundError(
        "Could not find df.pkl. Tried: " + ", ".join(str(p) for p in candidates)
    )


def show_property_valuation():
    # Hero Section
    st.markdown("""
    <div style='text-align: center; padding: 0 0 1rem 0;'>
        <h1 style='font-size: 3.5rem; font-weight: 900; margin-bottom: 0; 
                   line-height: 1; letter-spacing: 6px;'>
            <span style='color: #ffffff; text-shadow: 2px 2px 4px rgba(0,0,0,0.5);'>PROPERTY </span><span style='color: #5fcf7c; text-shadow: 2px 2px 4px rgba(95, 207, 124, 0.5);'>VALUATION</span>
        </h1>
        <div style='width: 250px; height: 4px; background: linear-gradient(90deg, #ffffff 0%, #5fcf7c 100%);
                    margin: 1rem auto; border-radius: 2px;'></div>
        <p style='font-size: 1.2rem; color: #5fcf7c; font-weight: 600; 
                  margin-top: 0.5rem; line-height: 1; letter-spacing: 4px;'>
            Property Price Estimation for Gurugram
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
        <div style='background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%); 
                    padding: 1.5rem; border-radius: 10px; margin: 1rem 0;
                    border-left: 5px solid #64B5F6;'>
            <p style='font-size: 1.25rem; line-height: 1.6; color: #ffffff; margin: 0;'>
                Habitalytics’ Property Price Evaluation provides an estimated property price based 
                on the details you enter and patterns observed in historical 
                real estate data from <strong>Gurugram</strong>. 
            </p>
            <p style='font-size: 1.25rem; line-height: 1.6; color: #ffffff; margin-top: 1rem;'>
                The result is an estimate intended to support comparison and decision-making, 
                not a guaranteed sale or purchase price. Actual prices may vary based on negotiation, 
                property condition, timing, and local market conditions.
            </p>

        </div>
    """, unsafe_allow_html=True)

    # For local: http://localhost:8000
    API_URL = os.getenv("API_URL", "http://localhost:8000")

    # Load data for dropdowns only (no model loading)
    try:
        df = _load_dropdown_df()
    except FileNotFoundError as e:
        st.error(str(e))
        return

    # Input Section Header with Info Button
    col_header, _, col_info = st.columns([3, 2, 1])

    with col_header:
        st.markdown("""
            <h2 style='font-size: 1.8rem; font-weight: 600; margin: 1.5rem 0 1rem 0; color: #64B5F6;'>
                Enter Property Details
            </h2>
        """, unsafe_allow_html=True)

    with col_info:
        with st.popover("Field Guide",icon="ℹ️" ,use_container_width=True):
            st.markdown("""
                <h3 style='color: #5fcf7c; font-size: 1.5rem; margin-bottom: 0.2rem; text-align: center;'>
                    Field Guide
                </h3>
            """, unsafe_allow_html=True)

            guide_sections = [
                (
                    "Property Type",
                    "<strong>Flat (apartment):</strong> Unit in a multi-storey building/society."
                    "<br><strong>House:</strong> Independent house/villa/builder floor-type property.",
                ),
                ("Sector", "The locality/sector in Gurugram where the property is located."),
                ("Built-up Area", "The property’s built-up area in square feet."),
                ("Number of Bedrooms (BHK)", "Count of bedrooms (1–10 in your dropdown)."),
                ("Number of Bathrooms", "Total bathrooms (including attached + common)."),
                ("Number of Balconies", "Allowed values: 0, 1, 2, 3, 3+"),
                (
                    "Property Age",
                    "<strong>• New Property:</strong> ~0–1 year old / immediate possession.<br>"
                    "<strong>• Relatively New:</strong> ~1–5 years old.<br>"
                    "<strong>• Moderately Old:</strong> ~5–10 years old.<br>"
                    "<strong>• Old Property:</strong> 10+ years old.<br>"
                    "<strong>• Under Construction:</strong> Not ready; possession date in future.",
                ),
                (
                    "Furnishing Type",
                    "<strong>• Unfurnished:</strong> Bare unit (no major furniture, basic fittings only).<br>"
                    "<strong>• Semifurnished:</strong> Some fixed fittings (wardrobes/modular kitchen/ACs etc.).<br>"
                    "<strong>• Furnished:</strong> Move-in ready with most furniture/appliances.",
                ),
                (
                    "Luxury Category",
                    "<strong>• Low:</strong> Basic/generic amenities (e.g., lift/park/security).<br>"
                    "<strong>• Medium:</strong> Typical gated-society amenities "
                    "<br>(e.g., gym/clubhouse/pool or multiple facilities).<br>"
                    "<strong>• High:</strong> Premium/luxury amenities set (many high-end facilities).",
                ),
                (
                    "Floor Category",
                    "<strong>• Low Floor:</strong> Floors 0–2<br>"
                    "<strong>• Mid Floor:</strong> Floors 3–10<br>"
                    "<strong>• High Floor:</strong> Floors 11+",
                ),
                (
                    "Servant Room",
                    "<strong>What it means:</strong> Dedicated servant/helper room present.<br>"
                    "<strong>How to answer:</strong> Yes (1) if there is a separate servant/helper room, otherwise No (0).",
                ),
                (
                    "Store Room",
                    "<strong>What it means:</strong> Dedicated storage/store room present.<br>"
                    "<strong>How to answer:</strong> Yes (1) if there’s a separate store room, otherwise No (0).",
                ),
            ]

            for title, desc in guide_sections:
                st.markdown(
                    f"""
                    <div class="guide-section">
                        <div class="guide-title">{title}</div>
                        <div class="guide-desc">{desc}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )


    # Create two columns for better layout
    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.markdown("""
            <h4 style='color: #64B5F6; font-size: 1.2rem; font-weight: 600; margin-bottom: 1rem;'>
                Basic Information
            </h4>
        """, unsafe_allow_html=True)
        property_type = st.selectbox('Property Type', ['flat', 'house'])
        sector = st.selectbox('Sector', sorted(df['sector'].unique().tolist()))
        bedrooms = int(st.selectbox('Number of Bedrooms', sorted(df['bedRoom'].unique().tolist())))
        bathroom = int(st.selectbox('Number of Bathrooms', sorted(df['bathroom'].unique().tolist())))
        balcony = st.selectbox('Number of Balconies', sorted(df['balcony'].unique().tolist()))
        property_age = st.selectbox('Property Age', sorted(df['agePossession'].unique().tolist()))

    with col2:
        st.markdown("""
            <h4 style='color: #64B5F6; font-size: 1.2rem; font-weight: 600; margin-bottom: 1rem;'>
                Area & Features
            </h4>
        """, unsafe_allow_html=True)
        built_up_area = float(st.number_input('Built-up Area (in sqft)', min_value=0.0, step=50.0))
        servant_room = int(st.selectbox('Servant Room', [0, 1]))
        store_room = int(st.selectbox('Store Room', [0, 1]))
        furnishing_type = st.selectbox('Furnishing Type', sorted(df['furnishing_type'].unique().tolist()))
        luxury_category = st.selectbox('Luxury Category', sorted(df['luxury_category'].unique().tolist()))
        floor_category = st.selectbox('Floor Category', sorted(df['floor_category'].unique().tolist()))

    st.markdown("<br>", unsafe_allow_html=True)

    # Predict Button with custom styling
    _, col_btn2, _ = st.columns([1, 2, 1])
    with col_btn2:
        predict_button = st.button('Predict Price', use_container_width=True, type="primary")

    if predict_button:
        # Validate input
        if built_up_area <= 0:
            st.markdown("""
                <div style='background: linear-gradient(135deg, #3a1a1a 0%, #4a2a2a 100%); 
                            padding: 1.2rem; border-radius: 12px; margin: 1rem 0;
                            border-left: 4px solid #ff6b6b;
                            box-shadow: 0 2px 8px rgba(255, 107, 107, 0.2);'>
                    <p style='color: #ffcccc; margin: 0; font-size: 1rem; line-height: 1.6;'>
                        ⚠️ Please enter a valid Built-up Area
                    </p>
                </div>
            """, unsafe_allow_html=True)
        else:
            # Prepare request payload
            payload = {
                "property_type": property_type,
                "sector": sector,
                "bedRoom": bedrooms,
                "bathroom": bathroom,
                "balcony": str(balcony),
                "agePossession": property_age,
                "built_up_area": built_up_area,
                "servant_room": servant_room,
                "store_room": store_room,
                "furnishing_type": furnishing_type,
                "luxury_category": luxury_category,
                "floor_category": floor_category
            }
            
            # Call FastAPI endpoint
            try:
                with st.spinner("Predicting price..."):
                    response = requests.post(f"{API_URL}/predict", json=payload, timeout=30)
                    response.raise_for_status()
                    result = response.json()
                    
                    base_price = result["base_price"]
                    low = result["lower_range"]
                    high = result["upper_range"]
            except requests.exceptions.ConnectionError:
                st.markdown("""
                    <div style='background: linear-gradient(135deg, #3a1a1a 0%, #4a2a2a 100%); 
                                padding: 1.2rem; border-radius: 12px; margin: 1rem 0;
                                border-left: 4px solid #ff6b6b;
                                box-shadow: 0 2px 8px rgba(255, 107, 107, 0.2);'>
                        <p style='color: #ffcccc; margin: 0; font-size: 1rem; line-height: 1.6;'>
                            ⚠️ Cannot connect to prediction service. Please ensure the API server is running.
                        </p>
                    </div>
                """, unsafe_allow_html=True)
                st.markdown(f"""
                    <div style='background: linear-gradient(135deg, #1a1a2e 0%, #2a2a4e 100%); 
                                padding: 1rem; border-radius: 12px; margin: 1rem 0;
                                border-left: 4px solid #64B5F6;'>
                        <p style='color: #ffffff; margin: 0; font-size: 0.9rem; line-height: 1.6;'>
                            ℹ️ Trying to connect to: {API_URL}
                        </p>
                    </div>
                """, unsafe_allow_html=True)
                return
            except requests.exceptions.RequestException as e:
                st.markdown(f"""
                    <div style='background: linear-gradient(135deg, #3a1a1a 0%, #4a2a2a 100%); 
                                padding: 1.2rem; border-radius: 12px; margin: 1rem 0;
                                border-left: 4px solid #ff6b6b;
                                box-shadow: 0 2px 8px rgba(255, 107, 107, 0.2);'>
                        <p style='color: #ffcccc; margin: 0; font-size: 1rem; line-height: 1.6;'>
                            ⚠️ Error connecting to prediction service: {str(e)}
                        </p>
                    </div>
                """, unsafe_allow_html=True)
                return

            # Display Results with styling
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Single card container for all prices - using HTML structure
            low_val = round(low, 2)
            base_val = round(base_price, 2)
            high_val = round(high, 2)
            
            st.markdown(f"""
                <div style='background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%); 
                            padding: 1.5rem 1.5rem; border-radius: 16px; margin: 1rem 0;
                            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);'>
                    <div style='display: flex; justify-content: space-around; align-items: flex-start; gap: 1.5rem; flex-wrap: wrap;'>
                        <div style='flex: 1; min-width: 150px; text-align: center;'>
                            <div style='color: #ffffff; font-size: 0.95rem; margin-bottom: 0.5rem;'>
                                🔻 Lower Range
                            </div>
                            <div style='color: #ffffff; font-size: 1.8rem; font-weight: 700;'>
                                ₹ {low_val} Cr
                            </div>
                        </div>
                        <div style='flex: 1; min-width: 150px; text-align: center;'>
                            <div style='color: #ffffff; font-size: 0.95rem; margin-bottom: 0.5rem;'>
                                🎯 Base Price
                            </div>
                            <div style='color: #ffffff; font-size: 1.8rem; font-weight: 700; margin-bottom: 0.5rem;'>
                                ₹ {base_val} Cr
                            </div>
                            <div style='color: #5fcf7c; background-color: rgba(95, 207, 124, 0.2); 
                                        border-radius: 6px; padding: 0.25rem 0.5rem; display: inline-block; font-size: 0.85rem;'>
                                ↑ Estimated
                            </div>
                        </div>
                        <div style='flex: 1; min-width: 150px; text-align: center;'>
                            <div style='color: #ffffff; font-size: 0.95rem; margin-bottom: 0.5rem;'>
                                🔺 Upper Range
                            </div>
                            <div style='color: #ffffff; font-size: 1.8rem; font-weight: 700;'>
                                ₹ {high_val} Cr
                            </div>
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            # Modern Property Summary
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("""
                <h3 style='color: #64B5F6; font-size: 1.75rem; margin: 1.5rem 0 1rem 0;'>
                    Property Summary
                </h3>
            """, unsafe_allow_html=True)
            
            # Summary Cards
            summary_col1, summary_col2 = st.columns(2, gap="small")
            
            with summary_col1:
                st.markdown(f"""
                    <div style='background: linear-gradient(135deg, #1a1a2e 0%, #2a2a4e 100%); 
                                padding: 1.0rem; border-radius: 12px; 
                                border-left: 4px solid #64B5F6; height: 100%;'>
                        <h4 style='color: #64B5F6; margin-bottom: 0.5rem; font-size: 1.25rem;'>
                            Property Details
                        </h4>
                        <div style='color: #ffffff; line-height: 2;'>
                            <div style='display: flex; justify-content: space-between; padding: 0.5rem 0; border-bottom: 1px solid #3a3a5e;'>
                                <span>Type:</span>
                                <strong style='color: #5fcf7c;'>{property_type.title()}</strong>
                            </div>
                            <div style='display: flex; justify-content: space-between; padding: 0.5rem 0; border-bottom: 1px solid #3a3a5e;'>
                                <span>Location:</span>
                                <strong style='color: #5fcf7c;'>{sector}</strong>
                            </div>
                            <div style='display: flex; justify-content: space-between; padding: 0.5rem 0; border-bottom: 1px solid #3a3a5e;'>
                                <span>Built-up Area:</span>
                                <strong style='color: #5fcf7c;'>{int(built_up_area)} sqft</strong>
                            </div>
                            <div style='display: flex; justify-content: space-between; padding: 0.5rem 0; border-bottom: 1px solid #3a3a5e;'>
                                <span>Property Age:</span>
                                <strong style='color: #5fcf7c;'>{property_age}</strong>
                            </div>
                            <div style='display: flex; justify-content: space-between; padding: 0.5rem 0; border-bottom: 1px solid #3a3a5e;'>
                                <span>Floor Category:</span>
                                <strong style='color: #5fcf7c;'>{floor_category}</strong>
                            </div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
            
            with summary_col2:
                st.markdown(f"""
                    <div style='background: linear-gradient(135deg, #1a1a2e 0%, #2a2a4e 100%); 
                                padding: 1.0rem; border-radius: 12px; 
                                border-left: 4px solid #5fcf7c; height: 100%;'>
                        <h4 style='color: #5fcf7c; margin-bottom: 0.5rem; font-size: 1.25rem;'>
                            Features & Amenities
                        </h4>
                        <div style='color: #ffffff; line-height: 2;'>
                            <div style='display: flex; justify-content: space-between; padding: 0.5rem 0; border-bottom: 1px solid #3a3a5e;'>
                                <span>Bedrooms:</span>
                                <strong style='color: #64B5F6;'>{int(bedrooms)} BHK</strong>
                            </div>
                            <div style='display: flex; justify-content: space-between; padding: 0.5rem 0; border-bottom: 1px solid #3a3a5e;'>
                                <span>Bathrooms:</span>
                                <strong style='color: #64B5F6;'>{int(bathroom)}</strong>
                            </div>
                            <div style='display: flex; justify-content: space-between; padding: 0.5rem 0; border-bottom: 1px solid #3a3a5e;'>
                                <span>Balconies:</span>
                                <strong style='color: #64B5F6;'>{balcony}</strong>
                            </div>
                            <div style='display: flex; justify-content: space-between; padding: 0.5rem 0; border-bottom: 1px solid #3a3a5e;'>
                                <span>Furnishing:</span>
                                <strong style='color: #64B5F6;'>{furnishing_type.title()}</strong>
                            </div>
                            <div style='display: flex; justify-content: space-between; padding: 0.5rem 0; border-bottom: 1px solid #3a3a5e;'>
                                <span>Luxury Tier:</span>
                                <strong style='color: #64B5F6;'>{luxury_category}</strong>
                            </div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
            
            # Additional Rooms Row
            servant_icon = "✅" if servant_room == 1 else "❌"
            store_icon = "✅" if store_room == 1 else "❌"
            st.markdown(f"""
                <div style='background: linear-gradient(135deg, #1a1a2e 0%, #2a2a4e 100%); 
                            padding: 1.0rem; border-radius: 12px; margin-top: 0.75rem;
                            border-left: 4px solid #64B5F6;'>
                    <h4 style='color: #64B5F6; margin-bottom: 0.5rem; font-size: 1.25rem;'>
                        Additional Spaces
                    </h4>
                    <div style='display: grid; grid-template-columns: repeat(2, 1fr); gap: 1rem; color: #cccccc;'>
                        <div style='background: rgba(100, 181, 246, 0.1); padding: 1rem; border-radius: 8px; text-align: center;'>
                            <div style='font-size: 1.5rem; margin-bottom: 0.5rem;'>
                                {servant_icon}
                            </div>
                            <div style='font-size: 0.9rem; color: #ffffff;'>Servant Room</div>
                        </div>
                        <div style='background: rgba(95, 207, 124, 0.1); padding: 1rem; border-radius: 8px; text-align: center;'>
                            <div style='font-size: 1.5rem; margin-bottom: 0.5rem;'>
                                {store_icon}
                            </div>
                            <div style='font-size: 0.9rem; color: #ffffff;'>Store Room</div>
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    
    # Footer information
    st.markdown("""
        <div style='background: #1a1a2e; padding: 1.5rem; border-radius: 12px; 
                    border-left: 5px solid #5fcf7c; margin: 1rem 0;'>
            <h4 style='color: #5fcf7c; margin-bottom: 1rem;'>How Our Model Works</h4>
            <p style='color: #ffffff; font-size: 1.25rem; line-height: 1.8; margin: 0;'>
                The model is trained on historical property transaction data, 
                where it learns how different property features have related to 
                observed prices in similar market contexts.
            </p>
            <p style='color: #ffffff; font-size: 1.25rem; line-height: 1.8; margin: 0; margin-top: 1rem;'>
                When you submit your inputs, the system evaluates all features together such as location,
                size, and amenities to generate a price estimate that reflects patterns present 
                in the training data. The estimate does not rely on real-time market data and 
                should be used as a data-driven reference rather than a precise valuation.
            </p>
        </div>
    """, unsafe_allow_html=True)


# Call the main function
if __name__ == "__main__":
    show_property_valuation()