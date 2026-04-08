from fastapi import FastAPI
from pydantic import BaseModel

from src.credit_card_fraud_detection.pipeline.prediction_pipeline import PredictionPipeline


app = FastAPI()

pipeline = PredictionPipeline()


class TransactionData(BaseModel):

    TransactionID: int
    TransactionDate: str
    Amount: float
    MerchantID: int
    TransactionType: str
    Location: str


@app.get("/")
def home():

    return {

        "message": "Fraud Detection API running successfully 🚀"

    }


@app.post("/predict")
def predict(data: TransactionData):

    result = pipeline.predict(data.dict())

    return result