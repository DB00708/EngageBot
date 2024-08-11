import platform
from sqlalchemy.dialects import mysql

ENVIRONMENT = "local"
LAPTOP_NAME = platform.uname()[1]


def set_db_password(laptop_name):
    password_dict = {
        "NerdyTech": "",
        "your_laptop_name": "your password"
    }

    return password_dict.get(laptop_name, "")


def get_db_config(environment):
    DB_CONFIG = {
        'dev': {
            'DB_HOST': "",
            'DB_PASSWORD': "",
            'DB_DATABASE': "engage_bot_dev"
        },
        'local': {
            'DB_HOST': "127.0.0.1",
            'DB_PASSWORD': set_db_password(LAPTOP_NAME),
            'DB_DATABASE': "engage_bot_local"
        },
        'docker': {
            'DB_HOST': "host.docker.internal",
            'DB_PASSWORD': set_db_password(LAPTOP_NAME),
            'DB_DATABASE': "engage_bot_docker"
        }
    }

    environment = environment.lower()
    db_settings = DB_CONFIG.get(environment, DB_CONFIG['dev'])

    return db_settings


def get_database_connection():
    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_DATABASE
    )


db_config = get_db_config(ENVIRONMENT)
DB_HOST = db_config['DB_HOST']
DB_PASSWORD = db_config['DB_PASSWORD']
DB_DATABASE = db_config['DB_DATABASE']
DB_USER = "root"
