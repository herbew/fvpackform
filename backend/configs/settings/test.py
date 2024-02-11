from backend.configs.settings.base import *  

SQLALCHEMY_DATABASE_URI = config.get("DATABASE_URL_TEST", 
    "postgres://uflaskvuepftest:PwDflaskvuepftestSatu1Dua3@127.0.0.1/db_flaskvuepftest")

TESTING = True