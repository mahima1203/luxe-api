from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
import models, schemas
import datetime

def get_product_reviews(product_id: int, db: Session):
    """Fetch all reviews for a product with reviewer names."""
    reviews = db.query(models.Review).filter(models.Review.product_id == product_id).all()
    
    result = []
    for r in reviews:
        result.append({
            "id": r.id,
            "user_id": r.user_id,
            "product_id": r.product_id,
            "rating": r.rating,
            "comment": r.comment,
            "created_at": r.created_at,
            "user_full_name": r.user.full_name if r.user else "Anonymous"
        })
    return result

def get_product_rating_stats(product_id: int, db: Session):
    """Calculate average rating and total count for a product."""
    stats = db.query(
        func.avg(models.Review.rating).label('average'),
        func.count(models.Review.id).label('count')
    ).filter(models.Review.product_id == product_id).first()
    
    return {
        "average_rating": float(stats.average) if stats.average else 0.0,
        "total_reviews": stats.count or 0
    }

def check_review_eligibility(user_id: int, product_id: int, db: Session):
    """
    Check if a user is allowed to review a product.
    Must have a 'delivered' order containing that product.
    """
    # 1. Did the user already review this?
    existing = db.query(models.Review).filter(
        models.Review.user_id == user_id, 
        models.Review.product_id == product_id
    ).first()
    if existing:
        return False, "You have already reviewed this product."

    # 2. Did the user buy this product and was it delivered?
    # We join OrderItem -> Order and filter by status and user_id
    delivered_order = db.query(models.Order).join(models.OrderItem).filter(
        models.Order.user_id == user_id,
        models.Order.status == "delivered",
        models.OrderItem.product_id == product_id
    ).first()

    if not delivered_order:
        return False, "You can only review products that have been delivered to you."

    return True, "Eligible to review."

def create_review(user_id: int, data: schemas.ReviewCreate, db: Session):
    """Create a new review after strict validation."""
    eligible, message = check_review_eligibility(user_id, data.product_id, db)
    if not eligible:
        raise HTTPException(status_code=403, detail=message)

    if not (1 <= data.rating <= 5):
        raise HTTPException(status_code=400, detail="Rating must be between 1 and 5.")

    new_review = models.Review(
        user_id=user_id,
        product_id=data.product_id,
        rating=data.rating,
        comment=data.comment
    )
    db.add(new_review)
    db.commit()
    db.refresh(new_review)
    return new_review
