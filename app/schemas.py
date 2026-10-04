from typing import Optional
from pydantic import BaseModel, Field


class TrafficRecord(BaseModel):
    duration: float = Field(ge=0)
    protocol: str = Field(min_length=1, max_length=10)
    src_bytes: float = Field(ge=0)
    dst_bytes: float = Field(ge=0)
    packets: float = Field(ge=1)
    bytes_per_packet: float = Field(ge=0)
    syn_count: float = Field(ge=0)
    ack_count: float = Field(ge=0)
    failed_logins: float = Field(ge=0)
    unique_dst_ports: float = Field(ge=0)
    dst_port: int = Field(ge=0, le=65535)
    flow_rate: float = Field(ge=0)


class PredictionResponse(BaseModel):
    threat: str
    confidence: float
    anomaly_score: float
    risk_score: float
    evidence: list[str]
    summary: str
    incident_id: Optional[int] = None
