# Habitalytics Frontend

Streamlit web application for real estate analytics and price predictions.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Ensure all required files are in place:
   - `df.pkl` - Data for dropdown options
   - `datasets/` - All dataset files
   - `pages/` - Streamlit pages

## Running Locally

```bash
streamlit run Home.py
```

## Environment Variables

Set the API URL for the backend service:

```bash
export API_URL=http://localhost:8000
```

Or on Windows:
```powershell
$env:API_URL="http://localhost:8000"
```

## Deployment on Render

1. Create a new Web Service
2. Set Root Directory: `12 WebApp/frontend`
3. Build Command: `pip install -r requirements.txt`
4. Start Command: `streamlit run Home.py --server.port $PORT --server.address 0.0.0.0`
5. Environment Variables:
   - `API_URL` - Backend API URL (e.g., `https://your-backend.onrender.com`)
   - `PORT` - Server port (automatically set by Render)

## Pages

- **Home** - Landing page
- **Price Predictor** - Property price prediction (requires backend API)
- **Analytics** - Data visualization and analysis
- **Recommend Apartments** - Property recommendation system

