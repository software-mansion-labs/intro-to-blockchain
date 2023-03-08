from flask import Flask


class Server:
    def __init__(self, node_name: str):
        self.app = Flask(node_name)

    def add_endpoint(self, path: str, type: str, method_name: str, method):
        self.app.add_url_rule(path, method_name, method, methods=[type])

