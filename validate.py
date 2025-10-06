"""
Simple validation script to check if the system components work
This script tests the core functionality without external dependencies
"""

import sys
import os

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test if all modules can be imported"""
    print("🔍 Testing module imports...")
    
    try:
        from src.data_processing.models import PatientData, Gender, ChestPainType
        print("   ✅ Data models imported successfully")
        
        from src.data_processing.algorithm_interface import AlgorithmInterface
        print("   ✅ Algorithm interface imported successfully")
        
        from src.visualization.report_generator import ReportGenerator  
        print("   ✅ Report generator imported successfully")
        
        from src.ui.user_interface import UserInterface
        print("   ✅ User interface imported successfully")
        
        return True
    except ImportError as e:
        print(f"   ❌ Import error: {e}")
        return False

def test_data_models():
    """Test data model creation and validation"""
    print("\n📋 Testing data models...")
    
    try:
        from src.data_processing.models import PatientData, Gender, ChestPainType, RestingECG, Slope, Thalassemia
        
        # Create a sample patient
        patient = PatientData(
            age=45,
            sex=Gender.MALE,
            chest_pain_type=ChestPainType.TYPICAL_ANGINA,
            resting_blood_pressure=140,
            cholesterol=240,
            fasting_blood_sugar=False,
            resting_ecg=RestingECG.NORMAL,
            max_heart_rate=160,
            exercise_induced_angina=False,
            st_depression=1.2,
            slope_peak_exercise=Slope.UPSLOPING,
            major_vessels=1,
            thalassemia=Thalassemia.NORMAL
        )
        
        print(f"   ✅ Patient created: {patient.age}yr {patient.sex.name}")
        
        # Test CSV conversion
        csv_data = patient.to_csv_row()
        print(f"   ✅ CSV conversion: {len(csv_data)} features")
        print(f"   ✅ Sample data: {csv_data[:5]}...")
        
        return True
    except Exception as e:
        print(f"   ❌ Data model error: {e}")
        return False

def test_algorithm_interface():
    """Test the algorithm interface simulation"""
    print("\n🤖 Testing algorithm interface...")
    
    try:
        from src.data_processing.models import PatientData, Gender, ChestPainType, RestingECG, Slope, Thalassemia
        from src.data_processing.algorithm_interface import AlgorithmInterface
        
        # Create algorithm interface
        algorithm = AlgorithmInterface()
        print("   ✅ Algorithm interface created")
        
        # Create test patient data
        patient = PatientData(
            age=60, sex=Gender.MALE, chest_pain_type=ChestPainType.TYPICAL_ANGINA,
            resting_blood_pressure=160, cholesterol=300, fasting_blood_sugar=True,
            resting_ecg=RestingECG.ST_T_ABNORMALITY, max_heart_rate=120, exercise_induced_angina=True,
            st_depression=2.5, slope_peak_exercise=Slope.FLAT, major_vessels=2, thalassemia=Thalassemia.REVERSIBLE_DEFECT
        )
        
        # Test analysis
        result = algorithm.send_patient_data(patient, "test_patient_001")
        print(f"   ✅ Analysis completed: {result.overall_risk_score:.1%} risk")
        print(f"   ✅ Diseases analyzed: {len(result.disease_results)}")
        print(f"   ✅ Recommendations: {len(result.recommended_actions)}")
        
        return True
    except Exception as e:
        print(f"   ❌ Algorithm interface error: {e}")
        return False

def test_report_generation():
    """Test report generation without visualization dependencies"""
    print("\n📊 Testing report generation...")
    
    try:
        from src.data_processing.models import PatientData, Gender, ChestPainType, RestingECG, Slope, Thalassemia
        from src.data_processing.algorithm_interface import AlgorithmInterface
        from src.visualization.report_generator import ReportGenerator
        
        # Create test data
        patient = PatientData(
            age=55, sex=Gender.FEMALE, chest_pain_type=ChestPainType.ATYPICAL_ANGINA,
            resting_blood_pressure=130, cholesterol=220, fasting_blood_sugar=False,
            resting_ecg=RestingECG.NORMAL, max_heart_rate=150, exercise_induced_angina=False,
            st_depression=0.8, slope_peak_exercise=Slope.UPSLOPING, major_vessels=0, thalassemia=Thalassemia.NORMAL
        )
        
        # Get analysis
        algorithm = AlgorithmInterface()
        analysis_result = algorithm.send_patient_data(patient, "test_patient_002")
        
        # Generate report (skip visualizations that need external libraries)
        report_generator = ReportGenerator()
        
        # Test individual report components
        patient_summary = report_generator._generate_patient_summary(analysis_result)
        print(f"   ✅ Patient summary generated: {patient_summary['patient_id']}")
        
        risk_assessment = report_generator._generate_risk_assessment(analysis_result)
        print(f"   ✅ Risk assessment: {risk_assessment['overall_risk_score']}")
        
        medical_summary = report_generator._generate_medical_summary(analysis_result)
        print(f"   ✅ Medical summary: {len(medical_summary)} characters")
        
        return True
    except Exception as e:
        print(f"   ❌ Report generation error: {e}")
        return False

def main():
    """Main validation function"""
    print("🏥 Heart Disease Detection System - Component Validation")
    print("=" * 60)
    
    tests = [
        test_imports,
        test_data_models, 
        test_algorithm_interface,
        test_report_generation
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        else:
            print("   ⚠️  Some functionality may be limited")
    
    print("\n" + "=" * 60)
    print(f"🧪 Validation Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("✅ All core components working correctly!")
        print("🚀 System ready for deployment")
    elif passed >= total - 1:
        print("⚠️  Most components working - minor issues detected")
        print("🔧 System mostly functional, may need dependency installation")
    else:
        print("❌ Major issues detected")
        print("🔧 Please check dependencies and imports")
    
    print("\n📖 Next steps:")
    print("   1. Install dependencies: pip install -r requirements.txt")
    print("   2. Run full demo: python demo.py")
    print("   3. Start web application: python app.py")
    print("   4. Access UI: http://localhost:5000")

if __name__ == "__main__":
    main()