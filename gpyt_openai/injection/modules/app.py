from loguru import logger
from sys import stderr
import requests
from flask import Flask
from flask_restful import Api
from opyoid import Module, SingletonScope

from gpyt_openai.interface.settings import Settings
from gpyt_openai.interface.template_aggregate_root import TemplateAggregateRoot


def register_as_target(settings: Settings) -> None:
    logger.debug("register_as_target called")
    url = str(settings.command_bus_url) + "/target"
    for item_key, item_value in settings.targets.items():
        logger.debug(f"Registering as target for: {item_key}, {item_value}")
        my_obj = {"name": item_key, "url": f"{str(settings.openai_url)}/{item_value}"}
        cmd_res = requests.post(url, json=my_obj, timeout=5)
        # response code should be 201 or 409, else raise error
        if not (cmd_res.status_code == 201 or cmd_res.status_code == 409):
            raise Exception(  # pylint: disable=broad-exception-raised
                "Error registering as target for command_bus"
            )
    url = str(settings.event_bus_url) + "/subscriber"
    my_obj = {"url": f"{str(settings.openai_url)}/event"}
    logger.debug(f"Registering as subscriber for: {url}, {my_obj}")
    cmd_res = requests.post(url, json=my_obj, timeout=5)
    # response code should be 201 or 409, else raise error
    if not (cmd_res.status_code == 201 or cmd_res.status_code == 409):
        raise Exception(  # pylint: disable=broad-exception-raised
            "Error registering as target for event_bus"
        )


class AppModule(Module):
    @staticmethod
    def get_app(
        settings: Settings,
        template_aggregate_root: TemplateAggregateRoot,
    ) -> Flask:
        logger.remove()
        logger.add(stderr, level=settings.log_level)
        logger.info("Starting app")
        app = Flask(__name__)
        api = Api(app)
        for res in settings.resources:
            for key, value in res.items():
                logger.debug(f"Adding resource: {key}, {value}")
                api.add_resource(
                    value,
                    key,
                    resource_class_kwargs={
                        "template_root": template_aggregate_root,  # type: ignore
                    },
                )
        register_as_target(settings)
        logger.success("App started")
        return app

    def configure(self) -> None:
        self.bind(Flask, to_provider=self.get_app, scope=SingletonScope)
