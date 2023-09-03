"""
Preconditions:
- name or aggregate_id must exist
"""

from flask import request
from flask_restful import Resource
from loguru import logger


class UpdateTemplate(Resource):
    def __init__(self, **kwargs):
        self.template_root = kwargs["template_root"]

    def post(self):
        request_json = request.get_json(force=True)
        logger.trace(f"Request json: {request_json}")
        try:
            if "aggregate_id" in request_json:
                logger.trace(f"Updating template by aggregate_id: {request_json['aggregate_id']}")
                self.template_root.update_template_by_id(request_json)
            else:
                logger.trace(f"Updating template by name: {request_json['name']}")
                self.template_root.update_template(request_json)
            return {"message": "template updated"}, 200
        except Exception as excpt:  # pylint: disable=broad-except
            logger.error(f"Error updating template: {excpt}")
            return {"error": f"Error creating template: {excpt}"}, 400
