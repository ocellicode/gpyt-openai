from uuid import UUID

from pydantic import BaseModel


class Template(BaseModel):
    aggregate_id: UUID
    name: str
    body: str
    revision: int = 0
