# File: app/logging_config.py
import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path


def setup_logging(
        log_level: str = "INFO",
        log_to_file: bool = True,
        log_dir: str = "logs",
        log_filename: str = "app.log",
        max_bytes: int = 10_485_760,  # 10 MB
        backup_count: int = 5,
) -> logging.Logger:
    """
    Configure application logging with both console and file handlers.

    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_to_file: Whether to write logs to file
        log_dir: Directory for log files
        log_filename: Name of the log file
        max_bytes: Max size per log file before rotation
        backup_count: Number of backup files to keep

    Returns:
        Configured root logger
    """
    # Create logger
    logger = logging.getLogger("wgai_app")
    logger.setLevel(getattr(logging, log_level.upper(), logging.INFO))

    # Prevent duplicate handlers on reload
    if logger.handlers:
        return logger

    # Log format with timestamp, level, module, and message
    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(name)s:%(funcName)s:%(lineno)d | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Console handler (stdout) - always enabled
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.DEBUG)
    logger.addHandler(console_handler)

    # File handler with rotation - optional
    if log_to_file:
        log_path = Path(log_dir)
        log_path.mkdir(parents=True, exist_ok=True)

        file_handler = RotatingFileHandler(
            filename=log_path / log_filename,
            maxBytes=max_bytes,
            backupCount=backup_count,
            encoding="utf-8",
        )
        file_handler.setFormatter(formatter)
        file_handler.setLevel(logging.DEBUG)
        logger.addHandler(file_handler)

    return logger


def get_logger(name: str = "wgai_app") -> logging.Logger:
    """Get a logger instance for a specific module."""
    return logging.getLogger(name)