from src.credit_card_fraud_detection.config.configuration import ConfiguartionManager
from src.credit_card_fraud_detection.components.data_ingestion import DataIngestion
from src.credit_card_fraud_detection.logging import logger

STAGE_NAME="Data Ingestion Stage"

class DataIngestionTrainingPipeline:
    def __init__(self):
        pass
    def initiate_data_ingestion(self):
        config=ConfiguartionManager()
        data_ingestion_config=config.get_data_ingestion_config()
        data_ingestion=DataIngestion(config=data_ingestion_config)
        data_ingestion.copy_file()
    

if __name__=='__main__':
    try:
        logger.info(f"stage {STAGE_NAME} started")
        obj=DataIngestionTrainingPipeline()
        obj.initiate_data_ingestion()
        logger.info(f"stage {STAGE_NAME} completed")
    except Exception as e:
        logger.exception(e)
        raise e