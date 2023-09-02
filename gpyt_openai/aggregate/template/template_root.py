from logging import Logger
from typing import List
from uuid import uuid4

from requests import request

from gpyt_openai.interface.settings import Settings
from gpyt_openai.interface.template import Template
from gpyt_openai.interface.template_aggregate_root import TemplateAggregateRoot

from .add_template import AddTemplate
from .delete_template import DeleteTemplate


class TemplateRoot(TemplateAggregateRoot):
    def __init__(self, settings: Settings, logger: Logger):
        self.hydrated = False
        self.settings = settings
        self.logger = logger
        self.state: List[Template] = []
        self.hydrate_all()  # TODO: This should be the result of a command to the command bus

    def hydrate_all(self) -> List[Template]:
        if not self.hydrated:
            self.logger.trace("hydrate_all called")  # type: ignore
            url = str(self.settings.event_bus_url) + "/events"
            obj = {"aggregate_name": "openai-template"}
            cmd_res = request("GET", url, json=obj, timeout=5)
            self.logger.trace(f"cmd_res: {cmd_res}")  # type: ignore
            if cmd_res.status_code == 200:
                for event in cmd_res.json():
                    self.apply(event)
                self.hydrated = True
                return self.state
            elif (
                cmd_res.status_code == 404
                and cmd_res.json()["message"] == "Events not found"
            ):
                self.logger.warning(f"Warning, during hydrating state: {cmd_res.text}")
                self.hydrated = True
                return self.state
            else:
                self.logger.error(f"Error, during hydrating state: {cmd_res.text}")
                raise ValueError(f"Error, during hydrating state: {cmd_res.text}")
        else:
            return self.state

    def apply(self, event: dict) -> None:
        self.logger.trace(f"apply called with event: {event}")  # type: ignore
        if event["event_type"] == "template_created":
            self.state = AddTemplate.add_one(event, self.state)
        if event["event_type"] == "template_deleted":
            self.state = DeleteTemplate.remove_one(event, self.state)
        self.logger.trace(f"state: {self.state}")  # type: ignore

    def raise_template_deleted_event(self, template: Template):
        url = str(self.settings.event_bus_url) + "/event"
        self.logger.debug(
            f"raise_template_deleted_event called for template: {template.revision}"
        )
        obj = {
            "aggregate_id": str(template.aggregate_id),
            "aggregate_name": "openai-template",
            "event_type": "template_deleted",
            "meta_data": {},
            "revision": template.revision + 1,
            "data": template.dict(exclude={"aggregate_id"}),
        }
        self.logger.debug(f"new template: {obj['revision']}")
        cmd_res = request("POST", url, json=obj, timeout=5)
        self.logger.trace(f"cmd_res: {cmd_res.text}")  # type: ignore

    def delete_template(self, template_name: str):
        self.logger.info(f"delete_template called with template_name: {template_name}")
        for template in self.state:
            if template.name == template_name:
                self.raise_template_deleted_event(template)
                return True
        self.logger.warning(f"Template with name {template_name} does not exist")
        raise ValueError(f"Template with name {template_name} does not exist")

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
        if template.name not in [t.name for t in self.state]:
            self.raise_template_created_event(template)
            return template.dict()
        else:
            self.logger.warning(f"Template with name {template.name} already exists")
            raise ValueError(
                f"Template with name {template.name} already exists"
            )  # pylint: disable=broad-exception-raised
