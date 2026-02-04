# Habitalytics Backend API

FastAPI backend service for property price predictions using machine learning models.

## Overview

The backend provides a RESTful API for the Habitalytics frontend application. It serves ML-powered property price predictions using a trained Random Forest model.

## Setup

### Prerequisites
- Python 3.7 or higher
- pip package manager

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
- **Response**: JSON with status "healthy" if model is loaded

### `POST /predict`
- **Description**: Predict property price based on input features
- **Content-Type**: `application/json`

#### Request Body
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
- `lower_range`: Conservative estimate (22% below base)
- `upper_range`: Optimistic estimate (22% above base)

#### Example using curl
```bash
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{
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
  }'
```

## CORS Configuration

The API has CORS enabled to allow requests from the Streamlit frontend:
- **Allowed Origins**: `*` (all origins) - **Change this in production!**
- **Allowed Methods**: All methods
- **Allowed Headers**: All headers

**⚠️ Security Note**: For production deployment, restrict CORS to your frontend URL:
```python
allow_origins=["https://your-frontend.railway.app"]
```

## Dependencies

Key packages (see `requirements.txt` for full list):
- `fastapi==0.115.0` - Web framework
- `uvicorn[standard]==0.30.6` - ASGI server
- `pydantic==2.9.2` - Data validation
- `scikit-learn==1.7.2` - ML library
- `joblib==1.4.2` - Model serialization
- `pandas==2.3.3` - Data manipulation
- `numpy==2.3.4` - Numerical computing

## Deployment on Railway

1. **Create a new Web Service** on Railway
2. **Configuration**:
   - **Root Directory**: `12_WebApp/backend`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn api:app --host 0.0.0.0 --port $PORT`
3. **Environment Variables**:
   - `PORT` - Server port (automatically set by Railway, don't set manually)

### Deployment Checklist
- [ ] Ensure `pipeline.joblib` is in the backend directory
- [ ] Verify all dependencies are in `requirements.txt`
- [ ] Update CORS settings for production (restrict origins)
- [ ] Test API endpoints after deployment
- [ ] Update frontend `API_URL` environment variable with Railway URL

## Environment Variables

- `PORT` - Server port (default: 8000, automatically set by Railway)

## Model Information

- **Model Type**: Random Forest Regressor
- **Pipeline**: Includes preprocessing (scaling, encoding) and model
- **Input Features**: 11 property attributes
- **Output**: Price prediction in Crores (₹)
- **File Format**: Joblib (.joblib)

## Troubleshooting

### Model not loading
- Verify `pipeline.joblib` exists in the backend directory
- Check file permissions
- Ensure joblib version matches training environment

### Import errors
- Verify all dependencies: `pip install -r requirements.txt`
- Check Python version (3.7+ required)

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

## 📞 Integration with Frontend

The frontend connects to this API using the `API_URL` environment variable:
```python
API_URL = os.getenv("API_URL", "http://localhost:8000")
```

Ensure the frontend's `API_URL` matches the backend's deployed URL.

