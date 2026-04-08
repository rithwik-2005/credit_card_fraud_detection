from src.credit_card_fraud_detection.logging.logger import logger
from src.credit_card_fraud_detection.entity.config_entity import ModelEvaluationConfig
import os
import pandas as pd
from sklearn.metrics import accuracy_score,confusion_matrix,classification_report
import mlflow
import mlflow.sklearn
import numpy as np
import joblib
from urllib.parse import urlparse
from src.credit_card_fraud_detection.constants import *
from src.credit_card_fraud_detection.utils.common import read_yaml,create_directories,save_json
from dotenv import load_dotenv

load_dotenv()

class ModelEvaluation:
    def __init__(self,config:ModelEvaluationConfig):
        self.config=config
    
    def eval_metrics(self,actual,pred):
        # Get basic accuracy
        accuracy = accuracy_score(actual, pred)
        # Detailed report (Precision, Recall, F1-score)
        report = classification_report(actual, pred)
        # Confusion Matrix
        matrix = confusion_matrix(actual, pred)
        return accuracy,report,matrix
    
    def log_into_mlflow(self):
        try:
            logger.info("Starting model evaluation")
            x_test=pd.read_csv(self.config.x_test_data_path)
            y_test=pd.read_csv(self.config.y_test_data_path)
            model=joblib.load(self.config.model_path)
            #mlflow
            mlflow.set_registry_uri(self.config.mlflow_uri)
            tracking_url_type_store=urlparse(mlflow.get_tracking_uri()).scheme 

            with mlflow.start_run():
                predictions=model.predict(x_test)
                (accuracy,report,matrix)=self.eval_metrics(y_test,predictions)

                #saving metrics as local
                score={
                    "accuracy":accuracy,
                    "report":report,
                    "matrix":matrix.tolist()
                    }
                
                save_json(path=self.config.metric_file,
                          data=score
                          )
                logger.info("Metrics saved locally as JSON")
                #now logging in mlflow
                #log numerical metrics
                mlflow.log_params(self.config.all_params)
                mlflow.log_metric("accuracy",accuracy)
                #log classification report as artifacts
                with open(self.config.classification_report_path,"w") as f:
                    f.write(report)
                mlflow.log_artifact(self.config.classification_report_path)
                #log confusion matrix as artifacts
                np.savetxt(self.config.confusion_matrix_path,matrix,delimiter=",",fmt="%d")

                mlflow.log_artifact(self.config.confusion_matrix_path)
                logger.info("artifacts logged into MLflow successfully")

                #Model registry does not work with file store
                #https://mlflow.org/docs/latest/ml/model-registry/tutorial/

                if tracking_url_type_store!="file":
                    mlflow.sklearn.log_model(model,
                                              "model",
                                              registered_model_name=self.config.all_params.model
                                              )
                else:
                    mlflow.sklearn.log_model(model,
                                              "model"
                                              )
                logger.info("Model logged into Mlflow successfully")
        except Exception as e:
            logger.exception(e)
            raise e
