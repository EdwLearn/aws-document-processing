"""
Document processing service
"""
import boto3
import json
import asyncio
from typing import Dict, Any, Optional, List
import logging
from datetime import datetime
import uuid

from ..config.settings import settings
from ..models.document import ProcessingStatus, DocumentResponse

logger = logging.getLogger(__name__)

class DocumentProcessorService:
    """Service for handling document processing operations"""
    
    def __init__(self):
        self.s3_client = boto3.client('s3', region_name=settings.aws_region)
        self.lambda_client = boto3.client('lambda', region_name=settings.aws_region)
        
        # For now, we'll store status in memory (later move to database)
        self.document_status: Dict[str, Dict[str, Any]] = {}
    
    async def upload_and_process(
        self, 
        document_id: str, 
        filename: str, 
        file_content: bytes
    ) -> Dict[str, Any]:
        """
        Upload document to S3 and trigger processing
        
        Args:
            document_id: Unique document identifier
            filename: Original filename
            file_content: File content as bytes
            
        Returns:
            Upload result with S3 key
        """
        try:
            # Generate S3 key
            s3_key = f"uploads/{document_id}/{filename}"
            
            # Upload to S3
            self.s3_client.put_object(
                Bucket=settings.s3_document_bucket,
                Key=s3_key,
                Body=file_content,
                ContentType='application/pdf',
                Metadata={
                    'document_id': document_id,
                    'original_filename': filename,
                    'upload_timestamp': datetime.utcnow().isoformat()
                }
            )
            
            # Store document status
            self.document_status[document_id] = {
                'document_id': document_id,
                'filename': filename,
                'status': ProcessingStatus.UPLOADED,
                'upload_timestamp': datetime.utcnow(),
                's3_key': s3_key,
                'processing_started': None,
                'processing_completed': None,
                'error_message': None
            }
            
            # TODO: Trigger Lambda function for processing
            # For now, we'll simulate processing start
            await self._simulate_processing_start(document_id)
            
            logger.info(f"Document uploaded to S3: {s3_key}")
            
            return {
                's3_key': s3_key,
                'document_id': document_id,
                'status': 'uploaded'
            }
            
        except Exception as e:
            logger.error(f"Error uploading document: {str(e)}")
            raise
    
    async def get_processing_status(self, document_id: str) -> Optional[Dict[str, Any]]:
        """
        Get the current processing status of a document
        
        Args:
            document_id: Unique document identifier
            
        Returns:
            Document status information or None if not found
        """
        return self.document_status.get(document_id)
    
    async def get_processing_results(self, document_id: str) -> Optional[Dict[str, Any]]:
        """
        Get the processing results for a completed document
        
        Args:
            document_id: Unique document identifier
            
        Returns:
            Processing results or None if not found/completed
        """
        status_info = self.document_status.get(document_id)
        
        if not status_info or status_info['status'] != ProcessingStatus.COMPLETED:
            return None
        
        # TODO: Fetch actual results from S3
        # For now, return mock results
        return {
            'total_pages': 3,
            'extracted_text': 'Sample extracted text from the document...',
            'tables_found': 2,
            'forms_found': 1,
            'signatures_found': 1,
            'confidence_scores': {
                'overall': 0.95,
                'text_extraction': 0.97,
                'table_detection': 0.92
            },
            'processing_time': 15.5
        }
    
    async def list_documents(
        self, 
        limit: int = 10, 
        offset: int = 0, 
        status: Optional[ProcessingStatus] = None
    ) -> List[DocumentResponse]:
        """
        List documents with optional filtering
        
        Args:
            limit: Maximum number of documents to return
            offset: Number of documents to skip
            status: Filter by processing status
            
        Returns:
            List of document responses
        """
        documents = list(self.document_status.values())
        
        # Filter by status if provided
        if status:
            documents = [doc for doc in documents if doc['status'] == status]
        
        # Apply pagination
        documents = documents[offset:offset + limit]
        
        return [DocumentResponse(**doc) for doc in documents]
    
    async def delete_document(self, document_id: str) -> bool:
        """
        Delete a document and its processing results
        
        Args:
            document_id: Unique document identifier
            
        Returns:
            True if deleted successfully, False if not found
        """
        if document_id not in self.document_status:
            return False
        
        try:
            # Get document info
            doc_info = self.document_status[document_id]
            
            # Delete from S3
            if doc_info.get('s3_key'):
                self.s3_client.delete_object(
                    Bucket=settings.s3_document_bucket,
                    Key=doc_info['s3_key']
                )
            
            # Remove from status tracking
            del self.document_status[document_id]
            
            logger.info(f"Document deleted: {document_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error deleting document {document_id}: {str(e)}")
            raise
    
    async def _simulate_processing_start(self, document_id: str):
        """
        Simulate processing start (temporary until Lambda integration)
        
        Args:
            document_id: Document to start processing
        """
        # Update status to processing
        if document_id in self.document_status:
            self.document_status[document_id].update({
                'status': ProcessingStatus.PROCESSING,
                'processing_started': datetime.utcnow()
            })
            
            # Simulate processing completion after 10 seconds
            asyncio.create_task(self._simulate_processing_completion(document_id))
    
    async def _simulate_processing_completion(self, document_id: str):
        """
        Simulate processing completion (temporary)
        
        Args:
            document_id: Document to complete processing
        """
        await asyncio.sleep(10)  # Simulate processing time
        
        if document_id in self.document_status:
            self.document_status[document_id].update({
                'status': ProcessingStatus.COMPLETED,
                'processing_completed': datetime.utcnow()
            })
            
            logger.info(f"Document processing completed: {document_id}")