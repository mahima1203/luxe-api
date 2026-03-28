from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from typing import List
import schemas
from database import get_db
from services import product_service

router = APIRouter(prefix="/api/products", tags=["products"])

@router.get("", response_model=schemas.ProductListResponse)
def get_products(category: str = Query(...), page: int = Query(1), limit: int = Query(10), db: Session = Depends(get_db)):
    return product_service.get_paginated_products(category, page, limit, db)

@router.get("/search", response_model=List[schemas.Product])
def search_products(query: str = Query(...), limit: int = Query(5), db: Session = Depends(get_db)):
    return product_service.search_products(query, limit, db)

@router.get("/{product_id}", response_model=schemas.Product)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = product_service.get_product_by_id(product_id, db)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product
