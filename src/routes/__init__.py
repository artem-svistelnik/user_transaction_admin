from routes.health_routes import health_router
from routes.user_routes import user_router
from routes.transaction_routes import transaction_router


def include_routes(app):
    app.include_router(health_router)
    app.include_router(user_router)
    app.include_router(transaction_router)
