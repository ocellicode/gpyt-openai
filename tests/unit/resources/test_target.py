import unittest

from flask import Flask
from flask_restful import Api
from loguru import logger

from gpyt_openai.resources.root import Root


class TargetTestCase(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.api = Api(self.app)
        self.api.add_resource(
            Root,
            "/",
            resource_class_kwargs={"logger": logger},
        )
        self.client = self.app.test_client()
