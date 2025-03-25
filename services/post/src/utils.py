import inspect
import os
from pathlib import Path

from dotenv import load_dotenv


def load_environ(depth: int = 0, logger=None):
    """Function loads environment variables from .env file
    :param int depth: depth of executing file related to root
    directory of the service; "0" if is located in the root directory
    :param logger: project logger to be used on logging '.env not found'
    error as needed
    """
    caller_filename = inspect.stack()[1].filename
    base_dir = Path(caller_filename).resolve().parent
    for _ in range(depth):
        base_dir = base_dir.parent
    env_path = os.path.join(base_dir, ".env")
    if os.path.exists(env_path):
        load_dotenv(env_path)
    elif logger is not None:
        logger.warning(".env file not found")
