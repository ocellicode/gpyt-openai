"""
Preconditions:
- name must be unique
"""

from flask import request
from flask_restful import Resource
from loguru import logger


class CreateTemplate(Resource):
    def __init__(self, **kwargs):
        self.template_root = kwargs["template_root"]

    def post(self):
        request_json = request.get_json(force=True)
        logger.trace(f"Request json: {request_json}")
        try:
            self.template_root.create_template(request_json)
            return {"message": "template created"}, 201
        except Exception as excpt:  # pylint: disable=broad-except
            return {"error": f"Error creating template: {excpt}"}, 400
