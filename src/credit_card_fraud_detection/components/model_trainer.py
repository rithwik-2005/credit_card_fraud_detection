import pandas as pd
import os
from src.credit_card_fraud_detection.entity.config_entity import ModelTrainerConfig
from src.credit_card_fraud_detection.logging.logger import logger
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib

class ModelTrainer:
    def __init__(self,config:ModelTrainerConfig):
        self.config=config
    
    def train_test_data_split(self):
        try:
            df=pd.read_csv(self.config.input_data_path)
            logger.info("Data is import successfully to split")
            input_part_data=df.drop([self.config.target_column],axis=1)
            output_part_data=df[self.config.target_column]
            logger.info("Data is divided into two parts input and output")
            x_train,x_test,y_train,y_test=train_test_split(input_part_data,
                                                           output_part_data,
                                                           random_state=self.config.random_state,
                                                          test_size=self.config.test_size)
            logger.info("data is successfully divided using train_test_split")
            x_train.to_csv(self.config.x_train_data_path)
            x_test.to_csv(self.config.x_test_data_path)
            y_train.to_csv(self.config.y_train_data_path)
            y_test.to_csv(self.config.y_test_data_path)
            logger.info("splitted data is successfully saved in the root_dir folder")
        except Exception as e:
            logger.exception(e)
            raise e
        return x_train,x_test,y_train,y_test

    def model_training(self):
        try:
            x_train,x_test,y_train,y_test=self.train_test_data_split()
            model=RandomForestClassifier(random_state=self.config.random_state)
            model.fit(x_train,y_train)
            joblib.dump(model,os.path.join(self.config.root_dir,self.config.model_name))
        except Exception as e:
            logger.exception(e)
            raise e
            

