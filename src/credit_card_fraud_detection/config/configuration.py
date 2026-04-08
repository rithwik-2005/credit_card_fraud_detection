from dotenv import load_dotenv
import os
from src.credit_card_fraud_detection.constants import *
from src.credit_card_fraud_detection.utils.common import read_yaml,create_directories
from src.credit_card_fraud_detection.entity.config_entity import (DataIngestionConfig,
                                                                DataValidationConfig,
                                                                DataTransformationConfig,
                                                                ModelTrainerConfig,
                                                                ModelEvaluationConfig)


load_dotenv()


class ConfigurationManager:
    def __init__(self,
                 config_filepath=CONFIG_FILE_PATH,
                 params_filepath=PARAMS_FILE_PATH,
                 schema_filepath=SCHEMA_FILE_PATH):
        self.config=read_yaml(config_filepath)
        self.params=read_yaml(params_filepath)
        self.schema=read_yaml(schema_filepath)
        create_directories([self.config.artifact_root])
    
    def get_data_ingestion_config(self)->DataIngestionConfig:
        config=self.config.data_ingestion
        create_directories([config.root_dir])
        data_ingestion_config=DataIngestionConfig(
            root_dir=config.root_dir,
            source_file=config.source_file,
            local_data_file=config.local_data_file
        )
        return data_ingestion_config
    

    def get_data_validation_config(self)->DataValidationConfig:
        config=self.config.data_validation
        schema=self.schema.COLUMNS
        create_directories([config.root_dir])
        data_validation_config=DataValidationConfig(
            root_dir=config.root_dir,
            local_data_file=config.local_data_file,
            STATUS_FILE=config.STATUS_FILE,
            all_schema=schema
        )
        return data_validation_config
    
    def get_data_transformation_config(self)->DataTransformationConfig:
        config=self.config.data_transformation
        schema=self.schema
        create_directories([config.root_dir])
        data_transformation_config=DataTransformationConfig(
            root_dir=config.root_dir,
            input_data_path=config.input_data_path,
            transformed_data_path=config.transformed_data_path,
            encoding_columns=schema.ONEHOTENCODING_COLUMNS.encoding_columns,
            date_time_column=schema.DATE_TIME_COLUMN.name,
            drop_first=schema.ONEHOTENCODING_COLUMNS.drop_first,
            target_column=schema.TARGET_COLUMN.name
        )
        return data_transformation_config
    
    def get_model_trainer_config(self)->ModelTrainerConfig:
        config=self.config.model_trainer
        params=self.params.training_models
        schema=self.schema.TARGET_COLUMN
        create_directories([config.root_dir])
        model_trainer_config=ModelTrainerConfig(
            root_dir=config.root_dir,
            input_data_path=config.input_data_path,
            x_train_data_path=config.x_train_data_path,
            x_test_data_path=config.x_test_data_path,
            y_train_data_path=config.y_train_data_path,
            y_test_data_path=config.y_test_data_path,
            model_name=config.model_name,
            model=params.model,
            random_state=params.random_state,
            target_column=schema.name,
            test_size=params.test_size
        )
        return model_trainer_config
    
    def get_model_evaluation_config(self)->ModelEvaluationConfig:
        config=self.config.model_evaluation
        params=self.params
        schema=self.schema.TARGET_COLUMN
        create_directories([config.root_dir])
        model_evaluation_config=ModelEvaluationConfig(
            root_dir=config.root_dir,
            x_test_data_path=config.x_test_data_path,
            y_test_data_path=config.y_test_data_path,
            model_path=config.model_path,
            metric_file=config.metric_file,
            all_params=params.training_models,
            target_column=schema.name,
            mlflow_uri=os.getenv("MLFLOW_TRACKING_URI"),
            classification_report_path=config.classification_report_path,
            confusion_matrix_path=config.confusion_matrix_path
        )
        return model_evaluation_config

    
        