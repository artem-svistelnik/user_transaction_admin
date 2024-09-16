from routes.health_routes import health_router


def include_routes(app):
    app.include_router(health_router)