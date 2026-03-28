from sqlalchemy.orm import Session
import models

def get_paginated_products(category: str, page: int, limit: int, db: Session):
    start = (page - 1) * limit
    query = db.query(models.Product).filter(models.Product.category == category)
    total = query.count()
    products = query.offset(start).limit(limit).all()
    
    return {
        "products": products,
        "hasMore": (start + len(products)) < total,
        "total": total
    }

def search_products(query: str, limit: int, db: Session):
    q = query.lower().strip()
    if not q:
        return []
    
    filter_expr = (
        models.Product.name.ilike(f"%{q}%") |
        models.Product.brand.ilike(f"%{q}%") |
        models.Product.category.ilike(f"%{q}%") |
        models.Product.subcategory.ilike(f"%{q}%")
    )
    
    return db.query(models.Product).filter(filter_expr).limit(limit).all()

def get_product_by_id(product_id: int, db: Session):
    return db.query(models.Product).filter(models.Product.id == product_id).first()
