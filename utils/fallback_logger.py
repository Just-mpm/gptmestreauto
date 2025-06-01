"""
Fallback logger for when loguru is not available
"""
import logging
import sys
from typing import Any

class FallbackLogger:
    """Simple fallback logger that mimics loguru interface"""
    
    def __init__(self, name: str):
        self.logger = logging.getLogger(name)
        if not self.logger.handlers:
            handler = logging.StreamHandler(sys.stdout)
            formatter = logging.Formatter(
                '%(asctime)s | %(levelname)8s | %(name)s:%(lineno)d - %(message)s'
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
            self.logger.setLevel(logging.INFO)
    
    def info(self, message: str, *args, **kwargs):
        self.logger.info(message, *args, **kwargs)
    
    def warning(self, message: str, *args, **kwargs):
        self.logger.warning(message, *args, **kwargs)
    
    def warn(self, message: str, *args, **kwargs):
        self.warning(message, *args, **kwargs)
    
    def error(self, message: str, *args, **kwargs):
        self.logger.error(message, *args, **kwargs)
    
    def debug(self, message: str, *args, **kwargs):
        self.logger.debug(message, *args, **kwargs)
    
    def critical(self, message: str, *args, **kwargs):
        self.logger.critical(message, *args, **kwargs)

def get_fallback_logger(name: str) -> FallbackLogger:
    """Get fallback logger instance"""
    return FallbackLogger(name)