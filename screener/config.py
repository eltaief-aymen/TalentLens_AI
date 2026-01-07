import logging

MODEL_NAME = "llama3.1:8b"
LOG_LEVEL = logging.INFO

logging.basicConfig(
    level=LOG_LEVEL,
    format="%(levelname)s | %(message)s"
)
