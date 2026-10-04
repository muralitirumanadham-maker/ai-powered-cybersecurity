from pathlib import Path
import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier, IsolationForest
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from src.features import FEATURE_COLUMNS, NUMERIC_COLUMNS

DATA = Path("data/demo_network_traffic.csv")
MODEL_DIR = Path("models")
MODEL = MODEL_DIR / "threat_classifier.joblib"
ANOMALY = MODEL_DIR / "anomaly_detector.joblib"


def main():
    if not DATA.exists():
        raise FileNotFoundError("Run: python -m src.generate_demo_data")

    df = pd.read_csv(DATA)
    X = df[FEATURE_COLUMNS]
    y = df["threat"]

    categorical = ["protocol"]
    numeric = NUMERIC_COLUMNS

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", StandardScaler(), numeric),
            ("cat", OneHotEncoder(handle_unknown="ignore"), categorical),
        ]
    )

    clf = Pipeline([
        ("preprocess", preprocessor),
        ("model", RandomForestClassifier(
            n_estimators=250,
            random_state=42,
            class_weight="balanced",
            n_jobs=-1,
        )),
    ])

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    clf.fit(X_train, y_train)

    pred = clf.predict(X_test)
    print(classification_report(y_test, pred))

    # Isolation Forest is intentionally trained on the normal subset.
    normal = X_train[y_train == "BENIGN"]
    anomaly_preprocessor = ColumnTransformer(
        transformers=[
            ("num", StandardScaler(), numeric),
            ("cat", OneHotEncoder(handle_unknown="ignore"), categorical),
        ]
    )
    anomaly_model = Pipeline([
        ("preprocess", anomaly_preprocessor),
        ("model", IsolationForest(
            n_estimators=200,
            contamination=0.08,
            random_state=42,
        )),
    ])
    anomaly_model.fit(normal)

    MODEL_DIR.mkdir(exist_ok=True)
    joblib.dump(clf, MODEL)
    joblib.dump(anomaly_model, ANOMALY)
    print(f"Saved {MODEL}")
    print(f"Saved {ANOMALY}")


if __name__ == "__main__":
    main()
