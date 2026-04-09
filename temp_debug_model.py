from pathlib import Path
import sys
sys.path.append(r'd:/major_ml/credit_card_fraud_detection')
from src.credit_card_fraud_detection.pipeline.prediction_pipeline import PredictionPipeline
print('model file exists:', Path('artifacts/model_trainer/model.joblib').exists())
p = PredictionPipeline()
print('loaded model type:', type(p.model))
