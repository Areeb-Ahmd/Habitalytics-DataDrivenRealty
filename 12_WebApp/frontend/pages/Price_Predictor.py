import streamlit as st
import pandas as pd
import numpy as np
import pickle
import requests
import os


def show_price_predictor():
    # Hero Section
    st.markdown("""
    <div style='text-align: center; padding: 0 0 1rem 0;'>
        <h1 style='font-size: 3.5rem; font-weight: 900; margin-bottom: 0; 
                   line-height: 1; letter-spacing: 6px;'>
            <span style='color: #ffffff; text-shadow: 2px 2px 4px rgba(0,0,0,0.5);'>PRICE </span><span style='color: #5fcf7c; text-shadow: 2px 2px 4px rgba(95, 207, 124, 0.5);'>PREDICTOR</span>
        </h1>
        <div style='width: 250px; height: 4px; background: linear-gradient(90deg, #ffffff 0%, #5fcf7c 100%);
                    margin: 1rem auto; border-radius: 2px;'></div>
        <p style='font-size: 1.2rem; color: #5fcf7c; font-weight: 600; 
                  margin-top: 0.5rem; line-height: 1; letter-spacing: 4px;'>
            AI-Powered Property Valuation
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
        <div style='background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%); 
                    padding: 1.5rem; border-radius: 10px; margin: 1rem 0;
                    border-left: 5px solid #64B5F6;'>
            <p style='font-size: 1rem; line-height: 1.6; color: #ffffff; margin: 0;'>
                Get accurate property price predictions based on location, amenities, and market trends. 
                Our <strong>Machine Learning model</strong> analyzes multiple factors to provide you with 
                a <strong>reliable price range</strong> for your property.
            </p>
        </div>
    """, unsafe_allow_html=True)

    # API endpoint - use environment variable or default
    # For local: http://localhost:8000
    # For production: set API_URL environment variable
    API_URL = os.getenv("API_URL", "http://localhost:8000")

    # Load data for dropdowns only (no model loading)
    with open('df.pkl', 'rb') as file:
        df = pickle.load(file)

    # Input Section Header with Info Button
    col_header, col_spacer, col_info = st.columns([3, 2, 1])

    with col_header:
        st.markdown("""
            <h2 style='font-size: 1.8rem; font-weight: 600; margin: 1.5rem 0 1rem 0; color: #64B5F6;'>
                Enter Property Details
            </h2>
        """, unsafe_allow_html=True)

    with col_info:
        with st.popover("Field Guide",icon="ℹ️" ,use_container_width=True):
            st.markdown("""
                <style>
                .guide-section {
                    background: linear-gradient(135deg, #1a1a2e 0%, #2a2a4e 100%);
                    padding: 0.6rem 0.8rem;
                    border-radius: 6px;
                    margin-bottom: 0.5rem;
                    border-left: 3px solid #64B5F6;
                }
                .guide-title {
                    color: #64B5F6;
                    font-weight: bold;
                    font-size: 0.9rem;
                    margin-bottom: 0.2rem;
                }
                .guide-desc {
                    color: #cccccc;
                    font-size: 0.8rem;
                    line-height: 1.4;
                    margin: 0;
                }
                </style>
            """, unsafe_allow_html=True)
            
            st.markdown("""
                <h3 style='color: #5fcf7c; font-size: 1.1rem; margin-bottom: 0.4rem; text-align: center;'>
                    Field Guide
                </h3>
            """, unsafe_allow_html=True)
            
            st.markdown("""
                <div class="guide-section">
                    <div class="guide-title">Property Type</div>
                    <div class="guide-desc">Flat (apartment) <br> House (independent)</div>
                </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
                <div class="guide-section">
                    <div class="guide-title">Sector</div>
                    <div class="guide-desc">Location sector in Gurugram</div>
                </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
                <div class="guide-section">
                    <div class="guide-title">Built-up Area</div>
                    <div class="guide-desc">Total carpet area in square feet</div>
                </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
                <div class="guide-section">
                    <div class="guide-title">Property Age</div>
                    <div class="guide-desc">Years since construction completion</div>
                </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
                <div class="guide-section">
                    <div class="guide-title">Furnishing Type</div>
                    <div class="guide-desc">
                        • Furnished: Fully equipped<br>
                        • Semi-furnished: Partial<br>
                        • Unfurnished: No furniture
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
                <div class="guide-section">
                    <div class="guide-title">Luxury Category</div>
                    <div class="guide-desc">Property luxury tier based on amenities</div>
                </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
                <div class="guide-section">
                    <div class="guide-title">Floor Category</div>
                    <div class="guide-desc">Floor positioning (Low/Mid/High)</div>
                </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
                <div class="guide-section">
                    <div class="guide-title">Servant Room</div>
                    <div class="guide-desc">Servant/helper quarters availability</div>
                </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
                <div class="guide-section">
                    <div class="guide-title">Store Room</div>
                    <div class="guide-desc">Additional storage space availability</div>
                </div>
            """, unsafe_allow_html=True)


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
        bedrooms = float(st.selectbox('Number of Bedrooms', sorted(df['bedRoom'].unique().tolist())))
        bathroom = float(st.selectbox('Number of Bathrooms', sorted(df['bathroom'].unique().tolist())))
        balcony = st.selectbox('Number of Balconies', sorted(df['balcony'].unique().tolist()))
        property_age = st.selectbox('Property Age', sorted(df['agePossession'].unique().tolist()))

    with col2:
        st.markdown("""
            <h4 style='color: #64B5F6; font-size: 1.2rem; font-weight: 600; margin-bottom: 1rem;'>
                Area & Features
            </h4>
        """, unsafe_allow_html=True)
        built_up_area = float(st.number_input('Built-up Area (in sqft)', min_value=0.0, step=50.0))
        servant_room = float(st.selectbox('Servant Room', [0.0, 1.0]))
        store_room = float(st.selectbox('Store Room', [0.0, 1.0]))
        furnishing_type = st.selectbox('Furnishing Type', sorted(df['furnishing_type'].unique().tolist()))
        luxury_category = st.selectbox('Luxury Category', sorted(df['luxury_category'].unique().tolist()))
        floor_category = st.selectbox('Floor Category', sorted(df['floor_category'].unique().tolist()))

    st.write("")
    st.write("")

    # Predict Button with custom styling
    col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
    with col_btn2:
        predict_button = st.button('Predict Price', use_container_width=True, type="primary")

    if predict_button:
        # Validate input
        if built_up_area == 0:
            st.error("⚠️ Please enter a valid Built-up Area")
        else:
            # Prepare request payload
            payload = {
                "property_type": property_type,
                "sector": sector,
                "bedRoom": bedrooms,
                "bathroom": bathroom,
                "balcony": balcony,
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
                st.error("⚠️ Cannot connect to prediction service. Please ensure the API server is running.")
                st.info(f"Trying to connect to: {API_URL}")
                return
            except requests.exceptions.RequestException as e:
                st.error(f"⚠️ Error connecting to prediction service: {str(e)}")
                return

            # Display Results with styling
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("""
                <div style='background: linear-gradient(135deg, #0f2027 0%, #203a43 50%, #2c5364 100%); 
                            padding: 1rem; border-radius: 12px; margin: 1rem 0;
                            border: 2px solid #64B5F6;'>
                    <h3 style='color: #64B5F6; text-align: center; margin-bottom: 0.5rem; font-size: 2.5rem;'>
                        Predicted Price Range
                    </h3>
            """, unsafe_allow_html=True)
            
            # Display metrics in columns
            metric_col1, metric_col2, metric_col3 = st.columns(3)
            
            with metric_col1:
                st.metric(label="🔻 Lower Range", value=f"₹ {round(low, 2)} Cr")
            
            with metric_col2:
                st.metric(label="🎯 Base Price", value=f"₹ {round(base_price, 2)} Cr", delta="Estimated")
            
            with metric_col3:
                st.metric(label="🔺 Upper Range", value=f"₹ {round(high, 2)} Cr")
            
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Additional Info
            st.info("""
                💡 **Note:** The predicted price range is based on current market trends and property features. 
                Actual prices may vary based on specific location advantages, market conditions, and negotiation.
            """)
            
            # Modern Property Summary
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("""
                <h3 style='color: #64B5F6; font-size: 1.5rem; margin: 1.5rem 0 1rem 0;'>
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
                        <h4 style='color: #64B5F6; margin-bottom: 0.5rem; font-size: 1.2rem;'>
                            Property Details
                        </h4>
                        <div style='color: #cccccc; line-height: 2;'>
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
                        <h4 style='color: #5fcf7c; margin-bottom: 0.5rem; font-size: 1.2rem;'>
                            Features & Amenities
                        </h4>
                        <div style='color: #cccccc; line-height: 2;'>
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
            st.markdown(f"""
                <div style='background: linear-gradient(135deg, #1a1a2e 0%, #2a2a4e 100%); 
                            padding: 1.0rem; border-radius: 12px; margin-top: 0.75rem;
                            border-left: 4px solid #64B5F6;'>
                    <h4 style='color: #64B5F6; margin-bottom: 0.5rem; font-size: 1.2rem;'>
                        Additional Spaces
                    </h4>
                    <div style='display: grid; grid-template-columns: repeat(2, 1fr); gap: 1rem; color: #cccccc;'>
                        <div style='background: rgba(100, 181, 246, 0.1); padding: 1rem; border-radius: 8px; text-align: center;'>
                            <div style='font-size: 1.5rem; margin-bottom: 0.5rem;'>
                                {'✅' if servant_room == 1.0 else '❌'}
                            </div>
                            <div style='font-size: 0.9rem;'>Servant Room</div>
                        </div>
                        <div style='background: rgba(95, 207, 124, 0.1); padding: 1rem; border-radius: 8px; text-align: center;'>
                            <div style='font-size: 1.5rem; margin-bottom: 0.5rem;'>
                                {'✅' if store_room == 1.0 else '❌'}
                            </div>
                            <div style='font-size: 0.9rem;'>Store Room</div>
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)

    st.write("")
    st.write("") 
    
    # Footer information
    st.markdown("""
        <div style='background: #1a1a2e; padding: 1.5rem; border-radius: 12px; 
                    border-left: 5px solid #5fcf7c; margin: 1rem 0;'>
            <h4 style='color: #5fcf7c; margin-bottom: 1rem;'>How Our Model Works</h4>
            <p style='color: #cccccc; line-height: 1.8; margin: 0;'>
                Our ML model is trained on thousands of real estate transactions in Gurgaon. 
                It considers factors like location, property size, amenities, age, and market trends 
                to provide accurate price predictions with a confidence interval.
            </p>
        </div>
    """, unsafe_allow_html=True)


# Call the main function
if __name__ == "__main__":
    show_price_predictor()