"""
Heart Disease Detection System - Data Models
Defines the structure for patient data and analysis results
"""

from dataclasses import dataclass
from typing import Dict, List, Optional, Any
from enum import Enum


class Gender(Enum):
    MALE = 1
    FEMALE = 0


class ChestPainType(Enum):
    TYPICAL_ANGINA = 1
    ATYPICAL_ANGINA = 2
    NON_ANGINAL_PAIN = 3
    ASYMPTOMATIC = 4


class RestingECG(Enum):
    NORMAL = 0
    ST_T_ABNORMALITY = 1
    LEFT_VENTRICULAR_HYPERTROPHY = 2


class Slope(Enum):
    UPSLOPING = 1
    FLAT = 2
    DOWNSLOPING = 3


class Thalassemia(Enum):
    NORMAL = 3
    FIXED_DEFECT = 6
    REVERSIBLE_DEFECT = 7


@dataclass
class PatientData:
    """Represents patient input data for heart disease analysis"""
    age: int
    sex: Gender
    chest_pain_type: ChestPainType
    resting_blood_pressure: int  # mm Hg
    cholesterol: int  # mg/dl
    fasting_blood_sugar: bool  # > 120 mg/dl
    resting_ecg: RestingECG
    max_heart_rate: int
    exercise_induced_angina: bool
    st_depression: float  # oldpeak
    slope_peak_exercise: Slope
    major_vessels: int  # 0-3
    thalassemia: Thalassemia
    
    def to_csv_row(self) -> List[float]:
        """Convert to the format expected by the algorithm team"""
        return [
            float(self.age),
            float(self.sex.value),
            float(self.chest_pain_type.value),
            float(self.resting_blood_pressure),
            float(self.cholesterol),
            float(1 if self.fasting_blood_sugar else 0),
            float(self.resting_ecg.value),
            float(self.max_heart_rate),
            float(1 if self.exercise_induced_angina else 0),
            float(self.st_depression),
            float(self.slope_peak_exercise.value),
            float(self.major_vessels),
            float(self.thalassemia.value)
        ]


@dataclass
class DiseaseAnalysisResult:
    """Result from a single disease detection agent"""
    disease_name: str
    probability: float  # 0.0 to 1.0
    confidence: float  # 0.0 to 1.0
    key_factors: List[str]  # Features that contributed most to the decision
    factor_weights: Dict[str, float]  # Weight of each contributing factor
    risk_level: str  # "Low", "Medium", "High"
    recommendations: List[str]  # Medical recommendations


@dataclass
class ComprehensiveAnalysisResult:
    """Complete analysis result from all disease detection agents"""
    patient_id: str
    timestamp: str
    patient_data: PatientData
    disease_results: List[DiseaseAnalysisResult]
    overall_risk_score: float
    primary_concerns: List[str]
    recommended_actions: List[str]
    
    def get_highest_risk_disease(self) -> Optional[DiseaseAnalysisResult]:
        """Get the disease with highest probability"""
        if not self.disease_results:
            return None
        return max(self.disease_results, key=lambda x: x.probability)


# Field descriptions for user-friendly interface
FIELD_DESCRIPTIONS = {
    "age": "Patient's age in years",
    "sex": "Biological sex",
    "chest_pain_type": "Type of chest pain experienced",
    "resting_blood_pressure": "Blood pressure at rest (normal: 120/80 mmHg)",
    "cholesterol": "Serum cholesterol level (normal: < 200 mg/dl)",
    "fasting_blood_sugar": "Blood sugar after fasting > 120 mg/dl",
    "resting_ecg": "Electrocardiogram results at rest",
    "max_heart_rate": "Maximum heart rate achieved during exercise",
    "exercise_induced_angina": "Chest pain during physical activity",
    "st_depression": "ST depression induced by exercise (0-6.2)",
    "slope_peak_exercise": "Slope of peak exercise ST segment",
    "major_vessels": "Number of major vessels colored by fluoroscopy (0-3)",
    "thalassemia": "Blood disorder affecting hemoglobin"
}

# Normal ranges for guidance
NORMAL_RANGES = {
    "age": (1, 120),
    "resting_blood_pressure": (90, 180),
    "cholesterol": (100, 400),
    "max_heart_rate": (60, 220),
    "st_depression": (0, 6.2),
    "major_vessels": (0, 3)
}