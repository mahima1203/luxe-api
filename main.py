from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import models
from database import engine

from api.routers import products, auth, users, addresses, orders, payments

# Create backend tables if they don't exist
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Luxe Fashion API")

import os

# Configure CORS
# Define base origins that are always allowed (local dev)
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

# Pull production origins from an Environment Variable (comma-separated list)
env_origins = os.getenv("ALLOWED_ORIGINS")
if env_origins:
    origins.extend([o.strip() for o in env_origins.split(",")])

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Welcome to Luxe Fashion API"}

# Register Routers (Controllers)
app.include_router(products.router)
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(addresses.router)
app.include_router(orders.router)
app.include_router(payments.router)

