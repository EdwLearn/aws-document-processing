#!/usr/bin/env python3
"""
Vehicle Document Classification - Inference Script
Production-ready inference for document classification
"""

import tensorflow as tf
import numpy as np
import cv2
import argparse
import json
from pathlib import Path

class VehicleDocumentClassifier:
    """Production inference class for vehicle document classification"""
    
    def __init__(self, model_path="models/cpu_model.h5"):
        """Initialize classifier with trained model"""
        self.model = tf.keras.models.load_model(model_path)
        self.class_names = ['document', 'licence', 'odometer']
        self.input_size = (224, 224)
        
    def preprocess_image(self, image_path):
        """Preprocess image for model inference"""
        # Load image
        image = cv2.imread(str(image_path))
        if image is None:
            raise ValueError(f"Could not load image: {image_path}")
        
        # Convert BGR to RGB
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # Resize to model input size
        image = cv2.resize(image, self.input_size)
        
        # Normalize to [0, 1]
        image = image.astype(np.float32) / 255.0
        
        # Add batch dimension
        image = np.expand_dims(image, axis=0)
        
        return image
    
    def predict(self, image_path, return_confidence=True):
        """Make prediction on single image"""
        # Preprocess
        processed_image = self.preprocess_image(image_path)
        
        # Predict
        predictions = self.model.predict(processed_image, verbose=0)
        
        # Get class and confidence
        class_idx = np.argmax(predictions[0])
        confidence = float(predictions[0][class_idx])
        class_name = self.class_names[class_idx]
        
        result = {
            'predicted_class': class_name,
            'confidence': confidence,
            'image_path': str(image_path)
        }
        
        if return_confidence:
            # Add all class probabilities
            result['all_probabilities'] = {
                self.class_names[i]: float(predictions[0][i]) 
                for i in range(len(self.class_names))
            }
        
        return result

def main():
    """Main inference function"""
    parser = argparse.ArgumentParser(description='Vehicle Document Classification Inference')
    parser.add_argument('--image', required=True, help='Path to image file')
    parser.add_argument('--model', default='models/cpu_model.h5', help='Path to model file')
    parser.add_argument('--output', help='Output JSON file for results')
    
    args = parser.parse_args()
    
    # Initialize classifier
    try:
        classifier = VehicleDocumentClassifier(args.model)
        print(f"✅ Model loaded: {args.model}")
    except Exception as e:
        print(f"❌ Error loading model: {e}")
        return
    
    # Make prediction
    try:
        result = classifier.predict(args.image)
        
        print(f"\n📊 CLASSIFICATION RESULT:")
        print(f"  Image: {result['image_path']}")
        print(f"  Predicted Class: {result['predicted_class']}")
        print(f"  Confidence: {result['confidence']:.3f} ({result['confidence']*100:.1f}%)")
        
        print(f"\n📈 All Probabilities:")
        for class_name, prob in result['all_probabilities'].items():
            print(f"  {class_name}: {prob:.3f} ({prob*100:.1f}%)")
        
        # Save to file if requested
        if args.output:
            with open(args.output, 'w') as f:
                json.dump(result, f, indent=2)
            print(f"\n💾 Results saved to: {args.output}")
            
    except Exception as e:
        print(f"❌ Error during prediction: {e}")

if __name__ == "__main__":
    main()
