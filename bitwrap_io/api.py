import request
import os
from flask import Flask
from flask import render_template
from flask import request
from flask_jsonpify import jsonify
import bitwrap_io 

log = bitwrap_io.log
app = Flask(__name__)

@app.route('/')
def index():
    """ Serve the client-side application. """
    return render_template('index.html')

def main():
    """ Start reactor and run flask app. """
    bitwrap_io.start() 
    app.run(host='0.0.0.0', port=8080)

if __name__ == '__main__':
    log.info('api starting')
    main()
