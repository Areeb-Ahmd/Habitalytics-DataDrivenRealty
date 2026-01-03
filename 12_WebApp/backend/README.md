# Habitalytics Backend API

FastAPI backend service for property price predictions.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Ensure `pipeline.joblib` is in the backend directory

## Running Locally

```bash
python api.py
```

Or with uvicorn:
```bash
uvicorn api:app --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

## API Endpoints

- `GET /` - API status
- `GET /health` - Health check
- `POST /predict` - Predict property price

### Predict Endpoint

**Request Body:**
```json
{
  "property_type": "flat",
  "sector": "Sector 1",
  "bedRoom": 2.0,
  "bathroom": 2.0,
  "balcony": 2,
  "agePossession": "New Property",
  "built_up_area": 1200.0,
  "servant_room": 0.0,
  "store_room": 1.0,
  "furnishing_type": "Semi-Furnished",
  "luxury_category": "Medium",
  "floor_category": "Mid"
}
```

**Response:**
```json
{
  "base_price": 1.5,
  "lower_range": 1.28,
  "upper_range": 1.72
}
```

## Deployment on Render

1. Create a new Web Service
2. Set Root Directory: `12 WebApp/backend`
3. Build Command: `pip install -r requirements.txt`
4. Start Command: `uvicorn api:app --host 0.0.0.0 --port $PORT`
5. Environment Variables: `PORT` (automatically set by Render)

## Environment Variables

- `PORT` - Server port (default: 8000)

