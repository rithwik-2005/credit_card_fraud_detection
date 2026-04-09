import os
from flask import Flask, render_template, request
import pandas as pd
import requests

APP_DIR = os.path.dirname(os.path.abspath(__file__))
app = Flask(
    __name__,
    template_folder=os.path.join(APP_DIR, "..", "templates")
)

# Get FastAPI URL from environment, default to localhost for local dev
FASTAPI_URL = os.getenv("FASTAPI_URL", "http://localhost:8000/predict")

# Path to raw data for dropdown values
RAW_CSV_PATH = os.path.join(APP_DIR, "..", "artifacts", "data_ingestion", "raw.csv")

try:
    df = pd.read_csv(RAW_CSV_PATH)
    transaction_types = sorted(df["TransactionType"].dropna().unique())
    locations = sorted(df["Location"].dropna().unique())
    print(f"[OK] Loaded dropdown values from {RAW_CSV_PATH}")
except FileNotFoundError:
    # Hardcoded fallback so Flask starts even if raw.csv is missing
    print(f"[WARN] {RAW_CSV_PATH} not found — using hardcoded fallback dropdown values")
    transaction_types = ["purchase", "refund"]
    locations = [
        "Austin", "Chicago", "Dallas", "Houston",
        "Los Angeles", "Miami", "New York",
        "Phoenix", "San Antonio", "San Diego"
    ]


@app.route("/")
def landing():
    return render_template("landing.html")


@app.route("/predict_page", methods=["GET", "POST"])
def predict_page():
    if request.method == "POST":
        data = {
            "TransactionID": int(request.form["TransactionID"]),
            "TransactionDate": request.form["TransactionDate"],
            "Amount": float(request.form["Amount"]),
            "MerchantID": int(request.form["MerchantID"]),
            "TransactionType": request.form["TransactionType"],
            "Location": request.form["Location"]
        }

        try:
            response = requests.post(FASTAPI_URL, json=data, timeout=30)
            response.raise_for_status()
            prediction_json = response.json()
            prediction = prediction_json.get("message", str(prediction_json))
        except requests.exceptions.ConnectionError:
            prediction = "❌ Prediction service unavailable — FastAPI not reachable"
        except requests.exceptions.Timeout:
            prediction = "❌ Prediction timed out — please try again"
        except Exception as e:
            prediction = f"❌ Unexpected error: {str(e)}"

        return render_template("result.html", prediction=prediction)

    return render_template(
        "predict.html",
        transaction_types=transaction_types,
        locations=locations
    )


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
