from datetime import datetime
from typing import List, Optional
from app.modules.documents.models import Document, DocumentStatus
from app.modules.documents.schemas import ProcessingTimelineItem

TIMELINE_STAGES = [
    {"key": "fetched", "label": "Fetched from Source", "status_match": [DocumentStatus.FETCHED, DocumentStatus.NORMALIZED, DocumentStatus.CHUNKED, DocumentStatus.EMBEDDED, DocumentStatus.GRAPH_BUILT, DocumentStatus.READY]},
    {"key": "normalized", "label": "Normalized", "status_match": [DocumentStatus.NORMALIZED, DocumentStatus.CHUNKED, DocumentStatus.EMBEDDED, DocumentStatus.GRAPH_BUILT, DocumentStatus.READY]},
    {"key": "chunked", "label": "Chunked", "status_match": [DocumentStatus.CHUNKED, DocumentStatus.EMBEDDED, DocumentStatus.GRAPH_BUILT, DocumentStatus.READY]},
    {"key": "embedded", "label": "Embedded", "status_match": [DocumentStatus.EMBEDDED, DocumentStatus.GRAPH_BUILT, DocumentStatus.READY]},
    {"key": "graph_built", "label": "Graph Built", "status_match": [DocumentStatus.GRAPH_BUILT, DocumentStatus.READY]},
    {"key": "ready", "label": "Ready", "status_match": [DocumentStatus.READY]},
]

STATUS_ORDER = {
    DocumentStatus.PENDING: 0,
    DocumentStatus.FETCHED: 1,
    DocumentStatus.NORMALIZED: 2,
    DocumentStatus.CHUNKED: 3,
    DocumentStatus.EMBEDDED: 4,
    DocumentStatus.GRAPH_BUILT: 5,
    DocumentStatus.READY: 6,
    DocumentStatus.FAILED: -1,
}

def generate_document_timeline(doc: Document) -> List[ProcessingTimelineItem]:
    """
    Derives the processing timeline based on the current Document state.
    """
    timeline = []
    current_status_val = STATUS_ORDER.get(doc.status, 0)
    
    for i, stage in enumerate(TIMELINE_STAGES):
        stage_status_val = i + 1  # 1 to 6
        
        status = "pending"
        timestamp: Optional[datetime] = None
        
        if doc.status == DocumentStatus.FAILED:
            # If failed, the stage right after the last successful one is FAILED
            if stage_status_val == 1 and current_status_val < 1:
                status = "failed"
                timestamp = doc.updated_at
            elif stage_status_val == current_status_val + 1:
                status = "failed"
                timestamp = doc.updated_at
            elif stage_status_val <= current_status_val:
                status = "completed"
                # Fallback to last_synced_at or updated_at for completed steps 
                timestamp = doc.last_synced_at or doc.updated_at
        else:
            if stage_status_val < current_status_val:
                status = "completed"
                timestamp = doc.last_synced_at or doc.updated_at
            elif stage_status_val == current_status_val:
                if doc.status == DocumentStatus.READY:
                    status = "completed"
                else:
                    status = "current"
                timestamp = doc.updated_at
            else:
                status = "pending"
                
        timeline.append(
            ProcessingTimelineItem(
                key=stage["key"],
                label=stage["label"],
                status=status,
                timestamp=timestamp
            )
        )
        
    return timeline
