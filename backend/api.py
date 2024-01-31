import MetaTrader5 as meta
from flask import Flask, jsonify
from typing import List, Callable

class Endpoint():
    name: str
    handler: Callable

    def __init__(self, name: str, handler: Callable):
        self.name = name
        self.handler = handler

class API():
    app = None

    def __init__(self, name, endpoints: List[Endpoint]):
        self.app = Flask(name)
        for e in endpoints:
            self.app.add_url_rule(e.name, view_func=e.handler)

    def run(self):
        self.app.run("localhost", 5000)
