# AI-Powered Cybersecurity Threat Detection and Investigation Agent


## 1. Problem
Traditional security teams receive large amounts of network telemetry. Manually checking every flow is slow. The project provides a prototype that prioritizes suspicious flows and produces an investigation-oriented explanation.

## 2. Architecture
- FastAPI: service/API layer
- Pandas/NumPy: data preparation
- Random Forest: threat classification
- Isolation Forest: anomaly signal
- LangGraph: investigation workflow
- Gemini: natural-language explanation
- SQLite: incident history
- HTML/CSS/JS: analyst dashboard

## 3. Live demonstration
1. Start `uvicorn app.main:app --reload`.
2. Open the dashboard.
3. Upload `data/demo_network_traffic.csv`.
4. Explain one PORT_SCAN incident:
   - many destination ports
   - high SYN count
   - classifier confidence
   - anomaly score
5. Explain one BRUTE_FORCE incident:
   - repeated failed logins
   - sensitive service port
6. Open `/docs`.
7. Execute `/api/detect` with a single record.
8. Show the returned investigation summary.
9. Open incident history.

## 4. Important academic point
The ML prediction is not treated as unquestionable truth. The system presents evidence and asks the analyst to validate related logs before taking action. This is safer and more realistic than an automatic blocking system.
