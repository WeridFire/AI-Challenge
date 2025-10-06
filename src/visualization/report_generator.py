"""
Visualization Module for Heart Disease Detection System
Generates comprehensive reports and visualizations
"""

import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from typing import List, Dict, Any

from ..data_processing.models import ComprehensiveAnalysisResult, DiseaseAnalysisResult, PatientData


class ReportGenerator:
    """Generates comprehensive medical reports and visualizations"""
    
    def __init__(self):
        self.setup_style()
    
    def setup_style(self):
        """Setup visualization styles"""
        try:
            plt.style.use('seaborn-v0_8')
            sns.set_palette("husl")
        except:
            # Fallback if seaborn style is not available
            plt.style.use('default')
        
        # Custom color schemes for risk levels
        self.risk_colors = {
            'Low': '#2E8B57',      # Sea Green
            'Medium': '#FF8C00',   # Dark Orange  
            'High': '#DC143C'      # Crimson
        }
    
    def generate_comprehensive_report(self, analysis_result: ComprehensiveAnalysisResult) -> Dict[str, Any]:
        """Generate a comprehensive medical report with visualizations"""
        
        report = {
            'patient_summary': self._generate_patient_summary(analysis_result),
            'risk_assessment': self._generate_risk_assessment(analysis_result),
            'visualizations': self._generate_visualizations(analysis_result),
            'detailed_analysis': self._generate_detailed_analysis(analysis_result),
            'recommendations': self._generate_recommendations_report(analysis_result),
            'medical_summary': self._generate_medical_summary(analysis_result)
        }
        
        return report
    
    def _generate_patient_summary(self, analysis_result: ComprehensiveAnalysisResult) -> Dict[str, Any]:
        """Generate patient demographic and input summary"""
        patient = analysis_result.patient_data
        
        return {
            'patient_id': analysis_result.patient_id,
            'analysis_date': analysis_result.timestamp,
            'demographics': {
                'age': patient.age,
                'sex': patient.sex.name,
                'overall_risk_score': f"{analysis_result.overall_risk_score:.1%}"
            },
            'key_measurements': {
                'resting_blood_pressure': f"{patient.resting_blood_pressure} mmHg",
                'cholesterol': f"{patient.cholesterol} mg/dl",
                'max_heart_rate': f"{patient.max_heart_rate} bpm",
                'chest_pain_type': patient.chest_pain_type.name.replace('_', ' ').title()
            },
            'risk_indicators': {
                'exercise_induced_angina': "Yes" if patient.exercise_induced_angina else "No",
                'fasting_blood_sugar_elevated': "Yes" if patient.fasting_blood_sugar else "No",
                'st_depression': f"{patient.st_depression:.1f}",
                'major_vessels_affected': patient.major_vessels
            }
        }
    
    def _generate_risk_assessment(self, analysis_result: ComprehensiveAnalysisResult) -> Dict[str, Any]:
        """Generate overall risk assessment"""
        disease_risks = []
        
        for disease in analysis_result.disease_results:
            disease_risks.append({
                'disease': disease.disease_name,
                'probability': f"{disease.probability:.1%}",
                'risk_level': disease.risk_level,
                'confidence': f"{disease.confidence:.1%}"
            })
        
        # Sort by probability
        disease_risks.sort(key=lambda x: float(x['probability'].strip('%')), reverse=True)
        
        return {
            'overall_risk_score': f"{analysis_result.overall_risk_score:.1%}",
            'primary_concerns': analysis_result.primary_concerns,
            'disease_risks': disease_risks,
            'risk_distribution': self._calculate_risk_distribution(analysis_result.disease_results)
        }
    
    def _generate_visualizations(self, analysis_result: ComprehensiveAnalysisResult) -> Dict[str, str]:
        """Generate all visualizations for the report"""
        visualizations = {}
        
        try:
            # Risk probability chart
            visualizations['risk_probabilities'] = self._create_risk_probability_chart(analysis_result.disease_results)
        except Exception as e:
            print(f"Warning: Could not generate risk probability chart: {e}")
            visualizations['risk_probabilities'] = "<div>Chart unavailable</div>"
        
        try:
            # Risk level distribution
            visualizations['risk_distribution'] = self._create_risk_distribution_chart(analysis_result.disease_results)
        except Exception as e:
            print(f"Warning: Could not generate risk distribution chart: {e}")
            visualizations['risk_distribution'] = "<div>Chart unavailable</div>"
        
        try:
            # Factor importance heatmap
            visualizations['factor_importance'] = self._create_factor_importance_heatmap(analysis_result.disease_results)
        except Exception as e:
            print(f"Warning: Could not generate factor importance heatmap: {e}")
            visualizations['factor_importance'] = "<div>Chart unavailable</div>"
        
        try:
            # Patient profile radar chart
            visualizations['patient_profile'] = self._create_patient_profile_radar(analysis_result.patient_data)
        except Exception as e:
            print(f"Warning: Could not generate patient profile radar: {e}")
            visualizations['patient_profile'] = "<div>Chart unavailable</div>"
        
        try:
            # Confidence vs Risk scatter plot
            visualizations['confidence_risk'] = self._create_confidence_risk_scatter(analysis_result.disease_results)
        except Exception as e:
            print(f"Warning: Could not generate confidence risk scatter: {e}")
            visualizations['confidence_risk'] = "<div>Chart unavailable</div>"
        
        return visualizations
    
    def _create_risk_probability_chart(self, disease_results: List[DiseaseAnalysisResult]) -> str:
        """Create risk probability bar chart"""
        diseases = [d.disease_name for d in disease_results]
        probabilities = [d.probability * 100 for d in disease_results]
        colors = [self.risk_colors[d.risk_level] for d in disease_results]
        
        fig = go.Figure(data=[
            go.Bar(
                x=diseases,
                y=probabilities,
                marker_color=colors,
                text=[f'{p:.1f}%' for p in probabilities],
                textposition='auto',
            )
        ])
        
        fig.update_layout(
            title='Disease Risk Probabilities',
            xaxis_title='Disease Type',
            yaxis_title='Risk Probability (%)',
            template='plotly_white',
            height=400
        )
        
        return fig.to_html(full_html=False, include_plotlyjs='cdn')
    
    def _create_risk_distribution_chart(self, disease_results: List[DiseaseAnalysisResult]) -> str:
        """Create risk level distribution pie chart"""
        risk_counts = {'Low': 0, 'Medium': 0, 'High': 0}
        for disease in disease_results:
            risk_counts[disease.risk_level] += 1
        
        labels = list(risk_counts.keys())
        values = list(risk_counts.values())
        colors = [self.risk_colors[label] for label in labels]
        
        fig = go.Figure(data=[
            go.Pie(
                labels=labels,
                values=values,
                marker_colors=colors,
                textinfo='label+percent',
                hole=0.3
            )
        ])
        
        fig.update_layout(
            title='Risk Level Distribution',
            template='plotly_white',
            height=400
        )
        
        return fig.to_html(full_html=False, include_plotlyjs='cdn')
    
    def _create_factor_importance_heatmap(self, disease_results: List[DiseaseAnalysisResult]) -> str:
        """Create factor importance heatmap"""
        # Collect all unique factors
        all_factors = set()
        for disease in disease_results:
            all_factors.update(disease.factor_weights.keys())
        
        # Create matrix
        diseases = [d.disease_name for d in disease_results]
        factors = list(all_factors)
        
        z_data = []
        for disease in disease_results:
            row = []
            for factor in factors:
                weight = disease.factor_weights.get(factor, 0)
                row.append(weight)
            z_data.append(row)
        
        fig = go.Figure(data=go.Heatmap(
            z=z_data,
            x=factors,
            y=diseases,
            colorscale='RdYlBu_r',
            text=[[f'{val:.2f}' for val in row] for row in z_data],
            texttemplate="%{text}",
            textfont={"size": 10},
        ))
        
        fig.update_layout(
            title='Factor Importance by Disease Type',
            template='plotly_white',
            height=400
        )
        
        return fig.to_html(full_html=False, include_plotlyjs='cdn')
    
    def _create_patient_profile_radar(self, patient_data: PatientData) -> str:
        """Create patient profile radar chart"""
        # Normalize patient values for radar chart
        categories = [
            'Age Risk',
            'Blood Pressure Risk', 
            'Cholesterol Risk',
            'Heart Rate Risk',
            'Exercise Tolerance',
            'ECG Risk'
        ]
        
        values = [
            min(patient_data.age / 100, 1.0),  # Age risk
            min(patient_data.resting_blood_pressure / 200, 1.0),  # BP risk
            min(patient_data.cholesterol / 400, 1.0),  # Cholesterol risk
            1.0 - min(patient_data.max_heart_rate / 220, 1.0),  # Heart rate risk (inverted)
            1.0 if patient_data.exercise_induced_angina else 0.2,  # Exercise tolerance
            patient_data.resting_ecg.value / 2  # ECG risk
        ]
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=categories,
            fill='toself',
            name='Patient Profile',
            line_color='rgb(1,90,190)'
        ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 1]
                )),
            showlegend=True,
            title="Patient Risk Profile",
            template='plotly_white',
            height=400
        )
        
        return fig.to_html(full_html=False, include_plotlyjs='cdn')
    
    def _create_confidence_risk_scatter(self, disease_results: List[DiseaseAnalysisResult]) -> str:
        """Create confidence vs risk scatter plot"""
        diseases = [d.disease_name for d in disease_results]
        confidences = [d.confidence * 100 for d in disease_results]
        risks = [d.probability * 100 for d in disease_results]
        colors = [self.risk_colors[d.risk_level] for d in disease_results]
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=confidences,
            y=risks,
            mode='markers+text',
            marker=dict(
                size=12,
                color=colors,
                line=dict(width=2, color='DarkSlateGrey')
            ),
            text=diseases,
            textposition='top center',
            name='Disease Analysis'
        ))
        
        fig.update_layout(
            title='Model Confidence vs Risk Probability',
            xaxis_title='Confidence (%)',
            yaxis_title='Risk Probability (%)',
            template='plotly_white',
            height=400
        )
        
        return fig.to_html(full_html=False, include_plotlyjs='cdn')
    
    def _generate_detailed_analysis(self, analysis_result: ComprehensiveAnalysisResult) -> List[Dict[str, Any]]:
        """Generate detailed analysis for each disease"""
        detailed_analyses = []
        
        for disease in analysis_result.disease_results:
            analysis = {
                'disease_name': disease.disease_name,
                'risk_assessment': {
                    'probability': f"{disease.probability:.1%}",
                    'risk_level': disease.risk_level,
                    'confidence': f"{disease.confidence:.1%}"
                },
                'key_contributing_factors': disease.key_factors,
                'factor_weights': disease.factor_weights,
                'clinical_interpretation': self._generate_clinical_interpretation(disease),
                'specific_recommendations': disease.recommendations
            }
            detailed_analyses.append(analysis)
        
        return detailed_analyses
    
    def _generate_clinical_interpretation(self, disease: DiseaseAnalysisResult) -> str:
        """Generate clinical interpretation for each disease"""
        interpretations = {
            'Coronary Artery Disease': f"""
            The analysis indicates a {disease.risk_level.lower()} risk for coronary artery disease with 
            {disease.probability:.1%} probability. Key risk factors include {', '.join(disease.key_factors[:3])}.
            This assessment is based on established cardiovascular risk factors and should be interpreted 
            in conjunction with clinical examination.
            """,
            'Heart Attack Risk': f"""
            The patient shows {disease.risk_level.lower()} risk for acute cardiac events with 
            {disease.probability:.1%} probability. Primary risk drivers are {', '.join(disease.key_factors[:2])}.
            Immediate attention may be required if risk is high.
            """,
            'Arrhythmia Risk': f"""
            Analysis suggests {disease.risk_level.lower()} risk for cardiac rhythm disorders with 
            {disease.probability:.1%} probability. Contributing factors include {', '.join(disease.key_factors[:2])}.
            ECG monitoring may be recommended for further evaluation.
            """
        }
        
        return interpretations.get(disease.disease_name, f"""
        {disease.disease_name} shows {disease.risk_level.lower()} risk level with 
        {disease.probability:.1%} probability based on the provided clinical parameters.
        """).strip()
    
    def _generate_recommendations_report(self, analysis_result: ComprehensiveAnalysisResult) -> Dict[str, Any]:
        """Generate comprehensive recommendations report"""
        return {
            'immediate_actions': self._get_immediate_actions(analysis_result),
            'follow_up_care': self._get_follow_up_care(analysis_result),
            'lifestyle_modifications': self._get_lifestyle_modifications(analysis_result),
            'monitoring_schedule': self._get_monitoring_schedule(analysis_result),
            'specialist_referrals': self._get_specialist_referrals(analysis_result)
        }
    
    def _get_immediate_actions(self, analysis_result: ComprehensiveAnalysisResult) -> List[str]:
        """Get immediate action recommendations"""
        actions = []
        high_risk_diseases = [d for d in analysis_result.disease_results if d.risk_level == "High"]
        
        if high_risk_diseases:
            actions.extend([
                "Schedule urgent consultation with healthcare provider",
                "Discuss findings with primary care physician within 48 hours",
                "Consider emergency care if experiencing chest pain or shortness of breath"
            ])
        else:
            actions.extend([
                "Schedule routine follow-up with healthcare provider",
                "Discuss results during next planned medical visit"
            ])
        
        return actions
    
    def _get_follow_up_care(self, analysis_result: ComprehensiveAnalysisResult) -> List[str]:
        """Get follow-up care recommendations"""
        return [
            "Regular cardiovascular risk assessment",
            "Periodic blood pressure monitoring",
            "Annual cholesterol screening",
            "ECG monitoring as recommended by physician",
            "Stress testing if indicated by clinical evaluation"
        ]
    
    def _get_lifestyle_modifications(self, analysis_result: ComprehensiveAnalysisResult) -> List[str]:
        """Get lifestyle modification recommendations"""
        patient = analysis_result.patient_data
        modifications = [
            "Adopt heart-healthy diet (Mediterranean or DASH diet)",
            "Regular aerobic exercise (150 minutes/week moderate intensity)",
            "Maintain healthy weight (BMI 18.5-24.9)",
            "Stress management and adequate sleep",
            "Smoking cessation if applicable"
        ]
        
        if patient.cholesterol > 240:
            modifications.append("Focus on cholesterol-lowering diet and exercise")
        
        if patient.resting_blood_pressure > 140:
            modifications.append("Implement blood pressure management strategies")
        
        return modifications
    
    def _get_monitoring_schedule(self, analysis_result: ComprehensiveAnalysisResult) -> Dict[str, str]:
        """Get recommended monitoring schedule"""
        high_risk_count = sum(1 for d in analysis_result.disease_results if d.risk_level == "High")
        
        if high_risk_count > 0:
            return {
                "Blood Pressure": "Weekly self-monitoring, monthly clinical check",
                "Cholesterol": "Every 3 months",
                "ECG": "Every 6 months or as clinically indicated",
                "Exercise Tolerance": "Monitor during regular activity",
                "Symptoms": "Daily awareness, immediate reporting of changes"
            }
        else:
            return {
                "Blood Pressure": "Monthly self-monitoring",
                "Cholesterol": "Annually",
                "ECG": "As clinically indicated",
                "General Health": "Annual comprehensive exam"
            }
    
    def _get_specialist_referrals(self, analysis_result: ComprehensiveAnalysisResult) -> List[str]:
        """Get specialist referral recommendations"""
        referrals = []
        
        for disease in analysis_result.disease_results:
            if disease.risk_level == "High":
                if "Coronary" in disease.disease_name:
                    referrals.append("Cardiology consultation for CAD evaluation")
                elif "Heart Attack" in disease.disease_name:
                    referrals.append("Urgent cardiology evaluation")
                elif "Arrhythmia" in disease.disease_name:
                    referrals.append("Electrophysiology consultation")
        
        if not referrals:
            referrals.append("Routine cardiology screening if indicated by primary care")
        
        return list(set(referrals))  # Remove duplicates
    
    def _generate_medical_summary(self, analysis_result: ComprehensiveAnalysisResult) -> str:
        """Generate executive medical summary"""
        patient = analysis_result.patient_data
        highest_risk = analysis_result.get_highest_risk_disease()
        
        summary = f"""
        CARDIOVASCULAR RISK ASSESSMENT SUMMARY
        
        Patient: {analysis_result.patient_id}
        Date: {analysis_result.timestamp.split('T')[0]}
        
        OVERALL ASSESSMENT:
        The {patient.age}-year-old {patient.sex.name.lower()} patient presents with an overall cardiovascular 
        risk score of {analysis_result.overall_risk_score:.1%}. 
        
        PRIMARY FINDINGS:
        """
        
        if highest_risk:
            summary += f"""
        The highest concern is {highest_risk.disease_name} with {highest_risk.probability:.1%} probability 
        and {highest_risk.risk_level.lower()} risk level. Key contributing factors include: 
        {', '.join(highest_risk.key_factors[:3])}.
        """
        
        summary += f"""
        
        CLINICAL PARAMETERS:
        - Blood Pressure: {patient.resting_blood_pressure} mmHg
        - Cholesterol: {patient.cholesterol} mg/dl  
        - Maximum Heart Rate: {patient.max_heart_rate} bpm
        - Exercise Tolerance: {'Reduced' if patient.exercise_induced_angina else 'Normal'}
        
        RECOMMENDATIONS:
        {' '.join(analysis_result.recommended_actions[:2])}
        
        This analysis should be reviewed with a qualified healthcare provider for clinical correlation 
        and treatment planning.
        """
        
        return summary.strip()
    
    def _calculate_risk_distribution(self, disease_results: List[DiseaseAnalysisResult]) -> Dict[str, int]:
        """Calculate distribution of risk levels"""
        distribution = {'Low': 0, 'Medium': 0, 'High': 0}
        for disease in disease_results:
            distribution[disease.risk_level] += 1
        return distribution