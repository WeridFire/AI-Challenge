"""
User Interface Module for Heart Disease Detection System
Handles friendly data collection from users
"""

from flask import Flask, render_template, request, jsonify, session
import uuid
from datetime import datetime
from typing import Dict, Any, Optional

from ..data_processing.models import (
    PatientData, Gender, ChestPainType, RestingECG, 
    Slope, Thalassemia, FIELD_DESCRIPTIONS, NORMAL_RANGES
)


class UserInterface:
    """Handles user interaction and data collection"""
    
    def __init__(self, app: Flask):
        self.app = app
        self.setup_routes()
    
    def setup_routes(self):
        """Setup Flask routes for the UI"""
        
        @self.app.route('/')
        def index():
            """Main page with patient data collection form"""
            return render_template('index.html', 
                                 field_descriptions=FIELD_DESCRIPTIONS,
                                 normal_ranges=NORMAL_RANGES)
        
        @self.app.route('/collect_data', methods=['POST'])
        def collect_data():
            """Collect patient data from the form"""
            try:
                # Generate unique patient ID
                patient_id = str(uuid.uuid4())
                session['patient_id'] = patient_id
                
                # Parse form data
                patient_data = self._parse_form_data(request.form)
                
                # Store in session for later use (convert enums to values)
                session['patient_data'] = self._serialize_patient_data_for_session(patient_data)
                
                return jsonify({
                    'status': 'success',
                    'patient_id': patient_id,
                    'message': 'Patient data collected successfully',
                    'data': self._serialize_patient_data(patient_data)
                })
                
            except Exception as e:
                return jsonify({
                    'status': 'error',
                    'message': f'Error collecting data: {str(e)}'
                }), 400
        
        @self.app.route('/validate_field', methods=['POST'])
        def validate_field():
            """Validate individual form fields"""
            field_name = request.json.get('field_name')
            value = request.json.get('value')
            
            validation_result = self._validate_field(field_name, value)
            return jsonify(validation_result)
        
        @self.app.route('/get_guidance', methods=['GET'])
        def get_guidance():
            """Provide guidance for filling out the form"""
            field = request.args.get('field')
            guidance = self._get_field_guidance(field)
            return jsonify(guidance)
    
    def _parse_form_data(self, form_data: Dict[str, Any]) -> PatientData:
        """Parse form data into PatientData object"""
        
        # Convert string values to appropriate types
        age = int(form_data.get('age'))
        sex = Gender(int(form_data.get('sex')))
        chest_pain_type = ChestPainType(int(form_data.get('chest_pain_type')))
        resting_bp = int(form_data.get('resting_blood_pressure'))
        cholesterol = int(form_data.get('cholesterol'))
        fasting_bs = form_data.get('fasting_blood_sugar') == '1'
        resting_ecg = RestingECG(int(form_data.get('resting_ecg')))
        max_hr = int(form_data.get('max_heart_rate'))
        exercise_angina = form_data.get('exercise_induced_angina') == '1'
        st_depression = float(form_data.get('st_depression'))
        slope = Slope(int(form_data.get('slope_peak_exercise')))
        major_vessels = int(form_data.get('major_vessels'))
        thalassemia = Thalassemia(int(form_data.get('thalassemia')))
        
        return PatientData(
            age=age,
            sex=sex,
            chest_pain_type=chest_pain_type,
            resting_blood_pressure=resting_bp,
            cholesterol=cholesterol,
            fasting_blood_sugar=fasting_bs,
            resting_ecg=resting_ecg,
            max_heart_rate=max_hr,
            exercise_induced_angina=exercise_angina,
            st_depression=st_depression,
            slope_peak_exercise=slope,
            major_vessels=major_vessels,
            thalassemia=thalassemia
        )
    
    def _validate_field(self, field_name: str, value: Any) -> Dict[str, Any]:
        """Validate individual form field"""
        try:
            if field_name in NORMAL_RANGES:
                min_val, max_val = NORMAL_RANGES[field_name]
                numeric_value = float(value)
                
                if not (min_val <= numeric_value <= max_val):
                    return {
                        'valid': False,
                        'message': f'Value should be between {min_val} and {max_val}',
                        'severity': 'warning' if abs(numeric_value - min_val) < (max_val - min_val) * 0.2 or abs(numeric_value - max_val) < (max_val - min_val) * 0.2 else 'error'
                    }
            
            return {'valid': True, 'message': 'Valid input'}
            
        except ValueError:
            return {
                'valid': False,
                'message': 'Please enter a valid number',
                'severity': 'error'
            }
    
    def _get_field_guidance(self, field: str) -> Dict[str, Any]:
        """Get guidance information for a specific field"""
        guidance_info = {
            'age': {
                'description': FIELD_DESCRIPTIONS['age'],
                'tips': ['Enter age in complete years', 'Typical range: 29-77 years'],
                'examples': ['45', '62', '38']
            },
            'resting_blood_pressure': {
                'description': FIELD_DESCRIPTIONS['resting_blood_pressure'],
                'tips': ['Use systolic pressure (top number)', 'Normal: 90-120 mmHg', 'High: >140 mmHg'],
                'examples': ['120', '140', '160']
            },
            'cholesterol': {
                'description': FIELD_DESCRIPTIONS['cholesterol'],
                'tips': ['Total cholesterol level', 'Desirable: <200 mg/dl', 'High: >240 mg/dl'],
                'examples': ['180', '220', '280']
            },
            'max_heart_rate': {
                'description': FIELD_DESCRIPTIONS['max_heart_rate'],
                'tips': ['Maximum during stress test or exercise', 'Rough estimate: 220 - age'],
                'examples': ['150', '175', '190']
            },
            'st_depression': {
                'description': FIELD_DESCRIPTIONS['st_depression'],
                'tips': ['From exercise stress test', 'Normal: 0-1.0', 'Significant: >2.0'],
                'examples': ['0.0', '1.5', '3.2']
            }
        }
        
        return guidance_info.get(field, {
            'description': FIELD_DESCRIPTIONS.get(field, 'No description available'),
            'tips': ['Please consult with your healthcare provider'],
            'examples': []
        })
    
    def _serialize_patient_data(self, patient_data: PatientData) -> Dict[str, Any]:
        """Convert PatientData to serializable format"""
        return {
            'age': patient_data.age,
            'sex': patient_data.sex.name,
            'chest_pain_type': patient_data.chest_pain_type.name,
            'resting_blood_pressure': patient_data.resting_blood_pressure,
            'cholesterol': patient_data.cholesterol,
            'fasting_blood_sugar': patient_data.fasting_blood_sugar,
            'resting_ecg': patient_data.resting_ecg.name,
            'max_heart_rate': patient_data.max_heart_rate,
            'exercise_induced_angina': patient_data.exercise_induced_angina,
            'st_depression': patient_data.st_depression,
            'slope_peak_exercise': patient_data.slope_peak_exercise.name,
            'major_vessels': patient_data.major_vessels,
            'thalassemia': patient_data.thalassemia.name
        }
    
    def _serialize_patient_data_for_session(self, patient_data: PatientData) -> Dict[str, Any]:
        """Convert PatientData to session-safe format (with enum values)"""
        return {
            'age': patient_data.age,
            'sex': patient_data.sex.value,
            'chest_pain_type': patient_data.chest_pain_type.value,
            'resting_blood_pressure': patient_data.resting_blood_pressure,
            'cholesterol': patient_data.cholesterol,
            'fasting_blood_sugar': patient_data.fasting_blood_sugar,
            'resting_ecg': patient_data.resting_ecg.value,
            'max_heart_rate': patient_data.max_heart_rate,
            'exercise_induced_angina': patient_data.exercise_induced_angina,
            'st_depression': patient_data.st_depression,
            'slope_peak_exercise': patient_data.slope_peak_exercise.value,
            'major_vessels': patient_data.major_vessels,
            'thalassemia': patient_data.thalassemia.value
        }