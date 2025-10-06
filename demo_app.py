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
            'risk_probabilities': '''
            <div style="background: white; padding: 20px; border-radius: 10px;">
                <h5>Disease Risk Probabilities</h5>
                <div style="margin: 10px 0;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin: 8px 0;">
                        <span>Coronary Artery Disease</span>
                        <div style="flex: 1; margin: 0 10px; background: #e9ecef; height: 25px; border-radius: 12px; overflow: hidden;">
                            <div style="width: 65%; height: 100%; background: #dc3545; display: flex; align-items: center; justify-content: center; color: white; font-weight: bold;">65%</div>
                        </div>
                    </div>
                    <div style="display: flex; justify-content: space-between; align-items: center; margin: 8px 0;">
                        <span>Heart Attack Risk</span>
                        <div style="flex: 1; margin: 0 10px; background: #e9ecef; height: 25px; border-radius: 12px; overflow: hidden;">
                            <div style="width: 45%; height: 100%; background: #fd7e14; display: flex; align-items: center; justify-content: center; color: white; font-weight: bold;">45%</div>
                        </div>
                    </div>
                    <div style="display: flex; justify-content: space-between; align-items: center; margin: 8px 0;">
                        <span>Arrhythmia Risk</span>
                        <div style="flex: 1; margin: 0 10px; background: #e9ecef; height: 25px; border-radius: 12px; overflow: hidden;">
                            <div style="width: 25%; height: 100%; background: #198754; display: flex; align-items: center; justify-content: center; color: white; font-weight: bold;">25%</div>
                        </div>
                    </div>
                </div>
            </div>
            ''',
            'risk_distribution': '''
            <div style="background: white; padding: 20px; border-radius: 10px;">
                <h5>Risk Level Distribution</h5>
                <div style="display: flex; justify-content: center; align-items: center; height: 200px;">
                    <div style="position: relative; width: 150px; height: 150px;">
                        <svg width="150" height="150" style="transform: rotate(-90deg);">
                            <circle cx="75" cy="75" r="60" fill="none" stroke="#e9ecef" stroke-width="20"/>
                            <circle cx="75" cy="75" r="60" fill="none" stroke="#dc3545" stroke-width="20" 
                                    stroke-dasharray="113" stroke-dashoffset="34" opacity="0.8"/>
                            <circle cx="75" cy="75" r="60" fill="none" stroke="#fd7e14" stroke-width="20" 
                                    stroke-dasharray="75" stroke-dashoffset="109" opacity="0.8"/>
                            <circle cx="75" cy="75" r="60" fill="none" stroke="#198754" stroke-width="20" 
                                    stroke-dasharray="38" stroke-dashoffset="184" opacity="0.8"/>
                        </svg>
                        <div style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); text-align: center;">
                            <div style="font-size: 24px; font-weight: bold;">3</div>
                            <div style="font-size: 12px;">Risks</div>
                        </div>
                    </div>
                </div>
                <div style="text-align: center; margin-top: 10px;">
                    <span style="color: #dc3545;">●</span> High (1) &nbsp;
                    <span style="color: #fd7e14;">●</span> Medium (1) &nbsp;
                    <span style="color: #198754;">●</span> Low (1)
                </div>
            </div>
            ''',
            'factor_importance': '''
            <div style="background: white; padding: 20px; border-radius: 10px;">
                <h5>Factor Importance Heatmap</h5>
                <table style="width: 100%; border-collapse: collapse;">
                    <tr>
                        <th style="padding: 8px; text-align: left;"></th>
                        <th style="padding: 8px; text-align: center; font-size: 12px;">Age</th>
                        <th style="padding: 8px; text-align: center; font-size: 12px;">Cholesterol</th>
                        <th style="padding: 8px; text-align: center; font-size: 12px;">Blood Pressure</th>
                        <th style="padding: 8px; text-align: center; font-size: 12px;">Chest Pain</th>
                    </tr>
                    <tr>
                        <td style="padding: 8px; font-size: 12px;">CAD</td>
                        <td style="padding: 8px; background: #ff6b6b; text-align: center; color: white;">0.30</td>
                        <td style="padding: 8px; background: #ff8e53; text-align: center; color: white;">0.25</td>
                        <td style="padding: 8px; background: #4ecdc4; text-align: center; color: white;">0.20</td>
                        <td style="padding: 8px; background: #ff6b6b; text-align: center; color: white;">0.25</td>
                    </tr>
                    <tr>
                        <td style="padding: 8px; font-size: 12px;">Heart Attack</td>
                        <td style="padding: 8px; background: #ff8e53; text-align: center; color: white;">0.25</td>
                        <td style="padding: 8px; background: #ff6b6b; text-align: center; color: white;">0.30</td>
                        <td style="padding: 8px; background: #ff6b6b; text-align: center; color: white;">0.30</td>
                        <td style="padding: 8px; background: #95e1d3; text-align: center;">0.15</td>
                    </tr>
                    <tr>
                        <td style="padding: 8px; font-size: 12px;">Arrhythmia</td>
                        <td style="padding: 8px; background: #95e1d3; text-align: center;">0.15</td>
                        <td style="padding: 8px; background: #95e1d3; text-align: center;">0.10</td>
                        <td style="padding: 8px; background: #95e1d3; text-align: center;">0.15</td>
                        <td style="padding: 8px; background: #4ecdc4; text-align: center; color: white;">0.20</td>
                    </tr>
                </table>
            </div>
            ''',
            'patient_profile': '''
            <div style="background: white; padding: 20px; border-radius: 10px;">
                <h5>Patient Risk Profile</h5>
                <div style="display: flex; justify-content: center; align-items: center; height: 200px;">
                    <svg width="200" height="200">
                        <defs>
                            <polygon id="pentagon" points="100,20 180,70 145,150 55,150 20,70" 
                                     fill="rgba(52, 152, 219, 0.3)" stroke="#3498db" stroke-width="2"/>
                        </defs>
                        <!-- Grid lines -->
                        <polygon points="100,40 160,80 135,140 65,140 40,80" fill="none" stroke="#e9ecef" stroke-width="1"/>
                        <polygon points="100,60 140,90 125,130 75,130 60,90" fill="none" stroke="#e9ecef" stroke-width="1"/>
                        <!-- Data -->
                        <polygon points="100,45 150,85 130,135 70,135 50,85" 
                                 fill="rgba(231, 76, 60, 0.4)" stroke="#e74c3c" stroke-width="2"/>
                        <!-- Labels -->
                        <text x="100" y="15" text-anchor="middle" font-size="10">Age Risk</text>
                        <text x="185" y="75" text-anchor="start" font-size="10">BP Risk</text>
                        <text x="150" y="165" text-anchor="middle" font-size="10">Cholesterol</text>
                        <text x="50" y="165" text-anchor="middle" font-size="10">Exercise</text>
                        <text x="15" y="75" text-anchor="end" font-size="10">ECG Risk</text>
                    </svg>
                </div>
            </div>
            ''',
            'confidence_risk': '''
            <div style="background: white; padding: 20px; border-radius: 10px;">
                <h5>Model Confidence vs Risk</h5>
                <div style="position: relative; height: 200px; background: #f8f9fa; border-radius: 8px; margin: 10px 0;">
                    <div style="position: absolute; bottom: 0; left: 0; width: 100%; height: 1px; background: #dee2e6;"></div>
                    <div style="position: absolute; bottom: 0; left: 0; width: 1px; height: 100%; background: #dee2e6;"></div>
                    <!-- Data points -->
                    <div style="position: absolute; bottom: 130px; left: 85%; width: 10px; height: 10px; 
                                background: #dc3545; border-radius: 50%; transform: translate(-50%, 50%);"></div>
                    <div style="position: absolute; bottom: 90px; left: 78%; width: 8px; height: 8px; 
                                background: #fd7e14; border-radius: 50%; transform: translate(-50%, 50%);"></div>
                    <div style="position: absolute; bottom: 50px; left: 72%; width: 6px; height: 6px; 
                                background: #198754; border-radius: 50%; transform: translate(-50%, 50%);"></div>
                    <!-- Labels -->
                    <div style="position: absolute; bottom: 140px; left: 87%; font-size: 10px;">CAD</div>
                    <div style="position: absolute; bottom: 100px; left: 80%; font-size: 10px;">Heart Attack</div>
                    <div style="position: absolute; bottom: 60px; left: 74%; font-size: 10px;">Arrhythmia</div>
                    <!-- Axes labels -->
                    <div style="position: absolute; bottom: -20px; left: 50%; transform: translateX(-50%); font-size: 12px;">Confidence (%)</div>
                    <div style="position: absolute; top: 50%; left: -30px; transform: rotate(-90deg) translateX(-50%); font-size: 12px;">Risk (%)</div>
                </div>
            </div>
            '''
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