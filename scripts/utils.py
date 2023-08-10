import logging

def setup_logger(level, logger_name):
    """
    Set up logging
    """

    possible_levels = ["INFO", "DEBUG"]
    if level not in possible_levels:
        raise ValueError("Invalid level for the logger. Allowed levels are: {}".format(
            ', '.join(possible_levels)))
    
    logger = logging.getLogger(logger_name)
    logger.setLevel(getattr(logging, level))
    console_handler = logging.StreamHandler()
    formatter = logging.Formatter('[%(levelname)s] %(message)s')
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    logger.debug('LOGGER IS SET UP')  

    return logger


### PUT FETCH DATA HERE?