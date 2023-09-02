"""
Preconditions:
- template with name must exist
"""

from flask import request
from flask_restful import Resource


class DeleteTemplate(Resource):
    def __init__(self, **kwargs):
        self.logger = kwargs["logger"]
        self.template_root = kwargs["template_root"]

    def post(self):
        request_json = request.get_json(force=True)
        self.logger.trace(f"Request json: {request_json}")
        try:
            self.template_root.delete_template(request_json["name"])
            return {"message": "template deleted"}, 200
        except Exception as excpt:  # pylint: disable=broad-except
            return {"error": f"Error deleting template: {excpt}"}, 400
