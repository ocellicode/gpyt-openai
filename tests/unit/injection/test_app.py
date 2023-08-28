import unittest
from unittest.mock import MagicMock, patch

from flask import Flask
from flask_restful import Api
from opyoid import SingletonScope

from gpyt_openai.aggregate.template.template_root import TemplateRoot
from gpyt_openai.injection.modules.app import AppModule
from gpyt_openai.interface.settings import Settings
from gpyt_openai.interface.template_aggregate_root import TemplateAggregateRoot


class TestAppModule(unittest.TestCase):
    def setUp(self):
        self.settings = MagicMock(spec=Settings)
        self.settings.command_bus_url = "http://localhost:8080"
        self.settings.openai_url = "http://localhost:8081"
        self.settings.log_level = "INFO"
        self.settings.event_bus_url = "http://localhost:8082"
        self.logger = MagicMock()
        self.mock_template_aggregate_root = MagicMock(spec=TemplateAggregateRoot)

    def test_get_app(self):
        app_module = AppModule()

        # Mock resource settings
        resource_settings = {"/path1": MagicMock(), "/path2": MagicMock()}
        self.settings.resources = [resource_settings]
        self.settings.targets = {"foo": MagicMock()}

        # Mock Flask and Api objects
        mock_flask = MagicMock(spec=Flask)
        mock_api = MagicMock(spec=Api)

        # Mock add_resource method of the Api object
        mock_api.add_resource = MagicMock()

        # Patch the Flask and Api objects
        with patch(
            "gpyt_openai.injection.modules.app.Flask", return_value=mock_flask
        ), patch("gpyt_openai.injection.modules.app.Api", return_value=mock_api), patch(
            "gpyt_openai.injection.modules.app.requests.post", return_value=MagicMock()
        ) as mock_post:
            mock_post.return_value.status_code = 201
            # Call the get_app method
            app = app_module.get_app(
                self.settings, self.logger, self.mock_template_aggregate_root
            )

            # Assert that the Flask object is returned
            self.assertEqual(app, mock_flask)

            # Assert that add_resource is called for each resource
            for key, value in resource_settings.items():
                mock_api.add_resource.assert_any_call(
                    value,
                    key,
                    resource_class_kwargs={
                        "logger": self.logger,
                        "template_root": self.mock_template_aggregate_root,
                    },
                )

    def test_configure(self):
        app_module = AppModule()
        app_module.bind = MagicMock()

        # Call the configure method
        app_module.configure()

        # Assert that the bind method is called with the correct arguments
        app_module.bind.assert_called_with(
            Flask, to_provider=app_module.get_app, scope=SingletonScope
        )
