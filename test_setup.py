#!/usr/bin/env python3
"""Script para verificar que todas las librerías estén correctamente instaladas"""

import sys
import importlib

def test_imports():
    """Test que todas las librerías se importan correctamente"""
    libraries = {
        'cv2': 'OpenCV',
        'PIL': 'Pillow', 
        'sklearn': 'Scikit-learn',
        'tensorflow': 'TensorFlow',
        'numpy': 'NumPy',
        'pandas': 'Pandas',
        'matplotlib': 'Matplotlib',
        'seaborn': 'Seaborn',
        'dvc': 'DVC',
        'mlflow': 'MLflow',
        'tqdm': 'TQDM',
        'kaggle': 'Kaggle'
    }
    
    print("🧪 TESTING IMPORTS:")
    print("=" * 40)
    
    success_count = 0
    for lib, name in libraries.items():
        try:
            importlib.import_module(lib)
            print(f"✅ {name}")
            success_count += 1
        except ImportError as e:
            print(f"❌ {name}: {e}")
    
    print(f"\n📊 RESULTS: {success_count}/{len(libraries)} libraries imported successfully")
    print(f"🐍 Python version: {sys.version}")
    
    # Test específicos
    if success_count == len(libraries):
        print("\n🔍 SPECIFIC TESTS:")
        
        # Test OpenCV
        import cv2
        print(f"📸 OpenCV version: {cv2.__version__}")
        
        # Test TensorFlow
        import tensorflow as tf
        print(f"🧠 TensorFlow version: {tf.__version__}")
        gpu_devices = tf.config.list_physical_devices('GPU')
        print(f"🔧 GPU available: {len(gpu_devices) > 0} ({len(gpu_devices)} devices)")
        
        # Test NumPy
        import numpy as np
        print(f"🔢 NumPy version: {np.__version__}")
        
        print("\n🎉 ALL SYSTEMS GO! Ready to start the project!")
    else:
        print(f"\n⚠️  Some libraries failed to import. Please check the errors above.")

if __name__ == "__main__":
    test_imports()
