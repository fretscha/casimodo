import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = False
    TESTING = False
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    SESSION_TIMEOUT = 300
    CAS_PREFIX = '/cas'
    CAS_DEFAULT_SERVICE_URL = 'http://127.0.0.1/debug'
    CAS_ALLOWED_SEVICES = [r'http://127.0.0.1/debug']


class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
