import MetaTrader5 as meta
from flask import Flask, jsonify
from typing import List, Callable
from flask_cors import CORS

class Endpoint():
    name: str
    handler: Callable

    def __init__(self, name: str, handler: Callable):
        self.name = name
        self.handler = handler

class WebService():
    app = None

    def __init__(self, name, endpoints: List[Endpoint]):
        self.app = Flask(name)
        CORS(self.app)
        for e in endpoints:
            self.app.add_url_rule(e.name, view_func=e.handler)

    def run(self):
        self.app.run("localhost", 5000)
