from flask import request
from flask_restful import Resource
from loguru import logger


class TemplateEvent(Resource):
    def __init__(self, **kwargs):
        self.template_root = kwargs["template_root"]

    def post(self):
        request_json = request.get_json(force=True)
        logger.trace(f"Request json: {request_json}")
        try:
            self.template_root.apply(request_json)
            return {"message": "template event applied"}, 200
        except Exception as excpt:  # pylint: disable=broad-except
            return {"error": f"Error applying template event: {excpt}"}, 400
