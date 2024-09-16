from typing import Optional

from schemas.base import BaseSchemaModel
from pydantic import Field

from schemas.transaction_schemas import TransactionSchema


class SignUpSchema(BaseSchemaModel):
    username: str = Field(min_length=8, max_length=100)


class SignUpResponseSchema(BaseSchemaModel):
    id: int


class UserSchema(BaseSchemaModel):
    id: int
    username: str
    transactions: Optional[list[TransactionSchema]] = []