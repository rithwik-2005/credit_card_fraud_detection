from src.credit_card_fraud_detection.config.configuration import ConfigurationManager
from src.credit_card_fraud_detection.components.data_transformation import DataTransformation
from src.credit_card_fraud_detection.logging.logger import logger

STAGE_NAME="Data Transformation Stage"

class DataTransformationPipeline:
    def __init__(self):
        pass

    def initiate_data_transformation(self):
        try:
            config=ConfigurationManager()
            data_transformation_config=config.get_data_transformation_config()
            data_transformation=DataTransformation(config=data_transformation_config)
            data_transformation.transform_data()
        except Exception as e:
            raise e
        
            
