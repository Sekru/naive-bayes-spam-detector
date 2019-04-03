from flask import request, url_for, json, abort
import os
from flask_api import FlaskAPI
from naiveBayes import think, train
from flask_cors import CORS

app = FlaskAPI(__name__)
CORS(app)

def getStaticJsonFile(filename):
    url = os.path.join(app.root_path, app.static_folder, filename)
    return json.load(open(url))

@app.route("/api/ham")
def hamWordsEndpoint():
    try:
        return json.dumps(getStaticJsonFile("hamWords.json")), 200, {'ContentType':'application/json'} 
    except FileNotFoundError:
        abort(404)

@app.route("/api/spam")
def spamWordsEndpoint():
    try:
        return json.dumps(getStaticJsonFile("spamWords.json")), 200, {'ContentType':'application/json'} 
    except FileNotFoundError:
        abort(404)

@app.route("/api/generals")
def generalsEndpoint():
    try:
        return json.dumps(getStaticJsonFile("generals.json")), 200, {'ContentType':'application/json'} 
    except FileNotFoundError:
        abort(404)

@app.route("/api/train")
def trainEndpoint():
    try:
        train()
        return json.dumps({'success':True}), 200, {'ContentType':'application/json'} 
    except:
        abort(500)


@app.route("/api/think", methods=['POST'])
def thinkEndpoint():
    try:
        pSResult, pHResult = think(request.get_json())
        return json.dumps({"pSResult": pSResult, "pHResult": pHResult}), 200, {'ContentType':'application/json'}
    except:
        abort(500)    
