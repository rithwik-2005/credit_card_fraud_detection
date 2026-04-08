import sys
from src.credit_card_fraud_detection.logging.logger import logger
from src.credit_card_fraud_detection.pipeline.data_ingestion_pipeline import DataIngestionTrainingPipeline
from src.credit_card_fraud_detection.pipeline.data_validation_pipeline import DataValidationTrainingPipeline
from src.credit_card_fraud_detection.pipeline.data_transformation_pipeline import DataTransformationPipeline
from src.credit_card_fraud_detection.pipeline.model_trainer_pipeline import ModelTrainerPipeline
from src.credit_card_fraud_detection.pipeline.model_evaluation_pipeline import ModelEvaluationPipeline

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

STAGE_NAME="Data Ingestion Stage"
try:
    logger.info(f"stage {STAGE_NAME} started")
    data_ingestion=DataIngestionTrainingPipeline()
    data_ingestion.initiate_data_ingestion()
    logger.info(f"stage {STAGE_NAME} completed\n\n")
except Exception as e:
    logger.exception(e)
    raise e


STAGE_NAME="Data Validation Stage"
try:
    logger.info(f"stage {STAGE_NAME} is started")
    data_validation=DataValidationTrainingPipeline()
    data_validation.initiate_data_validation()
    logger.info(f"stage {STAGE_NAME} is completed\n\n")
except Exception as e:
    logger.exception(e)
    raise e

STAGE_NAME="Data Transformation Stage"
try:
    logger.info(f"stage {STAGE_NAME} started")
    data_transformation=DataTransformationPipeline()
    data_transformation.initiate_data_transformation()
    logger.info(f"stage {STAGE_NAME} is completed\n\n")
except Exception as e:
    logger.exception(e)
    raise e

STAGE_NAME="Model Trainer Stage"
try:
    logger.info(f"stage {STAGE_NAME} is started")
    model_trainer=ModelTrainerPipeline()
    model_trainer.initiate_model_trainer()
    logger.info(f"stage {STAGE_NAME} is completed\n\n")
except Exception as e:
    logger.exception(e)
    raise e

STAGE_NAME="Model Evaluation Stage"
try:
    logger.info(f"stage {STAGE_NAME} started")
    model_evaluation=ModelEvaluationPipeline()
    model_evaluation.initiate_model_evaluation()
    logger.info(f"stage {STAGE_NAME} is completed")
except Exception as e:
    logger.exception(e)
    raise e
