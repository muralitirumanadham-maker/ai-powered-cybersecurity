import io
import json
from pathlib import Path

import pandas as pd
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.database import Incident, get_db
from app.schemas import TrafficRecord, PredictionResponse
from app.services.detector import predict
from app.services.investigation import investigate

router = APIRouter(prefix="/api", tags=["Detection"])

REQUIRED = [
    "duration", "protocol", "src_bytes", "dst_bytes", "packets",
    "bytes_per_packet", "syn_count", "ack_count", "failed_logins",
    "unique_dst_ports", "dst_port", "flow_rate"
]


def save_incident(db, result):
    incident = Incident(
        threat=result["threat"],
        confidence=result["confidence"],
        anomaly_score=result["anomaly_score"],
        risk_score=result["risk_score"],
        evidence=json.dumps(result["evidence"]),
        summary=result["summary"],
    )
    db.add(incident)
    db.commit()
    db.refresh(incident)
    return incident.id


def analyze_dataframe(df, db, limit=50):
    missing = [c for c in REQUIRED if c not in df.columns]
    if missing:
        raise HTTPException(400, {"missing_columns": missing})

    results = []
    for _, row in df.head(limit).iterrows():
        item = {k: row[k] for k in REQUIRED}
        result = predict(item)
        result["summary"] = investigate(result)
        result["incident_id"] = save_incident(db, result)
        results.append(result)
    return results


@router.post("/detect", response_model=PredictionResponse)
def detect(record: TrafficRecord, db: Session = Depends(get_db)):
    result = predict(record.model_dump())
    result["summary"] = investigate(result)
    result["incident_id"] = save_incident(db, result)
    return result


@router.post("/detect/upload")
async def detect_upload(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    if not file.filename.lower().endswith(".csv"):
        raise HTTPException(400, "Only CSV files are supported.")

    raw = await file.read()
    try:
        df = pd.read_csv(io.BytesIO(raw))
    except Exception as exc:
        raise HTTPException(400, f"Invalid CSV: {exc}")

    results = analyze_dataframe(df, db, limit=50)

    return {
        "filename": file.filename,
        "processed_rows": len(results),
        "results": results,
    }


@router.post("/demo/analyze")
def analyze_demo(
    db: Session = Depends(get_db),
):
    """
    Analyze the bundled synthetic demo dataset.
    The endpoint processes 50 rows per click so the demo remains responsive.
    """
    demo_path = Path("data/demo_network_traffic.csv")
    if not demo_path.exists():
        raise HTTPException(
            404,
            "Demo dataset not found. Run: python -m src.generate_demo_data"
        )

    try:
        df = pd.read_csv(demo_path)
    except Exception as exc:
        raise HTTPException(500, f"Could not read demo dataset: {exc}")

    results = analyze_dataframe(df, db, limit=50)

    return {
        "filename": demo_path.name,
        "processed_rows": len(results),
        "results": results,
    }
