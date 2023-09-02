from typing import Dict, List, Literal

from pydantic import AnyUrl, BaseSettings, PyObject

from gpyt_openai.interface.settings import Settings as ICommandBusSettings
from gpyt_openai.resources.create_template import CreateTemplate
from gpyt_openai.resources.delete_template import DeleteTemplate
from gpyt_openai.resources.event.resource import TemplateEvent

LogLevel = Literal["TRACE", "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]


class Settings(BaseSettings, ICommandBusSettings):
    resources: List[Dict[str, PyObject]] = [
        {"/create-template": CreateTemplate},
        {"/event": TemplateEvent},
        {"/delete-template": DeleteTemplate},
    ]
    command_bus_url: AnyUrl = "http://192.168.1.192:8080"  # type: ignore
    event_bus_url: AnyUrl = "http://192.168.1.192:8081"  # type: ignore
    openai_url: AnyUrl = "http://192.168.1.192:8082"  # type: ignore
    log_level: LogLevel = "TRACE"
    targets: Dict[str, str] = {
        "openai-create-template": "create-template",
        "openai-update-template": "update-template",
        "openai-delete-template": "delete-template",
    }

    class Config:
        env_prefix = "GPYT_"
        env_file = ".env"
