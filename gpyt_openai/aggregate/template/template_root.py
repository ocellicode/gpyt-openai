from logging import Logger
from typing import List
from uuid import uuid4

from requests import request

from gpyt_openai.interface.settings import Settings
from gpyt_openai.interface.template import Template
from gpyt_openai.interface.template_aggregate_root import TemplateAggregateRoot

from .add_template import AddTemplate


class TemplateRoot(TemplateAggregateRoot):
    def __init__(self, settings: Settings, logger: Logger):
        self.settings = settings
        self.logger = logger
        self.state: List[Template] = []

    def hydrate_all(self) -> List[Template]:
        self.logger.trace("hydrate_all called")  # type: ignore
        url = str(self.settings.event_bus_url) + "/events"
        obj = {"aggregate_name": "openai-template"}
        cmd_res = request("GET", url, json=obj, timeout=5)
        self.logger.trace(f"cmd_res: {cmd_res}")  # type: ignore
        if cmd_res.status_code == 200:
            return AddTemplate.add_many(cmd_res.json(), [])
        elif (
            cmd_res.status_code == 404
            and cmd_res.json()["message"] == "Events not found"
        ):
            self.logger.warning(f"Warning, during hydrating state: {cmd_res.text}")
            return []
        else:
            self.logger.error(f"Error, during hydrating state: {cmd_res.text}")
            raise ValueError(f"Error, during hydrating state: {cmd_res.text}")

    def apply(self, event: dict) -> None:
        self.logger.trace(f"apply called with event: {event}")  # type: ignore
        if event["event_type"] == "template_created":
            self.state = AddTemplate.add_one(event, self.hydrate_all())
        self.logger.trace(f"state: {self.state}")  # type: ignore

    def raise_template_created_event(self, template: Template):
        url = str(self.settings.event_bus_url) + "/event"
        obj = {
            "aggregate_id": str(template.aggregate_id),
            "aggregate_name": "openai-template",
            "event_type": "template_created",
            "meta_data": {},
            "revision": 0,
            "data": template.dict(exclude={"aggregate_id"}),
        }
        cmd_res = request("POST", url, json=obj, timeout=5)
        self.logger.trace(f"cmd_res: {cmd_res.text}")  # type: ignore

    def create_template(self, template_json: dict):
        template = Template(aggregate_id=uuid4(), **template_json)
        self.logger.info(f"create_template called with template: {template}")
        if template.name not in [t.name for t in self.hydrate_all()]:
            self.raise_template_created_event(template)
            return template.dict()
        else:
            self.logger.warning(f"Template with name {template.name} already exists")
            raise ValueError(
                f"Template with name {template.name} already exists"
            )  # pylint: disable=broad-exception-raised
