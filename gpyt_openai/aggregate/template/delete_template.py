from typing import List
from uuid import UUID

from loguru import logger

from gpyt_openai.interface.template import Template


class DeleteTemplate:
    @staticmethod
    def remove_one(event: dict, state: List[Template]):
        logger.trace(f"remove_one called with event: {event}")
        logger.trace(f"state: {state}")
        for template in state:
            if template.aggregate_id == UUID(event["aggregate_id"]):
                state.remove(template)
        return state
