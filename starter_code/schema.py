from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, Dict, Any
from datetime import datetime

# ==========================================
# ROLE 1: LEAD DATA ARCHITECT
# ==========================================
# Your task is to define the Unified Schema for all sources.
# This is v1. Note: A breaking change is coming at 11:00 AM!

class UnifiedDocument(BaseModel):
    # TODO: Define the v1 schema. 
    # Suggested fields: document_id, content, source_type, author, timestamp, metadata
    
    # Allow tolerant ingestion while keeping a strict normalized output shape.
    model_config = ConfigDict(populate_by_name=True, extra="allow")

    document_id: str = Field(..., description="Stable unique identifier for the document")
    content: str = Field(..., min_length=1, description="Primary extracted content")
    source_type: str = Field(..., description="PDF/Video/HTML/CSV/Code/... source category")
    author: Optional[str] = Field(default="Unknown")
    timestamp: Optional[datetime] = Field(default=None)
    
    # You might want a dict for source-specific metadata
    source_metadata: Dict[str, Any] = Field(default_factory=dict)
