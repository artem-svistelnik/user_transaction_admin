from models.transaction import Transaction
from repositories.base import GenericRepository
from schemas.transaction_schemas import CreateTransactionSchema


class TransactionRepository(GenericRepository[Transaction]):

    async def create_transaction(self, transaction_dta: CreateTransactionSchema):
        transaction = await self.create(
            self.model(
                transaction_type=transaction_dta.transaction_type,
                amount=transaction_dta.amount,
                user_id=transaction_dta.user_id,
            ),
            refresh=True,
        )
        return transaction