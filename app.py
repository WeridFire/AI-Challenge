"""
Main Application Module for Heart Disease Detection System
Orchestrates the entire workflow from data collection to visualization
"""

from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import os
import sys
from datetime import datetime

# Add the src directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.ui.user_interface import UserInterface
from src.data_processing.algorithm_interface import AlgorithmInterface
from src.data_processing.models import PatientData, Gender, ChestPainType, RestingECG, Slope, Thalassemia
from src.visualization.report_generator import ReportGenerator


class HeartDiseaseDetectionApp:
    """Main application class that orchestrates the entire system"""
    
    def __init__(self):
        # Initialize Flask app
        self.app = Flask(__name__, 
                        template_folder='templates', 
                        static_folder='static')
        self.app.secret_key = 'heart_disease_detection_secret_key_2024'
        
        # Initialize components
        self.algorithm_interface = AlgorithmInterface()
        self.report_generator = ReportGenerator()
        self.user_interface = UserInterface(self.app)
        
        # Setup additional routes
        self.setup_analysis_routes()
    
    def setup_analysis_routes(self):
        """Setup routes for analysis and results"""
        
        @self.app.route('/analyze/<patient_id>')
        def analyze_patient(patient_id):
            """Analyze patient data and generate report"""
            try:
                # Get patient data from session
                patient_data_dict = session.get('patient_data')
                if not patient_data_dict:
                    return redirect(url_for('index'))
                
                # Reconstruct PatientData object
                patient_data = self._reconstruct_patient_data(patient_data_dict)
                
                # Send data to algorithm for analysis
                analysis_result = self.algorithm_interface.send_patient_data(patient_data, patient_id)
                
                # Generate comprehensive report
                report = self.report_generator.generate_comprehensive_report(analysis_result)
                
                # Don't store complex objects in session - just pass to template
                return render_template('results.html', report=report, analysis=analysis_result)
                
            except Exception as e:
                print(f"Analysis error: {e}")  # Debug print
                return jsonify({
                    'status': 'error',
                    'message': f'Analysis failed: {str(e)}'
                }), 500
        
        @self.app.route('/api/patient_data/<patient_id>')
        def get_patient_data(patient_id):
            """API endpoint to get patient data (for algorithm team)"""
            try:
                patient_data_dict = session.get('patient_data')
                if not patient_data_dict:
                    return jsonify({'error': 'Patient data not found'}), 404
                
                # Convert to the format expected by algorithm team
                patient_data = self._reconstruct_patient_data(patient_data_dict)
                csv_row = patient_data.to_csv_row()
                
                return jsonify({
                    'patient_id': patient_id,
                    'timestamp': datetime.now().isoformat(),
                    'features': csv_row,
                    'feature_names': [
                        "age", "sex", "cp", "trestbps", "chol", "fbs", 
                        "restecg", "thalach", "exang", "oldpeak", 
                        "slope", "ca", "thal"
                    ],
                    'metadata': {
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
                })
                
            except Exception as e:
                return jsonify({'error': str(e)}), 500
        
        @self.app.route('/api/submit_results/<patient_id>', methods=['POST'])
        def submit_analysis_results(patient_id):
            """API endpoint for algorithm team to submit results"""
            try:
                results_data = request.get_json()
                
                # In a real implementation, this would:
                # 1. Validate the results format
                # 2. Store results in a database
                # 3. Trigger notification to user
                # 4. Generate the final report
                
                return jsonify({
                    'status': 'success',
                    'message': 'Results received successfully',
                    'patient_id': patient_id,
                    'results_url': f'/analyze/{patient_id}'
                })
                
            except Exception as e:
                return jsonify({
                    'status': 'error',
                    'message': str(e)
                }), 500
        
        @self.app.route('/download_report/<patient_id>')
        def download_report(patient_id):
            """Download report as PDF (placeholder)"""
            # In a real implementation, this would generate and return a PDF
            return jsonify({
                'message': 'PDF generation not implemented yet',
                'note': 'Use browser print function for now'
            })
        
        @self.app.route('/health')
        def health_check():
            """Health check endpoint for monitoring"""
            return jsonify({
                'status': 'healthy',
                'timestamp': datetime.now().isoformat(),
                'components': {
                    'user_interface': 'operational',
                    'algorithm_interface': 'operational',
                    'report_generator': 'operational'
                }
            })
    
    def _reconstruct_patient_data(self, patient_data_dict):
        """Reconstruct PatientData object from dictionary"""
        return PatientData(
            age=patient_data_dict['age'],
            sex=Gender(patient_data_dict['sex']),
            chest_pain_type=ChestPainType(patient_data_dict['chest_pain_type']),
            resting_blood_pressure=patient_data_dict['resting_blood_pressure'],
            cholesterol=patient_data_dict['cholesterol'],
            fasting_blood_sugar=patient_data_dict['fasting_blood_sugar'],
            resting_ecg=RestingECG(patient_data_dict['resting_ecg']),
            max_heart_rate=patient_data_dict['max_heart_rate'],
            exercise_induced_angina=patient_data_dict['exercise_induced_angina'],
            st_depression=patient_data_dict['st_depression'],
            slope_peak_exercise=Slope(patient_data_dict['slope_peak_exercise']),
            major_vessels=patient_data_dict['major_vessels'],
            thalassemia=Thalassemia(patient_data_dict['thalassemia'])
        )
    
    def run(self, debug=True, host='127.0.0.1', port=5000):
        """Run the Flask application"""
        print(f"""
        ====================================================
        Heart Disease Detection System
        ====================================================
        
        🏥 User Interface: http://{host}:{port}
        📊 API Health Check: http://{host}:{port}/health
        📋 Patient Data API: http://{host}:{port}/api/patient_data/<patient_id>
        
        Features:
        ✅ Friendly data collection interface
        ✅ Real-time form validation and guidance
        ✅ AI-powered disease risk analysis
        ✅ Comprehensive medical reports
        ✅ Interactive visualizations
        ✅ Clinical recommendations
        
        Ready for integration with algorithm team!
        ====================================================
        """)
        
        self.app.run(debug=debug, host=host, port=port)


def main():
    """Main entry point"""
    app = HeartDiseaseDetectionApp()
    app.run(debug=True)


if __name__ == '__main__':
    main()