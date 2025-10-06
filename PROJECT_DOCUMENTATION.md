# Heart Disease Detection System

A comprehensive AI-powered system for cardiovascular risk assessment with user-friendly data collection and visualization.

## 🎯 Project Overview

This system provides:

- **User-friendly data collection interface** with real-time validation
- **AI-powered disease detection** through multiple specialized agents
- **Comprehensive medical reports** with visualizations
- **Clinical recommendations** for healthcare providers

## 🏗️ Architecture

```
src/
├── ui/                     # User Interface Components
│   └── user_interface.py   # Flask-based web interface
├── data_processing/        # Data Processing & Algorithm Interface
│   ├── models.py          # Data models and structures
│   └── algorithm_interface.py  # Communication with AI algorithms
└── visualization/          # Report Generation & Visualization
    └── report_generator.py # Comprehensive medical reports

templates/                  # HTML templates
├── index.html             # Data collection form
└── results.html           # Analysis results display

app.py                     # Main application orchestrator
```

## 🚀 Key Features

### 1. User-Friendly Data Collection

- **Interactive form** with guidance tooltips
- **Real-time validation** with helpful feedback
- **Progressive completion** tracking
- **Medical context** explanations for each field

### 2. AI Disease Detection

The system interfaces with multiple AI agents analyzing:

- **Coronary Artery Disease** risk
- **Heart Attack** probability
- **Arrhythmia** risk assessment
- **General cardiovascular** health

### 3. Comprehensive Reporting

- **Visual risk assessment** with interactive charts
- **Clinical interpretation** of findings
- **Detailed recommendations** for follow-up care
- **Factor importance analysis** showing what drives the risk

### 4. Medical Visualizations

- Risk probability charts
- Factor importance heatmaps
- Patient profile radar charts
- Confidence vs risk analysis

## 📊 Data Pipeline

1. **Data Collection**: User fills out medical questionnaire
2. **Validation**: Real-time field validation and guidance
3. **Processing**: Data sent to AI algorithm agents
4. **Analysis**: Multiple disease-specific models analyze risk
5. **Reporting**: Comprehensive medical report generated
6. **Visualization**: Interactive charts and recommendations

## 🔧 Technical Implementation

### Core Components

**Data Models** (`models.py`):

- Structured patient data representation
- Enum-based categorical variables
- Validation and serialization methods

**User Interface** (`user_interface.py`):

- Flask-based web interface
- Real-time form validation
- Guidance system for medical terms

**Algorithm Interface** (`algorithm_interface.py`):

- Communication with AI detection agents
- Result parsing and structuring
- Error handling and fallback mechanisms

**Report Generator** (`report_generator.py`):

- Comprehensive medical reports
- Interactive visualizations with Plotly
- Clinical recommendations engine

### Integration Points

**For Algorithm Team**:

- Standardized data format (13 features matching UCI dataset)
- RESTful API endpoints for data exchange
- Structured result format specification

**API Endpoints**:

- `GET /api/patient_data/<patient_id>` - Retrieve patient data
- `POST /api/submit_results/<patient_id>` - Submit analysis results
- `GET /health` - System health check

## 📋 Required Patient Data

The system collects 13 key medical parameters:

1. **Demographics**: Age, Sex
2. **Cardiovascular**: Blood pressure, Heart rate, Cholesterol
3. **Clinical**: Chest pain type, ECG results, Exercise tolerance
4. **Specialized**: ST depression, Vessel analysis, Thalassemia test

## 🎨 User Experience

### Data Collection Flow

1. **Welcome screen** with system overview
2. **Guided form completion** with helpful tooltips
3. **Real-time validation** and progress tracking
4. **Confirmation** before analysis submission

### Results Visualization

1. **Executive summary** with overall risk score
2. **Detailed disease analysis** with confidence levels
3. **Interactive visualizations** for deeper insights
4. **Actionable recommendations** for healthcare providers

## 🔒 Privacy & Security

- **No data persistence** in current implementation
- **Session-based** data handling
- **Anonymized patient IDs** for tracking
- **HIPAA-ready** architecture for future compliance

## 🚀 Getting Started

### Prerequisites

```bash
pip install -r requirements.txt
```

### Running the System

```bash
python app.py
```

Access the system at: `http://localhost:5000`

### Integration with Algorithm Team

The system provides standardized interfaces:

**Data Format**:

```python
# 13-feature vector matching UCI heart disease dataset
[age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal]
```

**Expected Response Format**:

```json
{
  "disease_results": [
    {
      "disease_name": "Coronary Artery Disease",
      "probability": 0.75,
      "confidence": 0.85,
      "key_factors": ["High cholesterol", "Age factor"],
      "risk_level": "High"
    }
  ]
}
```

## 📈 Future Enhancements

1. **PDF Report Generation** for offline sharing
2. **Database Integration** for patient history tracking
3. **Advanced Visualizations** with machine learning explanations
4. **Mobile-Responsive Design** for tablet/phone access
5. **Multi-language Support** for international use
6. **Integration with EHR Systems** for seamless clinical workflow

## 🤝 Team Collaboration

This visualization and UI system is designed to integrate seamlessly with:

- **Algorithm Team**: Provides standardized data interface
- **Medical Team**: Offers clinically-relevant reporting
- **Product Team**: Delivers user-friendly experience

The modular architecture allows independent development while maintaining clear integration points.

## 📚 Medical Context

The system is based on the UCI Heart Disease dataset and follows established medical protocols for cardiovascular risk assessment. All recommendations should be validated with qualified healthcare providers before clinical use.

---

**Note**: This is a prototype system for the AI Career Competition. Production deployment would require additional security, compliance, and validation measures.
