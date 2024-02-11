# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

"""
ATTENTION PLEASE UPDATE IF ANY ERROR FOR ACTIVATING THE COMMAND console--
../lib/python3.10/site-packages/flask_script/__init__.py", line 15, in <module>

    ...
    #from flask._compat import text_type
    
    try:
         from flask._compat import text_type
    except:
         from flask_script._compat import text_type
    ...

"""
# Some time absolute path not working in Flask
import sys, os, logging, pytest


from flask_migrate import Migrate #from Flask-Migrate==4.0.5

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.libs.flask_script import Manager, Command, Shell
from backend.libs.flask_migrate import MigrateCommand

from backend.logs import FILE_HANDLER
from backend.run import app, db, port

logging.basicConfig(level=logging.DEBUG)

log = logging.getLogger(__file__)
file_handler = FILE_HANDLER
log.addHandler(file_handler)

# The Flask-Script extension provides support for writing external scripts in
# Flask, which includes running a development server. For more info, visit:
# http://flask-script.readthedocs.org/en/latest/.
def make_shell_context():
    return dict(app=app, os=os, sys=sys)

# DB Migration
from backend.apps.masters.models.companies import Company
from backend.apps.masters.models.customers import Customer
from backend.apps.sales.models.orders import Order
from backend.apps.sales.models.order_items import OrderItem
from backend.apps.stocks.models.deliveries import Delivery

migrate = Migrate(app, db)

manager = Manager(app)

manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

@manager.command
def runserver(port=port, debug=True):
    #===========================================================================
    # BLUEPRINT
    #===========================================================================
    from backend.blueprints.admins.restapis.sales.order_items import (
        admin_api_sales_order_item as bp_admin_api_sales_order_item)
    
    app.register_blueprint(bp_admin_api_sales_order_item, 
                           url_prefix="/admin/api/sales/")
    
    app.run(threaded=True, debug=True, host='0.0.0.0', port=port)
    
from backend.apps.commands.displays import get_logger
# /home/<username>/venvbackend/bin/python3 manage.py logger --msg='hallo hallo bandong'
# or /home/<username>/venvbackend/bin/python3 manage.py logger
# or /home/<username>/venvbackend/bin/python3 manage.py logger --msg='hallo hallo bandong' --others='Onather One'
@manager.command
def logger(msg="Hello Test Display Command", others="No Others"):
    get_logger(msg)
    print(f"This others input parameter '{others}'")

from backend.apps.commands.databases import database_populate
# /home/<username>/venvbackend/bin/python3 manage.py db_populate
@manager.command
def db_populate():
    print("Populate Database On progress")
    database_populate()
    print("Populate Database On progress")
    
if __name__ == '__main__':
    # log.debug("Welcome messaging manage.py Service!!")
    # log.info("Welcome messaging manage.py Service!!")
    # log.warning("Welcome messaging manage.py Service!!")
    # log.error("Welcome messaging manage.py Service!!")
    # log.critical("Welcome messaging manage.py Service!!")
    manager.run()
    
#==========================================================
# assume the directoris /home/herbew
# /home/<username>/venvbackend/bin/python3 messaging/manage.py shell
#
# IF ANY ERROR
# File "/home/<username>/messaging/messaging/manage.py", line 15, in <module>
#     from flask_script import Manager, Command, Shell
#   File "/home/<username>/venvbackend/lib/python3.10/site-packages/flask_script/__init__.py", line 15, in <module>
#     from flask._compat import text_type
# ModuleNotFoundError: No module named 'flask._compat'
#
# ...
# /venvbackend/lib/python3.10/site-packages/flask_script/__init__.py
#
# try:
#     from flask._compat import text_type
# except:
#     from flask_script._compat import text_type
# ....
#==========================================================


