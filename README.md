# credit_card_fraud_detection
## End to End Data Science Project

### Workflows--ML Pipeline

1. Data Ingestion
2. Data Validation
3. Data Transformation-- Feature Engineering,Data Preprocessing
4. Model Trainer
5. Model Evaluation- MLFLOW,Dagshub

### Workflows

1. Update config.yaml
2. Update schema.yaml
3. Update params.yaml
4. Update the entity
5. Update the configuration manager in src config
6. Update the components
7. Update the pipeline 
8. Update the main.py

# ML Pipeline Configuration Workflow (README Guide)

## Overview

Modern machine learning pipeline projects use a structured configuration workflow to manage:

* config.yaml
* params.yaml
* schema.yaml

These files store settings separately from code, making projects cleaner, reproducible, and production-ready.

This README explains the **complete configuration workflow architecture** used in modular ML pipelines.

---

# Why Configuration Files Are Used

Instead of writing values inside Python scripts:

```
learning_rate = 0.01
file_path = "data/train.csv"
```

we store them inside YAML files:

```
config.yaml
params.yaml
schema.yaml
```

Benefits:

* easier experiment tracking
* reusable pipelines
* cleaner project structure
* faster debugging
* production-ready setup

---

# Role of Each YAML File

## config.yaml

Stores **file paths and directory structure**

Example:

```yaml
artifacts_root: artifacts

data_ingestion:
  root_dir: artifacts/data_ingestion
  source_URL: https://example.com/data.zip
  local_data_file: artifacts/data_ingestion/data.zip
  unzip_dir: artifacts/data_ingestion
```

Used for:

* dataset locations
* artifact folders
* output directories

## params.yaml

Stores **model hyperparameters**

Example:

```yaml
learning_rate: 0.01
batch_size: 32
epochs: 50
```

Used for:

* training parameters
* tuning experiments
* reproducibility

## schema.yaml

Stores **dataset structure information**

Example:

```yaml
columns:
  age: int
  salary: float
  fraud: int
```

Used for:

* validation rules
* column checking
* preventing data drift

---

# Why Store YAML Paths in constants/**init**.py

Example:

```
src/project/constants/__init__.py
```

Example code:

```python
from pathlib import Path

CONFIG_FILE_PATH = Path("config/config.yaml")
PARAMS_FILE_PATH = Path("params.yaml")
SCHEMA_FILE_PATH = Path("schema.yaml")
```

Why this is important:

Advantages:

* avoids hardcoding paths everywhere
* single source of truth
* easier refactoring
* safer imports across modules

Example usage:

```python
from project.constants import CONFIG_FILE_PATH

config = read_yaml(CONFIG_FILE_PATH)
```

---

# Complete Configuration Workflow Architecture

Typical pipeline flow:

```
YAML Files
   ↓
constants/__init__.py
   ↓
read_yaml() utility
   ↓
ConfigBox object
   ↓
configuration.py
   ↓
config_entity.py (dataclass objects)
   ↓
pipeline components
```

Each layer has a specific responsibility.

<p align="center">
  <img src="images/flow.png">
</p>

---

# Step 1: constants/**init**.py

Stores file paths

```python
from pathlib import Path

CONFIG_FILE_PATH = Path("config/config.yaml")
PARAMS_FILE_PATH = Path("params.yaml")
SCHEMA_FILE_PATH = Path("schema.yaml")
```

This ensures paths remain consistent.

---

# Step 2: read_yaml() Utility Function

Located inside:

```
utils/common.py
```

Example:

```python
from ensure import ensure_annotations
from box import ConfigBox
from pathlib import Path
import yaml


@ensure_annotations

def read_yaml(path_to_yaml: Path) -> ConfigBox:

    with open(path_to_yaml) as yaml_file:

        content = yaml.safe_load(yaml_file)

        return ConfigBox(content)
```

Purpose:

* loads YAML
* converts dictionary → ConfigBox
* enables dot notation access

Example:

```
config.data_ingestion.root_dir
```

---

# Step 3: configuration.py

Reads YAML and prepares configuration objects

Location:

```
config/configuration.py
```

Example:

```python
from project.constants import CONFIG_FILE_PATH
from project.utils.common import read_yaml


class ConfigurationManager:

    def __init__(self):

        self.config = read_yaml(CONFIG_FILE_PATH)
```

Purpose:

Central configuration loader

---

# Step 4: config_entity.py (Using dataclass)

Creates structured configuration objects

Example:

```python
from dataclasses import dataclass
from pathlib import Path


@dataclass
class DataIngestionConfig:

    root_dir: Path

    source_URL: str

    local_data_file: Path

    unzip_dir: Path
```

Why this matters:

Advantages:

* structured configs
* type-safe values
* clean pipeline communication

---

# Step 5: configuration.py Returns Dataclass Objects

Example:

```python
from project.entity.config_entity import DataIngestionConfig


def get_data_ingestion_config(self):

    config = self.config.data_ingestion

    return DataIngestionConfig(

        root_dir=config.root_dir,

        source_URL=config.source_URL,

        local_data_file=config.local_data_file,

        unzip_dir=config.unzip_dir

    )
```

Purpose:

Convert YAML values → structured dataclass object

---

# Step 6: Pipeline Component Uses Config Object

Example:

```
components/data_ingestion.py
```

Example:

```python
class DataIngestion:

    def __init__(self, config: DataIngestionConfig):

        self.config = config
```

Usage:

```
self.config.root_dir
```

Cleaner than dictionary access.

---

# Why ensure_annotations Is Used

Example:

```
@ensure_annotations
```

Purpose:

Ensures function arguments match expected types

Example:

```
read_yaml("config.yaml") ❌

read_yaml(Path("config.yaml")) ✅
```

Prevents runtime bugs.

---

# Why ConfigBox Is Used

Converts:

```
dictionary → dot-access object
```

Example:

Instead of:

```
config["data_ingestion"]["root_dir"]
```

We use:

```
config.data_ingestion.root_dir
```

Cleaner and safer.

---

# Why dataclass Is Used

Creates structured configuration containers

Example:

```
DataIngestionConfig
ModelTrainerConfig
DataValidationConfig
```

Benefits:

* readable
* immutable (optional)
* type-safe
* pipeline-friendly

---

# Final Workflow Summary

Complete architecture:

```
constants/__init__.py
        ↓
read_yaml()
        ↓
ConfigBox
        ↓
configuration.py
        ↓
config_entity.py (dataclass)
        ↓
pipeline components
```

This structure is used in professional ML pipeline repositories because it keeps configuration:

* centralized
* readable
* reusable
* scalable
* production-ready

---

# Why This Architecture Is Industry Standard

Because it supports:

* experiment reproducibility
* modular pipelines
* clean configuration management
* large team collaboration
* deployment-ready ML systems

This workflow is commonly used in end-to-end machine learning projects such as fraud detection pipelines.
