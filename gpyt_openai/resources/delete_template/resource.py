"""
Preconditions:
- template with name must exist
"""

from flask import request
from flask_restful import Resource
from loguru import logger


class DeleteTemplate(Resource):
    def __init__(self, **kwargs):
        self.template_root = kwargs["template_root"]

    def post(self):
        request_json = request.get_json(force=True)
        logger.trace(f"Request json: {request_json}")
        try:
            if "aggregate_id" in request_json:
                self.template_root.delete_template_by_id(request_json["aggregate_id"])
                return {"message": "template deleted"}, 200
            else:
                self.template_root.delete_template(request_json["name"])
                return {"message": "template deleted"}, 200
        except Exception as excpt:  # pylint: disable=broad-except
            return {"error": f"Error deleting template: {excpt}"}, 400
