# Habitalytics Frontend

Streamlit web application for real estate analytics and price predictions.

## Overview

The frontend is a comprehensive Streamlit application that provides:
- **Property Valuation**: ML-powered price predictions (requires backend API)
- **Analytics Dashboard**: Interactive visualizations and market insights
- **Property Recommender**: Location-based property recommendations

## Setup

### Prerequisites
- Python 3.8 or higher (Dockerfile uses Python 3.12-slim)
- pip

### Installation

1. **Install dependencies**:
```bash
pip install -r requirements.txt
```

2. **Ensure all required files are in place**:
   - `Home.py` - Main application entry point
   - `sidebar.py` - Sidebar navigation (imported by `Home.py`)
   - `df.pkl` - Dataset for dropdown options
   - `static/theme.css` - Custom styles (loaded by `Home.py`)
   - `datasets/` - Pickle files, CSVs, images for Analytics and Recommender
   - `pages/` - Streamlit page modules: `Property_Valuation.py`, `Analytics_Dashboard.py`, `Property_Recommender.py`

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

Only the Property Valuation page calls the backend. `API_URL` is read in `pages/Property_Valuation.py` via `os.getenv("API_URL", "http://localhost:8000")`.

1. **Start the backend API** (in a separate terminal, from repo root):
   ```bash
   cd webapp/backend
   python api.py
   ```
   Backend runs on `http://localhost:8000` by default.

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

| Variable   | Required | Default                  | Description |
|------------|----------|--------------------------|-------------|
| `API_URL`  | No       | `http://localhost:8000`  | Backend API base URL. Used only in `pages/Property_Valuation.py` for `/predict` requests. Set when backend is on another host/port or when deployed. |
| `PORT`     | No       | 8080 (in Docker only)    | Used by the Dockerfile CMD to set Streamlit's port. Not read by Python code. |

No other environment variables are used in the frontend code.

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
- `pandas==2.3.3`, `numpy==2.3.4` - Data
- `plotly==6.3.1` - Interactive visualizations
- `matplotlib==3.10.7`, `seaborn==0.13.2` - Plotting
- `wordcloud==1.9.4` - Word clouds
- `requests==2.28.2` - HTTP calls to backend (Property Valuation)
- `beautifulsoup4==4.12.2`, `retrying==1.3.4` - Used by app logic

## Running with Docker

The frontend has a `Dockerfile` in this directory. Multi-stage build (Python 3.12-slim); the container runs Streamlit and uses the `PORT` environment variable (default 8080).

From the repository root:

```bash
cd webapp/frontend
docker build -t habitalytics-frontend .
docker run -p 8080:8080 -e PORT=8080 -e API_URL=http://localhost:8000 habitalytics-frontend
```

App URL: `http://localhost:8080`. If the frontend runs in Docker and the backend on the host, set `API_URL` to a URL the container can reach (e.g. `http://host.docker.internal:8000` on Docker Desktop).

## Deployment

The repository does not include `cloudbuild.yaml` or deployment scripts. The Dockerfile uses `PORT` (default 8080), which fits platforms like Google Cloud Run. Deploy the built image as a service and set `API_URL` to the deployed backend URL. Frontend and backend are deployed as separate services.

## Project Structure

```
webapp/frontend/
├── Home.py                      # Main Streamlit app (loads static/theme.css)
├── sidebar.py                   # Sidebar navigation
├── Dockerfile                   # Container image (Python 3.12, PORT default 8080)
├── requirements.txt
├── df.pkl                       # Dataset for dropdowns
├── sector_coordinates.csv
├── static/
│   ├── theme.css                # Custom theme (dark, mobile)
│   └── sidebar.js
├── datasets/                    # Data for Analytics and Recommender
│   ├── cosine_sim1.pkl
│   ├── cosine_sim2.pkl
│   ├── cosine_sim3.pkl
│   ├── data_viz1.csv
│   ├── feature_text.pkl
│   ├── link_loc.pkl
│   ├── location_distance.pkl
│   ├── wordcloud_df.pkl
│   ├── property_images.csv
│   └── [logo images]
└── pages/
    ├── __init__.py
    ├── Property_Valuation.py    # Calls backend at API_URL/predict
    ├── Analytics_Dashboard.py
    └── Property_Recommender.py
```

## Styling

`Home.py` injects `static/theme.css` into the page. The theme includes a dark background, green (#5fcf7c) and blue (#64B5F6) accents, mobile styles (≤768px), and custom button/card styling.

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
- Check Python version (3.8+ required)

## Notes

- Property Valuation is the only page that uses the backend; it sends POST requests to `{API_URL}/predict`. Analytics Dashboard and Property Recommender use only local data in `datasets/`.
- The backend must be running and reachable at `API_URL` for price predictions to work.
- Datasets are loaded from pickle/CSV under `datasets/`; images come from CSV or a fallback asset.