# backend/utils/logger.py
import logging
import os

# Ensure log directory exists
log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)

# Logger setup
logger = logging.getLogger("secure_doc_sharing_logger")
logger.setLevel(logging.DEBUG)  # Log all levels DEBUG and above

# Formatter
formatter = logging.Formatter("[%(asctime)s] %(levelname)s - %(message)s", "%Y-%m-%d %H:%M:%S")

# Console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(formatter)

# File handler
file_handler = logging.FileHandler(f"{log_dir}/app.log")
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)

# Add handlers to logger
logger.addHandler(console_handler)
logger.addHandler(file_handler)
