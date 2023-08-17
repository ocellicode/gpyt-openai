from typing import Dict, List, Literal

from pydantic import AnyUrl, BaseSettings, PyObject, Field

from gpyt_openai.interface.settings import Settings as ICommandBusSettings
from gpyt_openai.resources.root import Root
from gpyt_openai.resources.template import Template
from gpyt_openai.resources.template.event import TemplateEvent

LogLevel = Literal["TRACE", "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]


class Settings(BaseSettings, ICommandBusSettings):
    resources: List[Dict[str, PyObject]] = [
        {"/": Root},
        {"/template": Template},
        {"/template/event": TemplateEvent},
    ]
    command_bus_url: AnyUrl = "http://localhost:8080"  # type: ignore
    event_bus_url: AnyUrl = "http://localhost:8081"  # type: ignore
    openai_url: AnyUrl = "http://localhost:8082"  # type: ignore
    log_level: LogLevel = "INFO"
    targets: Dict[str, str] = {"openai": "", "openai-template": "template"}

    class Config:
        env_prefix = "GPYT_"
        env_file = ".env"
