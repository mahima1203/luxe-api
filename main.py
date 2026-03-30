from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import models
from database import engine

from api.routers import products, auth, users, addresses, orders, payments

# Create backend tables if they don't exist
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Luxe Fashion API")

# Configure CORS
# This allows:
# 1. Local development (localhost:3000)
# 2. ANY Vercel deployment URL (ending in .vercel.app)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_origin_regex=r"https://.*\.vercel\.app",
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

