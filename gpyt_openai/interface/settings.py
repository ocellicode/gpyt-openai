from abc import ABC
from typing import Any, Callable, Dict, List

from pydantic import AnyUrl


class Settings(ABC):
    resources: List[Dict[str, Callable[..., Any]]]
    log_level: str
    command_bus_url: AnyUrl
    openai_url: AnyUrl
    event_bus_url: AnyUrl
