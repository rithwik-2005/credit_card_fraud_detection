# Using YAML Configuration Files with Dot Notation in Python (ConfigBox Guide)

## Overview

In machine learning projects and production-style Python applications, configuration values are usually stored in **YAML files** such as:

* `config.yaml`
* `params.yaml`
* `schema.yaml`

By default, when YAML files are loaded in Python, they become **dictionaries**. This means values are accessed using bracket notation:

```python
config["database"]["host"]
```

However, this is harder to read and maintain in large projects. A better approach is to enable **dot notation access**:

```python
config.database.host
```

This can be achieved using the `ConfigBox` class from the **python-box** library.

---

## Step 1: Install Required Library

Install python-box:

```bash
pip install python-box
```

---

## Step 2: Create a Sample YAML File

Example: `config.yaml`

```yaml
database:
  host: localhost
  port: 5432
  username: admin
  password: secret123

model:
  name: fraud_detector
  learning_rate: 0.01
  epochs: 50
```

---

## Step 3: Read YAML File Normally (Default Behavior)

```python
import yaml

with open("config.yaml") as file:
    config = yaml.safe_load(file)

print(config["database"]["host"])
```

Output:

```
localhost
```

Dot notation will NOT work here:

```python
config.database.host
```

Error:

```
AttributeError: 'dict' object has no attribute 'database'
```

---

## Step 4: Enable Dot Notation Using ConfigBox

```python
from box import ConfigBox
import yaml

with open("config.yaml") as file:
    config = ConfigBox(yaml.safe_load(file))

print(config.database.host)
```

Output:

```
localhost
```

Now nested keys can be accessed cleanly.

---

## Step 5: Create a Reusable YAML Reader Function (Recommended Practice)

Create file:

```
src/project/utils/common.py
```

Add:

```python
from box import ConfigBox
import yaml


def read_yaml(path):
    with open(path) as file:
        return ConfigBox(yaml.safe_load(file))
```

Usage anywhere in project:

```python
from utils.common import read_yaml

config = read_yaml("config.yaml")

print(config.database.host)
print(config.model.learning_rate)
```

---

## Why Dot Notation is Preferred in ML Projects

Advantages:

* Cleaner syntax
* Easier debugging
* Better readability
* Works well with nested configurations
* Industry-standard practice in modular ML pipelines

Example comparison:

Dictionary style:

```python
config["model"]["learning_rate"]
```

Dot notation style:

```python
config.model.learning_rate
```

Dot notation is easier to maintain in large projects.

---

## Typical Usage in Machine Learning Project Structure

Example project structure:

```
src/
 └── credit_card_fraud_detection/
     ├── components/
     ├── config/
     ├── utils/
     │    └── common.py
     ├── pipeline/
     └── entity/
```

Typical workflow:

```python
config = read_yaml("config/config.yaml")
params = read_yaml("params.yaml")
schema = read_yaml("schema.yaml")
```

Then access values like:

```python
config.database.host
params.model.learning_rate
schema.columns.target
```

---

## Summary

Default YAML behavior:

```python
config["database"]["host"]
```

Using ConfigBox (recommended):

```python
config.database.host
```

ConfigBox enables cleaner, scalable configuration handling and is widely used in structured machine learning pipelines.


# Understanding BoxValueError in Python (ConfigBox Error Handling Guide)

## Overview

When working with YAML configuration files using **ConfigBox** from the `python-box` library, you may encounter an error called:

```
BoxValueError
```

This error usually occurs when the YAML file is **empty**, **invalid**, or contains unexpected structure.

Understanding this error helps make configuration-loading utilities safer in machine learning pipelines.

---

## What is BoxValueError?

`BoxValueError` is an exception raised by the **python-box** library when it cannot properly convert data into a `ConfigBox` object.

Example situation:

```python
from box import ConfigBox

ConfigBox(None)
```

Error:

```
BoxValueError
```

This happens because `ConfigBox` expects dictionary-like data.

---

## Most Common Cause in ML Projects

Typical cause:

```
Empty YAML file
```

Example empty file:

```
config.yaml
```

(no content inside)

When loaded:

```python
import yaml
from box import ConfigBox

with open("config.yaml") as file:
    content = yaml.safe_load(file)

ConfigBox(content)
```

Result:

```
BoxValueError
```

Because:

```
content = None
```

---

## Example YAML File That Works Correctly

Valid YAML example:

```yaml
model:
  name: fraud_detector
  learning_rate: 0.01
```

Now:

```python
config = ConfigBox(content)
```

Works successfully.

---

## How to Handle BoxValueError Properly (Best Practice)

Recommended approach inside ML utility function:

```
src/project/utils/common.py
```

Example:

```python
from ensure import ensure_annotations
from box import ConfigBox
from box.exceptions import BoxValueError
from pathlib import Path
import yaml


@ensure_annotations

def read_yaml(path_to_yaml: Path) -> ConfigBox:

    try:

        with open(path_to_yaml) as yaml_file:

            content = yaml.safe_load(yaml_file)

            if content is None:
                raise ValueError("YAML file is empty")

            return ConfigBox(content)

    except BoxValueError:

        raise ValueError("YAML file format is invalid")
```

This prevents crashes later in the pipeline.

---

## Why Handling BoxValueError is Important

Advantages:

* Detects empty configuration files early
* Prevents pipeline failure later
* Improves debugging experience
* Makes configuration utilities production-ready
* Encourages safer ML project structure

Without handling this error, debugging becomes difficult.

---

## Example of Safe YAML Reader Utility (Industry Pattern)

Example:

```python
from ensure import ensure_annotations
from box import ConfigBox
from box.exceptions import BoxValueError
from pathlib import Path
import yaml


@ensure_annotations

def read_yaml(path_to_yaml: Path) -> ConfigBox:

    try:

        with open(path_to_yaml) as yaml_file:

            content = yaml.safe_load(yaml_file)

            if content is None:
                raise ValueError("YAML file is empty")

            return ConfigBox(content)

    except BoxValueError:

        raise ValueError("Failed to parse YAML file")
```

Usage:

```python
config = read_yaml(Path("config/config.yaml"))
```

Now errors are handled safely.

---

## Difference Between ValueError and BoxValueError

| Error Type    | Meaning                      |
| ------------- | ---------------------------- |
| ValueError    | Python built-in error        |
| BoxValueError | Raised by python-box library |

Example:

```
Empty YAML → ValueError
Invalid structure → BoxValueError
```

Both should be handled in configuration utilities.

---

## Typical Usage in Machine Learning Pipeline Projects

Used inside:

```
utils/common.py
```

Example workflow:

```python
config = read_yaml(Path("config/config.yaml"))
params = read_yaml(Path("params.yaml"))
schema = read_yaml(Path("schema.yaml"))
```

If any file is empty or invalid:

```
Error raised immediately
```

This protects the pipeline from silent failures.

---

## Summary

`BoxValueError` occurs when:

* YAML file is empty
* YAML structure is invalid
* ConfigBox cannot convert content

Best practice:

Always handle this error inside configuration-reading utility functions.

Example safe pattern:

```
try:
    return ConfigBox(content)
except BoxValueError:
    raise ValueError("Invalid YAML configuration")
```

This makes machine learning pipelines more reliable and easier to debug.


# Using ensure_annotations in Python (Type Safety Guide for ML Projects)

## Overview

In structured Python and machine learning projects, **type safety** helps reduce bugs and improves code readability.

The `ensure_annotations` decorator is commonly used to enforce function argument types at runtime.

It is especially useful when working with configuration readers such as:

* YAML readers
* utility helper functions
* pipeline components

This decorator is available in:

```
ensure
```

library.

---

## Step 1: Install Required Library

Install the package:

```bash
pip install ensure
```

---

## Step 2: Basic Example Without ensure_annotations

Example function:

```python

def add(a: int, b: int) -> int:
    return a + b
```

This function expects integers, but Python will still allow:

```python
add("2", "3")
```

Output:

```
23
```

This happens because Python does **not enforce type hints by default**.

---

## Step 3: Using ensure_annotations

Example:

```python
from ensure import ensure_annotations


@ensure_annotations

def add(a: int, b: int) -> int:
    return a + b
```

Now if you run:

```python
add("2", "3")
```

Error:

```
TypeError
```

This ensures the function only accepts integers.

---

## Step 4: Example with YAML Reader Function

Common usage inside ML utilities:

File:

```
src/project/utils/common.py
```

Example:

```python
from ensure import ensure_annotations
from box import ConfigBox
import yaml
from pathlib import Path


@ensure_annotations

def read_yaml(path_to_yaml: Path) -> ConfigBox:

    with open(path_to_yaml) as yaml_file:
        content = yaml.safe_load(yaml_file)
        return ConfigBox(content)
```

Usage:

```python
config = read_yaml("config.yaml")
```

This will raise an error because the function expects:

```
Path object
```

Correct usage:

```python
from pathlib import Path

config = read_yaml(Path("config.yaml"))
```

---

## Why ensure_annotations is Useful in ML Projects

Advantages:

* Enforces correct input types
* Prevents silent runtime bugs
* Improves debugging
* Makes pipeline utilities safer
* Encourages structured coding practice

Example benefit:

Incorrect input:

```python
read_yaml(123)
```

Raises error immediately instead of failing later.

---

## Typical Usage in ML Pipeline Utilities

Common helper functions using ensure_annotations:

```
read_yaml()
create_directories()
save_json()
load_json()
```

Example:

```python
from ensure import ensure_annotations
from pathlib import Path


@ensure_annotations

def create_directories(path: list):

    for p in path:
        Path(p).mkdir(parents=True, exist_ok=True)
```

This ensures only list input is accepted.

---

## Comparison: Without vs With ensure_annotations

Without decorator:

```
Type hints are suggestions only
```

With decorator:

```
Type hints are enforced
```

This improves reliability of shared utility functions.

---

## Best Practice Recommendation

Use `ensure_annotations` in:

* utility helper functions
* configuration readers
* directory creators
* data validation helpers

Example recommended pattern:

```python
from ensure import ensure_annotations


@ensure_annotations

def function_name(parameter: expected_type) -> return_type:
    pass
```

---

## Summary

Without ensure_annotations:

```
Python ignores type hints
```

With ensure_annotations:

```
Python enforces type hints at runtime
```

This makes utility functions safer and is commonly used in structured machine learning project templates.
