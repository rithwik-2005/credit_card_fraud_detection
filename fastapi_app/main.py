from typing import Any, Dict

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from src.credit_card_fraud_detection.pipeline.prediction_pipeline import PredictionPipeline


app = FastAPI()

# Load ML model on startup
pipeline = PredictionPipeline()


class TransactionData(BaseModel):
    """Schema for transaction data input"""
    TransactionID: int
    TransactionDate: str
    Amount: float
    MerchantID: int
    TransactionType: str
    Location: str


@app.get("/")
def home():
    """Health check endpoint"""
    return {
        "message": "Fraud Detection API running successfully 🚀"
    }


@app.post("/predict")
def predict(data: TransactionData) -> Dict[str, Any]:
    """
    Predict if transaction is fraud or legitimate.
    
    Args:
        data: TransactionData with transaction details
        
    Returns:
        Dict with prediction result and message
        
    Raises:
        HTTPException: If prediction fails
    """
    try:
        result = pipeline.predict(data.dict())
        return result
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Prediction failed: {exc}"
        )
