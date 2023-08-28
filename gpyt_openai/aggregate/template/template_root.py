from gpyt_openai.interface.settings import Settings
from gpyt_openai.interface.template import Template
from typing import List
from requests import request
from uuid import uuid4
from .add_template import AddTemplate


class TemplateRoot:
    def __init__(self, **kwargs):
        self.settings: Settings = kwargs["settings"]
        self.logger = kwargs["logger"]
        self.state: List[Template] = []

    def hydrate_all(self) -> List[Template]:
        self.logger.trace("hydrate_all called")
        url = str(self.settings.event_bus_url) + "/events"
        obj = {"aggregate_name": "openai-template"}
        cmd_res = request("GET", url, json=obj, timeout=5)
        self.logger.trace(f"cmd_res: {cmd_res}")
        if cmd_res.status_code == 200:
            return AddTemplate.add_many(cmd_res.json(), [])
        elif cmd_res.status_code == 404 and cmd_res.json()["message"] == "Events not found":
            self.logger.warning(f"Warning, during hydrating state: {cmd_res.text}")
            return []

    def apply(self, event: dict) -> None:
        self.logger.trace(f"apply called with event: {event}")
        if event['event_type'] == 'template_created':
            self.state = AddTemplate.add_one(event, self.hydrate_all())
        self.logger.trace(f"state: {self.state}")

    def raise_template_created_event(self, template: Template):
        url = str(self.settings.event_bus_url) + "/event"
        obj = dict()
        obj['data'] = template.dict(exclude={"aggregate_id"})
        obj["aggregate_id"] = str(template.aggregate_id)
        obj["aggregate_name"] = "openai-template"
        obj["event_type"] = "template_created"
        obj['meta_data'] = {}
        obj['revision'] = 0
        cmd_res = request("POST", url, json=obj, timeout=5)
        self.logger.trace(f"cmd_res: {cmd_res.text}")

    def create_template(self, template_json: dict):
        template = Template(aggregate_id=uuid4(), **template_json)
        self.logger.info(f"create_template called with template: {template}")
        if template.name not in [t.name for t in self.hydrate_all()]:
            self.raise_template_created_event(template)
            return template.dict()
        else:
            self.logger.warning(f"Template with name {template.name} already exists")
            raise Exception(f"Template with name {template.name} already exists")
