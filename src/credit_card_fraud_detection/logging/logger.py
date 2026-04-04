import os
import sys  #sys is a built-in Python module that lets you interact with the Python runtime environment.
import logging
from datetime import datetime

LOG_DIR="logs"
os.makedirs(LOG_DIR,exist_ok=True)
Log_file=datetime.now().strftime("%m_%d_%Y_%H_%M_%S.log")
Log_filepath=os.path.join(LOG_DIR,Log_file)

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s: %(levelname)s : %(module)s: %(message)s]",
    handlers=[
        logging.FileHandler(Log_filepath),
        logging.StreamHandler(sys.stdout)
    ]
)

logger=logging.getLogger(__name__)
"""
__name__ is a special built-in Python variable.

It stores the name of the current module.
"""