import streamlit as st
import pickle
import pandas as pd
import os

def property_recommender_model():
    # Hero Section
    st.markdown("""
    <div style='text-align: center; padding: 0 0 1rem 0;'>
        <h1 style='font-size: 3.5rem; font-weight: 900; margin-bottom: 0; 
                   line-height: 1; letter-spacing: 6px;'>
            <span style='color: #ffffff; text-shadow: 2px 2px 4px rgba(0,0,0,0.5);'>PROPERTY </span><span style='color: #5fcf7c; text-shadow: 2px 2px 4px rgba(95, 207, 124, 0.5);'>RECOMMENDER</span>
        </h1>
        <div style='width: 300px; height: 4px; background: linear-gradient(90deg, #ffffff 0%, #5fcf7c 100%);
                    margin: 1rem auto; border-radius: 2px;'></div>
        <p style='font-size: 1.2rem; color: #5fcf7c; font-weight: 600; 
                  margin-top: 0.5rem; line-height: 1; letter-spacing: 4px;'>
            Smart Property Recommendations
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
        <div style='background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%); 
                    padding: 1.5rem; border-radius: 10px; margin: 1rem 0;
                    border-left: 5px solid #64B5F6;'>
            <p style='font-size: 1rem; line-height: 1.6; color: #ffffff; margin: 0;'>
                Find apartments near your preferred location and discover similar properties 
                based on <strong>amenities, features, and location advantages</strong>. 
                Our <strong>intelligent recommendation system</strong> helps you explore the best options.
            </p>
        </div>
    """, unsafe_allow_html=True)

    # Load Dataset and Model
    location_df = pickle.load(open('datasets/location_distance.pkl', 'rb'))
    cosine_sim1 = pickle.load(open('datasets/cosine_sim1.pkl', 'rb'))
    cosine_sim2 = pickle.load(open('datasets/cosine_sim2.pkl', 'rb'))
    cosine_sim3 = pickle.load(open('datasets/cosine_sim3.pkl', 'rb'))
    link_loc = pickle.load(open('datasets/link_loc.pkl', 'rb'))
    
    # NEW: Load the pre-scraped images
    try:
        images_df = pd.read_csv('datasets/property_images.csv')
    except FileNotFoundError:
        st.error("Image database not found. Please ensure property_images.csv is in datasets folder.")
        images_df = pd.DataFrame(columns=['PropertyName', 'ImageURL'])

    # Constants for weighting in the similarity matrix
    weight_1 = 0.5
    weight_2 = 0.8
    weight_3 = 1

    # Recommendation System Logic (Based on location)
    def recommend_properties_with_scores(property_name, top_n=247):
        # Combine similarity matrices with weights
        cosine_sim_matrix = weight_1 * cosine_sim1 + weight_2 * cosine_sim2 + weight_3 * cosine_sim3
        
        # Get the similarity scores for the property using its name as the index
        sim_scores = list(enumerate(cosine_sim_matrix[location_df.index.get_loc(property_name)]))
        
        # Sort properties based on the similarity scores
        sorted_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        
        # Get the indices and scores of the top_n most similar properties
        top_indices = [i[0] for i in sorted_scores[1:top_n+1]]
        top_scores = [i[1] for i in sorted_scores[1:top_n+1]]
        
        # Retrieve the names of the top properties using the indices
        top_properties = location_df.index[top_indices].tolist()
        
        # Create a dataframe with the results
        recommendations_df = pd.DataFrame({
            'PropertyName': top_properties,
            'SimilarityScore': top_scores
        })
        
        return recommendations_df

    @st.cache_data
    def get_apartments_list(location_df, selected_location, radius):
        result_ser = location_df[location_df[selected_location] < radius * 1000][selected_location].sort_values()

        if len(result_ser) == 0:
            return []

        return result_ser.index.to_list()

    @st.cache_data
    def get_recommendation_df(selected_apartment):
        return recommend_properties_with_scores(selected_apartment, 5)

    # NEW: Image display function using CSV lookup
    def image_lookup(row):
        prop_name = row["PropertyName"]
        
        # Find the image URL in our pre-loaded CSV
        img_row = images_df[images_df['PropertyName'] == prop_name]
        
        img_src = None
        if not img_row.empty and pd.notna(img_row.iloc[0]['ImageURL']):
            img_src = img_row.iloc[0]['ImageURL']
            
        if img_src:
            st.image(img_src, caption=f'{prop_name}', width=400)
        else:
            # Fallback logic
            fallback_path = 'datasets/No_images.jpg'
            if os.path.exists(fallback_path):
                st.image(fallback_path, caption="No image available", width=400)
            else:
                st.write("Image not available")

    # Recommend properties based on location
    st.markdown("""
        <h2 style='font-size: 1.8rem; font-weight: 600; margin: 1.5rem 0 1rem 0; color: #64B5F6;'>
            Select Location and Radius
        </h2>
    """, unsafe_allow_html=True)
    
    # Add custom CSS for Search and Recommend buttons and card styling
    st.markdown("""
        <style>
        /* Style Search and Recommend buttons */
        div[data-testid="column"] button,
        .stButton > button {
            background-color: #1a3a2a !important;
            border: 2px solid #5fcf7c !important;
            color: #5fcf7c !important;
            font-weight: 600 !important;
            padding: 0.5rem 2rem !important;
            border-radius: 8px !important;
            transition: all 0.3s ease !important;
        }
        
        .stButton > button:hover {
            background-color: #2d5a3d !important;
            border-color: #5fcf7c !important;
            color: #5fcf7c !important;
            box-shadow: 0 0 10px rgba(95, 207, 124, 0.3) !important;
            transform: translateY(-2px) !important;
        }
        
        .stButton > button:active {
            transform: translateY(0) !important;
        }
        
        /* Ensure all text in recommendations is visible */
        .stMarkdown p,
        .stMarkdown div,
        .stMarkdown span {
            color: #ffffff !important;
        }
        
        /* Card link hover effect */
        a[href*="99acres"] {
            transition: all 0.3s ease !important;
        }
        
        /* 99acres button hover - blue */
        a[href*="99acres"]:hover {
            background: linear-gradient(135deg, #0066CC 0%, #0052A3 100%) !important;
            box-shadow: 0 4px 12px rgba(0, 120, 215, 0.4) !important;
            transform: translateY(-2px) !important;
        }
        
        /* Generic listing button hover */
        a.listing-button:hover {
            box-shadow: 0 4px 12px rgba(95, 207, 124, 0.4) !important;
            transform: translateY(-2px) !important;
        }
        </style>
    """, unsafe_allow_html=True)
    
    selected_location = st.selectbox('Location', sorted(location_df.columns.to_list()), index=21)
    radius = st.number_input('Radius in Kms', min_value=0, max_value=330, value=0, step=2)

    # Cache the apartments_list
    apartments_list = get_apartments_list(location_df, selected_location, radius)

    if st.button('Search'):
        if apartments_list:
            # Display results in modern card grid
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Create columns for grid layout (2 columns)
            num_results = len(apartments_list)
            cols_per_row = 2
            
            for i in range(0, num_results, cols_per_row):
                cols = st.columns(cols_per_row, gap="medium")
                
                for j, col in enumerate(cols):
                    if i + j < num_results:
                        key = apartments_list[i + j]
                        distance = round(location_df.at[key, selected_location] / 1000, 1)
                        
                        with col:
                            st.markdown(f"""
                                <div style='background: linear-gradient(135deg, #1a1a2e 0%, #2a2a4e 100%); 
                                            padding: 1.2rem; border-radius: 12px; 
                                            border-left: 3px solid #64B5F6;
                                            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
                                            margin-bottom: 1rem;
                                            transition: transform 0.2s ease;
                                            cursor: pointer;'>
                                    <div style='display: flex; justify-content: space-between; align-items: start; margin-bottom: 0.5rem;'>
                                        <h4 style='color: #ffffff; margin: 0; font-size: 1.1rem; font-weight: 600; line-height: 1.3;'>
                                            {key}
                                        </h4>
                                    </div>
                                    <div style='display: flex; align-items: center; margin-top: 0.8rem;'>
                                        <span style='color: #64B5F6; font-size: 0.9rem; font-weight: 500;'>
                                            📍 {distance} Kms away
                                        </span>
                                    </div>
                                </div>
                            """, unsafe_allow_html=True)
        else:
            st.markdown("""
                <div style='background: linear-gradient(135deg, #3a1a1a 0%, #4a2a2a 100%); 
                            padding: 1.2rem; border-radius: 12px; margin: 1rem 0;
                            border-left: 4px solid #ff6b6b;
                            box-shadow: 0 2px 8px rgba(255, 107, 107, 0.2);'>
                    <p style='color: #ffcccc; margin: 0; font-size: 1rem; line-height: 1.6;'>
                        ⚠️ No properties found in the selected area. Try increasing the radius or selecting a different location.
                    </p>
                </div>
            """, unsafe_allow_html=True)


    # Recommendation section
    st.markdown("""
        <h2 style='font-size: 1.8rem; font-weight: 600; margin: 1.5rem 0 1rem 0; color: #64B5F6;'>
            Recommend Properties
        </h2>
    """, unsafe_allow_html=True)
    
    if apartments_list:
        selected_apartment = st.selectbox('Select an Apartment', apartments_list, index=None)
        
        # Button to trigger the recommendation process
        if st.button('Recommend'):
            if selected_apartment:
                # Get and display property recommendations based on similarity scores
                recommendation_df = get_recommendation_df(selected_apartment)
                # Adding property links to the recommendation DataFrame
                recommendation_df['Link'] = [link_loc[key].values[0] if key in link_loc and len(link_loc[key].values) > 0 else '#' for key in recommendation_df['PropertyName']]
                # Check if there are any recommendations
                if recommendation_df.empty:
                    st.markdown("""
                        <div style='background: linear-gradient(135deg, #3a1a1a 0%, #4a2a2a 100%); 
                                    padding: 1.2rem; border-radius: 12px; margin: 1rem 0;
                                    border-left: 4px solid #ff6b6b;
                                    box-shadow: 0 2px 8px rgba(255, 107, 107, 0.2);'>
                            <p style='color: #ffcccc; margin: 0; font-size: 1rem; line-height: 1.6;'>
                                ⚠️ No Recommendations found!
                            </p>
                        </div>
                    """, unsafe_allow_html=True)
                else:
                    # Display recommendations in modern card style
                    for idx, (index, row) in enumerate(recommendation_df.iterrows(), 1):
                        # Get image URL
                        prop_name = row["PropertyName"]
                        img_row = images_df[images_df['PropertyName'] == prop_name]
                        img_src = None
                        if not img_row.empty and pd.notna(img_row.iloc[0]['ImageURL']):
                            img_src = img_row.iloc[0]['ImageURL']
                        
                        # Get location/sector for the property
                        # Find the sector with minimum distance for this property
                        property_location = "Gurgaon"
                        if prop_name in location_df.index:
                            prop_distances = location_df.loc[prop_name]
                            # Find the sector with minimum distance (closest sector)
                            min_distance_sector = prop_distances.idxmin()
                            if pd.notna(prop_distances[min_distance_sector]) and prop_distances[min_distance_sector] < 5000:  # Within 5km
                                property_location = min_distance_sector.replace('_', ' ').title()
                        
                        # Determine listing site from link and set colors
                        listing_site = "Listing"
                        link = row["Link"]
                        button_bg = "linear-gradient(135deg, #1a3a2a 0%, #2d5a3d 100%)"
                        button_color = "#5fcf7c"
                        button_border = "#5fcf7c"
                        button_hover_bg = "linear-gradient(135deg, #2d5a3d 0%, #3d6a4d 100%)"
                        
                        if "99acres" in link.lower():
                            listing_site = "99acres Listing"
                            # 99acres brand blue colors
                            button_bg = "linear-gradient(135deg, #0078D7 0%, #0066CC 100%)"
                            button_color = "#ffffff"
                            button_border = "#0078D7"
                            button_hover_bg = "linear-gradient(135deg, #0066CC 0%, #0052A3 100%)"
                        
                        # Create card layout with columns
                        col_img, col_info = st.columns([1, 2], gap="medium")
                        
                        with col_img:
                            # Display image in card
                            if img_src:
                                st.markdown(f"""
                                    <div style='border-radius: 12px; overflow: hidden; 
                                                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);'>
                                """, unsafe_allow_html=True)
                                st.image(img_src, use_container_width=True)
                                st.markdown("</div>", unsafe_allow_html=True)
                            else:
                                fallback_path = 'datasets/No_images.jpg'
                                if os.path.exists(fallback_path):
                                    st.markdown(f"""
                                        <div style='border-radius: 12px; overflow: hidden; 
                                                    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);'>
                                    """, unsafe_allow_html=True)
                                    st.image(fallback_path, use_container_width=True)
                                    st.markdown("</div>", unsafe_allow_html=True)
                        
                        with col_info:
                            # Property card with modern styling
                            similarity_score = row['SimilarityScore']
                            similarity_percent = round(similarity_score * 100, 1)
                            
                            st.markdown(f"""
                                <div style='background: linear-gradient(135deg, #1a1a2e 0%, #2a2a4e 100%); 
                                            padding: 1.5rem; border-radius: 12px; 
                                            border-left: 4px solid #5fcf7c;
                                            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.4);
                                            margin-bottom: 1.5rem;
                                            transition: transform 0.3s ease;'>
                                    <div style='display: flex; justify-content: space-between; align-items: start; margin-bottom: 0.8rem;'>
                                        <div>
                                            <h3 style='color: #ffffff; margin: 0 0 0.5rem 0; font-size: 1.4rem; font-weight: 600;'>
                                                {idx}. {row["PropertyName"]}
                                            </h3>
                                            <p style='color: #64B5F6; margin: 0; font-size: 1rem; font-weight: 500;'>
                                                📍 {property_location}
                                            </p>
                                        </div>
                                        <span style='background: rgba(95, 207, 124, 0.2); 
                                                     color: #5fcf7c; 
                                                     padding: 0.3rem 0.8rem; 
                                                     border-radius: 20px; 
                                                     font-size: 0.85rem; 
                                                     font-weight: 600;'>
                                            {similarity_percent}% Match
                                        </span>
                                    </div>
                                    <div style='margin-top: 1rem;'>
                                        <a href="{row["Link"]}" 
                                           target="_blank"
                                           class="listing-button-{idx}"
                                           style='display: inline-block;
                                                  background: {button_bg};
                                                  color: {button_color};
                                                  padding: 0.6rem 1.5rem;
                                                  border-radius: 8px;
                                                  text-decoration: none;
                                                  font-weight: 600;
                                                  border: 2px solid {button_border};
                                                  transition: all 0.3s ease;'>
                                            View {listing_site} →
                                        </a>
                                    </div>
                                </div>
                            """, unsafe_allow_html=True)
                        
                        # Add spacing between cards
                        st.markdown("<br>", unsafe_allow_html=True)
            else:
                st.markdown("""
                    <div style='background: linear-gradient(135deg, #3a1a1a 0%, #4a2a2a 100%); 
                                padding: 1.2rem; border-radius: 12px; margin: 1rem 0;
                                border-left: 4px solid #ff6b6b;
                                box-shadow: 0 2px 8px rgba(255, 107, 107, 0.2);'>
                        <p style='color: #ffcccc; margin: 0; font-size: 1rem; line-height: 1.6;'>
                            ⚠️ Please select an apartment first.
                        </p>
                    </div>
                """, unsafe_allow_html=True)
    else:
        st.markdown("""
            <div style='background: linear-gradient(135deg, #3a1a1a 0%, #4a2a2a 100%); 
                        padding: 1.2rem; border-radius: 12px; margin: 1rem 0;
                        border-left: 4px solid #ff6b6b;
                        box-shadow: 0 2px 8px rgba(255, 107, 107, 0.2);'>
                <p style='color: #ffcccc; margin: 0; font-size: 1rem; line-height: 1.6;'>
                    ⚠️ No property available in the selected area. Please adjust your location and radius settings above.
                </p>
            </div>
        """, unsafe_allow_html=True)

    
    # Footer information
    st.markdown("""
        <div style='background: #1a1a2e; padding: 1.5rem; border-radius: 12px; 
                    border-left: 5px solid #5fcf7c; margin: 1rem 0;'>
            <h4 style='color: #5fcf7c; margin-bottom: 1rem;'>How Recommendations Work</h4>
            <p style='color: #cccccc; line-height: 1.8; margin: 0;'>
                Our recommendation engine uses <strong>cosine similarity</strong> to compare apartments based on 
                location advantages, property features, amenities, size, and market positioning. 
                The system analyzes multiple factors to suggest properties similar to your selection.
            </p>
        </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    property_recommender_model()