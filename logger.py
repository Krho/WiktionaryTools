import logging
import sys


FMT = '%(asctime)s    %(module)s    %(levelname)s    %(message)s'
LOGGER_NAME = 'WiktionaryTools'


def logger(debug=False):
    """Singleton logger.

    Args:
        debug (bool): switch level to logging.DEBUG
    """
    log = logging.getLogger(name=LOGGER_NAME)
    if not len(log.handlers):
        # handlers have not yet been added
        setup(log, debug=debug)
    return log


def setup(log, debug=True):
    """Configure logger.

    Logging to stdout.
    """
    console_handler = logging.StreamHandler(stream=sys.stdout)
    formatter = logging.Formatter(FMT)
    console_handler.setFormatter(formatter)
    if debug:
        console_handler.setLevel(logging.DEBUG)
        log.addHandler(console_handler)
        log.setLevel(logging.DEBUG)
    else:
        console_handler.setLevel(logging.INFO)
        log.addHandler(console_handler)
        log.setLevel(logging.INFO)
    log.debug('Setting up logger for %s', LOGGER_NAME)
