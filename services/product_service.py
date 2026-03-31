from sqlalchemy.orm import Session
import models
from services import review_service

def get_paginated_products(category: str, page: int, limit: int, db: Session):
    start = (page - 1) * limit
    query = db.query(models.Product).filter(models.Product.category == category)
    total = query.count()
    products = query.offset(start).limit(limit).all()
    
    # Enrich with rating stats
    enriched_products = []
    for p in products:
        stats = review_service.get_product_rating_stats(p.id, db)
        # We manually attach these to the model instance for the Pydantic schema to pick up
        p.average_rating = stats["average_rating"]
        p.total_reviews = stats["total_reviews"]
        enriched_products.append(p)
    
    return {
        "products": enriched_products,
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
    
    products = db.query(models.Product).filter(filter_expr).limit(limit).all()
    
    for p in products:
        stats = review_service.get_product_rating_stats(p.id, db)
        p.average_rating = stats["average_rating"]
        p.total_reviews = stats["total_reviews"]
        
    return products

def get_product_by_id(product_id: int, db: Session):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if product:
        stats = review_service.get_product_rating_stats(product.id, db)
        product.average_rating = stats["average_rating"]
        product.total_reviews = stats["total_reviews"]
    return product
