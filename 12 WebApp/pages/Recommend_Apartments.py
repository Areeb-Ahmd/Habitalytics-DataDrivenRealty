import streamlit as st
import pickle
import pandas as pd
import requests
from bs4 import BeautifulSoup

def recommendation_model():
    # Hero Section
    st.markdown("""
    <div style='text-align: center; padding: 0 0 1rem 0;'>
        <h1 style='font-size: 3.5rem; font-weight: 900; margin-bottom: 0; 
                   line-height: 1; letter-spacing: 6px;'>
            <span style='color: #ffffff; text-shadow: 2px 2px 4px rgba(0,0,0,0.5);'>APARTMENT </span><span style='color: #5fcf7c; text-shadow: 2px 2px 4px rgba(95, 207, 124, 0.5);'>RECOMMENDER</span>
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

    # Optimized scraping with mobile headers (Strategy 3 that worked)
    def fetch_property_page(url):
        session = requests.Session()
        
        # Use the mobile headers that worked successfully
        mobile_headers = {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_7_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Mobile/15E148 Safari/604.1',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }
        
        try:
            response = session.get(url, headers=mobile_headers, timeout=60, allow_redirects=True)
            response.raise_for_status()
            return response, session
            
        except Exception as e:
            session.close()
            raise Exception(f"Failed to fetch page: {e}")

    def image_scrap(row):
        url = row["Link"]
        
        try:
            # Use the working mobile headers strategy
            response, session = fetch_property_page(url)
            
            # Parse the HTML content of the fetched URL
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Use the working selector that found the image successfully
            img_element = soup.select_one('img[src*="99acres"]')
            
            if img_element and img_element.get('src'):
                img_src = img_element.get('src')
                # Handle relative URLs
                if img_src.startswith('//'):
                    img_src = 'https:' + img_src
                elif img_src.startswith('/'):
                    img_src = 'https://www.99acres.com' + img_src
                
                # Optimize image quality by trying to get higher resolution version
                original_img_src = img_src
                # Replace common low-res suffixes with higher quality ones
                if '_med.jpg' in img_src:
                    img_src = img_src.replace('_med.jpg', '_large.jpg')
                elif '_small.jpg' in img_src:
                    img_src = img_src.replace('_small.jpg', '_large.jpg')
                elif '_thumb.jpg' in img_src:
                    img_src = img_src.replace('_thumb.jpg', '_large.jpg')
                elif '.jpg' in img_src and '_large' not in img_src and '_med' not in img_src:
                    # Try to get a larger version by adding _large suffix
                    img_src = img_src.replace('.jpg', '_large.jpg')
                
                # Try to get location text
                location_element = soup.select_one('h1 span')
                if location_element:
                    location_text = location_element.text.strip()
                    _ = st.markdown(f"📍 **Location:** {location_text}")
                
                st.image(img_src, caption=f'{row["PropertyName"]}', width=400)
            else:
                # Debug: Check if the fallback image file exists
                import os
                fallback_path = 'datasets/No_images.jpg'
                if os.path.exists(fallback_path):
                    st.image(fallback_path, caption="No image available", width=400)
                else:
                    st.error(f"Fallback image not found at: {fallback_path}")
                    st.image('datasets/No_images.jpg', caption="No image available", width=400)
                
        except Exception as e:
            # Debug: Check if the fallback image file exists
            import os
            fallback_path = 'datasets/No_images.jpg'
            if os.path.exists(fallback_path):
                st.image(fallback_path, caption="Image not available", width=400)
            else:
                st.error(f"Fallback image not found at: {fallback_path}")
                st.image('datasets/No_images.jpg', caption="Image not available", width=400)
        finally:
            try:
                session.close()
            except:
                pass

    # Recommend properties based on location
    st.markdown("""
        <h2 style='font-size: 1.8rem; font-weight: 600; margin: 1.5rem 0 1rem 0; color: #64B5F6;'>
            Select Location and Radius
        </h2>
    """, unsafe_allow_html=True)
    
    selected_location = st.selectbox('Location', sorted(location_df.columns.to_list()), index=21)
    radius = st.number_input('Radius in Kms', min_value=0, max_value=330, value=0, step=2)

    # Cache the apartments_list
    apartments_list = get_apartments_list(location_df, selected_location, radius)

    if st.button('Search'):
        if apartments_list:
            for key in apartments_list:
                st.write(f'{key} :  {round(location_df.at[key, selected_location] / 1000, 1)} Kms')
        else:
            st.warning("No properties found in the selected area. Try increasing the radius or selecting a different location.")


    # Recommendation section
    st.markdown("""
        <h2 style='font-size: 1.8rem; font-weight: 600; margin: 1.5rem 0 1rem 0; color: #64B5F6;'>
            Recommend Apartments
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
                    st.warning(f'No Recommendations found!')
                else:
                    # Display success message and recommended apartments
                    st.success("### Recommended Apartments:")
                    # Iterate through each recommended property and display its details
                    for index, row in recommendation_df.iterrows():
                        # Display property name as clickable but styled like regular text
                        _ = st.markdown("---")
                        _ = st.markdown(f'<a href="{row["Link"]}" style="text-decoration: none; color: inherit; font-weight: bold; font-size: 18px;">{row["PropertyName"]}</a>', unsafe_allow_html=True)
                        image_scrap(row)
            else:
                st.warning("Please select an apartment first.")
    else:
        st.warning("No apartments available in the selected area. Please adjust your location and radius settings above.")

    
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


# Call the main function
if __name__ == "__main__":
    recommendation_model()