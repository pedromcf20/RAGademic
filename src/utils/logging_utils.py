import logging
import os

def setup_logging():
    """
    Sets up the logging configuration to log messages only to a file.
    Ensures that a 'logs' directory is created if it does not exist.
    """
    logs_dir = 'logs'
    log_file = os.path.join(logs_dir, 'rag_chain.log')

    # Create 'logs' directory if it does not exist
    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)

    # Create a logger
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)  # Set the logging level

    # Create a file handler that logs even debug messages
    fh = logging.FileHandler(log_file, mode='a')  # Append mode
    fh.setLevel(logging.INFO)

    # Create a formatter and set it for the handler
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)

    # Remove any existing handlers attached to the logger
    if logger.hasHandlers():
        logger.handlers.clear()

    # Add the file handler to the logger
    logger.addHandler(fh)