from logging import Logger

from opyoid import Module, SingletonScope

from gpyt_openai.aggregate.template.template_root import TemplateRoot
from gpyt_openai.interface.settings import Settings
from gpyt_openai.interface.template_aggregate_root import TemplateAggregateRoot


class TemplateAggregateRootModule(Module):
    @staticmethod
    def get_template_aggregate_root(
        settings: Settings, logger: Logger
    ) -> TemplateAggregateRoot:
        return TemplateRoot(settings=settings, logger=logger)

    def configure(self) -> None:
        self.bind(
            TemplateAggregateRoot,
            to_provider=self.get_template_aggregate_root,
            scope=SingletonScope,
        )
