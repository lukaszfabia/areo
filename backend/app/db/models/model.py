from bson import ObjectId
from pydantic import BaseModel, Field
from datetime import datetime, timezone
from typing import Optional, Annotated, Any, Callable
from pydantic_core import core_schema


class _ObjectIdPydanticAnnotation:

    @classmethod
    def __get_pydantic_core_schema__(
        cls,
        _source_type: Any,
        _handler: Callable[[Any], core_schema.CoreSchema],
    ) -> core_schema.CoreSchema:
        def validate_from_str(input_value: str) -> ObjectId:
            return ObjectId(input_value)

        return core_schema.union_schema(
            [
                core_schema.is_instance_schema(ObjectId),
                core_schema.no_info_plain_validator_function(validate_from_str),
            ],
            serialization=core_schema.to_string_ser_schema(),
        )


PydanticObjectId = Annotated[ObjectId, _ObjectIdPydanticAnnotation]


class Model(BaseModel):
    id: Optional[PydanticObjectId] = Field(default_factory=ObjectId, alias="_id")
    created_at: datetime = Field(default_factory=lambda: datetime.now(tz=timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(tz=timezone.utc))
    deleted_at: Optional[datetime] = None

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True
        populate_by_name = True
        json_encoders = {ObjectId: str}

    @staticmethod
    def editable(field: str) -> bool:
        # immutable fields for user
        return field not in (
            "id",
            "_id",
            "created_at",
            "updated_at",
            "deleted_at",
        )
