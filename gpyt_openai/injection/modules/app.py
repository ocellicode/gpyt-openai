from logging import Logger

import requests
from flask import Flask
from flask_restful import Api
from opyoid import Module, SingletonScope

from gpyt_openai.interface.settings import Settings


def register_as_target(settings: Settings) -> None:
    url = str(settings.command_bus_url) + "/target"
    my_obj = {"name": "openai", "url": str(settings.openai_url)}
    cmd_res = requests.post(url, json=my_obj, timeout=5)
    # response code should be 201 or 409, else raise error
    if cmd_res.status_code != 201 and cmd_res.status_code != 409:
        raise Exception(  # pylint: disable=broad-exception-raised
            "Error registering as target for command_bus"
        )


class AppModule(Module):
    @staticmethod
    def get_app(settings: Settings, logger: Logger) -> Flask:
        app = Flask(__name__)
        api = Api(app)
        for res in settings.resources:
            for key, value in res.items():
                api.add_resource(
                    value,
                    key,
                    resource_class_kwargs={
                        "logger": logger,
                    },
                )
        register_as_target(settings)
        return app

    def configure(self) -> None:
        self.bind(Flask, to_provider=self.get_app, scope=SingletonScope)
