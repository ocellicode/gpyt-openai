from flask_restful import Resource


class Root(Resource):
    def __init__(self, **kwargs):
        self.logger = kwargs["logger"]
