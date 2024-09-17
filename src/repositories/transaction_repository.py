from datetime import timedelta

from sqlalchemy import and_
from sqlalchemy import func
from sqlalchemy import select

from models.transaction import Transaction, TransactionType
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

    async def get_transaction_sum(self, start_date=None, end_date=None):
        if end_date:
            end_date = end_date + timedelta(days=1)
        query = select(
            Transaction.transaction_type,
            func.count(Transaction.id).label("count"),
            func.sum(Transaction.amount).label("total_sum"),
        ).group_by(
            Transaction.transaction_type,
        )
        if start_date and end_date:
            query = query.where(
                and_(
                    Transaction.created_at >= start_date,
                    Transaction.created_at <= end_date,
                )
            )
        elif start_date:
            query = query.where(Transaction.created_at >= start_date)
        elif end_date:
            query = query.where(Transaction.created_at <= end_date)
        results = await self._run_query(query)
        data = results[0].all()
        result_dict = {}
        for row in data:
            result_dict[row.transaction_type] = {
                "count": row.count,
                "total_sum": row.total_sum,
            }
        if len(result_dict) > 0:
            income_count = result_dict.get(TransactionType.INCOME, {"count": 0}).get(
                "count", 0
            )
            expense_count = result_dict.get(TransactionType.EXPENSE, {"count": 0}).get(
                "count", 0
            )
            income_sum = result_dict.get(TransactionType.INCOME, {"total_sum": 0}).get(
                "total_sum", 0
            )
            expense_sum = result_dict.get(
                TransactionType.EXPENSE, {"total_sum": 0}
            ).get("total_sum", 0)
            return {
                "count": income_count + expense_count,
                "total_sum": income_sum - expense_sum,
            }
        return {
            "count": 0,
            "total_sum": 0,
        }

    async def get_transactions(self, start_date=None, end_date=None):
        if end_date:
            end_date = end_date + timedelta(days=1)
        query = select(
            Transaction.created_at.label("date"),
            Transaction.transaction_type.label("transaction_type"),
            func.sum(Transaction.amount).label("total_amount"),
        ).group_by(Transaction.created_at, Transaction.transaction_type)

        if start_date and end_date:
            query = query.where(
                Transaction.created_at >= start_date, Transaction.created_at <= end_date
            )
        elif start_date:
            query = query.where(Transaction.created_at >= start_date)
        elif end_date:
            query = query.where(Transaction.created_at <= end_date)

        results = await self._run_query(query)
        rows = results[0].all()
        return [
            {
                "date": row.date.date(),
                "transaction_type": row.transaction_type,
                "total_amount": row.total_amount,
            }
            for row in rows
        ]
