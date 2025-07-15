# 🧾 Invoice Processing SaaS Platform

> AI-powered invoice processing and inventory management for Colombian retail businesses

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com)
[![AWS](https://img.shields.io/badge/AWS-Textract-orange.svg)](https://aws.amazon.com/textract)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15+-blue.svg)](https://postgresql.org)

## 🎯 Problem Statement

Colombian retail stores (specifically remate/discount stores) face significant challenges:
- **83% need better inventory control** (validated through customer surveys)
- **Manual invoice processing** takes 4+ hours daily
- **15-20% error rates** in manual data entry
- **Limited tech solutions** for this specific market segment

## 🚀 Solution

A **B2B SaaS platform** that automates invoice processing using AWS Textract and Computer Vision, specifically designed for Colombian retail businesses working with importers.

### Key Features ✨

- **🤖 AI-Powered Extraction**: AWS Textract + OpenCV for 95%+ accuracy
- **📱 Mobile Support**: Process paper invoices via smartphone photos
- **🏢 Multi-Tenant**: Secure isolation for multiple businesses
- **📊 Real-Time Dashboard**: Inventory tracking and analytics
- **💰 Pay-per-Use**: Flexible pricing ($1,500-2,000 COP per invoice)
- **⚡ Fast Processing**: <30 seconds per invoice

## 🏗️ Architecture
Mobile/Web Upload → FastAPI Gateway → AWS S3 → AWS Textract
↓
PostgreSQL ← Lambda Processing ← Structured Data ← Analysis
↓
Dashboard → Analytics & Reports

### Tech Stack 🛠️

**Backend:**
- **FastAPI** - High-performance API framework
- **SQLAlchemy** - ORM with async support
- **PostgreSQL** - Production database
- **Pydantic** - Data validation and serialization

**AI/ML:**
- **AWS Textract** - Document intelligence
- **OpenCV** - Image preprocessing
- **Tesseract** - Fallback OCR

**Infrastructure:**
- **AWS S3** - Document storage
- **AWS Lambda** - Serverless processing
- **Docker** - Containerization
- **Alembic** - Database migrations

## 📋 Current Status

### ✅ Completed Features

- [x] **Core API Infrastructure**
  - Multi-tenant FastAPI application
  - PostgreSQL database with full schema
  - Authentication system
  - Async request handling

- [x] **Invoice Processing Pipeline**
  - PDF upload and storage
  - AWS Textract integration
  - Data extraction and validation
  - Error handling and fallbacks

- [x] **REST API Endpoints**
POST   /api/v1/invoices/upload
GET    /api/v1/invoices/{id}/status
GET    /api/v1/invoices/{id}/data
GET    /api/v1/invoices/
DELETE /api/v1/invoices/{id}
GET    /api/v1/invoices/analytics/summary
### 🚧 In Development

- [ ] **Computer Vision for Mobile Photos**
- [ ] **Web Dashboard Interface**
- [ ] **Stripe Payment Integration**
- [ ] **Advanced Analytics**

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- PostgreSQL 15+
- Docker & Docker Compose
- AWS Account (for Textract)

### Installation

**Clone the repository**
 ```bash
 git clone https://github.com/yourusername/document-processing-system.git
 cd document-processing-system
 ```
## 🗂️ Project Structure
 ```bash
src/
├── api/                    # FastAPI application
│   ├── main.py            # Application entry point
│   └── routers/           # API route handlers
├── config/                # Configuration management
├── database/              # Database models and connection
├── models/                # Pydantic data models
└── services/              # Business logic
    ├── invoice_processor.py
    └── textract_service.py

tests/                     # Test suite
migrations/                # Alembic database migrations
docs/                     # Documentation
 ```



