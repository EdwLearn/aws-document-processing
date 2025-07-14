"""
Document data models
"""
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime
from enum import Enum

class ProcessingStatus(str, Enum):
    """Document processing status"""
    UPLOADED = "uploaded"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    DELETED = "deleted"

class DocumentCreate(BaseModel):
    """Schema for creating a new document"""
    filename: str = Field(..., description="Original filename")
    file_size: Optional[int] = Field(None, description="File size in bytes")
    content_type: str = Field(default="application/pdf")

class DocumentResponse(BaseModel):
    """Schema for document response"""
    document_id: str = Field(..., description="Unique document identifier")
    filename: str = Field(..., description="Original filename")
    status: ProcessingStatus = Field(..., description="Current processing status")
    upload_timestamp: datetime = Field(..., description="When document was uploaded")
    processing_started: Optional[datetime] = Field(None, description="When processing started")
    processing_completed: Optional[datetime] = Field(None, description="When processing completed")
    s3_key: Optional[str] = Field(None, description="S3 object key")
    error_message: Optional[str] = Field(None, description="Error message if processing failed")
    message: Optional[str] = Field(None, description="Status message")
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
