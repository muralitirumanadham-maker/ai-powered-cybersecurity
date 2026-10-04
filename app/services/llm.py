from app.config import settings


def local_summary(result):
    threat = result["threat"]
    confidence = result["confidence"]
    risk = result["risk_score"]
    evidence = "; ".join(result["evidence"])

    if risk >= 75:
        severity = "high"
    elif risk >= 45:
        severity = "medium"
    else:
        severity = "low"

    return (
        f"The detector classified this flow as {threat} with "
        f"{confidence:.1%} model confidence. The calculated risk level is "
        f"{severity} ({risk:.1f}/100). Evidence: {evidence}. "
        "An analyst should validate the source host, destination, time window, "
        "related flows and authentication/network logs before taking action."
    )


def gemini_summary(result):
    if not settings.gemini_api_key:
        return local_summary(result)

    try:
        from google import genai

        client = genai.Client(api_key=settings.gemini_api_key)
        prompt = f"""
You are a SOC analyst assistant. Summarize this machine-learning detection.
Do not invent facts. Clearly separate model output from analyst verification.

Threat: {result['threat']}
Confidence: {result['confidence']}
Anomaly score: {result['anomaly_score']}
Risk score: {result['risk_score']}
Evidence:
- """ + "\n- ".join(result["evidence"]) + """

Return:
1. What was detected
2. Why it is suspicious
3. Evidence
4. Safe investigation steps
5. What the analyst should verify next
"""
        response = client.models.generate_content(
            model=settings.gemini_model,
            contents=prompt,
        )
        return response.text.strip()
    except Exception as exc:
        # Keep the system usable if the external LLM is unavailable.
        return local_summary(result) + f" Gemini fallback reason: {type(exc).__name__}."
