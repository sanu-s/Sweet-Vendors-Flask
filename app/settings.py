import os
from datetime import timedelta


BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    JSON_SORT_KEYS = False

    CSRF_ENABLED = True
    SESSION_COOKIE_SAMESITE = "Lax"

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)


class ProductionSettings(Config):
    DEBUG = False
    TESTING = False
    SECRET_KEY = "H$#47HGF753H*$G344G5J@%^&!9SDFH6+JKS%&%&^#@#36~"
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_DOMAIN = "127.0.0.1:5002"
    SERVER_NAME = "127.0.0.1:5002"

    SQLALCHEMY_DATABASE_URI = "mysql://username:password@server/db"

    JWT_SECRET_KEY = "^&$!#DL;AS15#5@8GJH786Y7JJGHU857$^&)*+JHAWQ23XN"

    SITE_ORIGIN = "http://127.0.0.1:4200"

    if os.name == 'nt':
        MEDIA_ROOT = r'E:\media\production'
    elif os.name == 'posix':
        MEDIA_ROOT = r'/datadrive/sweetvendors/production'


class StagingSettings(Config):
    DEBUG = True
    TESTING = True
    SECRET_KEY = "H$#47HGF753H*$G3LK5GJ@%^&!9SDFH6+JKS%&%&^#@#27*"
    SESSION_COOKIE_SECURE = False
    SESSION_COOKIE_DOMAIN = "127.0.0.1:5001"
    SERVER_NAME = "127.0.0.1:5001"

    SQLALCHEMY_DATABASE_URI = "mysql://username:password@server/db"

    JWT_SECRET_KEY = "DF@%@^FDGKLAAVGKJ^%$544357DSFJHC&&&^%&%&^#@#87^"

    SITE_ORIGIN = "http://127.0.0.1:4200"

    if os.name == 'nt':
        MEDIA_ROOT = r'E:\media\staging'
    elif os.name == 'posix':
        MEDIA_ROOT = r'/datadrive/sweetvendors/staging'


class DevelopmentSettings(Config):
    DEBUG = True
    TESTING = True
    SECRET_KEY = "J%947HGF753H*$G344G5J@%^&!9SDFH6+JKS%&%&^#@#87^"
    SESSION_COOKIE_SECURE = False
    SESSION_COOKIE_DOMAIN = "127.0.0.1:5000"
    SERVER_NAME = "127.0.0.1:5000"

    SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://myuser:mypassword@127.0.0.1:5432/sweetvendors"

    JWT_SECRET_KEY = "KHSD547%^HJF%^JKDS^$^098GJHSD$^^7U834~SD56%^&*S"

    SITE_ORIGIN = "http://127.0.0.1:2000"

    if os.name == 'nt':
        MEDIA_ROOT = r'E:\media\development'
    elif os.name == 'posix':
        MEDIA_ROOT = r'/datadrive/sweetvendors/development'
