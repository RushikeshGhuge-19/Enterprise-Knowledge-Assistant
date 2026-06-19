"""Logging configuration for the application."""
import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path

# Create logs directory
logs_dir = Path("logs")
logs_dir.mkdir(exist_ok=True)

# Logger configuration
def setup_logger(name: str, log_level: int = logging.INFO) -> logging.Logger:
    """Setup logger with file and console handlers."""
    logger = logging.getLogger(name)
    logger.setLevel(log_level)
    
    # Format
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # File handler with rotation
    file_handler = RotatingFileHandler(
        logs_dir / f"{name}.log",
        maxBytes=10485760,  # 10MB
        backupCount=5
    )
    file_handler.setLevel(log_level)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    return logger


# Create application logger
app_logger = setup_logger("knowledge_assistant")
auth_logger = setup_logger("auth")
db_logger = setup_logger("database")
