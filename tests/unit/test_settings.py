import pytest

from gpyt_openai.resources.root import Root
from gpyt_openai.resources.template import Template
from gpyt_openai.resources.template.event import TemplateEvent
from gpyt_openai.settings import Settings


@pytest.fixture
def settings():
    # note: values are read from pyproject.toml
    return Settings()


def test_default_values(settings):
    assert settings.resources == [
        {"/": Root},
        {"/template": Template},
        {"/template/event": TemplateEvent},
    ]


def test_env_prefix(settings):
    assert settings.Config.env_prefix == "GPYT_"


def test_env_file(settings):
    assert settings.Config.env_file == ".env"
