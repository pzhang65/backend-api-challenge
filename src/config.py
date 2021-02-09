# /src/config.py

import os

class Development(object):
    """
    Development environment configuration
    """
    DEBUG = True
    TESTING = False

class Testing(object):
    """
    Testing environment configuration
    """
    DEBUG = False
    TESTING = True

app_config = {
    'development': Development,
    'testing': Testing
}
