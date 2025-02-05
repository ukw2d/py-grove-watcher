import json
import logging
import logging.config
from pathlib import Path


def setup_logging(config_file='logging.json'):
    """Setup logging configuration from a JSON file."""
    path = Path(__file__).parent / config_file
    if path.exists():
        with open(path, 'rt') as f:
            config = json.load(f)
        return logging.config.dictConfig(config)
    else:
        # Fallback to basic configuration if the config file is not found
        return logging.basicConfig(level=logging.WARNING)
