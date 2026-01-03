# Habitalytics Frontend

Streamlit web application for real estate analytics and price predictions.

## Overview

The frontend is a comprehensive Streamlit application that provides:
- **Property Valuation**: ML-powered price predictions (requires backend API)
- **Analytics Dashboard**: Interactive visualizations and market insights
- **Property Recommender**: Location-based property recommendations

## Setup

### Prerequisites
- Python 3.7 or higher
- pip package manager

### Installation

1. **Install dependencies**:
```bash
pip install -r requirements.txt
```

2. **Ensure all required files are in place**:
   - `Home.py` - Main application entry point
   - `df.pkl` - Dataset for dropdown options
   - `datasets/` - All dataset files (pickle files, CSVs, images)
   - `pages/` - Streamlit page modules:
     - `Property_Valuation.py`
     - `Analytics_Dashboard.py`
     - `Property_Recommender.py`

## Running Locally

### Basic Setup

1. **Activate virtual environment** (if using one):
   ```bash
   # Windows
   .venv\Scripts\activate
   
   # Linux/Mac
   source .venv/bin/activate
   ```

2. **Run the Streamlit application**:
   ```bash
   streamlit run Home.py
   ```

3. **Access the application**:
   - The app will automatically open in your default web browser
   - Default URL: `http://localhost:8501`

### With Backend API (for Property Valuation)

1. **Start the backend API** (in a separate terminal):
   ```bash
   cd ../backend
   python api.py
   ```
   Backend will run on `http://localhost:8000`

2. **Set environment variable** (in frontend terminal):
   ```bash
   # Windows PowerShell
   $env:API_URL="http://localhost:8000"
   
   # Windows CMD
   set API_URL=http://localhost:8000
   
   # Linux/Mac
   export API_URL=http://localhost:8000
   ```

3. **Run the frontend**:
   ```bash
   streamlit run Home.py
   ```

## Environment Variables

### API_URL (Optional)
- **Purpose**: Backend API URL for Property Valuation feature
- **Default**: `http://localhost:8000`
- **Usage**: Set this if backend is running on a different host/port
- **Example**:
  ```bash
  export API_URL=https://your-backend.railway.app
  ```

## Features

### Home Page
- Project overview and navigation
- Feature highlights
- Contact information
- **Mobile Responsive**: Optimized for mobile devices (≤768px)

### Property Valuation
- Interactive form with field guide
- Real-time price predictions via FastAPI
- Price range display (lower, base, upper)
- Property summary cards

### Analytics Dashboard
- Sector-wise interactive price maps
- Word clouds for property features
- Statistical visualizations (scatter, pie, box plots)
- Price distribution analysis

### Property Recommender
- Location-based search with radius filtering
- Content-based recommendations using cosine similarity
- Property cards with images and similarity scores
- Direct links to 99acres.com listings

## Dependencies

Key packages (see `requirements.txt` for full list):
- `streamlit==1.50.0` - Web framework
- `streamlit-option-menu==0.4.0` - Navigation menu
- `pandas==2.3.3` - Data manipulation
- `plotly==6.3.1` - Interactive visualizations
- `wordcloud==1.9.4` - Word cloud generation
- `requests==2.28.2` - HTTP requests to backend API

## Deployment on Render

1. **Create a new Web Service** on Render
2. **Configuration**:
   - **Root Directory**: `12_WebApp/frontend`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `streamlit run Home.py --server.port $PORT --server.address 0.0.0.0`
3. **Environment Variables**:
   - `API_URL` - Backend API URL (e.g., `https://your-backend.railway.app`)
   - `PORT` - Server port (automatically set by Render)

## 📁 Project Structure

```
frontend/
├── Home.py                      # Main Streamlit app
├── requirements.txt             # Python dependencies
├── df.pkl                       # Dataset for dropdowns
├── sector_coordinates.csv       # Sector coordinates
├── latlong_scraper.py          # Coordinate scraper
├── generate_images.py           # Image generator utility
├── datasets/                    # All data files
│   ├── cosine_sim1.pkl          # Similarity matrix 1
│   ├── cosine_sim2.pkl          # Similarity matrix 2
│   ├── cosine_sim3.pkl          # Similarity matrix 3
│   ├── data_viz1.csv            # Visualization data
│   ├── feature_text.pkl         # Feature text
│   ├── link_loc.pkl             # Property links
│   ├── location_distance.pkl    # Distance matrix
│   ├── wordcloud_df.pkl         # Word cloud data
│   ├── property_images.csv      # Property images
│   └── [logo images]            # App logos
└── pages/                       # Streamlit pages
    ├── __init__.py
    ├── Property_Valuation.py    # Price prediction page
    ├── Analytics_Dashboard.py   # Analytics page
    └── Property_Recommender.py # Recommender page
```

## Styling

The application uses custom CSS for:
- Dark theme (black background)
- Custom color scheme (green accents: #5fcf7c, blue accents: #64B5F6)
- Mobile responsiveness (media queries for ≤768px)
- Custom button and card styling

## Troubleshooting

### Property Valuation not working
- Ensure backend API is running
- Check `API_URL` environment variable is set correctly
- Verify backend is accessible at the specified URL

### Missing datasets error
- Ensure all files in `datasets/` folder are present
- Check file paths in code match your directory structure

### Import errors
- Verify all dependencies are installed: `pip install -r requirements.txt`
- Check Python version (3.7+ required)

## Notes

- The Property Valuation feature requires the backend API to be running
- Analytics Dashboard and Property Recommender work independently
- All datasets are loaded from pickle files for performance
- Images are loaded from CSV file or fallback to `No_images.jpg`

