# 🏠 Habitalytics - Data-Driven Real Estate Analytics Platform

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

## ✨ Features

### 🔹 Price Predictor
- Predict property prices across Gurgaon using ML models
- Considers location, area, furnishing, amenities, and market trends
- Provides instant price estimates for buying or renting decisions

### 🔹 Analytics Dashboard
- Sector-wise interactive visualizations
- Price trend analysis
- Property distribution insights
- Market dynamics exploration
- Word clouds and feature analysis

### 🔹 Apartment Recommender
- Personalized apartment recommendations
- Location-based filtering with radius search
- Similarity-based recommendations using cosine similarity
- Multi-factor property matching (amenities, features, location)

---

## 📁 Project Structure

```
Habitalytics/
│
├── 01 Original Dataset/
│   ├── 99_acres_scrap.py          # Web scraper for 99acres.com
│   ├── flats.csv                   # Scraped flats data
│   ├── houses.csv                  # Scraped houses data
│   └── appartments.csv             # Scraped apartments data
│
├── 02 Preprocessing and Cleaning/
│   ├── data-preprocessing-flats.ipynb
│   ├── data-preprocessing-houses.ipynb
│   ├── data-preprocessing-level-2.ipynb
│   ├── merge-flats-and-house.ipynb
│   └── [cleaned datasets]
│
├── 03 Feature Engineering/
│   ├── feature-engineering.ipynb
│   └── gurgaon_properties_cleaned_v2.csv
│
├── 04 EDA/
│   ├── eda-univariate-analysis.ipynb
│   ├── eda-multivariate-analysis.ipynb
│   └── gurgaon_properties_cleaned_v2.csv
│
├── 05 Outlier Detection/
│   ├── outlier-treatment.ipynb
│   └── gurgaon_properties_outlier_treated.csv
│
├── 06 Missing Value Imputation/
│   ├── missing-value-imputation.ipynb
│   └── gurgaon_properties_missing_value_imputation.csv
│
├── 07 Feature Selection/
│   ├── feature-selection.ipynb
│   ├── feature-selection-and-feature-engineering.ipynb
│   └── gurgaon_properties_post_feature_selection.csv
│
├── 08 Baseline Prediction Model/
│   ├── baseline model.ipynb
│   └── gurgaon_properties_post_feature_selection.csv
│
├── 09 Model Selection/
│   ├── model-selection.ipynb      # Model comparison and selection
│   ├── pipeline.pkl                # Trained ML pipeline
│   ├── df.pkl                      # Processed dataset
│   └── gurgaon_properties_post_feature_selection_v2.csv
│
├── 10 Analytics Module/
│   ├── data-visualization.ipynb
│   ├── data_viz1.csv
│   ├── feature_text.pkl
│   ├── wordcloud_df.pkl
│   └── latlong.csv
│
├── 11 Recommender System/
│   ├── recommender-system.ipynb
│   ├── cosine_sim1.pkl            # Similarity matrices
│   ├── cosine_sim2.pkl
│   ├── cosine_sim3.pkl
│   ├── location_distance.pkl
│   ├── link_loc.pkl
│   └── appartments.csv
│
└── 12 WebApp/
    ├── Home.py                     # Main Streamlit application
    ├── requirements.txt             # Python dependencies
    ├── pipeline.pkl                # ML model pipeline
    ├── df.pkl                       # Dataset for predictions
    ├── sector_coordinates.csv       # Sector location data
    ├── latlong_scraper.py          # Latitude/longitude scraper
    ├── datasets/                    # All required datasets and models
    │   ├── cosine_sim1.pkl
    │   ├── cosine_sim2.pkl
    │   ├── cosine_sim3.pkl
    │   ├── data_viz1.csv
    │   ├── feature_text.pkl
    │   ├── link_loc.pkl
    │   ├── location_distance.pkl
    │   ├── wordcloud_df.pkl
    │   └── [logo images]
    └── pages/
        ├── Price_Predictor.py      # Price prediction page
        ├── Analysis_App.py         # Analytics dashboard page
        └── Recommend_Apartments.py # Recommender system page
```

---

## 🚀 Installation

### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)
- Git (for cloning the repository)

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/Habitalytics.git
cd Habitalytics
```

### Step 2: Navigate to WebApp Directory

```bash
cd "12 WebApp"
```

### Step 3: Create Virtual Environment

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

### Step 4: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 5: Verify Installation

Ensure all required files are present in the `12 WebApp` directory:
- `Home.py`
- `pipeline.pkl`
- `df.pkl`
- `datasets/` folder with all pickle files and CSVs

---

## 💻 Usage

### Running the Web Application

1. **Activate your virtual environment** (if not already activated):
   ```bash
   # Windows
   .venv\Scripts\activate
   
   # Linux/Mac
   source .venv/bin/activate
   ```

2. **Navigate to the WebApp directory**:
   ```bash
   cd "12 WebApp"
   ```

3. **Run the Streamlit application**:
   ```bash
   streamlit run Home.py
   ```

4. **Access the application**:
   - The app will automatically open in your default web browser
   - Default URL: `http://localhost:8501`

### Using the Application

#### 🏠 Home Page
- Overview of the platform
- Navigation to different modules
- Information about features and benefits

#### 💰 Price Predictor
1. Select property details:
   - Sector (location)
   - Property type
   - Bedrooms, Bathrooms
   - Built-up area
   - Furnishing type
   - Age/Possession
   - Floor category
   - Balcony count
   - Additional rooms (servant room, store room)
   - Luxury category

2. Click **"Predict Price"** to get instant price prediction

#### 📊 Analytics Dashboard
- Explore sector-wise average prices
- View interactive visualizations
- Analyze property distributions
- Generate word clouds for property features
- Explore market trends

#### 🎯 Apartment Recommender
1. Enter apartment name or select from dropdown
2. Specify search radius (in km)
3. Get personalized recommendations based on:
   - Location proximity
   - Similar amenities
   - Property features
   - Market characteristics

---

## 🛠️ Technologies

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

## 🔄 Data Pipeline

### 1. Data Collection
- Web scraping from 99acres.com
- Extraction of property details (price, area, location, amenities, etc.)
- Data stored in CSV format

### 2. Data Preprocessing
- Handling missing values
- Data type conversions
- Merging datasets (flats and houses)
- Initial cleaning and standardization

### 3. Feature Engineering
- Creating derived features
- Categorical encoding
- Feature transformations
- Luxury category classification
- Floor category creation

### 4. Exploratory Data Analysis (EDA)
- Univariate analysis
- Multivariate analysis
- Correlation analysis
- Distribution analysis

### 5. Outlier Detection & Treatment
- Statistical methods for outlier detection
- Outlier removal/treatment
- Data quality improvement

### 6. Missing Value Imputation
- Advanced imputation techniques
- Handling missing categorical and numerical features

### 7. Feature Selection
- Feature importance analysis
- Dimensionality reduction
- Optimal feature subset selection

### 8. Model Development
- Baseline model creation
- Multiple model comparison
- Cross-validation
- Hyperparameter tuning
- Model selection based on performance metrics (R², MAE)

### 9. Model Deployment
- Pipeline creation
- Model serialization (pickle)
- Integration with web application

---

## 🤖 Machine Learning Models

The project implements and compares multiple regression models:

| Model | Description |
|-------|-------------|
| **Linear Regression** | Baseline linear model |
| **SVR** | Support Vector Regression with RBF kernel |
| **Ridge** | L2 regularization |
| **Lasso** | L1 regularization |
| **Decision Tree** | Tree-based non-linear model |
| **Random Forest** | Ensemble of decision trees |
| **Extra Trees** | Extremely Randomized Trees |
| **Gradient Boosting** | Sequential ensemble method |
| **AdaBoost** | Adaptive Boosting |
| **MLP** | Multi-Layer Perceptron neural network |
| **XGBoost** | Extreme Gradient Boosting |

### Model Selection Criteria
- **R² Score** - Coefficient of determination
- **Mean Absolute Error (MAE)** - Prediction accuracy
- **Cross-Validation** - 10-fold CV for robust evaluation

### Preprocessing Pipeline
- StandardScaler for numerical features
- OneHotEncoder for categorical features
- Log transformation for target variable (price)
- PCA (optional) for dimensionality reduction

---

## 🌐 Web Application

### Architecture
- **Frontend**: Streamlit (Python-based)
- **Backend**: Python with scikit-learn
- **Data Storage**: Pickle files and CSV

### Pages

#### 1. Home (`Home.py`)
- Landing page with project overview
- Navigation menu
- Feature highlights
- Contact information

#### 2. Price Predictor (`pages/Price_Predictor.py`)
- Interactive form for property details
- Real-time price prediction
- Model confidence indicators

#### 3. Analytics Dashboard (`pages/Analysis_App.py`)
- Interactive maps (sector-wise prices)
- Statistical visualizations
- Word clouds
- Trend analysis

#### 4. Apartment Recommender (`pages/Recommend_Apartments.py`)
- Property search interface
- Location-based filtering
- Similarity scoring
- Recommendation display

---

## 📊 Dataset Information

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
No environment variables required for basic usage.

### File Paths
Ensure all paths in the code match your directory structure:
- Model files: `pipeline.pkl`, `df.pkl`
- Dataset files: `datasets/` directory
- Logo images: `datasets/logo*.jpg`

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

**Made with ❤️ for Data-Driven Real Estate Decisions**

⭐ Star this repo if you find it helpful!

</div>

