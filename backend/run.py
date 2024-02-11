# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

import sys, os, logging, time

from datetime import datetime

from flask import (Flask, g, request, current_app, 
    abort, redirect, url_for, render_template)


from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy


from dotenv import dotenv_values

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from backend.libs.flask.json import JSONEncoder
from backend.logs import FILE_HANDLER

# Get a specific log of group, example: 'MAIN', 'APIx', 'APIy' etc 
# or base name each module. 
logging.basicConfig(level=logging.DEBUG)

log = logging.getLogger(__file__)
file_handler = FILE_HANDLER
log.addHandler(file_handler)

# Read from .env
config = dotenv_values(os.path.join(os.path.dirname(os.path.abspath(__file__)),'.env'))

# Set setting module
os.environ['FLASK_SETTINGS_MODULE'] = config.get("FLASK_SETTINGS_MODULE", "configs/settings/local.py") 

# Multiple Language
# https://github.com/schmidni/multilingualFlask

class MiniJSONEncoder(JSONEncoder):
    """Minify JSON output."""
    item_separator = ','
    key_separator = ':'
    
# Initialize Flask App
app = Flask(__name__, 
            static_folder='static',
            template_folder="templates")

# Initial ENV
app.config.from_pyfile(os.environ["FLASK_SETTINGS_MODULE"])

app.json_encoder = MiniJSONEncoder
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

# Initialize Data
db = SQLAlchemy(app)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})


@app.route('/')
def welcome():
    html = """
    Welcome to PackForm
    """
    
    return html


#API
from backend.apps.apis.welcomes import(
    welcome as welcomes__welcome
    )

app.add_url_rule('/api/', view_func=welcomes__welcome, methods=['GET'], endpoint='welcomes__welcome')

#===============================================================================
# BLUEPRINT
#===============================================================================
from backend.blueprints.admin.restapis.sales.order_items import (
    admin_api_sales_order_item as bp_admin_api_sales_order_item)

app.register_blueprint(bp_admin_api_sales_order_item, 
                       url_prefix="/admin/api/sales/")

port = int(os.environ.get('PORT', 8181))

if __name__ == '__main__':
    log.debug("Welcome messaging run.py Service!!")
    log.info("Welcome messaging run.py Service!!")
    log.warn("Welcome messaging run.py Service!!")
    log.error("Welcome messaging run.py Service!!")
    log.critical("Welcome messaging run.py Service!!")
    app.run(threaded=True, debug=True, host='0.0.0.0', port=port)
    
    
    
    
    
    
    