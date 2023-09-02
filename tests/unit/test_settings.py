import pytest

from gpyt_openai.resources.create_template import CreateTemplate
from gpyt_openai.resources.delete_template import DeleteTemplate
from gpyt_openai.resources.event import TemplateEvent
from gpyt_openai.settings import Settings


@pytest.fixture
def settings():
    # note: values are read from pyproject.toml
    return Settings()


def test_default_values(settings):
    assert settings.resources == [
        {"/create-template": CreateTemplate},
        {"/event": TemplateEvent},
        {"/delete-template": DeleteTemplate},
    ]


def test_env_prefix(settings):
    assert settings.Config.env_prefix == "GPYT_"


def test_env_file(settings):
    assert settings.Config.env_file == ".env"
