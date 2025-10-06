"""
Algorithm Interface Module
Handles communication with the algorithm team's disease detection system
"""

import json
from typing import List, Dict, Any
from datetime import datetime

from ..data_processing.models import PatientData, DiseaseAnalysisResult, ComprehensiveAnalysisResult


class AlgorithmInterface:
    """Interface to communicate with the disease detection algorithm"""
    
    def __init__(self, algorithm_endpoint: str = None):
        # For now, we'll simulate the algorithm responses
        # In production, this would be the actual endpoint
        self.algorithm_endpoint = algorithm_endpoint or "http://localhost:8001/api/analyze"
        
        # Mock disease agents for demonstration
        self.disease_agents = [
            "coronary_artery_disease",
            "heart_attack_risk", 
            "arrhythmia_risk",
            "heart_failure_risk",
            "general_cardiovascular_risk"
        ]
    
    def send_patient_data(self, patient_data: PatientData, patient_id: str) -> ComprehensiveAnalysisResult:
        """Send patient data to the algorithm and get analysis results"""
        
        # Prepare data in the format expected by the algorithm team
        analysis_request = {
            "patient_id": patient_id,
            "timestamp": datetime.now().isoformat(),
            "features": patient_data.to_csv_row(),
            "feature_names": [
                "age", "sex", "cp", "trestbps", "chol", "fbs", 
                "restecg", "thalach", "exang", "oldpeak", 
                "slope", "ca", "thal"
            ]
        }
        
        try:
            # In production, this would be a real API call
            # response = requests.post(self.algorithm_endpoint, json=analysis_request)
            # results = response.json()
            
            # For now, simulate the algorithm response
            results = self._simulate_algorithm_response(analysis_request)
            
            # Parse results into our data structure
            return self._parse_algorithm_results(results, patient_data, patient_id)
            
        except Exception as e:
            # Handle algorithm service errors
            return self._create_error_result(patient_data, patient_id, str(e))
    
    def _simulate_algorithm_response(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Simulate the response from the algorithm team's system"""
        
        # Extract features for simulation
        features = request_data["features"]
        age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal = features
        
        # Simulate multiple disease detection agents
        simulated_results = []
        
        # Coronary Artery Disease Agent
        cad_risk = self._calculate_cad_risk(age, sex, cp, chol, thalach, ca, thal)
        simulated_results.append({
            "disease_name": "Coronary Artery Disease",
            "probability": cad_risk,
            "confidence": 0.85,
            "key_factors": self._get_cad_factors(age, sex, cp, chol, ca, thal),
            "factor_weights": {
                "age": 0.15,
                "chest_pain": 0.25,
                "cholesterol": 0.20,
                "major_vessels": 0.25,
                "thalassemia": 0.15
            },
            "risk_level": "High" if cad_risk > 0.7 else "Medium" if cad_risk > 0.4 else "Low"
        })
        
        # Heart Attack Risk Agent
        ha_risk = self._calculate_heart_attack_risk(age, sex, trestbps, chol, exang, oldpeak)
        simulated_results.append({
            "disease_name": "Heart Attack Risk",
            "probability": ha_risk,
            "confidence": 0.78,
            "key_factors": self._get_heart_attack_factors(age, sex, trestbps, chol, exang),
            "factor_weights": {
                "age": 0.20,
                "blood_pressure": 0.25,
                "cholesterol": 0.20,
                "exercise_angina": 0.25,
                "st_depression": 0.10
            },
            "risk_level": "High" if ha_risk > 0.6 else "Medium" if ha_risk > 0.3 else "Low"
        })
        
        # Arrhythmia Risk Agent
        arr_risk = self._calculate_arrhythmia_risk(age, restecg, thalach, exang)
        simulated_results.append({
            "disease_name": "Arrhythmia Risk",
            "probability": arr_risk,
            "confidence": 0.72,
            "key_factors": self._get_arrhythmia_factors(restecg, thalach, exang),
            "factor_weights": {
                "resting_ecg": 0.30,
                "max_heart_rate": 0.25,
                "exercise_angina": 0.25,
                "age": 0.20
            },
            "risk_level": "High" if arr_risk > 0.6 else "Medium" if arr_risk > 0.3 else "Low"
        })
        
        return {
            "patient_id": request_data["patient_id"],
            "timestamp": request_data["timestamp"],
            "disease_results": simulated_results,
            "overall_risk_score": max([r["probability"] for r in simulated_results]),
            "processing_time_ms": 1250
        }
    
    def _calculate_cad_risk(self, age, sex, cp, chol, thalach, ca, thal) -> float:
        """Simulate CAD risk calculation"""
        risk = 0.0
        
        # Age factor
        if age > 60:
            risk += 0.3
        elif age > 45:
            risk += 0.15
        
        # Sex factor (males higher risk)
        if sex == 1:
            risk += 0.1
        
        # Chest pain type
        if cp in [1, 2]:  # Typical or atypical angina
            risk += 0.25
        
        # Cholesterol
        if chol > 240:
            risk += 0.2
        elif chol > 200:
            risk += 0.1
        
        # Major vessels
        risk += ca * 0.15
        
        # Thalassemia
        if thal in [6, 7]:  # Fixed or reversible defect
            risk += 0.2
        
        # Max heart rate (lower = higher risk for older patients)
        expected_max_hr = 220 - age
        if thalach < expected_max_hr * 0.8:
            risk += 0.15
        
        return min(risk, 1.0)
    
    def _calculate_heart_attack_risk(self, age, sex, trestbps, chol, exang, oldpeak) -> float:
        """Simulate heart attack risk calculation"""
        risk = 0.0
        
        # Age and sex
        if age > 65:
            risk += 0.25
        if sex == 1 and age > 45:
            risk += 0.15
        elif sex == 0 and age > 55:
            risk += 0.15
        
        # Blood pressure
        if trestbps > 140:
            risk += 0.2
        elif trestbps > 130:
            risk += 0.1
        
        # Cholesterol
        if chol > 240:
            risk += 0.2
        
        # Exercise-induced angina
        if exang == 1:
            risk += 0.25
        
        # ST depression
        if oldpeak > 2.0:
            risk += 0.2
        elif oldpeak > 1.0:
            risk += 0.1
        
        return min(risk, 1.0)
    
    def _calculate_arrhythmia_risk(self, age, restecg, thalach, exang) -> float:
        """Simulate arrhythmia risk calculation"""
        risk = 0.0
        
        # Resting ECG abnormalities
        if restecg in [1, 2]:
            risk += 0.3
        
        # Age factor
        if age > 70:
            risk += 0.2
        
        # Abnormal heart rate response
        expected_max_hr = 220 - age
        if thalach > expected_max_hr * 0.95 or thalach < expected_max_hr * 0.6:
            risk += 0.2
        
        # Exercise-induced symptoms
        if exang == 1:
            risk += 0.15
        
        return min(risk, 1.0)
    
    def _get_cad_factors(self, age, sex, cp, chol, ca, thal) -> List[str]:
        """Get key factors for CAD risk"""
        factors = []
        if age > 60:
            factors.append(f"Advanced age ({age} years)")
        if cp in [1, 2]:
            factors.append("Chest pain pattern consistent with angina")
        if chol > 240:
            factors.append(f"High cholesterol ({chol} mg/dl)")
        if ca > 0:
            factors.append(f"Blocked major vessels ({ca})")
        if thal in [6, 7]:
            factors.append("Abnormal thalassemia test")
        return factors
    
    def _get_heart_attack_factors(self, age, sex, trestbps, chol, exang) -> List[str]:
        """Get key factors for heart attack risk"""
        factors = []
        if age > 65:
            factors.append(f"Advanced age ({age} years)")
        if trestbps > 140:
            factors.append(f"High blood pressure ({trestbps} mmHg)")
        if chol > 240:
            factors.append(f"High cholesterol ({chol} mg/dl)")
        if exang == 1:
            factors.append("Exercise-induced chest pain")
        return factors
    
    def _get_arrhythmia_factors(self, restecg, thalach, exang) -> List[str]:
        """Get key factors for arrhythmia risk"""
        factors = []
        if restecg in [1, 2]:
            factors.append("Abnormal resting ECG")
        if thalach < 100:
            factors.append(f"Low maximum heart rate ({thalach} bpm)")
        if exang == 1:
            factors.append("Exercise-induced symptoms")
        return factors
    
    def _parse_algorithm_results(self, results: Dict[str, Any], 
                               patient_data: PatientData, patient_id: str) -> ComprehensiveAnalysisResult:
        """Parse algorithm results into our data structure"""
        
        disease_results = []
        for disease_result in results["disease_results"]:
            # Generate recommendations based on risk level
            recommendations = self._generate_recommendations(disease_result)
            
            disease_analysis = DiseaseAnalysisResult(
                disease_name=disease_result["disease_name"],
                probability=disease_result["probability"],
                confidence=disease_result["confidence"],
                key_factors=disease_result["key_factors"],
                factor_weights=disease_result["factor_weights"],
                risk_level=disease_result["risk_level"],
                recommendations=recommendations
            )
            disease_results.append(disease_analysis)
        
        # Generate overall recommendations
        overall_recommendations = self._generate_overall_recommendations(disease_results)
        primary_concerns = [d.disease_name for d in disease_results if d.risk_level in ["High", "Medium"]]
        
        return ComprehensiveAnalysisResult(
            patient_id=patient_id,
            timestamp=results["timestamp"],
            patient_data=patient_data,
            disease_results=disease_results,
            overall_risk_score=results["overall_risk_score"],
            primary_concerns=primary_concerns,
            recommended_actions=overall_recommendations
        )
    
    def _generate_recommendations(self, disease_result: Dict[str, Any]) -> List[str]:
        """Generate medical recommendations based on disease analysis"""
        recommendations = []
        risk_level = disease_result["risk_level"]
        disease_name = disease_result["disease_name"]
        
        if "Coronary" in disease_name:
            if risk_level == "High":
                recommendations.extend([
                    "Immediate consultation with a cardiologist",
                    "Consider cardiac catheterization",
                    "Start aggressive cholesterol management",
                    "Lifestyle modifications: diet and exercise"
                ])
            elif risk_level == "Medium":
                recommendations.extend([
                    "Follow-up with primary care physician",
                    "Stress testing recommended",
                    "Monitor cholesterol levels",
                    "Adopt heart-healthy lifestyle"
                ])
        
        elif "Heart Attack" in disease_name:
            if risk_level == "High":
                recommendations.extend([
                    "Urgent cardiology evaluation",
                    "Blood pressure management",
                    "Consider preventive medications",
                    "Emergency action plan discussion"
                ])
            elif risk_level == "Medium":
                recommendations.extend([
                    "Regular monitoring",
                    "Blood pressure control",
                    "Lifestyle counseling"
                ])
        
        elif "Arrhythmia" in disease_name:
            if risk_level == "High":
                recommendations.extend([
                    "Electrophysiology consultation",
                    "Holter monitor study",
                    "Medication review"
                ])
        
        return recommendations
    
    def _generate_overall_recommendations(self, disease_results: List[DiseaseAnalysisResult]) -> List[str]:
        """Generate overall recommendations based on all disease analyses"""
        recommendations = set()
        
        high_risk_count = sum(1 for d in disease_results if d.risk_level == "High")
        medium_risk_count = sum(1 for d in disease_results if d.risk_level == "Medium")
        
        if high_risk_count > 0:
            recommendations.add("Schedule immediate medical consultation")
            recommendations.add("Consider comprehensive cardiac evaluation")
        
        if medium_risk_count > 0 or high_risk_count > 0:
            recommendations.add("Implement heart-healthy lifestyle changes")
            recommendations.add("Regular monitoring and follow-up")
        
        recommendations.add("Discuss results with healthcare provider")
        recommendations.add("Keep detailed health records")
        
        return list(recommendations)
    
    def _create_error_result(self, patient_data: PatientData, 
                           patient_id: str, error_message: str) -> ComprehensiveAnalysisResult:
        """Create an error result when algorithm fails"""
        error_result = DiseaseAnalysisResult(
            disease_name="Analysis Error",
            probability=0.0,
            confidence=0.0,
            key_factors=[f"Error: {error_message}"],
            factor_weights={},
            risk_level="Unknown",
            recommendations=["Please try again later", "Consult with healthcare provider"]
        )
        
        return ComprehensiveAnalysisResult(
            patient_id=patient_id,
            timestamp=datetime.now().isoformat(),
            patient_data=patient_data,
            disease_results=[error_result],
            overall_risk_score=0.0,
            primary_concerns=["System Error"],
            recommended_actions=["Contact technical support", "Retry analysis"]
        )