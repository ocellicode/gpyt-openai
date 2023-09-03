from typing import List
from uuid import UUID

from loguru import logger

from gpyt_openai.interface.template import Template


class UpdateTemplate:
    @staticmethod
    def update_one(event: dict, state: List[Template]):
        logger.trace(f"update_one called with event: {event}")
        logger.trace(f"state: {state}")
        for template in state:
            if template.aggregate_id == UUID(event["aggregate_id"]):
                template.body = event["data"]["body"]
                template.revision = event["revision"]
        return state
