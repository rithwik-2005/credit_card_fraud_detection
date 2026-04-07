from src.credit_card_fraud_detection.config.configuration import ConfigurationManager
from src.credit_card_fraud_detection.components.data_validation import DataValidation
from src.credit_card_fraud_detection.logging.logger import logger

STAGE_NAME="Data Validation Stage"

class DataValidationTriningPipeline:
    def __init__(self):
        pass

    def initiate_data_validation(self):
        config=ConfigurationManager()
        data_validation_config=config.get_data_validation_config()
        data_validation=DataValidation(config=data_validation_config)
        data_validation.validate_all_columns()

