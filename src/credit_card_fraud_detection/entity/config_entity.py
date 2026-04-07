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

