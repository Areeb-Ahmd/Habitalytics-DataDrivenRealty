# Habitalytics - Real Estate Analytics Platform

<div align="center">

![Habitalytics](https://img.shields.io/badge/Habitalytics-Data%20Driven%20Realty-5fcf7c?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.50.0-FF4B4B?style=for-the-badge&logo=streamlit)
![Machine Learning](https://img.shields.io/badge/ML-Scikit--Learn-orange?style=for-the-badge&logo=scikit-learn)

**A comprehensive real estate analytics platform combining Data Science, Machine Learning, and Real Estate Intelligence for Gurgaon properties**

[Features](#-features) • [Installation](#-installation) • [Usage](#-usage) • [Project Structure](#-project-structure) • [Technologies](#-technologies)

</div>

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Project Structure](#-project-structure)
- [Installation](#-installation)
- [Usage](#-usage)
- [Technologies](#-technologies)
- [Data Pipeline](#-data-pipeline)
- [Machine Learning Models](#-machine-learning-models)
- [Web Application](#-web-application)
- [Configuration](#-configuration)
- [Deployment](#-deployment)
- [Contributing](#-contributing)
- [Contact](#-contact)

---

## 🎯 Overview

**Habitalytics** is an end-to-end real estate analytics platform designed specifically for the Gurgaon property market. The project leverages web scraping, advanced data preprocessing, feature engineering, and machine learning to provide:

- **Accurate Price Predictions** using ML models
- **Interactive Analytics Dashboard** with comprehensive visualizations
- **Intelligent Apartment Recommendations** based on location and preferences

The platform is built for **home buyers, real estate investors, property sellers, and market analysts** to make data-driven property decisions.

---

## Features

### Price Predictor
- Predict property prices across Gurgaon using ML models
- Considers location, area, furnishing, amenities, and market trends
- Provides instant price estimates for buying or renting decisions

### Analytics Dashboard
- Sector-wise interactive visualizations
- Price trend analysis
- Property distribution insights
- Market dynamics exploration
- Word clouds and feature analysis

### Property Recommender
- Personalized property recommendations using content-based filtering
- Location-based filtering with radius search (in kilometers)
- **Cosine Similarity**: Multiple similarity matrices (facilities-based, price-based, location-based) combined with weighted scoring
- **TF-IDF Vectorization**: Property features and amenities converted to vectors for similarity computation
- Multi-factor property matching (amenities, features, location advantages)

---

## 📁 Project Structure

```
Habitalytics/
│
├── config/                          # Configuration package
│   ├── __init__.py                  # Package initialization
│   └── paths.py                     # Centralized path management
│
├── data/                            # All data files (centralized)
│   ├── raw/                         # Raw scraped data
│   │   ├── flats.csv
│   │   ├── houses.csv
│   │   └── appartments.csv
│   ├── processed/                   # Processed datasets
│   │   ├── flats_cleaned.csv
│   │   ├── house_cleaned.csv
│   │   ├── gurgaon_properties.csv
│   │   ├── gurgaon_properties_cleaned_v1.csv
│   │   ├── gurgaon_properties_cleaned_v2.csv
│   │   ├── gurgaon_properties_outlier_treated.csv
│   │   ├── gurgaon_properties_missing_value_imputation.csv
│   │   ├── gurgaon_properties_post_feature_selection.csv
│   │   └── gurgaon_properties_post_feature_selection_v2.csv
│   ├── analytics/                   # Analytics datasets
│   │   ├── data_viz1.csv
│   │   ├── latlong.csv
│   │   └── sector_coordinates.csv
│   └── recommender/                 # Recommender datasets
│       ├── appartments.csv
│       └── property_images.csv
│
├── models/                          # All model files (centralized)
│   ├── pipeline.joblib              # Trained ML pipeline
│   ├── df.pkl                       # Processed dataset
│   ├── cosine_sim1.pkl              # Similarity matrices
│   ├── cosine_sim2.pkl
│   ├── cosine_sim3.pkl
│   ├── location_distance.pkl
│   ├── link_loc.pkl
│   ├── feature_text.pkl
│   └── wordcloud_df.pkl
│
├── notebooks/                       # Jupyter notebooks (organized by stage)
│   ├── 01_data_collection/
│   │   └── 99_acres_scrap.py
│   ├── 02_preprocessing/
│   │   ├── data-preprocessing-flats.ipynb
│   │   ├── data-preprocessing-houses.ipynb
│   │   ├── data-preprocessing-level-2.ipynb
│   │   └── merge-flats-and-house.ipynb
│   ├── 03_feature_engineering/
│   │   └── feature-engineering.ipynb
│   ├── 04_eda/
│   │   ├── eda-univariate-analysis.ipynb
│   │   └── eda-multivariate-analysis.ipynb
│   ├── 05_outlier_detection/
│   │   └── outlier-treatment.ipynb
│   ├── 06_missing_value_imputation/
│   │   └── missing-value-imputation.ipynb
│   ├── 07_feature_selection/
│   │   ├── feature-selection_1.ipynb
│   │   └── feature-selection_2.ipynb
│   ├── 08_baseline_model/
│   │   └── baseline-model.ipynb
│   ├── 09_model_selection/
│   │   └── model-selection.ipynb
│   ├── 10_analytics/
│   │   └── data-visualization.ipynb
│   ├── 11_recommender/
│   │   └── recommender-system.ipynb
│   └── requirements.txt
│
├── scripts/                         # Utility scripts
│   ├── 99_acres_scrap.py
│   ├── generate_images.py
│   └── latlong_scraper.py
│
├── webapp/                          # Web application
│   ├── backend/
│   │   ├── api.py                   # FastAPI backend service
│   │   ├── Dockerfile               # Container image (Python 3.12, PORT default 8000)
│   │   ├── pipeline.joblib          # ML model pipeline (copy)
│   │   ├── requirements.txt
│   │   └── README.md
│   │
│   └── frontend/
│       ├── Home.py                  # Main Streamlit application
│       ├── sidebar.py               # Sidebar navigation
│       ├── Dockerfile               # Container image (Python 3.12, PORT default 8080)
│       ├── requirements.txt
│       ├── df.pkl                   # Dataset for dropdown options
│       ├── sector_coordinates.csv
│       ├── static/                  # theme.css, sidebar.js
│       ├── datasets/                # Required datasets and models
│       │   ├── cosine_sim1.pkl
│       │   ├── cosine_sim2.pkl
│       │   ├── cosine_sim3.pkl
│       │   ├── data_viz1.csv
│       │   ├── feature_text.pkl
│       │   ├── link_loc.pkl
│       │   ├── location_distance.pkl
│       │   ├── wordcloud_df.pkl
│       │   ├── property_images.csv
│       │   └── [logo images]
│       └── pages/
│           ├── Property_Valuation.py
│           ├── Analytics_Dashboard.py
│           └── Property_Recommender.py
│
├── pyproject.toml                   # Package configuration
└── README.md                        # This file
```

**Note**: All notebooks use the centralized `config` package for path management. Data files are stored in `data/` and model files in `models/` directories, eliminating redundant copies.

---

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Git (for cloning the repository)

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/Habitalytics.git
cd Habitalytics
```

### Step 2: Install Configuration Package

Install the project's configuration package in editable mode to enable centralized path management:

```bash
pip install -e .
```

This installs the `habitalytics-config` package, allowing all notebooks and scripts to import paths from the `config` module.

### Step 3: Navigate to Frontend Directory

```bash
cd webapp/frontend
```

### Step 4: Create Virtual Environment

**Windows:**
```bash
python -m venv .venv
.venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Step 5: Install Frontend Dependencies

```bash
pip install -r requirements.txt
```

### Step 6: Setup Backend API (Optional but Recommended)

For the Property Valuation feature to work, you need to run the backend API:

1. Navigate to backend directory (from repo root: `webapp/backend`):
   ```bash
   cd webapp/backend
   ```

2. Install backend dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Ensure `pipeline.joblib` is present in the backend directory

4. Run the API server:
   ```bash
   python api.py
   ```
   Or with uvicorn:
   ```bash
   uvicorn api:app --host 0.0.0.0 --port 8000
   ```

5. Set environment variable for frontend (in a new terminal):
   ```bash
   # Windows
   $env:API_URL="http://localhost:8000"
   
   # Linux/Mac
   export API_URL=http://localhost:8000
   ```

### Step 7: Verify Installation

Ensure all required files are present:
- Configuration package installed (`pip install -e .`)
- `webapp/frontend/Home.py`
- `webapp/frontend/df.pkl`
- `webapp/frontend/datasets/` folder with all pickle files and CSVs
- `webapp/frontend/pages/` folder with all page modules
- `data/` directory with all data files
- `models/` directory with all model files

### Running with Docker (containerized)

Backend and frontend each have a `Dockerfile` in `webapp/backend/` and `webapp/frontend/`. There is no `docker-compose` in the project; run the two containers separately.

**Backend** (ensure `pipeline.joblib` is in `webapp/backend/` before building):

```bash
cd webapp/backend
docker build -t habitalytics-backend .
docker run -p 8000:8000 -e PORT=8000 habitalytics-backend
```

**Frontend** (in another terminal; set `API_URL` to the backend URL the browser or frontend container can reach):

```bash
cd webapp/frontend
docker build -t habitalytics-frontend .
docker run -p 8080:8080 -e PORT=8080 -e API_URL=http://localhost:8000 habitalytics-frontend
```

Frontend app: `http://localhost:8080`. Backend API: `http://localhost:8000`. If the frontend runs in Docker and the backend on the host, use the host’s address (e.g. `http://host.docker.internal:8000` on Docker Desktop) for `API_URL`.

The Dockerfiles use `PORT` (backend default 8000, frontend default 8080) and are suitable for platforms like Google Cloud Run; the repository does not include `cloudbuild.yaml` or gcloud deployment scripts.

---

## 💻 Usage

### Working with Notebooks

All notebooks use the centralized `config` package for path management. To use notebooks:

1. **Install the configuration package** (if not already installed):
   ```bash
   pip install -e .
   ```

2. **Import paths in your notebook**:
   ```python
   from config import DATA_RAW, DATA_PROCESSED, DATA_ANALYTICS, DATA_RECOMMENDER, MODELS_DIR, PROJECT_ROOT
   ```

3. **Use standardized paths**:
   ```python
   # Read data
   df = pd.read_csv(DATA_PROCESSED / 'gurgaon_properties_cleaned_v1.csv')
   
   # Save models
   joblib.dump(model, MODELS_DIR / 'pipeline.joblib')
   
   # Save processed data
   df.to_csv(DATA_PROCESSED / 'output.csv', index=False)
   ```

This ensures all file operations use consistent paths regardless of where the notebook is located.

### Running the Web Application

1. **Activate your virtual environment** (if not already activated):
   ```bash
   # Windows
   .venv\Scripts\activate
   
   # Linux/Mac
   source .venv/bin/activate
   ```

2. **Navigate to the frontend directory**:
   ```bash
   cd webapp/frontend
   ```
   
3. **Start the backend API** (in a separate terminal, if using Property Valuation):
   ```bash
   cd webapp/backend
   python api.py
   ```

4. **Run the Streamlit application**:
   ```bash
   streamlit run Home.py
   ```

5. **Access the application**:
   - The app will automatically open in your default web browser
   - Default URL: `http://localhost:8501`
   - Backend API (if running): `http://localhost:8000`

### Using the Application

#### Home Page
- Overview of the platform
- Navigation to different modules
- Information about features and benefits

#### Property Valuation
1. **Ensure backend API is running** (see Setup Step 5)
2. Select property details:
   - Property type (flat/house)
   - Sector (location in Gurgaon)
   - Bedrooms, Bathrooms, Balconies
   - Built-up area (in sqft)
   - Property age/Possession status
   - Furnishing type
   - Floor category (Low/Mid/High)
   - Additional rooms (servant room, store room)
   - Luxury category
3. Click **"Predict Price"** to get instant price prediction with:
   - Base price estimate
   - Lower range (22% below base - conservative estimate)
   - Upper range (22% above base - optimistic estimate)

#### Analytics Dashboard
- **Sector-wise Price Map**: Interactive map showing average prices per sqft across sectors
- **Features Word Cloud**: Visualize most common amenities by sector
- **Built-up Area vs Price**: Scatter plots showing price-area relationships
- **BHK Distribution**: Pie charts showing bedroom configuration distribution
- **Price Comparison**: Box plots comparing prices across different BHK configurations
- **Price Distribution**: Side-by-side histograms for houses vs flats

#### Property Recommender
1. **Select Location and Radius**:
   - Choose a location (sector) from dropdown
   - Set search radius in kilometers
   - Click "Search" to find properties in the area
2. **Get Recommendations**:
   - Select an apartment from the search results
   - Click "Recommend" to get similar properties
   - View recommendations with similarity scores
   - Access property listings on 99acres.com
3. **Recommendation Factors**:
   - Location proximity (distance-based)
   - Similar amenities and features (TF-IDF + Cosine Similarity)
   - Price range similarity
   - Property characteristics matching

---

## Technologies

### Core Technologies
- **Python 3.x** - Programming language
- **Streamlit** - Web application framework
- **Pandas** - Data manipulation and analysis
- **NumPy** - Numerical computing

### Machine Learning
- **Scikit-learn** - ML algorithms and preprocessing
- **XGBoost** - Gradient boosting framework
- Models tested:
  - Linear Regression
  - Support Vector Regression (SVR)
  - Ridge Regression
  - Lasso Regression
  - Decision Tree Regressor
  - Random Forest Regressor
  - Extra Trees Regressor
  - Gradient Boosting Regressor
  - AdaBoost Regressor
  - Multi-Layer Perceptron (MLP)
  - XGBoost Regressor

### Data Visualization
- **Plotly** - Interactive visualizations
- **Matplotlib** - Static plotting
- **Seaborn** - Statistical visualizations
- **WordCloud** - Text visualization

### Web Scraping
- **BeautifulSoup4** - HTML parsing
- **Selenium** - Web automation
- **Requests** - HTTP library

### Data Processing
- **Pickle** - Model serialization
- **Retrying** - Retry mechanisms for web scraping

---

## Data Pipeline

### 1. Data Collection
- **Web Scraping**: Built custom scraper using BeautifulSoup4 and Requests library
- Extracted property details from 99acres.com including:
  - Property information (name, type, price, area)
  - Configuration (bedrooms, bathrooms, balconies, additional rooms)
  - Location details (sector, address, nearby locations)
  - Features and amenities (furnishing details, property features)
  - Property metadata (age/possession, floor number, facing direction)
- Implemented rate limiting and random delays to prevent IP blocking
- Data stored in CSV format in `data/raw/` directory (flats.csv, houses.csv, appartments.csv)

### 2. Data Preprocessing
- Handling missing values
- Data type conversions
- Merging datasets (flats and houses)
- Initial cleaning and standardization

### 3. Feature Engineering
- **Area Feature Extraction**: Extracted Super Built-up, Built-up, and Carpet area from text using regex patterns
- **Derived Features**: Created luxury category (Low/Medium/High) and floor category (Low/Mid/High) from numerical scores
- **Additional Rooms**: Extracted binary features for servant room, store room, study room, pooja room from text data
- **Text Processing**: Used MultiLabelBinarizer to convert amenities and features lists into binary feature matrices
- **Categorical Encoding**: Applied OrdinalEncoder, OneHotEncoder, and TargetEncoder for different categorical features
- **Feature Transformations**: Log transformation for target variable to handle price distribution skewness

### 4. Exploratory Data Analysis (EDA)
- Univariate analysis
- Multivariate analysis
- Correlation analysis
- Distribution analysis

### 5. Outlier Detection & Treatment
- **IQR Method**: Used Interquartile Range (IQR) method for outlier detection
- Statistical analysis of price and price_per_sqft distributions
- Outlier removal/treatment to improve data quality and model performance

### 6. Missing Value Imputation
- **Statistical Imputation**: Used median ratios for area-related features (super_built_up_area, built_up_area, carpet_area)
- Calculated conversion ratios from complete data to impute missing values
- Handling missing categorical and numerical features with domain-specific strategies

### 7. Feature Selection
- Feature importance analysis
- Dimensionality reduction
- Optimal feature subset selection

### 8. Model Development
- Baseline model creation
- Multiple model comparison (11 regression models tested)
- 10-fold cross-validation for robust evaluation
- Hyperparameter tuning using RandomizedSearchCV
- Model selection based on performance metrics (R², MAE)
- **Final Model**: Random Forest Regressor (optimized with 200 estimators)

### 9. Model Deployment
- Pipeline creation
- Model serialization (joblib and pickle)
- Models stored in centralized `models/` directory
- Integration with web application
- **Path Management**: All notebooks use the `config` package for standardized file paths

---

## Machine Learning Models

**Final Model**: Random Forest Regressor (optimized with hyperparameter tuning)

The project implements and compares multiple regression models to select the best performing one:

| Model | Description |
|-------|-------------|
| **Linear Regression** | Baseline linear model |
| **SVR** | Support Vector Regression with RBF kernel |
| **Ridge** | L2 regularization |
| **Lasso** | L1 regularization |
| **Decision Tree** | Tree-based non-linear model |
| **Random Forest** ⭐ | Ensemble of decision trees (Final Selected Model) |
| **Extra Trees** | Extremely Randomized Trees |
| **Gradient Boosting** | Sequential ensemble method |
| **AdaBoost** | Adaptive Boosting |
| **MLP** | Multi-Layer Perceptron neural network |
| **XGBoost** | Extreme Gradient Boosting |

### Model Selection Process
- **Evaluation**: All 11 models were evaluated using 10-fold cross-validation
- **Metrics**: Performance assessed using R² Score and Mean Absolute Error (MAE)
- **Final Selection**: **Random Forest Regressor** was selected as the final model after comprehensive comparison
- **Hyperparameter Tuning**: RandomizedSearchCV was used to optimize Random Forest parameters:
  - `n_estimators`: [200, 300, 400, 500]
  - `max_depth`: [15, 20, 25, 30]
  - `max_samples`: [0.4, 0.5, 0.6, 0.7]
  - `max_features`: [None, 'sqrt', 0.6, 0.8]
  - `min_samples_split`: [2, 5, 10, 15]
  - `min_samples_leaf`: [1, 2, 4, 6]
- **Final Model**: Random Forest with 200 estimators (optimized hyperparameters: max_depth=25, max_samples=0.6, max_features=0.8)

### Model Selection Criteria
- **R² Score** - Coefficient of determination
- **Mean Absolute Error (MAE)** - Prediction accuracy
- **Cross-Validation** - 10-fold CV for robust evaluation

### Preprocessing Pipeline
- **StandardScaler** for numerical features (bedrooms, bathrooms, built-up area, servant room, store room)
- **OrdinalEncoder** for categorical features (property_type, balcony, furnishing_type, luxury_category, floor_category)
- **OneHotEncoder** for agePossession feature
- **TargetEncoder** (category_encoders) for sector encoding (high-cardinality categorical feature)
- **Log transformation** (log1p) for target variable (price) to handle skewness
- **PCA** (optional) for dimensionality reduction

---

## 🌐 Web Application

### Architecture
- **Frontend**: Streamlit (Python-based web framework)
- **Backend**: FastAPI (RESTful API for ML predictions)
- **Data Storage**: Pickle files (.pkl), CSV files, and Joblib models
- **Communication**: HTTP REST API between frontend and backend

### Frontend Pages

#### 1. Home (`Home.py`)
- Landing page with project overview
- Navigation menu using `streamlit-option-menu`
- Feature highlights and benefits
- Contact information and developer details
- **Mobile Responsive**: Optimized CSS for mobile devices (≤768px)

#### 2. Property Valuation (`pages/Property_Valuation.py`)
- Interactive form for property details
- Real-time price prediction via FastAPI backend
- Price range display (lower, base, upper)
- Property summary with all entered details
- Field guide with tooltips for each input field

#### 3. Analytics Dashboard (`pages/Analytics_Dashboard.py`)
- Interactive maps (Plotly scatter_mapbox) showing sector-wise prices
- Word clouds for property features by sector
- Scatter plots (Built-up Area vs Price)
- Pie charts (BHK distribution)
- Box plots (Price comparison by BHK)
- Side-by-side histograms (Price distribution by property type)

#### 4. Property Recommender (`pages/Property_Recommender.py`)
- Location-based property search with radius filtering
- Content-based recommendation system
- Multiple similarity matrices (weighted combination)
- Property cards with images, similarity scores, and direct links
- Integration with 99acres.com listings

### Backend API

#### FastAPI Service (`backend/api.py`)
- **Endpoints**:
  - `GET /` - API status and information
  - `GET /health` - Health check endpoint
  - `POST /predict` - Property price prediction
- **CORS**: Enabled for cross-origin requests from Streamlit frontend
- **Model Loading**: Loads `pipeline.joblib` at startup
- **Response Format**: JSON with base_price, lower_range, upper_range

---

## Dataset Information

### Data Source
- **Website**: 99acres.com
- **Location**: Gurgaon, India
- **Property Types**: Flats, Houses, Apartments

### Key Features
- Property details (bedrooms, bathrooms, area)
- Location information (sector, address)
- Pricing information
- Amenities and features
- Furnishing details
- Age/Possession status
- Nearby locations

### Data Quality
- Comprehensive preprocessing pipeline
- Outlier treatment
- Missing value imputation
- Feature engineering for enhanced predictive power

---

## 🔧 Configuration

### Environment Variables

#### Frontend
- `API_URL` (optional): Backend API URL (default: `http://localhost:8000`)
  - Set this if backend is running on a different host/port
  - Example: `export API_URL=https://your-backend.onrender.com`

#### Backend
- `PORT` (optional): Server port (default: 8000). Read in `webapp/backend/api.py`; used by the backend Dockerfile and deployment platforms (e.g. Cloud Run)

### File Paths

The project uses a centralized path management system through the `config` package. All notebooks and scripts import paths from `config`:

```python
from config import DATA_RAW, DATA_PROCESSED, DATA_ANALYTICS, DATA_RECOMMENDER, MODELS_DIR, PROJECT_ROOT
```

**Key Directories:**
- **Data files**: `data/raw/`, `data/processed/`, `data/analytics/`, `data/recommender/`
- **Model files**: `models/` directory
- **Notebooks**: `notebooks/` directory (organized by stage)
- **Web App**: `webapp/frontend/` and `webapp/backend/`

All file paths are standardized and managed centrally, eliminating hardcoded paths throughout the project.

---

## Deployment

The web app is containerized via Dockerfiles in `webapp/backend/` and `webapp/frontend/`. To deploy:

1. Build each image from its directory (backend image must include `pipeline.joblib`).
2. Deploy backend and frontend as separate services (e.g. Google Cloud Run). Each Dockerfile uses the `PORT` environment variable (backend default 8000, frontend default 8080).
3. Set the frontend service’s `API_URL` to the deployed backend URL. Restrict CORS on the backend to the frontend origin in production.

The repository does not include `cloudbuild.yaml` or gcloud scripts. See `webapp/backend/README.md` and `webapp/frontend/README.md` for API and run details.

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Contribution Guidelines
- Follow PEP 8 style guide
- Add comments for complex logic
- Update documentation as needed
- Test your changes thoroughly

---

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

---

## 👤 Contact

**Syed Areeb Ahmad**

- 📧 Email: [ahmad.syedareeb7@gmail.com](mailto:ahmad.syedareeb7@gmail.com)
- 💼 LinkedIn: [areeb-ahmad7](https://www.linkedin.com/in/areeb-ahmad7)
- 🐙 GitHub: [Areeb-Ahmd](https://github.com/Areeb-Ahmd)

---

## 🙏 Acknowledgments

- **99acres.com** - Data source
- **Streamlit** - Web framework
- **Scikit-learn** - Machine learning library
- **Open-source community** - For various Python packages

---

## 📈 Future Enhancements

- [ ] Expand to other cities (Delhi, Noida, etc.)
- [ ] Real-time data updates
- [ ] User authentication and saved searches
- [ ] Mobile app version
- [ ] Advanced ML models (Deep Learning)
- [ ] Property comparison feature
- [ ] Investment ROI calculator
- [ ] Market trend forecasting

---

## ⚠️ Disclaimer

This project is for educational and research purposes. Price predictions are estimates based on historical data and should not be considered as financial or investment advice. Always consult with real estate professionals for actual property transactions.

---

<div align="center">
⭐ Star this repo if you find it helpful!
</div>

