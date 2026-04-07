from src.credit_card_fraud_detection.config.configuration import ConfigurationManager
from src.credit_card_fraud_detection.components.data_ingestion import DataIngestion
from src.credit_card_fraud_detection.logging.logger import logger

STAGE_NAME="Data Ingestion Stage"

class DataIngestionTrainingPipeline:
    def __init__(self):
        pass
    def initiate_data_ingestion(self):
        config=ConfigurationManager()
        data_ingestion_config=config.get_data_ingestion_config()
        data_ingestion=DataIngestion(config=data_ingestion_config)
        data_ingestion.copy_file()
    

