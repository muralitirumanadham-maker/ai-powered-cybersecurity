# AI-Powered Cybersecurity Threat Detection and Investigation Agent

**Project short name:** CyberGuard AI
## AI-Powered Cybersecurity Threat Detection and Investigation Agent

A practical final-year project that combines:
- Machine Learning for network-threat classification
- Isolation Forest for anomaly scoring
- LangGraph for an investigation workflow
- Gemini (optional) for analyst-friendly incident explanations
- FastAPI for backend APIs
- A lightweight HTML/CSS/JavaScript dashboard
- SQLite for incident history

### Project basis
This implementation follows the project abstract supplied for the final-year project:
"AI-Powered Cybersecurity Threat Detection and Investigation Agent".
The abstract specifies Python/NumPy/Pandas preprocessing, Scikit-learn detection/classification, a LangGraph investigation workflow, Gemini explanations, and FastAPI integration.

### What makes this a realistic prototype
1. A security analyst can upload a CSV of network-flow records.
2. The system validates and preprocesses the records.
3. ML predicts a threat category and probability.
4. An anomaly detector adds an independent anomaly score.
5. A LangGraph workflow builds an investigation package.
6. Gemini can convert that package into an understandable incident report.
7. Incidents are stored in SQLite and shown on the dashboard.
8. The system also has a safe "demo traffic generator" for college demonstration.

> Important: The included synthetic dataset/model is for demonstration and development. It is not a production IDS and must not be represented as a validated real-world security detector. For serious evaluation, train/evaluate on a labeled dataset such as CICIDS2017/UNSW-NB15 and report precision, recall, F1 and confusion matrix.

---

## 1. Folder structure

```text
cyber_guard_ai/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── database.py
│   ├── schemas.py
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── health.py
│   │   ├── detect.py
│   │   └── incidents.py
│   └── services/
│       ├── __init__.py
│       ├── detector.py
│       ├── investigation.py
│       └── llm.py
├── src/
│   ├── __init__.py
│   ├── features.py
│   ├── generate_demo_data.py
│   └── train.py
├── frontend/
│   └── index.html
├── data/
│   ├── demo_network_traffic.csv
│   └── README.md
├── models/
├── tests/
│   └── test_api.py
├── .env.example
├── .gitignore
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── README.md
```

## 2. Windows setup

```powershell
cd cyber_guard_ai
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
```

Generate demo traffic and train the model:

```powershell
python -m src.generate_demo_data
python -m src.train
```

Start the API:

```powershell
uvicorn app.main:app --reload
```

Open:

- Dashboard: http://127.0.0.1:8000/
- Swagger: http://127.0.0.1:8000/docs
- Health: http://127.0.0.1:8000/api/health

## 3. Gemini setup

Gemini is optional. The application still works without an API key using a deterministic local explanation engine.

Create `.env`:

```env
GEMINI_API_KEY=your_key_here
GEMINI_MODEL=gemini-2.5-flash
```

Do not commit `.env`.

## 4. CSV format

The API accepts these columns:

```text
duration,protocol,src_bytes,dst_bytes,packets,bytes_per_packet,
syn_count,ack_count,failed_logins,unique_dst_ports,dst_port,flow_rate,threat
```

`threat` is required for training but optional during prediction.

Threat classes in the demo:
- BENIGN
- PORT_SCAN
- BRUTE_FORCE
- DOS
- DATA_EXFILTRATION

For real datasets, add a dataset adapter that maps the source dataset's columns into this canonical schema.

## 5. API examples

### Single prediction

```http
POST /api/detect
Content-Type: application/json
```

```json
{
  "duration": 2.4,
  "protocol": "TCP",
  "src_bytes": 180,
  "dst_bytes": 90,
  "packets": 40,
  "bytes_per_packet": 6.75,
  "syn_count": 32,
  "ack_count": 4,
  "failed_logins": 0,
  "unique_dst_ports": 24,
  "dst_port": 443,
  "flow_rate": 16.7
}
```

### CSV upload

```http
POST /api/detect/upload
multipart/form-data
file=<traffic.csv>
```

### Incident history

```http
GET /api/incidents
```

## 6. Investigation workflow

```text
Network flow
   ↓
Feature validation
   ↓
Random Forest threat classifier
   ↓
Isolation Forest anomaly detector
   ↓
Evidence extraction
   ↓
Risk scoring
   ↓
LangGraph investigation state
   ↓
Gemini explanation (optional)
   ↓
Incident record + dashboard
```

## 7. Demo flow for your project presentation

1. Open dashboard.
2. Click "Load demo data".
3. Show the generated traffic table.
4. Click "Analyze".
5. Show threat type, confidence and risk.
6. Open the incident explanation.
7. Show evidence such as unusual ports, SYN activity, failed logins and traffic rate.
8. Open incident history.
9. Open `/docs` and demonstrate the API.
10. Explain that Gemini is the natural-language analyst layer, while the ML model is responsible for detection.

## 8. Suggested evaluation for the final report

For a proper academic evaluation, compare:
- Random Forest
- Logistic Regression
- Isolation Forest

Report:
- Accuracy
- Precision
- Recall
- F1-score
- Confusion matrix
- ROC-AUC where applicable
- Inference time

Also evaluate the investigation agent qualitatively:
- Correctness of threat summary
- Evidence coverage
- Recommended analyst actions
- Hallucination rate when using the LLM

## 9. Production hardening ideas

- Authentication and role-based access
- HTTPS
- Redis/Celery for asynchronous analysis
- PostgreSQL instead of SQLite
- Model versioning
- SIEM integration
- Syslog ingestion
- PCAP/Zeek/Suricata adapters
- Alert deduplication
- Human analyst approval before remediation
- Audit logs
- Rate limiting
- Secret management
- Model drift monitoring

This repository intentionally does not perform automatic blocking, firewall changes, credential attacks, or destructive remediation.
