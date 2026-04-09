import pandas as pd
import mlflow.pyfunc
import joblib
from pathlib import Path

from src.credit_card_fraud_detection.logging.logger import logger


class PredictionPipeline:

    def __init__(self):

        try:

            logger.info("Loading Production model from MLflow Registry")

            #  Correct: load Production model
            self.model = mlflow.pyfunc.load_model(
                "models:/RandomForestClassifier/Production"
            )

            logger.info("Production model loaded successfully")

        except Exception:

            logger.warning(
                "Production model not found. Loading local fallback model."
            )

            local_model_path = Path("artifacts/model_trainer/model.joblib")
            if not local_model_path.exists():
                raise FileNotFoundError(
                    f"Local fallback model not found at {local_model_path}. "
                    "Make sure artifacts/model_trainer/model.joblib is included in the repository or available in your Docker build context."
                )

            self.model = joblib.load(local_model_path)


    def transform_input(self, input_data: dict):

        try:

            logger.info("Starting inference data transformation")

            df = pd.DataFrame([input_data])


            df["TransactionDate"] = pd.to_datetime(
                df["TransactionDate"],
                errors="coerce"
            )


            df["day_of_week"] = df["TransactionDate"].dt.dayofweek
            df["hour"] = df["TransactionDate"].dt.hour


            df.drop("TransactionDate", axis=1, inplace=True)


            df = pd.get_dummies(
                df,
                columns=["TransactionType", "Location"],
                drop_first=True
            )


            return df


        except Exception as e:

            logger.exception(e)
            raise e


    def align_columns(self, df):

        try:

            feature_columns_path = Path(
                "artifacts/data_transformation/feature_columns.pkl"
            )


            if feature_columns_path.exists():

                training_columns = joblib.load(feature_columns_path)


                for col in training_columns:

                    if col not in df.columns:
                        df[col] = 0


                df = df[training_columns]

            else:

                logger.warning(
                    "feature_columns.pkl not found — skipping alignment"
                )


            return df


        except Exception as e:

            logger.exception(e)
            raise e


    def predict(self, input_data: dict):

        try:

            transformed_df = self.transform_input(input_data)

            aligned_df = self.align_columns(transformed_df)


            prediction = self.model.predict(aligned_df)[0]


            if prediction == 1:

                return {
                    "prediction": 1,
                    "message": "Fraud Transaction "
                }

            else:

                return {
                    "prediction": 0,
                    "message": "Legitimate Transaction "
                }


        except Exception as e:

            logger.exception(e)
            raise e