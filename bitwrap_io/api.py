import os
import json
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

@app.route('/api')
def transform():
    """ process msg as json and queue up execution """
    msg = json.loads(request.args['msg'])
    machine = bitwrap_io.get(msg['signal']['schema'])
    return jsonify(machine.transform(msg)), 202

@app.route('/api-try')
def dryRun():
    """ perform a dry run execution """
    msg = json.loads(request.args['msg'])
    machine = bitwrap_io.get(msg['signal']['schema'])
    return jsonify(machine.transform(msg)), 200

def main():
    """ Start reactor and run flask app. """
    bitwrap_io.start() 
    app.run(host='0.0.0.0', port=8080)

if __name__ == '__main__':
    log.info('api starting')
    main()
