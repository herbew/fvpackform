# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

import sys, os, logging, time

from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

from dotenv import load_dotenv, dotenv_values

sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),"../"))
from backend.libs.flask.json import JSONEncoder
from backend.logs import FILE_HANDLER


# Get a specific log of group, example: 'MAIN', 'APIx', 'APIy' etc 
# or base name each module. 
logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__file__)
file_handler = FILE_HANDLER
log.addHandler(file_handler)

# Read from .env
config = dotenv_values(os.path.join(os.path.dirname(os.path.abspath(__file__)),'../.env'))

os.environ['FLASK_SETTINGS_MODULE'] = config.get("FLASK_SETTINGS_MODULE_TEST", "../configs/settings/test.py")


class MiniJSONEncoder(JSONEncoder):
    """Minify JSON output."""
    item_separator = ','
    key_separator = ':'
    
# Initialize Flask App
app = Flask(__name__, 
            static_folder=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),'static'),
            template_folder=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),'templates'))

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
    <!DOCTYPE html>
    <html lang="en">
        <head>
        </head>
        <body>
            <div>
                <h1> Welcome to PackForm</h1>
            </div>
        </body>
        <footer>
        </footer>
    </html>
    """
    
    return html


#API
from backend.apps.apis.welcomes import(
    welcome as welcomes__welcome
    )

app.add_url_rule('/api/', view_func=welcomes__welcome, methods=['GET'], endpoint='welcomes__welcome')

port = int(os.environ.get('PORT', 8383))

if __name__ == '__main__':
    log.debug("Welcome messaging run.py Service!!")
    log.info("Welcome messaging run.py Service!!")
    log.warn("Welcome messaging run.py Service!!")
    log.error("Welcome messaging run.py Service!!")
    log.critical("Welcome messaging run.py Service!!")
    app.run(threaded=True, debug=True, host='0.0.0.0', port=port)
    
    
    
    
    
    
    