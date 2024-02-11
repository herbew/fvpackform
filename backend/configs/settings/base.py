from __future__ import unicode_literals, absolute_import

import sys, os, logging, time
from dotenv import dotenv_values

# Read from .env
# load_dotenv()
config = dotenv_values(os.path.join(os.path.dirname(os.path.abspath(__file__)),'../../.env'))
# Local TIMEZONE
os.environ['TZ'] = config.get("LOCAL_TIMEZONE", "Asia/Jakarta")
time.tzset()


# # https://flask.palletsprojects.com/en/2.3.x/config/    
# Whether debug mode is enabled    
DEBUG = config.get('FLASK_DEBUG', False)

# Enable testing mode
TESTING = config.get('FLASK_TESTING', False)

# A secret key that will be used for securely signing the session cookie 
# and can be used for any other security related needs by extensions or your application
SECRET_KEY = config.get('FLASK_SECRET_KEY', 
    "192b9bdd22ab9ed4dmessagingcb9a393ec15f71bbf5dc987d54727823bcbf")


SQLALCHEMY_DATABASE_URI = config.get("DATABASE_URL", 
    "postgres://ufvpackform:PwDfvpackformSatu1Dua3@127.0.0.1/db_fvpackform")

SQLALCHEMY_TRACK_MODIFICATIONS = config.get("SQLALCHEMY_TRACK_MODIFICATIONS", False)


# Pagination
PAGINATION_PAGE = config.get('PAGINATION_PAGE', 1)
PAGINATION_PAGE_SIZE = config.get('PAGINATION_PAGE_SIZE', 10)
PAGINATION_MAX_PAGE_SIZE = config.get('PAGINATION_MAX_PAGE_SIZE', 100)

DEFAULT_PAGINATION_PARAMETERS = dict(
    page=PAGINATION_PAGE,
    page_size=PAGINATION_PAGE_SIZE,
    max_page_size=PAGINATION_MAX_PAGE_SIZE
    ) 





