# 🚗 Vehicle Document Classification System

[![Model Accuracy](https://img.shields.io/badge/Accuracy-87.67%25-success)](models/final_evaluation_report.json)
[![Model Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen)](models/cpu_model.h5)
[![DVC](https://img.shields.io/badge/DVC-Tracked-blue)](models/cpu_model.h5.dvc)

## 🎯 Project Overview

Advanced Computer Vision system for automatic classification of vehicle documents using Deep Learning. Achieves **87.67% accuracy** with comprehensive error analysis and production-ready deployment.

### 🏆 Key Results
- **Model Accuracy**: 87.67% (exceeds 80% target by 7.67%)
- **Error Analysis**: 9 logical errors out of 73 test samples
- **Confidence Separation**: Lower confidence in errors (good indicator)
- **Processing Speed**: 27.4 documents/second
- **Status**: Production Ready

## 🛠️ Technical Stack
- **Framework**: TensorFlow 2.15.0
- **CV Library**: OpenCV 4.8.1
- **Language**: Python 3.10.12
- **MLOps**: DVC for model versioning
- **Hardware**: CPU optimized (880K parameters)

## 📊 Model Performance

| Class | Precision | Recall | F1-Score | Support |
|-------|-----------|--------|----------|---------|
| Document | 0.64 | 0.88 | 0.74 | 8 |
| Licence | 0.92 | 0.94 | 0.93 | 47 |
| Odometer | 0.93 | 0.72 | 0.81 | 18 |
| **Overall** | **0.89** | **0.88** | **0.88** | **73** |

## 📚 Project Structure

```
vehicle-document-system/
├── data/
│   └── processed/car_plates/
│       ├── annotations/              # JSON splits
│       └── images_rois/             # Processed images (DVC)
├── models/
│   ├── cpu_model.h5                 # Production model (DVC)
│   └── final_evaluation_report.json # Complete metrics
├── notebooks/
│   ├── 01_data_exploration.ipynb    # EDA
│   ├── 02_preprocessing_opencv.ipynb # Data pipeline
│   ├── 03_model_training.ipynb      # Training
│   └── 04_model_evaluation.ipynb    # Evaluation & error analysis
└── README.md
```

## 🚀 Quick Start

```bash
# Clone repository
git clone <repository-url>
cd vehicle-document-system

# Setup environment
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Pull model with DVC
dvc pull

# Run inference
python inference.py --image path/to/document.jpg
```

## 🔬 Methodology

### 1. Data Collection & EDA
- **Multi-source integration**: 3 Kaggle datasets combined
- **Final dataset**: 729 balanced samples
- **Class distribution**: Licence(65%), Odometer(24%), Document(11%)

### 2. Preprocessing Pipeline
- **OpenCV processing**: Resize to 224×224, normalization
- **Data augmentation**: Balance minority classes
- **Quality control**: Manual verification of annotations

### 3. Model Architecture
```
Input (224×224×3)
    ↓
Conv2D(32) → BatchNorm → Conv2D(32) → MaxPool → Dropout(0.25)
    ↓
Conv2D(64) → BatchNorm → Conv2D(64) → MaxPool → Dropout(0.25)
    ↓
Conv2D(128) → BatchNorm → Conv2D(128) → MaxPool → Dropout(0.3)
    ↓
GlobalAvgPool → Dense(256) → Dense(128) → Dense(3)
```

### 4. Training Strategy
- **Class weights**: Document(3.04x), Licence(0.52x), Odometer(1.36x)
- **Optimization**: Adam optimizer with learning rate scheduling
- **Regularization**: Dropout, BatchNormalization
- **Validation**: Stratified train/val/test splits

### 5. Error Analysis
- **Total errors**: 9 out of 73 test samples (87.67% accuracy)
- **Error patterns**: Logical confusions between similar classes
- **Confidence analysis**: Model shows uncertainty in difficult cases
- **Quality indicator**: Lower confidence in errors vs correct predictions

## 📈 Business Impact

### Automation Benefits
- **87% of documents** can be processed automatically
- **Processing speed**: 27.4 documents/second
- **Manual review**: Only needed for 13% of cases
- **Cost reduction**: Significant labor savings

### Deployment Readiness
- **Model format**: Keras H5 (TensorFlow compatible)
- **Memory requirements**: 2GB RAM
- **Inference time**: <100ms per document
- **Scalability**: Ready for production deployment

## 🔧 Technical Specifications

### Model Details
- **Parameters**: 880,291
- **Model size**: ~3.4MB
- **Input format**: RGB images 224×224×3
- **Output**: 3-class probabilities
- **Framework**: TensorFlow 2.15.0

### System Requirements
- **Python**: 3.10.12+
- **RAM**: 4GB minimum, 8GB recommended
- **Storage**: 100MB for model + dependencies
- **GPU**: Optional (CPU version is production model)

## 🏆 Key Achievements

✅ **Exceeded target**: 87.67% vs 80% requirement (+7.67%)  
✅ **Production ready**: Comprehensive evaluation and error analysis  
✅ **MLOps integration**: DVC versioning for reproducibility  
✅ **Business value**: Clear automation potential with measurable impact  
✅ **Interpretable**: Understanding of model limitations and error patterns  

## 📋 Future Improvements

- [ ] **Real-time API**: FastAPI deployment
- [ ] **Data augmentation**: Advanced techniques for minority classes
- [ ] **Model ensemble**: Combine multiple architectures
- [ ] **Active learning**: Improve on difficult cases
- [ ] **A/B testing**: Production performance monitoring

## 👨‍💻 Author

**Eduardo** - Data Scientist & ML Engineer

*Specialized in Computer Vision, Deep Learning, and MLOps*

---

## 📄 License

This project is part of a professional portfolio demonstrating advanced ML engineering capabilities.

**Status**: ✅ Production Ready | **Last Updated**: December 2024
