import streamlit as st
import pandas as pd
import plotly.express as px
import pickle
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import seaborn as sns
import ast
import plotly.graph_objects as go

def show_analytics_dashboard():
    # Hero Section
    st.markdown("""
    <div style='text-align: center; padding: 0 0 1rem 0;'>
        <h1 style='font-size: 3.5rem; font-weight: 900; margin-bottom: 0; 
                   line-height: 1; letter-spacing: 6px;'>
            <span style='color: #ffffff; text-shadow: 2px 2px 4px rgba(0,0,0,0.5);'>ANALYTICS </span><span style='color: #5fcf7c; text-shadow: 2px 2px 4px rgba(95, 207, 124, 0.5);'>DASHBOARD</span>
        </h1>
        <div style='width: 280px; height: 4px; background: linear-gradient(90deg, #ffffff 0%, #5fcf7c 100%);
                    margin: 1rem auto; border-radius: 2px;'></div>
        <p style='font-size: 1.2rem; color: #5fcf7c; font-weight: 600; 
                  margin-top: 0.5rem; line-height: 1; letter-spacing: 4px;'>
            Interactive Data Visualization & Insights
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
        <div style='background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%); 
                    padding: 1.5rem; border-radius: 10px; margin: 1rem 0;
                    border-left: 5px solid #64B5F6;'>
            <p style='font-size: 1rem; line-height: 1.6; color: #ffffff; margin: 0;'>
                Explore <strong>Gurgaon's real estate landscape</strong> through interactive visualizations. 
                Analyze price trends, property distributions, and market insights across different sectors 
                with our <strong>comprehensive analytics dashboard</strong>.
            </p>
        </div>
    """, unsafe_allow_html=True)

    # Loading dataset and feature text
    new_df = pd.read_csv('datasets/data_viz1.csv')
    feature_text = pickle.load(open('datasets/feature_text.pkl', 'rb'))
    wordcloud_df = pickle.load(open('datasets/wordcloud_df.pkl', 'rb'))

    # Geo Map
    st.markdown("""
        <h2 style='font-size: 1.8rem; font-weight: 600; margin: 1.5rem 0 1rem 0; color: #64B5F6;'>
            Sector-wise Average Price per Sqft Map
        </h2>
    """, unsafe_allow_html=True)
    
    st.markdown("""
        <div style='background: #1a1a2e; padding: 1rem; border-radius: 8px; margin-bottom: 1rem;'>
            <p style='color: #cccccc; margin: 0;'>
                Explore the geographical distribution of property prices across different sectors. 
                Bubble size represents the average built-up area.
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    group_df = (
        new_df.groupby('sector')
        [['price','price_per_sqft','built_up_area','latitude','longitude']]
        .mean()
    )

    fig = px.scatter_map(group_df, lat="latitude", lon="longitude", color="price_per_sqft", size='built_up_area',
                    color_continuous_scale=px.colors.cyclical.IceFire, zoom=10,
                    map_style="open-street-map",width = 1200, height = 700, hover_name=group_df.index)

    fig.update_layout(
    paper_bgcolor="#020617",
    font=dict(color="#e5e7eb"),
    margin=dict(l=0, r=0, t=0, b=0),
    coloraxis_colorbar=dict(
        title=dict(
            text="Price / sqft",
            font=dict(color="#e5e7eb")
        ),
        tickfont=dict(color="#e5e7eb")
    )
    )
    st.plotly_chart(fig, use_container_width=True)


    # Wordcloud
    st.markdown("""
        <h2 style='font-size: 1.8rem; font-weight: 600; margin: 1.5rem 0 1rem 0; color: #64B5F6;'>
            Features Word Cloud
        </h2>
    """, unsafe_allow_html=True)
    
    st.markdown("""
        <div style='background: #1a1a2e; padding: 1rem; border-radius: 8px; margin-bottom: 1rem;'>
            <p style='color: #cccccc; margin: 0;'>
                Visualize the most common amenities and features available in properties across different sectors.
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    selected_sector_cloud = st.selectbox('Select a Sector', wordcloud_df['sector'].unique().tolist())
    new_cloud = wordcloud_df[wordcloud_df['sector'] == selected_sector_cloud]

    wordcloud_text = []
    for item in new_cloud['features'].dropna().apply(ast.literal_eval):
        wordcloud_text.extend(item)

    feature_texts = ' '.join(wordcloud_text)

    if feature_texts.strip():  # Check if there's actual text to generate wordcloud
        try:
            wordcloud = WordCloud(width=1200, height=800, background_color='white', stopwords={'s'}, min_font_size=10).generate(feature_texts)
            fig, ax = plt.subplots(figsize=(8, 8), facecolor=None)
            ax.imshow(wordcloud, interpolation='bilinear')
            ax.axis('off')
            plt.tight_layout(pad=0)
            st.pyplot(fig)
            plt.close(fig)
        except Exception as e:
            st.markdown("""
                <div style='background: linear-gradient(135deg, #3a1a1a 0%, #4a2a2a 100%); 
                            padding: 1.2rem; border-radius: 12px; margin: 1rem 0;
                            border-left: 4px solid #ff6b6b;
                            box-shadow: 0 2px 8px rgba(255, 107, 107, 0.2);'>
                    <p style='color: #ffcccc; margin: 0; font-size: 1rem; line-height: 1.6;'>
                        ⚠️ Unable to generate word cloud. No features available for the selected sector.
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
                    ⚠️ No features available for the selected sector to generate word cloud.
                </p>
            </div>
        """, unsafe_allow_html=True)


    # Scatter Plot (Built-up Area vs Price)
    st.markdown("""
        <h2 style='font-size: 1.8rem; font-weight: 600; margin: 1.5rem 0 1rem 0; color: #64B5F6;'>
            Built-up Area vs Price
        </h2>
    """, unsafe_allow_html=True)
    
    st.markdown("""
        <div style='background: #1a1a2e; padding: 1rem; border-radius: 8px; margin-bottom: 1rem;'>
            <p style='color: #cccccc; margin: 0;'>
                Analyze the relationship between property size and price, categorized by number of bedrooms.
            </p>
        </div>
    """, unsafe_allow_html=True)

    property_type = st.selectbox('Select Property Type', options=new_df['property_type'].unique())
    if property_type == 'house':
        fig1 = px.scatter(new_df[new_df['property_type'] == 'house'], x='built_up_area', y='price', color='bedRoom')
    else:
        fig1 = px.scatter(new_df[new_df['property_type'] == 'flat'], x='built_up_area', y='price', color='bedRoom')
    
    fig1.update_layout(
    xaxis_title="Built-Up Area (sq ft)",
    yaxis_title="Price (in Lakhs)",

    # Backgrounds
    plot_bgcolor="#0f172a",      # chart area
    paper_bgcolor="#020617",     # outer background

    # Font colors
    font=dict(color="#e5e7eb"),

    # Axis styling
    xaxis=dict(
        gridcolor="#334155",
        zerolinecolor="#475569"
    ),
    yaxis=dict(
        gridcolor="#334155",
        zerolinecolor="#475569"
    ),

    # Legend
    legend=dict(
        bgcolor="rgba(0,0,0,0)",
        title="Bedrooms"
    )
    )
    st.plotly_chart(fig1, use_container_width=True)


    # Pie Chart (BHK Distribution for sectors)
    st.markdown("""
        <h2 style='font-size: 1.8rem; font-weight: 600; margin: 1.5rem 0 1rem 0; color: #64B5F6;'>
            BHK Pie Chart for Sectors
        </h2>
    """, unsafe_allow_html=True)
    
    st.markdown("""
        <div style='background: #1a1a2e; padding: 1rem; border-radius: 8px; margin-bottom: 1rem;'>
            <p style='color: #cccccc; margin: 0;'>
                View the distribution of different bedroom configurations (BHK) in selected sectors.
            </p>
        </div>
    """, unsafe_allow_html=True)

    sector_options = new_df['sector'].unique().tolist()
    sector_options.insert(0, 'Overall')
    selected_sector = st.selectbox('Select Sector', options=sector_options)

    if selected_sector == 'Overall':
        fig2 = px.pie(new_df, names='bedRoom')
    else:
        fig2 = px.pie(
            new_df[new_df['sector'] == selected_sector],
            names='bedRoom'
        )

    fig2.update_layout(
        paper_bgcolor="#020617",
        font=dict(color="#e5e7eb"),
        margin=dict(l=20, r=20, t=20, b=60),
        legend=dict(
            font=dict(color="#e5e7eb"),
            bgcolor="rgba(0,0,0,0)"
        )
    )

    st.plotly_chart(fig2, use_container_width=True)

    
    

    # Box Plot (Bedroom Price)
    st.markdown("""
        <h2 style='font-size: 1.8rem; font-weight: 600; margin: 1.5rem 0 1rem 0; color: #64B5F6;'>
            BHK Price Comparison
        </h2>
    """, unsafe_allow_html=True)
    
    st.markdown("""
        <div style='background: #1a1a2e; padding: 1rem; border-radius: 8px; margin-bottom: 1rem;'>
            <p style='color: #cccccc; margin: 0;'>
                Compare price ranges across different bedroom configurations using box plots to identify median prices and outliers.
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    fig3 = px.box(
    new_df[new_df['bedRoom'] <= 4],
    x='bedRoom',
    y='price',
    title='BHK Price Range'
    )

    fig3.update_layout(
    paper_bgcolor="#020617",
    plot_bgcolor="#020617",

    # Global font
    font=dict(
        color="#E5E7EB",   # light gray (Tailwind slate-200)
        size=14
    ),

    title=dict(
        text="BHK Price Range",
        font=dict(color="#F8FAFC", size=18),
        x=0.01
    ),

    margin=dict(l=50, r=30, t=50, b=50),

    xaxis=dict(
        title=dict(
            text="BHK",
            font=dict(color="#E5E7EB", size=14)
        ),
        tickfont=dict(color="#CBD5E1"),
        gridcolor="#334155",
        zerolinecolor="#475569"
    ),

    yaxis=dict(
        title=dict(
            text="Price",
            font=dict(color="#E5E7EB", size=14)
        ),
        tickfont=dict(color="#CBD5E1"),
        gridcolor="#334155",
        zerolinecolor="#475569"
    )
    )

    fig3.update_traces(
    marker=dict(
        color="#60A5FA",       # outliers
        opacity=0.9
    ),
    line=dict(color="#93C5FD"),
    fillcolor="rgba(96,165,250,0.4)",
    boxmean="sd"
    )

    st.plotly_chart(fig3, use_container_width=True)

    # Displot (Price Distribution of Property Types)
    st.markdown("""
        <h2 style='font-size: 1.8rem; font-weight: 600; margin: 1.5rem 0 1rem 0; color: #64B5F6;'>
            Side by Side Distplot for Property Type
        </h2>
    """, unsafe_allow_html=True)
    
    st.markdown("""
        <div style='background: #1a1a2e; padding: 1rem; border-radius: 8px; margin-bottom: 1rem;'>
            <p style='color: #cccccc; margin: 0;'>
                Compare the price distribution patterns between houses and flats to understand market segmentation.
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # Create histograms for House and Flat with adjusted bin size and bar thickness
    hist_house = go.Histogram(x=new_df[new_df['property_type'] == 'house']['price'], nbinsx=100, name='house', opacity=0.6, marker=dict(color='blue', line=dict(color='white', width=0.5)))
    hist_flat = go.Histogram(x=new_df[new_df['property_type'] == 'flat']['price'], nbinsx=100, name='flat', opacity=0.6, marker=dict(color='orange', line=dict(color='white', width=0.5)))

    # Create subplot with two histograms
    fig_distplot = go.Figure(data=[hist_house, hist_flat], layout=go.Layout(barmode='overlay', title='Price Distribution by Property Type'))
    
    fig_distplot.update_layout(
    paper_bgcolor="#020617",
    plot_bgcolor="#020617",

    # Global font
    font=dict(
        color="#E5E7EB",
        size=14
    ),

    title=dict(
        text="Price Distribution by Property Type",
        font=dict(color="#F8FAFC", size=18),
        x=0.01
    ),

    margin=dict(l=50, r=30, t=60, b=50),

    xaxis=dict(
        title=dict(
            text="Price",
            font=dict(color="#E5E7EB")
        ),
        tickfont=dict(color="#CBD5E1"),
        gridcolor="#334155",
        zerolinecolor="#475569"
    ),

    yaxis=dict(
        title=dict(
            text="Count",
            font=dict(color="#E5E7EB")
        ),
        tickfont=dict(color="#CBD5E1"),
        gridcolor="#334155",
        zerolinecolor="#475569"
    ),

    legend=dict(
        font=dict(color="#E5E7EB"),
        bgcolor="rgba(0,0,0,0)"
    )
    )


    st.plotly_chart(fig_distplot, use_container_width=True)
    
    # Footer information
    st.markdown("""
        <div style='background: #1a1a2e; padding: 1.5rem; border-radius: 12px; 
                    border-left: 5px solid #64B5F6; margin: 1rem 0;'>
            <h4 style='color: #64B5F6; margin-bottom: 1rem;'>About This Dashboard</h4>
            <p style='color: #cccccc; line-height: 1.8; margin: 0;'>
                This analytics dashboard provides <strong>comprehensive insights</strong> into Gurgaon's real estate market 
                through interactive visualizations. Use these tools to make <strong>informed investment decisions</strong> 
                and understand market trends across different sectors and property types.
            </p>
        </div>
    """, unsafe_allow_html=True)


# Call the main function
if __name__ == "__main__":
    show_analytics_dashboard()