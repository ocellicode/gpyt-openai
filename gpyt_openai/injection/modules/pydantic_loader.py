from typing import List

from pydantic import BaseSettings, PyObject

from gpyt_openai.injection.modules.app import AppModule
from gpyt_openai.injection.modules.loguru_logger import LoguruModule
from gpyt_openai.injection.modules.settings import SettingsModule
from gpyt_openai.injection.modules.template_aggregate_root import (
    TemplateAggregateRootModule,
)


class PydanticLoader(BaseSettings):
    module_list: List[PyObject] = [
        SettingsModule,
        AppModule,
        LoguruModule,
        TemplateAggregateRootModule,
    ]

    class Config:
        env_prefix = "GPYT_"
