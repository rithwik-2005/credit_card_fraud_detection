from src.credit_card_fraud_detection.config.configuration import ConfiguartionManager
from src.credit_card_fraud_detection.components.data_validation import DataValidation
from src.credit_card_fraud_detection.logging import logger

STAGE_NAME="Data Validation Stage"

class DataValidationTriningPipeline:
    def __init__(self):
        pass

    def initiate_data_validation(self):
        config=ConfiguartionManager()
        data_validation_config=config.get_data_validation_config()
        data_validation=DataValidation(config=data_validation_config)
        data_validation.validate_all_columns()

if __name__=="__main__":
    try:
        logger.info(f"stage {STAGE_NAME} started")
        obj=DataValidationTriningPipeline()
        obj.initiate_data_validation()
        logger.info(f"stage {STAGE_NAME} completed")
    
    except Exception as e:
        logger.exception(e)
        raise e