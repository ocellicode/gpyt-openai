from loguru import logger
from typing import List
from uuid import uuid4

from requests import request

from gpyt_openai.interface.settings import Settings
from gpyt_openai.interface.template import Template
from gpyt_openai.interface.template_aggregate_root import TemplateAggregateRoot

from .add_template import AddTemplate
from .delete_template import DeleteTemplate
from .update_template import UpdateTemplate

from uuid import UUID


class TemplateRoot(TemplateAggregateRoot):
    def __init__(self, settings: Settings):
        self.hydrated = False
        self.settings = settings
        self.state: List[Template] = []
        self.hydrate_all()  # TODO: This should be the result of a command to the command bus

    def hydrate_all(self) -> List[Template]:
        if not self.hydrated:
            logger.trace("hydrate_all called")  # type: ignore
            url = str(self.settings.event_bus_url) + "/events"
            obj = {"aggregate_name": "openai-template"}
            cmd_res = request("GET", url, json=obj, timeout=5)
            logger.trace(f"cmd_res: {cmd_res}")  # type: ignore
            if cmd_res.status_code == 200:
                for event in cmd_res.json():
                    self.apply(event)
                self.hydrated = True
                return self.state
            elif (
                cmd_res.status_code == 404
                and cmd_res.json()["message"] == "Events not found"
            ):
                logger.warning(f"Warning, during hydrating state: {cmd_res.text}")
                self.hydrated = True
                return self.state
            else:
                logger.error(f"Error, during hydrating state: {cmd_res.text}")
                raise ValueError(f"Error, during hydrating state: {cmd_res.text}")
        else:
            logger.trace("hydrate_all called, but already hydrated")  # type: ignore
            return self.state

    def apply(self, event: dict) -> None:
        logger.trace(f"apply called with event: {event}")  # type: ignore
        if event["event_type"] == "template_created":
            self.state = AddTemplate.add_one(event, self.state)
        elif event["event_type"] == "template_deleted":
            self.state = DeleteTemplate.remove_one(event, self.state)
        elif event["event_type"] == "template_updated":
            self.state = UpdateTemplate.update_one(event, self.state)
        logger.trace(f"state: {self.state}")  # type: ignore

    def raise_template_updated_event(self, template: Template):
        url = str(self.settings.event_bus_url) + "/event"
        logger.debug(
            f"raise_template_updated_event called for template: {template.revision}"
        )
        obj = {
            "aggregate_id": str(template.aggregate_id),
            "aggregate_name": "openai-template",
            "event_type": "template_updated",
            "meta_data": {},
            "revision": template.revision + 1,
            "data": template.dict(exclude={"aggregate_id", "revision"}),
        }
        logger.debug(f"new template: {obj['revision']}")
        cmd_res = request("POST", url, json=obj, timeout=5)
        logger.trace(f"cmd_res: {cmd_res.text}")

    def update_template(self, template_json: dict):
        logger.info(f"update_template called with template: {template_json}")
        for template in self.state:
            if template.name == template_json["name"]:
                template.body = template_json["body"]
                self.raise_template_updated_event(template)
                return template.dict()
        logger.warning(f"Template with name {template_json['name']} does not exist")
        raise ValueError(f"Template with name {template_json['name']} does not exist")

    def update_template_by_id(self, template_json: dict):
        logger.info(f"update_template called with template: {template_json}")
        for template in self.state:
            if template.aggregate_id == template.aggregate_id:
                logger.debug(f"template: {template}")
                logger.debug(f"template_json: {template_json}")
                template.body = template_json["body"]
                self.raise_template_updated_event(template)
                return template.dict()
        logger.warning(f"Template with aggregate_id {template_json['aggregate_id']} does not exist")
        raise ValueError(f"Template with aggregate_id {template_json['aggregate_id']} does not exist")

    def raise_template_deleted_event(self, template: Template):
        logger.debug(
            f"raise_template_deleted_event called for template: {template.revision}"
        )
        obj = {
            "aggregate_id": str(template.aggregate_id),
            "aggregate_name": "openai-template",
            "event_type": "template_deleted",
            "meta_data": {},
            "revision": template.revision + 1,
            "data": template.dict(exclude={"aggregate_id", "revision"}),
        }
        logger.debug(f"new template: {obj['revision']}")
        cmd_res = request("POST", str(self.settings.event_bus_url) + "/event", json=obj, timeout=5)
        logger.trace(f"cmd_res: {cmd_res.text}")

    def delete_template(self, template_name: str):
        logger.info(f"delete_template called with template_name: {template_name}")
        for template in self.state:
            if template.name == template_name:
                self.raise_template_deleted_event(template)
                return True
        logger.warning(f"Template with name {template_name} does not exist")
        raise ValueError(f"Template with name {template_name} does not exist")

    def delete_template_by_id(self, aggregate_id: str):
        aggregate_id = UUID(aggregate_id)
        logger.info(f"delete_template_by_id called with aggregate_id: {aggregate_id}")
        for template in self.state:
            if template.aggregate_id == aggregate_id:
                self.raise_template_deleted_event(template)
                return True
        logger.warning(f"Template with aggregate_id {aggregate_id} does not exist")
        raise ValueError(f"Template with aggregate_id {aggregate_id} does not exist")

    def raise_template_created_event(self, template: Template):
        url = str(self.settings.event_bus_url) + "/event"
        obj = {
            "aggregate_id": str(template.aggregate_id),
            "aggregate_name": "openai-template",
            "event_type": "template_created",
            "meta_data": {},
            "revision": 0,
            "data": template.dict(exclude={"aggregate_id", "revision"}),
        }
        cmd_res = request("POST", url, json=obj, timeout=5)
        logger.trace(f"cmd_res: {cmd_res.text}")  # type: ignore

    def create_template(self, template_json: dict):
        template = Template(aggregate_id=uuid4(), **template_json)
        logger.info(f"create_template called with template: {template}")
        if template.name not in [t.name for t in self.state]:
            self.raise_template_created_event(template)
            return template.dict()
        else:
            logger.warning(f"Template with name {template.name} already exists")
            raise ValueError(
                f"Template with name {template.name} already exists"
            )  # pylint: disable=broad-exception-raised
