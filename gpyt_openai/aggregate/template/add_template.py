from typing import List

from loguru import logger

from gpyt_openai.interface.template import Template


class AddTemplate:
    @staticmethod
    def add_one(event: dict, state: List[Template]):
        logger.trace(f"add_one called with event: {event}")
        logger.trace(f"state: {state}")
        if event["event_type"] == "template_created":
            state.append(Template(aggregate_id=event["aggregate_id"], **event["data"]))
        return state
