import os
from src.credit_card_fraud_detection import logger
from src.credit_card_fraud_detection.entity.config_entity import DataIngestionConfig
import shutil

class DataIngestion:
    def __init__(self, config: DataIngestionConfig):
        self.config = config


    def copy_file(self):
        os.makedirs(self.config.root_dir, exist_ok=True)

        shutil.copy(
            self.config.source_file,
            self.config.local_data_file
        )

        logger.info("Dataset copied successfully to artifacts folder")