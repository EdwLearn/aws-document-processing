"""
Configuration settings
"""
import os
from typing import Optional

class Settings:
    """Application settings"""
    
    # API Configuration
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    environment: str = "development"
    
    # AWS Configuration
    aws_region: str = "us-east-1"
    s3_document_bucket: str = "document-processing-uploads"
    
    def __init__(self):
        # Load from environment variables if available
        self.api_host = os.getenv("API_HOST", self.api_host)
        self.api_port = int(os.getenv("API_PORT", self.api_port))
        self.environment = os.getenv("ENVIRONMENT", self.environment)
        self.aws_region = os.getenv("AWS_REGION", self.aws_region)

# Global settings instance
settings = Settings()
