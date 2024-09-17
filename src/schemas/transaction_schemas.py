import datetime

from models.transaction import TransactionType
from schemas.base import BaseSchemaModel


class TransactionSchema(BaseSchemaModel):
    id: int
    transaction_type: TransactionType
    amount: float
    created_at: datetime.datetime


class CreateTransactionSchema(BaseSchemaModel):
    transaction_type: TransactionType
    amount: float
    user_id: int
