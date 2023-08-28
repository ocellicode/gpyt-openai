from abc import ABC, abstractmethod


class TemplateAggregateRoot(ABC):
    @abstractmethod
    def create_template(self, template_json: dict):
        pass

    @abstractmethod
    def apply(self, event: dict) -> None:
        pass
