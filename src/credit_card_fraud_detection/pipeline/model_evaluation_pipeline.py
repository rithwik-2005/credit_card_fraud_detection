from src.credit_card_fraud_detection.config.configuration import ConfigurationManager
from src.credit_card_fraud_detection.components.model_evaluation import ModelEvaluation
from src.credit_card_fraud_detection.logging.logger import logger

class ModelEvaluationPipeline:
    def __init__(self):
        pass
    def initiate_model_evaluation(self):
        try:
            config=ConfigurationManager()
            model_evaluation_config=config.get_model_evaluation_config()
            model_evaluation=ModelEvaluation(config=model_evaluation_config)
            model_evaluation.log_into_mlflow()
        except Exception as e:
            logger.exception(e)
            raise e