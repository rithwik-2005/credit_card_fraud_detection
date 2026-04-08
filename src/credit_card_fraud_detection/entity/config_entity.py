from dataclasses import dataclass
from pathlib import Path
from typing import List

@dataclass
class DataIngestionConfig:
    root_dir: Path
    source_file: Path
    local_data_file: Path


@dataclass
class DataValidationConfig:
    root_dir: Path
    local_data_file: Path
    STATUS_FILE: Path
    all_schema: dict

@dataclass
class DataTransformationConfig:
    root_dir: Path
    input_data_path: Path
    transformed_data_path: Path
    date_time_column: str
    encoding_columns: List[str]
    drop_first: bool
    target_column: str


@dataclass
class ModelTrainerConfig:
    root_dir: Path
    input_data_path: Path
    x_train_data_path: Path
    x_test_data_path: Path
    y_train_data_path: Path
    y_test_data_path: Path
    model_name: str
    model:str
    random_state: int
    target_column: str
    test_size: float

@dataclass
class ModelEvaluationConfig:
    root_dir: Path
    x_test_data_path: Path
    y_test_data_path: Path
    model_path: Path
    metric_file: Path
    all_params: dict
    target_column: str
    mlflow_uri: str
    confusion_matrix_path: Path
    classification_report_path: Path


