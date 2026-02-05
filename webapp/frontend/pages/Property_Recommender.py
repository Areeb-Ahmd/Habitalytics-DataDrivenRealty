import streamlit as st
import pickle
import pandas as pd
from dataclasses import dataclass
from pathlib import Path
from typing import Any


DATA_DIR = Path(__file__).resolve().parents[1] / "datasets"
IMAGES_CSV_PATH = DATA_DIR / "property_images.csv"
FALLBACK_IMAGE_PATH = DATA_DIR / "No_images.jpg"

# Page constants
DEFAULT_LOCATION_INDEX = 21
MAX_RADIUS_KM = 330
NEARBY_COLUMNS_PER_ROW = 2
TOP_N_RECOMMENDATIONS = 5
SECTOR_MATCH_THRESHOLD_METERS = 5000

# Similarity weights (used to combine precomputed similarity matrices)
WEIGHT_1 = 0.5
WEIGHT_2 = 0.8
WEIGHT_3 = 1.0


@dataclass(frozen=True)
class RecommenderResources:
    location_df: pd.DataFrame
    cosine_sim_matrix: Any
    link_loc: Any
    images_df: pd.DataFrame
    images_csv_found: bool


@st.cache_resource(show_spinner=False)
def load_recommender_resources() -> RecommenderResources:
    """Load all datasets/models once per session (cached)."""
    location_df = pickle.load((DATA_DIR / "location_distance.pkl").open("rb"))
    cosine_sim1 = pickle.load((DATA_DIR / "cosine_sim1.pkl").open("rb"))
    cosine_sim2 = pickle.load((DATA_DIR / "cosine_sim2.pkl").open("rb"))
    cosine_sim3 = pickle.load((DATA_DIR / "cosine_sim3.pkl").open("rb"))
    link_loc = pickle.load((DATA_DIR / "link_loc.pkl").open("rb"))

    cosine_sim_matrix = WEIGHT_1 * cosine_sim1 + WEIGHT_2 * cosine_sim2 + WEIGHT_3 * cosine_sim3

    images_csv_found = IMAGES_CSV_PATH.exists()
    if images_csv_found:
        images_df = pd.read_csv(IMAGES_CSV_PATH)
    else:
        images_df = pd.DataFrame(columns=["PropertyName", "ImageURL"])

    return RecommenderResources(
        location_df=location_df,
        cosine_sim_matrix=cosine_sim_matrix,
        link_loc=link_loc,
        images_df=images_df,
        images_csv_found=images_csv_found,
    )

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
            Location and Similarity Based Recommendations
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
        <div style='background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%); 
                    padding: 1.5rem; border-radius: 10px; margin: 1rem 0;
                    border-left: 5px solid #64B5F6;'>
            <p style='font-size: 1.25rem; line-height: 1.6; color: #ffffff; margin: 0;'>
                The Property Recommender helps you explore properties in Gurugram in two simple ways. 
                You can discover properties located near a selected area within a chosen radius, 
                or find properties that are similar to a selected property based on shared characteristics.
            </p>
            <p style='font-size: 1.25rem; line-height: 1.6; color: #ffffff; margin-top: 1rem;'>
                Recommendations are generated using historical property data and feature similarity. 
                They are intended to support exploration and comparison, and do not represent 
                live listings or guaranteed availability.
            </p>
        </div>
    """, unsafe_allow_html=True)

    # Load all datasets/models (cached)
    resources = load_recommender_resources()
    location_df = resources.location_df
    cosine_sim_matrix = resources.cosine_sim_matrix
    link_loc = resources.link_loc
    images_df = resources.images_df

    # Build quick-lookup maps (avoids filtering dataframe per row)
    if not images_df.empty:
        images_map = (
            images_df.dropna(subset=["ImageURL"])
            .drop_duplicates(subset=["PropertyName"], keep="first")
            .set_index("PropertyName")["ImageURL"]
            .to_dict()
        )
    else:
        images_map = {}

    fallback_path = str(FALLBACK_IMAGE_PATH)
    has_fallback = FALLBACK_IMAGE_PATH.exists()

    if not resources.images_csv_found:
        st.warning(
            "Image database not found. Please ensure `property_images.csv` exists in `webapp/frontend/datasets/`."
        )

    def render_error(message: str) -> None:
        st.markdown(
            f"""
            <div style='background: linear-gradient(135deg, #3a1a1a 0%, #4a2a2a 100%);
                        padding: 1.2rem; border-radius: 12px; margin: 1rem 0;
                        border-left: 4px solid #ff6b6b;
                        box-shadow: 0 2px 8px rgba(255, 107, 107, 0.2);'>
                <p style='color: #ffcccc; margin: 0; font-size: 1rem; line-height: 1.6;'>
                    ⚠️ {message}
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    def get_listing_link(property_name: str) -> str:
        ser = link_loc.get(property_name)
        if ser is None or len(getattr(ser, "values", [])) == 0:
            return "#"
        return ser.values[0]

    def get_property_location(property_name: str) -> str:
        if property_name not in location_df.index:
            return "Gurgaon"
        distances = location_df.loc[property_name]
        sector = distances.idxmin()
        if pd.notna(distances[sector]) and distances[sector] < SECTOR_MATCH_THRESHOLD_METERS:
            return sector.replace("_", " ").title()
        return "Gurgaon"

    # Recommendation System Logic (Based on location)
    def recommend_properties_with_scores(property_name: str, top_n: int = TOP_N_RECOMMENDATIONS) -> pd.DataFrame:
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
        recommendations_df = pd.DataFrame({"PropertyName": top_properties, "SimilarityScore": top_scores})
        
        return recommendations_df

    @st.cache_data
    def get_apartments_list(location_df: pd.DataFrame, selected_location: str, radius_km: float) -> list[str]:
        result_ser = location_df.loc[location_df[selected_location] < radius_km * 1000, selected_location].sort_values()
        return result_ser.index.tolist()

    # Recommend properties based on location
    st.markdown("""
        <h2 style='font-size: 1.8rem; font-weight: 600; margin: 1rem 0 1rem 0; color: #64B5F6;'>
            Nearby Search
        </h2>
    """, unsafe_allow_html=True)
    
    # Add custom CSS for Search and Recommend buttons and card styling
    st.markdown("""
        <style>
        /* Cards: consistent hover behavior */
        .nearby-card,
        .recommendation-card {
            transition: transform 0.2s ease, box-shadow 0.2s ease !important;
        }

        .nearby-card:hover,
        .recommendation-card:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 6px 16px rgba(0, 0, 0, 0.45) !important;
        }

        /* Listing buttons */
        a.listing-button {
            display: inline-block !important;
            background: #2d5a3d !important;
            color: #ffffff !important;
            padding: 0.6rem 1.5rem !important;
            border-radius: 8px !important;
            text-decoration: none !important;
            font-weight: 600 !important;
            border: 2px solid #5fcf7c !important;
            transition: background 0.2s ease, transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease !important;
        }

        a.listing-button:hover {
            background: #3d6a4d !important;
            box-shadow: 0 4px 12px rgba(95, 207, 124, 0.4) !important;
            transform: translateY(-2px) !important;
        }

        /* 99acres variant */
        a.listing-button--99acres {
            background: #0066CC !important;
            border-color: #0066CC !important;
            color: #ffffff !important;
        }

        a.listing-button--99acres:hover {
            background: #0052A3 !important;
            border-color: #0052A3 !important;
            box-shadow: 0 4px 12px rgba(0, 102, 204, 0.45) !important;
        }
        </style>
    """, unsafe_allow_html=True)
    
    locations = sorted(location_df.columns.to_list())
    selected_location = st.selectbox("Location", locations, index=DEFAULT_LOCATION_INDEX)
    radius = st.number_input("Radius in Kms", min_value=0, max_value=MAX_RADIUS_KM, value=0, step=2)

    # Cache the apartments_list
    apartments_list = get_apartments_list(location_df, selected_location, radius)

    if st.button('Search', type="primary"):
        if apartments_list:
            # Display results in modern card grid
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Create columns for grid layout (2 columns)
            num_results = len(apartments_list)
            cols_per_row = NEARBY_COLUMNS_PER_ROW
            
            for i in range(0, num_results, cols_per_row):
                cols = st.columns(cols_per_row, gap="medium")
                
                for j, col in enumerate(cols):
                    if i + j < num_results:
                        key = apartments_list[i + j]
                        distance = round(location_df.at[key, selected_location] / 1000, 1)
                        
                        with col:
                            st.markdown(f"""
                                <div class="nearby-card" style='background: linear-gradient(135deg, #1a1a2e 0%, #2a2a4e 100%); 
                                            padding: 1.2rem; border-radius: 12px; 
                                            border-left: 3px solid #64B5F6;
                                            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
                                            margin-bottom: 1rem;
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
            render_error("No properties found in the selected area. Try increasing the radius or selecting a different location.")


    # Similarity-based Recommendation section
    st.markdown("""
        <h2 style='font-size: 1.8rem; font-weight: 600; margin: 1.5rem 0 1rem 0; color: #64B5F6;'>
            Similarity-based Recommendation
        </h2>
    """, unsafe_allow_html=True)
    
    if apartments_list:
        selected_apartment = st.selectbox('Select an Apartment', apartments_list, index=None)
        
        # Button to trigger the recommendation process
        if st.button('Recommend', type="primary"):
            if selected_apartment:
                # Get and display property recommendations based on similarity scores
                recommendation_df = recommend_properties_with_scores(selected_apartment, TOP_N_RECOMMENDATIONS)
                # Check if there are any recommendations
                if recommendation_df.empty:
                    render_error("No recommendations found.")
                else:
                    # Display recommendations in modern card style
                    for idx, row in enumerate(recommendation_df.itertuples(index=False), 1):
                        # Get image URL
                        prop_name = row.PropertyName
                        img_src = images_map.get(prop_name)
                        
                        # Get location/sector for the property
                        property_location = get_property_location(prop_name)
                        
                        # Determine listing site from link and set colors
                        listing_site = "Listing"
                        link = get_listing_link(prop_name)
                        button_class = "listing-button"
                        
                        if "99acres" in link.lower():
                            listing_site = "99acres Listing"
                            button_class = "listing-button listing-button--99acres"
                        
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
                                if has_fallback:
                                    st.markdown(f"""
                                        <div style='border-radius: 12px; overflow: hidden; 
                                                    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);'>
                                    """, unsafe_allow_html=True)
                                    st.image(fallback_path, use_container_width=True)
                                    st.markdown("</div>", unsafe_allow_html=True)
                        
                        with col_info:
                            # Property card with modern styling
                            similarity_percent = round(row.SimilarityScore * 100, 1)
                            
                            st.markdown(f"""
                                <div class="recommendation-card" style='background: linear-gradient(135deg, #1a1a2e 0%, #2a2a4e 100%); 
                                            padding: 1.5rem; border-radius: 12px; 
                                            border-left: 4px solid #5fcf7c;
                                            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.4);
                                            margin-bottom: 1.5rem;
                                            '>
                                    <div style='display: flex; justify-content: space-between; align-items: start; margin-bottom: 0.8rem;'>
                                        <div>
                                            <h3 style='color: #ffffff; margin: 0 0 0.5rem 0; font-size: 1.4rem; font-weight: 600;'>
                                                {idx}. {row.PropertyName}
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
                                        <a href="{link}" 
                                           target="_blank"
                                           class="{button_class}"
                                           >
                                            View {listing_site} →
                                        </a>
                                    </div>
                                </div>
                            """, unsafe_allow_html=True)
            else:
                render_error("Please select an apartment first.")
    else:
        render_error("No property available in the selected area. Please adjust your location and radius settings above.")

    
    # Footer information
    st.markdown("""
        <div style='background: #1a1a2e; padding: 1.5rem; border-radius: 12px; 
                    border-left: 5px solid #5fcf7c; margin: 1rem 0;'>
            <h4 style='color: #5fcf7c; margin-bottom: 1rem; font-size: 1.75rem;'>How Recommendations Work</h4>
            <p style='color: #ffffff; line-height: 1.8; margin: 0; font-size: 1.20rem;'>
                <strong style='color: #64B5F6;'>Nearby search (location and radius):</strong><br>
                When you select a reference location and a search radius, 
                the system identifies properties within that distance and ranks them by proximity.
            </p>
            <p style='color: #ffffff; line-height: 1.8; margin: 0; font-size: 1.20rem; margin-top: 1rem;'>
                <strong style='color: #64B5F6;'>Similarity-based recommendations:</strong><br>
                When you select a property, the system compares it with other properties based on 
                shared characteristics such as amenities, price and configuration patterns, 
                and proximity to key landmarks. These factors are evaluated together to 
                identify properties with similar profiles, and the most comparable options are recommended.
            </p>
            <p style='color: #ffffff; line-height: 1.8; margin: 0; font-size: 1.20rem; margin-top: 1rem;'>
                The recommendations reflect patterns present in the underlying data 
                and are intended to support exploration and comparison, 
                not to provide a definitive ranking or guarantee availability.
            </p>

        </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    property_recommender_model()