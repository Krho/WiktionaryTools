"""Cache module for API harvesting of information"""

import json

import logger


LOG = logger.logger(debug=True)  # logger in debug mode


def get(filename='cache.json'):
    """Return a cache dictionnary.

    If file with filename is not found, then return an empty dictionnary.

    Args:
        filename (str): name of cache file. Default 'cache.json'
    """
    cache = {
        'thesaurus': {},
        'words': {},
        'authors': {}
    }
    try:
        with open(filename) as f:
            cache = json.loads(f.read())
    except FileNotFoundError:
        LOG.warn(
            'Cache file %s was not found, start with empty cache',
            filename)
    return cache


def save(cache, filename='cache.json'):
    """Save a cache dictionnary to a file.

        Args:
        filename (str): name of cache file. Default 'cache.json'
    """
    with open(cache, 'w') as file:
        data = json.dumps(cache, indent=2)
        file.write(data)
