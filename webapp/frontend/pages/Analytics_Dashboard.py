from __future__ import annotations

import ast
import pickle
from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from wordcloud import WordCloud


DATASETS_DIR = Path("datasets")
DATA_VIZ_CSV = DATASETS_DIR / "data_viz1.csv"
WORDCLOUD_DF_PKL = DATASETS_DIR / "wordcloud_df.pkl"

# Reusable styling
COLORS = {
    "bg_paper": "#020617",
    "bg_plot": "#0f172a",
    "text": "#e5e7eb",
    "grid": "#334155",
    "zero": "#475569",
    "accent": "#64B5F6",
    "panel_bg": "#1a1a2e",
}


def _render_html(html: str) -> None:
    st.markdown(html, unsafe_allow_html=True)


def _render_section_title(title: str) -> None:
    _render_html(
        f"""
        <h2 style='font-size: 2rem; font-weight: 600; margin: 1.5rem 0 1rem 0; color: {COLORS["accent"]};'>
            {title}
        </h2>
        """
    )


def _render_description(text: str) -> None:
    _render_html(
        f"""
        <div style='background: {COLORS["panel_bg"]}; padding: 1rem; border-radius: 8px; margin-bottom: 1rem;'>
            <p style='color: #ffffff; margin: 0; font-size: 1.15rem;'>
                {text}
            </p>
        </div>
        """
    )


def _render_warning(message: str) -> None:
    _render_html(
        f"""
        <div style='background: linear-gradient(135deg, #3a1a1a 0%, #4a2a2a 100%);
                    padding: 1.2rem; border-radius: 12px; margin: 1rem 0;
                    border-left: 4px solid #ff6b6b;
                    box-shadow: 0 2px 8px rgba(255, 107, 107, 0.2);'>
            <p style='color: #ffcccc; margin: 0; font-size: 1rem; line-height: 1.6;'>
                ⚠️ {message}
            </p>
        </div>
        """
    )


def _apply_plotly_attribution_css() -> None:
    # Hide Plotly map attribution and logo
    _render_html(
        """
        <style>
        /* Plotly map (MapLibre) */
        .maplibregl-ctrl-attrib, .maplibregl-ctrl-logo { display: none !important; }
        /* Older Plotly map (Mapbox GL) */
        .mapboxgl-ctrl-attrib, .mapboxgl-ctrl-logo { display: none !important; }
        </style>
        """
    )


def _apply_plotly_dark_theme(fig: go.Figure, *, margin: dict[str, int] | None = None) -> go.Figure:
    fig.update_layout(
        paper_bgcolor=COLORS["bg_paper"],
        plot_bgcolor=COLORS["bg_plot"],
        font=dict(color=COLORS["text"]),
        margin=margin or dict(l=50, r=30, t=50, b=50),
        xaxis=dict(gridcolor=COLORS["grid"], zerolinecolor=COLORS["zero"]),
        yaxis=dict(gridcolor=COLORS["grid"], zerolinecolor=COLORS["zero"]),
        legend=dict(bgcolor="rgba(0,0,0,0)"),
    )
    return fig


def _safe_literal_eval_list(value: Any) -> list[str]:
    """
    Parse a column value that should represent a Python list of strings.
    Returns an empty list for invalid/missing values.
    """
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return []
    if isinstance(value, list):
        return [str(x) for x in value]
    if not isinstance(value, str) or not value.strip():
        return []
    try:
        parsed = ast.literal_eval(value)
    except (ValueError, SyntaxError):
        return []
    if isinstance(parsed, list):
        return [str(x) for x in parsed]
    return []


@st.cache_data(show_spinner=False)
def _load_data() -> tuple[pd.DataFrame, pd.DataFrame]:
    new_df = pd.read_csv(DATA_VIZ_CSV)
    with WORDCLOUD_DF_PKL.open("rb") as f:
        wordcloud_df = pickle.load(f)
    return new_df, wordcloud_df

def show_analytics_dashboard():
    """Render the Analytics Dashboard page."""
    # Hero Section
    _render_html("""
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
    """)
    
    _render_html("""
        <div style='background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%); 
                    padding: 1.5rem; border-radius: 10px; margin: 1rem 0;
                    border-left: 5px solid #64B5F6;'>
            <p style='font-size: 1rem; line-height: 1.6; color: #ffffff; margin: 0; font-size: 1.25rem;'>
                The Analytics Dashboard enables interactive exploration of Gurugram’s real 
                estate listings using historical data. It helps users analyze price patterns, 
                sector-level differences, and property configurations through visual comparisons, 
                supporting data-driven insight and market understanding.
            </p>
        </div>
    """)

    _apply_plotly_attribution_css()
    new_df, wordcloud_df = _load_data()

    # Geo Map
    _render_section_title("Geographic Price Overview")
    _render_description(
        "This map visualizes average property prices per square foot across Gurugram’s sectors. "
        "Color indicates relative price levels, while bubble size represents the average "
        "built-up area of listings in each sector."
    )
    
    group_df = (
        new_df.groupby("sector", as_index=False)[
            ["price", "price_per_sqft", "built_up_area", "latitude", "longitude"]
        ].mean()
    )

    fig = px.scatter_map(
        group_df,
        lat="latitude",
        lon="longitude",
        color="price_per_sqft",
        size="built_up_area",
        hover_name="sector",
        color_continuous_scale=px.colors.cyclical.IceFire,
        zoom=10,
        map_style="open-street-map",
    )

    fig.update_layout(
        paper_bgcolor=COLORS["bg_paper"],
        font=dict(color=COLORS["text"]),
        margin=dict(l=0, r=0, t=0, b=0),
        coloraxis_colorbar=dict(
            title=dict(text="Price / sqft <br>(in INR)", font=dict(color=COLORS["text"])),
            tickfont=dict(color=COLORS["text"]),
        ),
    )
    st.plotly_chart(fig, use_container_width=True, config={"displaylogo": False})

    # Wordcloud
    _render_section_title("Amenities Overview")
    _render_description(
        "This view summarizes the most frequently listed amenities for properties in a selected sector. "
        "Larger words represent features that appear more often in the dataset, helping highlight "
        "common amenity patterns across areas."
    )
    
    selected_sector_cloud = st.selectbox('Select a Sector', wordcloud_df['sector'].unique().tolist())
    new_cloud = wordcloud_df[wordcloud_df['sector'] == selected_sector_cloud]

    wordcloud_tokens: list[str] = []
    for value in new_cloud["features"].tolist():
        wordcloud_tokens.extend(_safe_literal_eval_list(value))

    feature_texts = " ".join(wordcloud_tokens)

    if feature_texts.strip():  # Check if there's actual text to generate wordcloud
        try:
            wordcloud = WordCloud(
                width=1200,
                height=800,
                background_color="white",
                stopwords={"s"},
                min_font_size=10,
            ).generate(feature_texts)
            fig, ax = plt.subplots(figsize=(8, 8), facecolor=None)
            ax.imshow(wordcloud, interpolation='bilinear')
            ax.axis('off')
            plt.tight_layout(pad=0)
            st.pyplot(fig)
            plt.close(fig)
        except Exception:
            _render_warning("Unable to generate word cloud for the selected sector.")
    else:
        _render_warning("No features available for the selected sector to generate word cloud.")


    # Scatter Plot (Built-up Area vs Price)
    _render_section_title("Built-up Area vs Price Distribution")
    _render_description(
        "This visualization explores the relationship between built-up area and listed price for "
        "individual properties in the dataset. Each point represents a listing, with color indicating "
        "the number of bedrooms (BHK), allowing comparison across different configurations."
    )

    property_type_options = sorted(new_df["property_type"].dropna().unique().tolist())
    property_type = st.selectbox("Select Property Type", options=property_type_options)
    filtered_df = new_df.loc[new_df["property_type"] == property_type]
    fig1 = px.scatter(filtered_df, x="built_up_area", y="price", color="bedRoom")
    
    _apply_plotly_dark_theme(fig1, margin=dict(l=50, r=30, t=30, b=50))
    fig1.update_layout(
        xaxis_title="Built-Up Area (in sq. ft.)",
        yaxis_title="Price (in Crores)",
        legend=dict(bgcolor="rgba(0,0,0,0)", title="Bedrooms (BHK)"),
    )
    st.plotly_chart(fig1, use_container_width=True)


    # Pie Chart (BHK Distribution for sectors)
    _render_section_title("Distribution of Bedroom Configurations")
    _render_description(
        "This chart shows the distribution of property listings by bedroom configuration (BHK) "
        "for the selected sector or across all sectors. Each slice represents the proportion of "
        "listings belonging to a specific BHK category within the filtered dataset."
    )

    sector_options = new_df['sector'].unique().tolist()
    sector_options.insert(0, 'Overall')
    selected_sector = st.selectbox('Select Sector', options=sector_options)

    pie_df = new_df if selected_sector == "Overall" else new_df.loc[new_df["sector"] == selected_sector]
    fig2 = px.pie(pie_df, names="bedRoom")

    fig2.update_layout(paper_bgcolor=COLORS["bg_paper"], font=dict(color=COLORS["text"]))
    fig2.update_layout(margin=dict(l=20, r=20, t=20, b=60), legend=dict(bgcolor="rgba(0,0,0,0)"))

    st.plotly_chart(fig2, use_container_width=True)

    # Box Plot (Bedroom Price)
    _render_section_title("BHK-wise Price Distribution")
    _render_description(
        "This chart compares price distributions across different bedroom configurations (BHK) using box plots. "
        "Each box summarizes the spread of prices within a BHK category, highlighting the median, variability, "
        "and outliers present in the dataset."
    )
    
    fig3 = px.box(new_df.loc[new_df["bedRoom"] <= 4], x="bedRoom", y="price")

    _apply_plotly_dark_theme(fig3)
    fig3.update_layout(
        plot_bgcolor=COLORS["bg_paper"],
        xaxis=dict(
            title=dict(text="Bedrooms (BHK)", font=dict(color=COLORS["text"], size=14)),
            tickfont=dict(color="#CBD5E1"),
            gridcolor=COLORS["grid"],
            zerolinecolor=COLORS["zero"],
        ),
        yaxis=dict(
            title=dict(text="Price (in Crores)", font=dict(color=COLORS["text"], size=14)),
            tickfont=dict(color="#CBD5E1"),
            gridcolor=COLORS["grid"],
            zerolinecolor=COLORS["zero"],
        ),
    )

    fig3.update_traces(
        marker=dict(color="#60A5FA", opacity=0.9),
        line=dict(color="#93C5FD"),
        fillcolor="rgba(96,165,250,0.4)",
        boxmean="sd",
    )

    st.plotly_chart(fig3, use_container_width=True)

    #(Price Distribution of Property Types)
    _render_section_title("Comparative Price Distribution: Flats vs Houses")
    _render_description(
        "This chart compares price distributions across property types, specifically flats and houses, "
        "using side-by-side histograms. Each distribution shows how listing prices are spread across "
        "the dataset for each property type."
    )
    
    # Create histograms for House and Flat with adjusted bin size and bar thickness
    hist_house = go.Histogram(
        x=new_df.loc[new_df["property_type"] == "house", "price"],
        nbinsx=100,
        name="Houses",
        opacity=0.6,
        marker=dict(color="orange", line=dict(color="white", width=0.5)),
    )
    hist_flat = go.Histogram(
        x=new_df.loc[new_df["property_type"] == "flat", "price"],
        nbinsx=100,
        name="Flats",
        opacity=0.6,
        marker=dict(color="green", line=dict(color="white", width=0.5)),
    )

    # Create subplot with two histograms
    fig_distplot = go.Figure(data=[hist_house, hist_flat], layout=go.Layout(barmode='overlay'))
    
    _apply_plotly_dark_theme(fig_distplot, margin=dict(l=50, r=30, t=60, b=50))
    fig_distplot.update_layout(
        plot_bgcolor=COLORS["bg_paper"],
        xaxis=dict(
            title=dict(text="Price (in Crores)", font=dict(color=COLORS["text"])),
            tickfont=dict(color="#CBD5E1"),
            gridcolor=COLORS["grid"],
            zerolinecolor=COLORS["zero"],
        ),
        yaxis=dict(
            title=dict(text="Number of Property Listings", font=dict(color=COLORS["text"])),
            tickfont=dict(color="#CBD5E1"),
            gridcolor=COLORS["grid"],
            zerolinecolor=COLORS["zero"],
        ),
        legend=dict(bgcolor="rgba(0,0,0,0)"),
    )
    st.plotly_chart(fig_distplot, use_container_width=True)
    
    # Footer information
    _render_html("""
        <div style='background: #1a1a2e; padding: 1.75rem; border-radius: 12px; 
                    border-left: 5px solid #64B5F6; margin: 1rem 0;'>
            <h4 style='color: #64B5F6; margin-bottom: 1rem; font-size: 1.75rem;'>About This Dashboard</h4>
            <p style='color: #ffffff; line-height: 1.8; margin: 0; font-size: 1.20rem;'>
                This dashboard provides an interactive way to explore Gurugram’s real estate listings 
                using historical data. Through a collection of visual views, it allows users to examine 
                sector-level differences, property types, and bedroom configurations, and to observe 
                how key variables such as price, price per square foot, built-up area, and amenities 
                vary across the dataset.
            </p>
            <p style='color: #ffffff; line-height: 1.8; margin: 0; font-size: 1.20rem; margin-top: 1rem;'>
                The visualizations are designed for exploration and comparison, helping users 
                understand patterns, distributions, and variability present in the data. 
                The dashboard reflects the structure and scope of the underlying dataset 
                and is intended for analytical understanding rather than live market tracking 
                or definitive pricing.
            </p>
        </div>
    """)


# Call the main function
if __name__ == "__main__":
    show_analytics_dashboard()