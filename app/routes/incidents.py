import json
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import Incident, get_db

router = APIRouter(prefix="/api/incidents", tags=["Incidents"])


@router.get("")
def list_incidents(limit: int = 50, db: Session = Depends(get_db)):
    limit = max(1, min(limit, 200))
    rows = (
        db.query(Incident)
        .order_by(Incident.created_at.desc())
        .limit(limit)
        .all()
    )
    return [
        {
            "id": r.id,
            "threat": r.threat,
            "confidence": r.confidence,
            "anomaly_score": r.anomaly_score,
            "risk_score": r.risk_score,
            "evidence": json.loads(r.evidence),
            "summary": r.summary,
            "created_at": r.created_at.isoformat() if r.created_at else None,
        }
        for r in rows
    ]


@router.delete("")
def clear_incidents(db: Session = Depends(get_db)):
    """Delete all stored incidents so the dashboard returns to a clean state."""
    deleted = db.query(Incident).delete(synchronize_session=False)
    db.commit()
    return {"message": "All incidents cleared successfully.", "deleted_count": deleted}
