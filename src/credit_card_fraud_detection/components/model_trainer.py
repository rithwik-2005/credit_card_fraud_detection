import pandas as pd
import os
from src.credit_card_fraud_detection.entity.config_entity import ModelTrainerConfig
from src.credit_card_fraud_detection.logging.logger import logger
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib
from imblearn.over_sampling import SMOTE

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
            x_train.to_csv(self.config.x_train_data_path, index=False)
            x_test.to_csv(self.config.x_test_data_path, index=False)
            y_train.to_csv(self.config.y_train_data_path, index=False)
            y_test.to_csv(self.config.y_test_data_path, index=False)
            logger.info("splitted data is successfully saved in the root_dir folder")
        except Exception as e:
            logger.exception(e)
            raise e
        return x_train,x_test,y_train,y_test

    def model_training(self):
        try:
            x_train,x_test,y_train,y_test=self.train_test_data_split()
            # Apply SMOTE to handle class imbalance
            smote = SMOTE(random_state=self.config.random_state)
            x_train, y_train = smote.fit_resample(x_train, y_train)
            logger.info("SMOTE applied to training data for class balancing")
            model=RandomForestClassifier(
                n_estimators=self.config.n_estimators,
                max_depth=self.config.max_depth,
                min_samples_split=self.config.min_samples_split,
                min_samples_leaf=self.config.min_samples_leaf,
                max_features=self.config.max_features,
                class_weight=self.config.class_weight,
                random_state=self.config.random_state
            )
            model.fit(x_train,y_train)
            joblib.dump(model,os.path.join(self.config.root_dir,self.config.model_name))
            logger.info("Model trained and saved successfully with hyperparameters and SMOTE")
        except Exception as e:
            logger.exception(e)
            raise e
            

