import logging
import logging.config


enable_debug_logging = False

logging.config.fileConfig('logging_config.ini')
logger = logging.getLogger(__name__)

if enable_debug_logging:
    logger.setLevel(logging.DEBUG)