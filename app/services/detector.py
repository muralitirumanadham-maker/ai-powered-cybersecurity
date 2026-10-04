from pathlib import Path
import joblib
import pandas as pd
import numpy as np
from app.config import settings

REQUIRED = [
    "duration", "protocol", "src_bytes", "dst_bytes", "packets",
    "bytes_per_packet", "syn_count", "ack_count", "failed_logins",
    "unique_dst_ports", "dst_port", "flow_rate"
]

_classifier = None
_anomaly = None


def load_models():
    global _classifier, _anomaly
    if not Path(settings.model_path).exists() or not Path(settings.anomaly_model_path).exists():
        raise FileNotFoundError(
            "ML models are missing. Run 'python -m src.generate_demo_data' "
            "and 'python -m src.train' first."
        )
    _classifier = joblib.load(settings.model_path)
    _anomaly = joblib.load(settings.anomaly_model_path)


def ensure_models():
    if _classifier is None or _anomaly is None:
        load_models()


def evidence(row):
    e = []
    if row["unique_dst_ports"] >= 15:
        e.append(f"High destination-port diversity: {int(row['unique_dst_ports'])} ports")
    if row["syn_count"] >= 20:
        e.append(f"High SYN activity: {int(row['syn_count'])}")
    if row["failed_logins"] >= 8:
        e.append(f"Repeated failed logins: {int(row['failed_logins'])}")
    if row["flow_rate"] >= 150:
        e.append(f"High packet flow rate: {row['flow_rate']:.1f} packets/s")
    if row["src_bytes"] >= 100000:
        e.append(f"Large outbound source volume: {row['src_bytes']:.0f} bytes")
    if row["dst_port"] in [21, 22, 23, 3389] and row["failed_logins"] >= 5:
        e.append(f"Sensitive service port with failed authentication: {int(row['dst_port'])}")
    return e or ["No single high-signal indicator exceeded the demo thresholds."]


def predict(row: dict):
    ensure_models()
    df = pd.DataFrame([row])
    threat = str(_classifier.predict(df)[0])
    probabilities = _classifier.predict_proba(df)[0]
    confidence = float(np.max(probabilities))

    raw_anomaly = float(_anomaly.decision_function(df)[0])
    anomaly_score = float(np.clip(0.5 - raw_anomaly, 0, 1))

    evidence_items = evidence(row)
    evidence_factor = min(len(evidence_items) / 4, 1)
    risk = float(np.clip(
        100 * (0.55 * confidence + 0.30 * anomaly_score + 0.15 * evidence_factor),
        0, 100
    ))

    return {
        "threat": threat,
        "confidence": round(confidence, 4),
        "anomaly_score": round(anomaly_score, 4),
        "risk_score": round(risk, 2),
        "evidence": evidence_items,
    }
