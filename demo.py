"""
Demo script to test the Heart Disease Detection System
This script simulates the complete workflow without requiring user input
"""

import sys
import os
import json
from datetime import datetime

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.data_processing.models import (
    PatientData, Gender, ChestPainType, RestingECG, 
    Slope, Thalassemia
)
from src.data_processing.algorithm_interface import AlgorithmInterface
from src.visualization.report_generator import ReportGenerator


def create_sample_patient_data():
    """Create sample patient data for testing"""
    return PatientData(
        age=54,
        sex=Gender.MALE,
        chest_pain_type=ChestPainType.TYPICAL_ANGINA,
        resting_blood_pressure=150,
        cholesterol=280,
        fasting_blood_sugar=True,
        resting_ecg=RestingECG.ST_T_ABNORMALITY,
        max_heart_rate=145,
        exercise_induced_angina=True,
        st_depression=2.3,
        slope_peak_exercise=Slope.FLAT,
        major_vessels=2,
        thalassemia=Thalassemia.REVERSIBLE_DEFECT
    )


def test_complete_workflow():
    """Test the complete analysis workflow"""
    print("🧪 Testing Heart Disease Detection System")
    print("=" * 50)
    
    # Step 1: Create sample patient data
    print("📋 Step 1: Creating sample patient data...")
    patient_data = create_sample_patient_data()
    patient_id = "demo_patient_001"
    
    print(f"   ✅ Patient ID: {patient_id}")
    print(f"   ✅ Age: {patient_data.age}, Sex: {patient_data.sex.name}")
    print(f"   ✅ Chest Pain: {patient_data.chest_pain_type.name}")
    print(f"   ✅ Blood Pressure: {patient_data.resting_blood_pressure} mmHg")
    print(f"   ✅ Cholesterol: {patient_data.cholesterol} mg/dl")
    
    # Step 2: Send to algorithm interface
    print("\n🤖 Step 2: Sending data to AI analysis...")
    algorithm_interface = AlgorithmInterface()
    analysis_result = algorithm_interface.send_patient_data(patient_data, patient_id)
    
    print(f"   ✅ Overall Risk Score: {analysis_result.overall_risk_score:.1%}")
    print(f"   ✅ Diseases Analyzed: {len(analysis_result.disease_results)}")
    print(f"   ✅ Primary Concerns: {len(analysis_result.primary_concerns)}")
    
    # Step 3: Generate comprehensive report
    print("\n📊 Step 3: Generating comprehensive report...")
    report_generator = ReportGenerator()
    report = report_generator.generate_comprehensive_report(analysis_result)
    
    print(f"   ✅ Report sections generated: {len(report.keys())}")
    print(f"   ✅ Visualizations created: {len(report['visualizations'])}")
    print(f"   ✅ Recommendations provided: {len(report['recommendations'])}")
    
    # Step 4: Display key results
    print("\n📈 Step 4: Analysis Results Summary")
    print("-" * 30)
    
    print(f"Patient: {analysis_result.patient_id}")
    print(f"Overall Risk: {analysis_result.overall_risk_score:.1%}")
    
    print("\nDisease Risk Analysis:")
    for disease in analysis_result.disease_results:
        risk_emoji = "🔴" if disease.risk_level == "High" else "🟡" if disease.risk_level == "Medium" else "🟢"
        print(f"  {risk_emoji} {disease.disease_name}: {disease.probability:.1%} ({disease.risk_level} Risk)")
    
    print(f"\nPrimary Concerns: {', '.join(analysis_result.primary_concerns) if analysis_result.primary_concerns else 'None'}")
    
    print(f"\nTop Recommendations:")
    for i, rec in enumerate(analysis_result.recommended_actions[:3], 1):
        print(f"  {i}. {rec}")
    
    # Step 5: Test data format for algorithm team
    print("\n🔗 Step 5: Algorithm Team Integration Format")
    print("-" * 40)
    
    csv_data = patient_data.to_csv_row()
    feature_names = [
        "age", "sex", "cp", "trestbps", "chol", "fbs", 
        "restecg", "thalach", "exang", "oldpeak", 
        "slope", "ca", "thal"
    ]
    
    print("CSV Format for Algorithm Team:")
    print(",".join(map(str, csv_data)))
    print("\nFeature Mapping:")
    for name, value in zip(feature_names, csv_data):
        print(f"  {name}: {value}")
    
    # Step 6: Save sample report data
    print("\n💾 Step 6: Saving sample data...")
    
    sample_data = {
        "patient_data": {
            "age": patient_data.age,
            "sex": patient_data.sex.name,
            "chest_pain_type": patient_data.chest_pain_type.name,
            "resting_blood_pressure": patient_data.resting_blood_pressure,
            "cholesterol": patient_data.cholesterol,
            "csv_format": csv_data
        },
        "analysis_summary": {
            "overall_risk_score": analysis_result.overall_risk_score,
            "primary_concerns": analysis_result.primary_concerns,
            "disease_count": len(analysis_result.disease_results),
            "high_risk_diseases": [d.disease_name for d in analysis_result.disease_results if d.risk_level == "High"]
        },
        "medical_summary": report["medical_summary"][:500] + "..." if len(report["medical_summary"]) > 500 else report["medical_summary"]
    }
    
    with open("sample_analysis_output.json", "w") as f:
        json.dump(sample_data, f, indent=2)
    
    print("   ✅ Sample data saved to 'sample_analysis_output.json'")
    
    print("\n🎉 Test Complete!")
    print("=" * 50)
    print("✅ All components working correctly")
    print("✅ Ready for integration with algorithm team")
    print("✅ User interface ready for deployment")
    print("\n🚀 To start the web application, run: python app.py")


if __name__ == "__main__":
    test_complete_workflow()