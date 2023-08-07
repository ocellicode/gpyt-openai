from opyoid import Module, SingletonScope

from gpyt_openai.interface.settings import Settings as ISettings
from gpyt_openai.settings import Settings


class SettingsModule(Module):
    def configure(self) -> None:
        self.bind(ISettings, to_class=Settings, scope=SingletonScope)
