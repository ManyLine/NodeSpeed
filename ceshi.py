import requests
import json
from flask import Flask,jsonify,request
import yaml
import os
import config
import checker

app = Flask(__name__)


@app.route('/check',methods=['POST'])
def check_():
    if request.is_json:
        clash_config = request.json.get("cfg", "")
    else:
        clash_config = request.form.get("cfg", "")
    print(clash_config)
    if checker.check(clash_config):
        cn = checker.get_remote_country()
        return jsonify({"status":True,"msg":"ok","country":cn})
    else:
        return jsonify({"status":False,"msg":"error"})


@app.route('/')
def hello_world():
    return 'Hello, World!'


app.run(port=config.test_server_port, host='0.0.0.0')