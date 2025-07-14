"""
Tests for FastAPI endpoints
"""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock
import io

from src.api.main import app

client = TestClient(app)

class TestDocumentAPI:
    
    def test_root_endpoint(self):
        """Test root endpoint"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "AWS Document Processing API"
        assert data["status"] == "healthy"
    
    def test_health_check(self):
        """Test health check endpoint"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
    
    @patch('src.services.document_processor.DocumentProcessorService.upload_and_process')
    def test_upload_document_success(self, mock_upload):
        """Test successful document upload"""
        # Mock the upload service
        mock_upload.return_value = {
            's3_key': 'uploads/test-id/test.pdf',
            'document_id': 'test-id',
            'status': 'uploaded'
        }
        
        # Create test PDF file
        pdf_content = b"%PDF-1.4 fake pdf content"
        
        response = client.post(
            "/api/v1/documents/upload",
            files={"file": ("test.pdf", io.BytesIO(pdf_content), "application/pdf")}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["filename"] == "test.pdf"
        assert data["status"] == "uploaded"
    
    def test_upload_invalid_file_type(self):
        """Test upload with invalid file type"""
        txt_content = b"This is not a PDF"
        
        response = client.post(
            "/api/v1/documents/upload",
            files={"file": ("test.txt", io.BytesIO(txt_content), "text/plain")}
        )
        
        assert response.status_code == 400
        assert "Only PDF files are supported" in response.json()["detail"]
    
    @patch('src.services.document_processor.DocumentProcessorService.get_processing_status')
    def test_get_document_status(self, mock_status):
        """Test get document status"""
        # Mock status response
        mock_status.return_value = {
            'document_id': 'test-id',
            'filename': 'test.pdf',
            'status': 'processing',
            'upload_timestamp': '2024-01-01T10:00:00',
            's3_key': 'uploads/test-id/test.pdf'
        }
        
        response = client.get("/api/v1/documents/test-id/status")
        
        assert response.status_code == 200
        data = response.json()
        assert data["document_id"] == "test-id"
        assert data["status"] == "processing"
    
    def test_get_document_status_not_found(self):
        """Test get status for non-existent document"""
        with patch('src.services.document_processor.DocumentProcessorService.get_processing_status') as mock_status:
            mock_status.return_value = None
            
            response = client.get("/api/v1/documents/nonexistent/status")
            
            assert response.status_code == 404
            assert "Document not found" in response.json()["detail"]

if __name__ == '__main__':
    pytest.main([__file__, '-v'])
