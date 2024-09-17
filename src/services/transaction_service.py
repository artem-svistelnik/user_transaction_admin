from datetime import date

from repositories.transaction_repository import TransactionRepository
from schemas.transaction_schemas import CreateTransactionSchema
from services.base import BaseService


class TransactionService(BaseService):
    def __init__(self, transaction_repository: TransactionRepository):
        self.transaction_repo = transaction_repository

    async def create_transaction(self, transaction: CreateTransactionSchema):
        return await self.transaction_repo.create_transaction(transaction)

    async def get_transaction_sum(self, start_date=None, end_date=None):
        return await self.transaction_repo.get_transaction_sum(start_date, end_date)

    async def get_transactions(self, start_date=None, end_date=None):
        return await self.transaction_repo.get_transactions(start_date, end_date)
