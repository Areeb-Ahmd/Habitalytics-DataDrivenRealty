from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import joblib
import pandas as pd
import numpy as np
import os

app = FastAPI(title="Habitalytics Price Prediction API")

# Enable CORS for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load model once at startup
pipeline = None

@app.on_event("startup")
async def load_model():
    global pipeline
    try:
        # Load from backend directory
        model_path = os.path.join(os.path.dirname(__file__), "pipeline.joblib")
        pipeline = joblib.load(model_path)
        print("Model loaded successfully")
    except Exception as e:
        print(f"Error loading model: {e}")
        raise

# Property Input Model
class PropertyInput(BaseModel):
    property_type: str
    sector: str
    bedRoom: float
    bathroom: float
    balcony: str
    agePossession: str
    built_up_area: float
    servant_room: float
    store_room: float
    furnishing_type: str
    luxury_category: str
    floor_category: str

# Price Prediction Model
class PricePrediction(BaseModel):
    base_price: float
    lower_range: float
    upper_range: float

@app.get("/")
async def root():
    return {"message": "Habitalytics Price Prediction API", "status": "running"}

@app.get("/health")
async def health_check():
    return {"status": "Healthy", "Prediction Model loaded successfully": pipeline is not None}

@app.post("/predict", response_model=PricePrediction)
async def predict_price(property: PropertyInput):
    if pipeline is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    try:
        # Normalize the input data
        normalized_property_type = property.property_type.lower().strip()
        normalized_sector = property.sector.lower().strip()
        normalized_age = property.agePossession.strip()
        normalized_furnishing = property.furnishing_type.strip()
        normalized_luxury = property.luxury_category.strip()
        normalized_floor = property.floor_category.strip()
        
        # Prepare input data
        input_data = [[
            normalized_property_type,
            normalized_sector,
            property.bedRoom,
            property.bathroom,
            property.balcony,
            normalized_age,
            property.built_up_area,
            property.servant_room,
            property.store_room,
            normalized_furnishing,
            normalized_luxury,
            normalized_floor
        ]]
        
        columns = [
            'property_type', 'sector', 'bedRoom', 'bathroom', 'balcony', 
            'agePossession', 'built_up_area', 'servant room', 'store room', 
            'furnishing_type', 'luxury_category', 'floor_category'
        ]
        
        # Create DataFrame with explicit dtype to match training data structure
        df = pd.DataFrame(input_data, columns=columns, dtype=object)
        
        # Ensure correct data types
        categorical_cols = ['property_type', 'sector', 'balcony', 'agePossession', 
                           'furnishing_type', 'luxury_category', 'floor_category']
        for col in categorical_cols:
            df[col] = df[col].astype(str).str.strip()
        
        # Numeric columns
        numeric_cols = ['bedRoom', 'bathroom', 'built_up_area', 'servant room', 'store room']
        for col in numeric_cols:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # Check for any NaN values in numeric columns
        null_numeric = df[numeric_cols].isnull().any().any()
        if null_numeric:
            null_cols = [col for col in numeric_cols if df[col].isnull().any()]
            raise HTTPException(
                status_code=400,
                detail=f"Invalid numeric values in columns: {null_cols}. Please check your input data."
            )
        
        # Ensure categorical columns don't have empty strings
        for col in categorical_cols:
            if df[col].str.strip().eq('').any():
                raise HTTPException(
                    status_code=400,
                    detail=f"Empty value in column: {col}. Please provide a valid value."
                )
        
        # Make prediction
        prediction_result = pipeline.predict(df)
        
        # Handle both array and scalar results
        if isinstance(prediction_result, np.ndarray):
            pred_value = prediction_result[0] if len(prediction_result) > 0 else prediction_result
        else:
            pred_value = prediction_result
        
        base_price = np.expm1(pred_value)
        lower_range = base_price - 0.22
        upper_range = base_price + 0.22
        
        return PricePrediction(
            base_price=round(base_price, 2),
            lower_range=round(lower_range, 2),
            upper_range=round(upper_range, 2)
        )
    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except ValueError as e:
        error_msg = str(e)
        if "unknown categories" in error_msg.lower():
            # Extract the category name from the error
            import re
            match = re.search(r"\[(.*?)\]", error_msg)
            if match:
                category = match.group(1)
                raise HTTPException(
                    status_code=400,
                    detail=f"Invalid category value: {category}. This value was not seen during model training. Please select a valid option from the dropdown."
                )
            else:
                raise HTTPException(
                    status_code=400,
                    detail=f"Invalid category value. Please ensure all categorical fields match the training data."
                )
        else:
            raise HTTPException(status_code=400, detail=f"Validation error: {error_msg}")
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"Error details: {error_details}")
        error_msg = str(e)
        if "could not convert string to float" in error_msg.lower():
            error_msg = "Invalid data type in input. Please check all fields are correctly formatted."
        elif "expected" in error_msg.lower() and "got" in error_msg.lower():
            error_msg = f"Data format error: {error_msg}"
        raise HTTPException(
            status_code=500, 
            detail=f"Prediction error: {error_msg}"
        )

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)