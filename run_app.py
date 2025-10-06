"""
Quick fix script for the Flask app
Run this to test the system quickly
"""

import sys
import os

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from app import HeartDiseaseDetectionApp
    
    print("🚀 Starting Heart Disease Detection System...")
    print("📝 Fixed JSON serialization issue with enums")
    print("🌐 Server will start at: http://localhost:5000")
    print("=" * 50)
    
    # Create and run the app
    app = HeartDiseaseDetectionApp()
    app.run(debug=True, host='127.0.0.1', port=5000)
    
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("🔧 Please install dependencies: pip install flask pandas numpy matplotlib seaborn plotly")
except Exception as e:
    print(f"❌ Error starting app: {e}")
    print("🔧 Check the error above and fix any issues")