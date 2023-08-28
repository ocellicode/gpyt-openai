from gpyt_openai.interface.template import Template
from typing import List
from loguru import logger


class AddTemplate:
    @staticmethod
    def add_one(event: dict, state: List[Template]):
        logger.trace(f"add_one called with event: {event}")
        logger.trace(f"state: {state}")
        if event['event_type'] == 'template_created':
            state.append(Template(aggregate_id=event['aggregate_id'], **event["data"]))
        return state

    @staticmethod
    def add_many(events: List[dict], state: List[Template]):
        logger.trace(f"add_many called with events: {events}")
        logger.trace(f"state: {state}")
        for event in events:
            logger.trace(f"event: {event}")
            if event['event_type'] == 'template_created':
                state.append(Template(aggregate_id=event['aggregate_id'], **event["data"]))
                logger.trace(f"state: {state}")
        return state
