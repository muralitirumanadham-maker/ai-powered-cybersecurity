from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "CyberGuard AI"
    database_url: str = "sqlite:///./cyber_guard.db"
    model_path: str = "models/threat_classifier.joblib"
    anomaly_model_path: str = "models/anomaly_detector.joblib"
    gemini_api_key: str = ""
    gemini_model: str = "gemini-2.5-flash"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
