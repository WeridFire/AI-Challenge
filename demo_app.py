"""
Minimal Flask app for demo - no complex dependencies
"""

from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import uuid
from datetime import datetime
import json

app = Flask(__name__, template_folder='templates')
app.secret_key = 'demo_secret_key'

# Simple patient data structure
class SimplePatientData:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/test')
def quick_test():
    return render_template('quick_test.html')

@app.route('/collect_data', methods=['POST'])
def collect_data():
    try:
        print("=== COLLECT DATA CALLED ===")
        print(f"Form data: {dict(request.form)}")
        
        # Generate unique patient ID
        patient_id = str(uuid.uuid4())
        session['patient_id'] = patient_id
        
        # Store form data directly (already primitive types)
        patient_data = dict(request.form)
        session['patient_data'] = patient_data
        
        print(f"Generated patient_id: {patient_id}")
        print("Data stored in session successfully")
        
        return jsonify({
            'status': 'success',
            'patient_id': patient_id,
            'message': 'Patient data collected successfully'
        })
        
    except Exception as e:
        print(f"ERROR in collect_data: {e}")
        return jsonify({
            'status': 'error',
            'message': f'Error collecting data: {str(e)}'
        }), 400

@app.route('/validate_field', methods=['POST'])
def validate_field():
    return jsonify({'valid': True, 'message': 'Valid input'})

@app.route('/get_guidance', methods=['GET'])
def get_guidance():
    field = request.args.get('field', '')
    return jsonify({
        'description': f'Guidance for {field}',
        'tips': ['Please enter a valid value'],
        'examples': ['Example value']
    })

@app.route('/analyze/<patient_id>')
def analyze_patient(patient_id):
    try:
        print(f"=== ANALYZE CALLED for patient_id: {patient_id} ===")
        
        # Get patient data from session
        patient_data = session.get('patient_data', {})
        print(f"Patient data from session: {patient_data}")
        
        if not patient_data:
            print("No patient data found, redirecting to index")
            return redirect(url_for('index'))
        
        # Create simple mock report
        report = create_mock_report(patient_data, patient_id)
        print("Report created successfully")
        
        return render_template('results.html', report=report)
        
    except Exception as e:
        print(f"ERROR in analyze_patient: {e}")
        import traceback
        traceback.print_exc()
        return f"<h1>Analysis Error</h1><p>{str(e)}</p><a href='/'>Try Again</a>", 500

def create_mock_report(patient_data, patient_id):
    """Create a simple mock report for demo"""
    age = int(patient_data.get('age', 50))
    sex = 'Male' if patient_data.get('sex') == '1' else 'Female'
    
    # Simple risk calculation
    risk_score = min(max((age - 30) * 1.5 + int(patient_data.get('cholesterol', 200)) / 10, 10), 90)
    
    return {
        'patient_summary': {
            'patient_id': patient_id,
            'analysis_date': datetime.now().strftime('%Y-%m-%d'),
            'demographics': {
                'age': age,
                'sex': sex,
                'overall_risk_score': f'{risk_score:.0f}%'
            },
            'key_measurements': {
                'resting_blood_pressure': f"{patient_data.get('resting_blood_pressure', 120)} mmHg",
                'cholesterol': f"{patient_data.get('cholesterol', 200)} mg/dl",
                'max_heart_rate': f"{patient_data.get('max_heart_rate', 150)} bpm",
                'chest_pain_type': 'Typical Angina'
            },
            'risk_indicators': {
                'exercise_induced_angina': 'No',
                'fasting_blood_sugar_elevated': 'No',
                'st_depression': '1.0',
                'major_vessels_affected': 0
            }
        },
        'risk_assessment': {
            'overall_risk_score': f'{risk_score:.0f}%',
            'primary_concerns': ['Cardiovascular Risk'] if risk_score > 50 else [],
            'disease_risks': [
                {
                    'disease': 'Coronary Artery Disease',
                    'probability': f'{risk_score:.0f}%',
                    'risk_level': 'High' if risk_score > 70 else 'Medium' if risk_score > 40 else 'Low',
                    'confidence': '85%'
                }
            ]
        },
        'visualizations': {
            'risk_probabilities': '<div class="alert alert-info">Interactive charts will be available with full dependencies installed.</div>',
            'risk_distribution': '<div class="alert alert-info">Visualization loading...</div>',
            'factor_importance': '<div class="alert alert-info">Chart coming soon...</div>',
            'patient_profile': '<div class="alert alert-info">Radar chart will load with plotly.</div>',
            'confidence_risk': '<div class="alert alert-info">Scatter plot available in full version.</div>'
        },
        'detailed_analysis': [
            {
                'disease_name': 'Coronary Artery Disease',
                'risk_assessment': {
                    'probability': f'{risk_score:.0f}%',
                    'risk_level': 'Medium',
                    'confidence': '85%'
                },
                'key_contributing_factors': [
                    f'Age factor ({age} years)',
                    f'Cholesterol level ({patient_data.get("cholesterol", 200)} mg/dl)'
                ],
                'factor_weights': {
                    'age': 0.3,
                    'cholesterol': 0.25,
                    'blood_pressure': 0.2
                },
                'clinical_interpretation': f'The patient shows moderate risk based on age and cardiovascular parameters.',
                'specific_recommendations': [
                    'Regular monitoring recommended',
                    'Lifestyle modifications beneficial',
                    'Follow up with healthcare provider'
                ]
            }
        ],
        'recommendations': {
            'immediate_actions': [
                'Schedule routine follow-up with healthcare provider',
                'Monitor blood pressure regularly'
            ],
            'follow_up_care': [
                'Annual cardiovascular screening',
                'Blood pressure monitoring',
                'Cholesterol level checks'
            ],
            'lifestyle_modifications': [
                'Heart-healthy diet (Mediterranean or DASH)',
                'Regular exercise (150 min/week)',
                'Stress management',
                'Maintain healthy weight'
            ],
            'specialist_referrals': [
                'Cardiology consultation if symptoms worsen'
            ],
            'monitoring_schedule': {
                'Blood Pressure': 'Monthly',
                'Cholesterol': 'Annually',
                'General Health': 'Annual exam'
            }
        },
        'medical_summary': f'''
CARDIOVASCULAR RISK ASSESSMENT SUMMARY

Patient: {patient_id}
Date: {datetime.now().strftime('%Y-%m-%d')}

OVERALL ASSESSMENT:
The {age}-year-old {sex.lower()} patient presents with an overall cardiovascular 
risk score of {risk_score:.0f}%.

CLINICAL PARAMETERS:
- Blood Pressure: {patient_data.get('resting_blood_pressure', 120)} mmHg
- Cholesterol: {patient_data.get('cholesterol', 200)} mg/dl
- Maximum Heart Rate: {patient_data.get('max_heart_rate', 150)} bpm

RECOMMENDATIONS:
Regular monitoring and lifestyle modifications recommended.

This analysis should be reviewed with a qualified healthcare provider.
        '''.strip()
    }

@app.route('/health')
def health_check():
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'mode': 'demo'
    })

if __name__ == '__main__':
    print("🚀 Demo Heart Disease Detection System")
    print("🌐 Running at: http://localhost:5000")
    print("📝 Simplified version - no complex dependencies needed")
    app.run(debug=True, port=5000)