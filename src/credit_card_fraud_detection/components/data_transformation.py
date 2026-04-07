import os
from src.credit_card_fraud_detection.entity.config_entity import DataTransformationConfig
from src.credit_card_fraud_detection.logging.logger import logger
import pandas as pd

class DataTransformation:
    def __init__(self,config: DataTransformationConfig):
        self.config=config
    
    def transform_data(self):
        try:
            logger.info("Starting data transformation process")
            #load the data
            df=pd.read_csv(self.config.input_data_path)
            logger.info("Dataset loaded successfully")
            #onehotencoding using pandas get_dummies
            #convert the date_time_column data type to datetime
            df[self.config.date_time_column]=pd.to_datetime(df[self.config.date_time_column],errors="coerce")
            logger.info("Datetime column converted successfully")
            df["day_of_week"]=df[self.config.date_time_column].dt.dayofweek
            df["hour"]=df[self.config.date_time_column].dt.hour
            logger.info("Datetime feature extraction is completed")
            df.drop(self.config.date_time_column,axis=1,inplace=True)
            df=pd.get_dummies(df,columns=self.config.encoding_columns,drop_first=self.config.drop_first)
            logger.info("Categorical encoding completed")
            #if root folder doesn't created by the configuation.py file then
            os.makedirs(self.config.root_dir,exist_ok=True)
            df.to_csv(self.config.transformed_data_path,index=False)
            logger.info("transformation dataset is completed")
        except Exception as e:
            logger.exception(e)
            raise e
        

        
        
        