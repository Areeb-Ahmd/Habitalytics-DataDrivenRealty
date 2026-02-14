# Habitalytics Backend API

FastAPI backend service for property price predictions using machine learning models.

## Overview

The backend provides a RESTful API for the Habitalytics frontend application. It serves ML-powered property price predictions using a trained Random Forest model.

## Setup

### Prerequisites
- Python 3.8 or higher (Dockerfile uses Python 3.12-slim)
- pip

### Installation

1. **Install dependencies**:
```bash
pip install -r requirements.txt
```

2. **Ensure model file is present**:
   - `pipeline.joblib` - Trained ML pipeline (must be in backend directory)
   - This file contains the complete preprocessing pipeline and Random Forest model

## Running Locally

### Option 1: Using Python script
```bash
python api.py
```

### Option 2: Using uvicorn directly
```bash
uvicorn api:app --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

### Verify API is running
- Visit `http://localhost:8000` in your browser
- Visit `http://localhost:8000/health` for health check
- API documentation: `http://localhost:8000/docs` (Swagger UI)
- Alternative docs: `http://localhost:8000/redoc` (ReDoc)

## 📡 API Endpoints

### `GET /`
- **Description**: API status and information
- **Response**: JSON with API name and status

### `GET /health`
- **Description**: Health check endpoint
- **Response**: JSON with `"status": "Healthy"` and `"Prediction Model loaded successfully": true/false`

### `POST /predict`
- **Description**: Predict property price based on input features
- **Content-Type**: `application/json`

#### Request Body

`PropertyInput` in `api.py`: all fields required. `balcony` is a string (e.g. `"2"`).

```json
{
  "property_type": "flat",
  "sector": "Sector 1",
  "bedRoom": 2.0,
  "bathroom": 2.0,
  "balcony": "2",
  "agePossession": "New Property",
  "built_up_area": 1200.0,
  "servant_room": 0.0,
  "store_room": 1.0,
  "furnishing_type": "Semi-Furnished",
  "luxury_category": "Medium",
  "floor_category": "Mid"
}
```

#### Response
```json
{
  "base_price": 1.5,
  "lower_range": 1.28,
  "upper_range": 1.72
}
```

**Response Fields**:
- `base_price`: Predicted price in Crores (₹)
- `lower_range`: base_price − 0.22 (Crores)
- `upper_range`: base_price + 0.22 (Crores)

#### Example using curl
```bash
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "property_type": "flat",
    "sector": "Sector 1",
    "bedRoom": 2.0,
    "bathroom": 2.0,
    "balcony": "2",
    "agePossession": "New Property",
    "built_up_area": 1200.0,
    "servant_room": 0.0,
    "store_room": 1.0,
    "furnishing_type": "Semi-Furnished",
    "luxury_category": "Medium",
    "floor_category": "Mid"
  }'
```

## CORS Configuration

Configured in `api.py`:
- **allow_origins**: `["*"]`
- **allow_credentials**: `True`
- **allow_methods**: `["*"]`
- **allow_headers**: `["*"]`

## Dependencies

Key packages (see `requirements.txt` for full list):
- `fastapi==0.115.0` - Web framework
- `uvicorn[standard]==0.30.6` - ASGI server
- `pydantic==2.9.2` - Data validation
- `scikit-learn==1.7.2` - ML library
- `joblib==1.4.2` - Model serialization
- `pandas==2.3.3` - Data manipulation
- `numpy==2.3.4` - Numerical computing
- `category-encoders==2.9.0` - Used by the trained pipeline

## Running with Docker

The backend has a `Dockerfile` in this directory. Multi-stage build (Python 3.12-slim); the container runs uvicorn and uses the `PORT` environment variable (default 8000).

From the repository root:

```bash
cd webapp/backend
docker build -t habitalytics-backend .
docker run -p 8000:8000 -e PORT=8000 habitalytics-backend
```

Ensure `pipeline.joblib` is in `webapp/backend/` before building. Build context should include `api.py`, `requirements.txt`, and `pipeline.joblib`.

## Deployment

The repository does not include `cloudbuild.yaml` or gcloud scripts. The Dockerfile is written to use `PORT` (default 8000), which platforms like Google Cloud Run set automatically. Deploy by building the image (e.g. with Cloud Build or Artifact Registry) and creating a service. Restrict CORS `allow_origins` in `api.py` to your frontend URL in production. Set the frontend's `API_URL` to the deployed backend URL.

## Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `PORT`   | No       | 8000    | Server port. Read in `api.py`; used by the Dockerfile and PaaS (e.g. Cloud Run). |

No other environment variables are used in the code.

## Model Information

- **Model Type**: Random Forest Regressor
- **Pipeline**: Includes preprocessing (scaling, encoding) and model
- **Input Features**: 12 property attributes (see `PropertyInput` in `api.py`)
- **Output**: Price prediction in Crores (₹)
- **File Format**: Joblib (.joblib)

## Troubleshooting

### Model not loading
- Verify `pipeline.joblib` exists in the backend directory
- Check file permissions
- Ensure joblib version matches training environment

### Import errors
- Verify all dependencies: `pip install -r requirements.txt`
- Check Python version (3.8+ required)

### CORS errors from frontend
- Verify CORS middleware is configured
- Check allowed origins match your frontend URL
- For local development, `allow_origins=["*"]` is acceptable

## 📝 API Documentation

FastAPI automatically generates interactive API documentation:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## 🔐 Security Considerations

1. **CORS**: Restrict allowed origins in production
2. **Input Validation**: Pydantic models validate all inputs
3. **Error Handling**: Errors are caught and returned as HTTP responses
4. **Rate Limiting**: Consider adding rate limiting for production use

## Integration with Frontend

The Streamlit frontend (`webapp/frontend`) calls this API using the `API_URL` environment variable (set in `pages/Property_Valuation.py`). Ensure the frontend's `API_URL` matches the backend's base URL (e.g. `http://localhost:8000` locally or the deployed service URL).