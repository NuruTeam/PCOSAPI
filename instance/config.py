import os


class Config(object):
    """Parent configuration class."""
    DEBUG = False
    CSRF_ENABLED = True
    SECRET = os.getenv('SECRET')

    # Assuming you are using Microsoft SQL Server
    SQLALCHEMY_DATABASE_URI = "mssql+pyodbc://{}:{}@{}/{}?driver=ODBC+Driver+17+for+SQL+Server".format(
        os.getenv('DEV_DB_USERNAME'),
        os.getenv('DEV_DATABASE_PASSWORD'),
        os.getenv('DEV_DATABASE_URL'),
        os.getenv('DEV_DB_NAME')
    )


class DevelopmentConfig(Config):
    """Configurations for Development."""
    DEBUG = True


class TestingConfig(Config):
    """Configurations for Testing, with a separate test database."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "mssql+pyodbc://{}:{}@{}/{}?driver=ODBC+Driver+17+for+SQL+Server".format(
        os.getenv('DEV_DB_USERNAME'),
        os.getenv('DEV_DATABASE_PASSWORD'),
        os.getenv('DEV_DATABASE_URL'),
        os.getenv('TEST_DB_NAME')
    )
    DEBUG = False


class StagingConfig(Config):
    """Configurations for Staging."""
    DEBUG = True


class ProductionConfig(Config):
    """Configurations for Production."""
    DEBUG = False
    TESTING = False
    SECRET = os.getenv('SECRET')

    SQLALCHEMY_DATABASE_URI = "mssql+pyodbc://{}:{}@{}/{}?driver=ODBC+Driver+17+for+SQL+Server".format(
        os.getenv('PROD_DB_USERNAME'),
        os.getenv('PROD_DATABASE_PASSWORD'),
        os.getenv('PROD_DATABASE_URL'),
        os.getenv('PROD_DB_NAME')
    )


app_config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'staging': StagingConfig,
    'production': ProductionConfig,
}
