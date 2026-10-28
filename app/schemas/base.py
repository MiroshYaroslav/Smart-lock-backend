from typing import Generic, TypeVar
from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel

ItemAny = TypeVar("ItemAny")

class BasePydanticModel(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        str_strip_whitespace=True,
        alias_generator=to_camel,
    )

class PaginatedResponse(BaseModel, Generic[ItemAny]):
    count: int = Field(description="Кількість елементів")
    items: list[ItemAny] = Field(description="Список елементів")