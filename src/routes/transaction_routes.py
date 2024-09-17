from dependency_injector.wiring import Provide

from fastapi import APIRouter
from containers.transactions_di import TransactionDI
from routes.depends import get_service
from schemas.transaction_schemas import CreateTransactionSchema, TransactionSchema
from services.transaction_service import TransactionService

transaction_router = APIRouter(prefix="/transactions", tags=["Transactions"])


@transaction_router.post("/", response_model=TransactionSchema)
async def create_transaction(
    transaction_dta: CreateTransactionSchema,
    service: TransactionService = get_service(Provide[TransactionDI.service]),
):
    transaction = await service.create_transaction(transaction_dta)
    return TransactionSchema.from_orm(transaction)
