from bson import ObjectId
from pydantic import BaseModel, Field
from datetime import datetime, timezone
from typing import Optional


class Model(BaseModel):
    id: ObjectId = Field(default_factory=ObjectId, alias="_id")
    created_at: datetime = Field(default_factory=lambda: datetime.now(tz=timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(tz=timezone.utc))
    deleted_at: Optional[datetime] = None

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True
        populate_by_name = True
        json_encoders = {ObjectId: str}

    def update(self):
        self.updated_at = datetime.now(tz=timezone.utc)
