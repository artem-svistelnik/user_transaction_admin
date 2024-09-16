from dependency_injector import containers, providers


from services.transaction_service import TransactionService
from repositories.transaction_repository import TransactionRepository


class TransactionDI(containers.DeclarativeContainer):
    transaction_repository = providers.Factory(
        TransactionRepository,
    )
    service = providers.Factory(
        TransactionService,
        transaction_repository=transaction_repository,
    )
