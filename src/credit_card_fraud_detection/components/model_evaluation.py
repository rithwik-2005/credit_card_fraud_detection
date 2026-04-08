from src.credit_card_fraud_detection.logging.logger import logger
from src.credit_card_fraud_detection.entity.config_entity import ModelEvaluationConfig

import pandas as pd
import numpy as np
import joblib
import mlflow
import mlflow.sklearn

from pathlib import Path
from urllib.parse import urlparse
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report, f1_score
from mlflow.tracking import MlflowClient

from src.credit_card_fraud_detection.utils.common import save_json
from dotenv import load_dotenv

load_dotenv()


class ModelEvaluation:

    def __init__(self, config: ModelEvaluationConfig):

        self.config = config


    def eval_metrics(self, actual, pred):

        accuracy = accuracy_score(actual, pred)

        f1 = f1_score(actual, pred, average='binary')  # For fraud detection, focus on minority class

        report = classification_report(
            actual,
            pred,
            zero_division=0
        )

        matrix = confusion_matrix(actual, pred)

        return accuracy, f1, report, matrix


    def promote_best_model(self, run_id):
        """
        Compare current model (challenger) with Production model (champion).
        Model is already registered via mlflow.sklearn.log_model().
        This method finds the new version and compares F1-score to decide promotion.
        
        If challenger F1-score >= champion F1-score:
            - New model is promoted to Production stage
            - Old model is automatically archived (removed from Production)
            - Only ONE model version is in Production at any time
        Otherwise:
            - Current Production model remains active
            - New model stays unarchived but not in Production
        """
        try:
            client = MlflowClient()
            model_name = self.config.all_params.model

            logger.info("Finding latest registered model version")

            # Get all versions to find the one we just created
            all_versions = client.search_model_versions(
                filter_string=f"name='{model_name}'"
            )
            
            # The latest version is the one we just created
            if all_versions:
                new_version_obj = all_versions[0]  # First in list is latest
                new_version = new_version_obj.version
                logger.info(f"Model {model_name} version {new_version} found")
            else:
                logger.error("No model versions found")
                return

            logger.info("Comparing MODEL F1-SCORE: Challenger vs Champion (Production)")

            try:
                latest_prod = client.get_latest_versions(
                    model_name,
                    stages=["Production"]
                )

                if latest_prod:
                    prod_run = client.get_run(latest_prod[0].run_id)
                    champion_f1 = prod_run.data.metrics.get("f1_score", 0)
                    champion_version = latest_prod[0].version
                else:
                    champion_f1 = 0
                    champion_version = "None"

            except Exception as e:
                logger.warning(f"No existing Production model found: {e}")
                champion_f1 = 0
                champion_version = "None"

            challenger_run = client.get_run(run_id)
            challenger_f1 = challenger_run.data.metrics.get("f1_score", 0)

            logger.info(f"Champion (Production) Version: {champion_version}, F1-Score: {champion_f1:.4f}")
            logger.info(f"Challenger (Current) Version: {new_version}, F1-Score: {challenger_f1:.4f}")

            if challenger_f1 >= champion_f1:
                client.transition_model_version_stage(
                    name=model_name,
                    version=new_version,
                    stage="Production",
                    archive_existing_versions=True
                )

                logger.info(f"SUCCESS: Version {new_version} PROMOTED to Production")
                logger.info(f"Old Production Version {champion_version} ARCHIVED (removed from Production)")
                logger.info("BEST MODEL RETAINED: Only this new model with highest F1-score is now in Production")

            else:
                logger.info(f"RETAINED: Production Version {champion_version} remains active")
                logger.info(f"Current model (v{new_version}) has lower F1-score, will not be promoted")
                logger.info("BEST MODEL RETAINED: Previous best model (Champion) still in Production with highest accuracy")

        except Exception as e:
            logger.exception(e)
            raise e


    def log_into_mlflow(self):

        try:

            logger.info("Starting model evaluation")

            x_test = pd.read_csv(
                self.config.x_test_data_path
            )

            y_test = pd.read_csv(
                self.config.y_test_data_path
            ).squeeze()


            model = joblib.load(
                self.config.model_path
            )


            mlflow.set_tracking_uri(
                self.config.mlflow_uri
            )


            tracking_url_type_store = urlparse(
                mlflow.get_tracking_uri()
            ).scheme


            with mlflow.start_run() as run:

                predictions = model.predict(x_test)


                accuracy, f1, report, matrix = self.eval_metrics(
                    y_test,
                    predictions
                )


                score = {

                    "accuracy": accuracy,
                    "f1_score": f1,
                    "report": report,
                    "matrix": matrix.tolist()

                }


                save_json(
                    path=Path(self.config.metric_file),
                    data=score
                )


                logger.info(
                    "Metrics saved locally as JSON"
                )


                mlflow.log_params(
                    self.config.all_params
                )

                logger.info(
                    f"Hyperparameters logged: model={self.config.all_params.model}, "
                    f"n_estimators={self.config.all_params.n_estimators}, "
                    f"max_depth={self.config.all_params.max_depth}, "
                    f"random_state={self.config.all_params.random_state}"
                )


                mlflow.log_metric(
                    "accuracy",
                    accuracy
                )

                mlflow.log_metric(
                    "f1_score",
                    f1
                )


                with open(
                    self.config.classification_report_path,
                    "w"
                ) as f:

                    f.write(report)


                mlflow.log_artifact(
                    self.config.classification_report_path
                )


                np.savetxt(
                    self.config.confusion_matrix_path,
                    matrix,
                    delimiter=",",
                    fmt="%d"
                )


                mlflow.log_artifact(
                    self.config.confusion_matrix_path
                )


                logger.info(
                    "Artifacts logged into MLflow successfully"
                )


                # IMPORTANT: log model BEFORE registering
                # Log model with automatic registration
                mlflow.sklearn.log_model(
                    sk_model=model,
                    name="model",
                    registered_model_name=self.config.all_params.model
                )

                if tracking_url_type_store != "file":
                    # Promote to Production only if accuracy is acceptable
                    self.promote_best_model(
                        run.info.run_id
                    )


                logger.info(
                    "Model logged into MLflow successfully"
                )


        except Exception as e:

            logger.exception(e)

            raise e