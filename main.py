from fastapi import FastAPI
from backend.routes import auth_routes
from backend.routes import document_routes
from backend.routes import share_link_routes


# from backend.routes import order_items_routes

app = FastAPI() # fastapi instance

app.include_router(auth_routes.router)
app.include_router(document_routes.router)
app.include_router(share_link_routes.router)