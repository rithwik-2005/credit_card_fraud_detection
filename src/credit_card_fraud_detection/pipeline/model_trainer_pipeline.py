from src.credit_card_fraud_detection.config.configuration import ConfigurationManager
from src.credit_card_fraud_detection.components.model_trainer import ModelTrainer
from src.credit_card_fraud_detection.logging.logger import logger

STAGE_NAME="Model Trainer"

class ModelTrainerPipeline:
    def __init__(self):
        pass
    def initiate_model_trainer(self):
        try:
            config=ConfigurationManager()
            model_trainer_config=config.get_model_trainer_config()
            model_trainer=ModelTrainer(config=model_trainer_config)
            model_trainer.model_training()
        except Exception as e:
            logger.exception(e)
            raise e
