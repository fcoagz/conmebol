import json

from flask import Flask, render_template
from flask_cors import CORS
from exceptions import page_not_found, internal_server_error
from conmebol import Classification, Results, Matches

app = Flask(__name__)
CORS(app)

app.register_error_handler(404, page_not_found)
app.register_error_handler(500, internal_server_error)

def render_json(_object: dict):
    response = app.response_class(
        response=json.dumps(_object),
        status=200,
        mimetype='application/json'
    )

    return response

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/classification')
def classification():
    return render_json(Classification().get_positions)

@app.route('/api/results')
def results():
    return render_json(Results().get_results)

@app.route('/api/matches')
def matches():
    return render_json(Matches().get_matches)